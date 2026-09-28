"""htmx helpers and the vendored browser libraries."""

import base64
import hashlib
import json
import re
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase

from core.htmx import (
    hx_redirect,
    is_fragment_request,
    is_htmx,
    mark_fragment,
    trigger,
    vary_on_htmx,
)

VENDOR = Path(settings.BASE_DIR) / "source_static" / "vendor"


class HtmxHelperTests(SimpleTestCase):
    def request(self, **headers):
        return RequestFactory().get("/", headers=headers)

    def test_fragment_request_needs_hx_request(self):
        self.assertFalse(is_htmx(self.request()))
        self.assertTrue(is_fragment_request(self.request(HX_Request="true")))

    def test_history_restore_and_boosted_get_full_pages(self):
        restore = self.request(HX_Request="true", HX_History_Restore_Request="true")
        boosted = self.request(HX_Request="true", HX_Boosted="true")
        self.assertTrue(is_htmx(restore))
        self.assertFalse(is_fragment_request(restore))
        self.assertFalse(is_fragment_request(boosted))

    def test_hx_redirect_is_not_a_3xx(self):
        response = hx_redirect("/characters/1/detail/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["HX-Redirect"], "/characters/1/detail/")

    def test_headers(self):
        response = vary_on_htmx(mark_fragment(hx_redirect("/"), "chargen-step"))
        self.assertEqual(response["TG-Fragment"], "chargen-step")
        for header in ("HX-Request", "HX-History-Restore-Request", "HX-Boosted"):
            self.assertIn(header, response["Vary"])

    def test_trigger_merges_events(self):
        response = trigger(hx_redirect("/"), "a", {"x": 1})
        trigger(response, "b", True)
        self.assertEqual(json.loads(response["HX-Trigger"]), {"a": {"x": 1}, "b": True})
        trigger(response, "c", 1, header="HX-Trigger-After-Swap")
        self.assertEqual(json.loads(response["HX-Trigger-After-Swap"]), {"c": 1})


class VendoredLibraryTests(SimpleTestCase):
    """The include's SRI hashes, VENDOR.md and the files on disk must agree."""

    def scripts(self, **flags):
        html = render_to_string("core/includes/interactive_scripts.html", flags or {"ws": True})
        return re.findall(r'src="/static/(vendor/[^"]+)" integrity="([^"]+)"', html)

    def test_every_vendored_script_has_matching_sri(self):
        scripts = self.scripts()
        self.assertEqual(
            [path for path, _ in scripts],
            [
                "vendor/htmx/2.0.11/htmx.min.js",
                "vendor/htmx-ext-ws/2.0.4/ws.min.js",
                "vendor/alpinejs-csp/3.17.4/cdn.min.js",
            ],
        )
        manifest = (VENDOR / "VENDOR.md").read_text()
        for path, integrity in scripts:
            data = Path(finders.find(path)).read_bytes()
            digest = base64.b64encode(hashlib.sha384(data).digest()).decode()
            self.assertEqual(integrity, f"sha384-{digest}", path)
            self.assertIn(integrity, manifest)
            # Manifest storage rewrites sourceMappingURL comments, which would
            # change the bytes and break SRI on hashed URLs.
            self.assertNotIn(b"sourceMappingURL", data)

    def test_flags_choose_the_libraries(self):
        def paths(**flags):
            return [path for path, _ in self.scripts(**flags)]

        self.assertEqual(
            paths(chargen=True),
            ["vendor/htmx/2.0.11/htmx.min.js", "vendor/alpinejs-csp/3.17.4/cdn.min.js"],
        )
        self.assertEqual(
            paths(ws=True, alpine=False),
            ["vendor/htmx/2.0.11/htmx.min.js", "vendor/htmx-ext-ws/2.0.4/ws.min.js"],
        )

    def test_each_vendored_library_ships_its_license(self):
        for path, _ in self.scripts():
            self.assertTrue(
                (VENDOR / Path(path).relative_to("vendor").parent / "LICENSE").is_file()
            )

    def test_config_disables_eval_and_injected_styles(self):
        html = render_to_string("core/includes/interactive_scripts.html")
        config = json.loads(re.search(r"content='([^']+)'", html).group(1))
        self.assertFalse(config["allowEval"])
        self.assertFalse(config["includeIndicatorStyles"])
        self.assertTrue(config["selfRequestsOnly"])
