"""Before/after template screenshots: python scripts/template_screenshots.py <command>.

Commands:

* ``capture OUT_DIR`` builds a throwaway SQLite database, seeds it with
  ``core.tests.template_fixtures.seed()``, starts ``runserver`` on it and saves a
  full-page PNG plus the rendered HTML of every fixture page (detail, edit and
  list pages for each gameline, the character index and the scene page) into
  OUT_DIR, as the fixture storyteller. ``pages.json`` records each page's URL and
  HTTP status.
* ``compare BEFORE_DIR AFTER_DIR`` reports pages whose status changed, whose
  pixels differ (with a diff PNG in ``AFTER_DIR/_diff``) and whose visible text
  differs.

Typical use: ``capture /tmp/before`` on the base commit, ``capture /tmp/after``
on the branch, then ``compare /tmp/before /tmp/after``. Requires the optional
``playwright`` Python package (``pip install playwright``) and a Chromium build
(``PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`` in the cloud container; do not
run ``playwright install`` there). Requests to other hosts are blocked so CDN
availability cannot change a screenshot.
"""

import argparse
import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

import django
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.core.management import call_command
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
SETTINGS = "scripts.screenshot_settings"


def _free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def seed_pages():
    django.setup()
    call_command("migrate", run_syncdb=True, verbosity=0, interactive=False)
    # Models can only load once Django is set up on the throwaway database.
    from core.tests.template_fixtures import fixture_pages, seed

    fixtures = seed()
    return fixture_pages(fixtures), fixtures


def _session_cookie(user):
    session = SessionStore()
    session[SESSION_KEY] = str(user.pk)
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session.session_key


def capture(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    db = out / "fixtures.sqlite3"
    db.unlink(missing_ok=True)
    os.environ["TG_SCREENSHOT_DB"] = str(db)
    os.environ["DJANGO_SETTINGS_MODULE"] = SETTINGS
    pages, fixtures = seed_pages()
    (out / "skipped.json").write_text(json.dumps(fixtures.skipped, indent=2, sort_keys=True))
    session_key = _session_cookie(fixtures.st)

    port = _free_port()
    env = dict(os.environ, TG_SCREENSHOT_DB=str(db), DJANGO_SETTINGS_MODULE=SETTINGS)
    server = subprocess.Popen(
        [sys.executable, "manage.py", "runserver", f"127.0.0.1:{port}", "--noreload"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base = f"http://127.0.0.1:{port}"
    results = {}
    try:
        for _ in range(100):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
                break
            except OSError:
                time.sleep(0.2)
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            context.add_cookies([{"name": "sessionid", "value": session_key, "url": base}])
            context.route(re.compile(r"^(?!http://127\.0\.0\.1).*"), lambda route: route.abort())
            page = context.new_page()
            for slug, url in sorted(pages.items()):
                response = page.goto(base + url, wait_until="load")
                page.add_style_tag(content="*{animation:none!important;transition:none!important}")
                results[slug] = {"url": url, "status": response.status if response else None}
                page.screenshot(path=str(out / f"{slug}.png"), full_page=True)
                (out / f"{slug}.html").write_text(page.content())
                (out / f"{slug}.txt").write_text(page.inner_text("body"))
            browser.close()
    finally:
        server.terminate()
        server.wait()
    (out / "pages.json").write_text(json.dumps(results, indent=2, sort_keys=True))
    bad = {k: v for k, v in results.items() if v["status"] != 200}
    print(f"Captured {len(results)} pages into {out}; non-200: {len(bad)}")
    for slug, info in sorted(bad.items()):
        print(f"  {info['status']} {slug} {info['url']}")


def compare(before_dir, after_dir):
    before, after = Path(before_dir), Path(after_dir)
    b_pages = json.loads((before / "pages.json").read_text())
    a_pages = json.loads((after / "pages.json").read_text())
    diff_dir = after / "_diff"
    diff_dir.mkdir(exist_ok=True)
    report = {"missing": [], "added": [], "status": [], "pixels": [], "text": []}
    report["missing"] = sorted(set(b_pages) - set(a_pages))
    report["added"] = sorted(set(a_pages) - set(b_pages))
    for slug in sorted(set(b_pages) & set(a_pages)):
        if b_pages[slug]["status"] != a_pages[slug]["status"]:
            report["status"].append(
                f"{slug}: {b_pages[slug]['status']} -> {a_pages[slug]['status']}"
            )
        img_a = Image.open(before / f"{slug}.png").convert("RGB")
        img_b = Image.open(after / f"{slug}.png").convert("RGB")
        if img_a.size != img_b.size:
            report["pixels"].append(f"{slug}: size {img_a.size} -> {img_b.size}")
        else:
            box = ImageChops.difference(img_a, img_b).getbbox()
            if box:
                report["pixels"].append(f"{slug}: region {box}")
                ImageChops.difference(img_a, img_b).save(diff_dir / f"{slug}.png")
        text_a = (before / f"{slug}.txt").read_text().split()
        text_b = (after / f"{slug}.txt").read_text().split()
        if text_a != text_b:
            report["text"].append(slug)
    for key, rows in report.items():
        print(f"## {key}: {len(rows)}")
        for row in rows:
            print(f"  {row}")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    cap = sub.add_parser("capture")
    cap.add_argument("out_dir")
    cmp_ = sub.add_parser("compare")
    cmp_.add_argument("before_dir")
    cmp_.add_argument("after_dir")
    args = parser.parse_args(argv)
    if args.command == "capture":
        capture(args.out_dir)
    else:
        compare(args.before_dir, args.after_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
