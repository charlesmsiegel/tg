"""Real-browser tests for live scene chat over htmx WebSockets (Step 11).

A Daphne server runs in a child process on the test database, so the
sockets, the in-memory channel layer and the HTTP fallback are real. Writes
made from the test process go straight to the database and are never
broadcast, which is how these tests create "missed" posts. Needs the
``playwright`` package and Chromium (see the chargen browser tests); the tests
skip without them. Never run ``playwright install``.
"""

import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.db import connections
from django.template.loader import render_to_string
from django.test import Client, TransactionTestCase

from characters.models.core.human import Human
from characters.tests.browser.test_chargen_interactive import chromium_binary
from game.models import Chronicle, Gameline, Post, Scene, STRelationship
from game.selectors import scene_post

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # development-only dependency
    sync_playwright = None


class SceneChatBrowserTests(TransactionTestCase):
    host = "127.0.0.1"

    @classmethod
    def setUpClass(cls):
        if sync_playwright is None:
            raise unittest.SkipTest("Install the playwright package to run browser tests")
        binary = chromium_binary()
        if binary is None:
            raise unittest.SkipTest("Set TG_BROWSER_BINARY to a Chromium binary")
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.start_server()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(executable_path=binary)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.terminate()
        cls.server.wait(10)
        cls.server_dir.cleanup()
        super().tearDownClass()

    @classmethod
    def start_server(cls):
        """Run Daphne on this test database in a child process.

        ``subprocess`` rather than ``multiprocessing`` (Channels' live server
        test case) so it also works inside ``--parallel`` workers, which are
        daemonic and may not fork; and Channels 4.1's test case predates
        Django 5.2's class-level ``_pre_setup``.
        """
        cls.server_dir = tempfile.TemporaryDirectory()
        database = str(connections["default"].settings_dict["NAME"])
        Path(cls.server_dir.name, "scene_chat_live_settings.py").write_text(
            f"from {os.environ['DJANGO_SETTINGS_MODULE']} import *  # noqa: F403\n"
            f"DATABASES['default']['NAME'] = {database!r}  # noqa: F405\n"
            f"ALLOWED_HOSTS = [{cls.host!r}]\n"
        )
        Path(cls.server_dir.name, "scene_chat_live_asgi.py").write_text(
            "from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler\n"
            "from tg.asgi import application as app\n"
            "application = ASGIStaticFilesHandler(app)\n"
        )
        with socket.socket() as probe:
            probe.bind((cls.host, 0))
            port = probe.getsockname()[1]
        env = dict(
            os.environ,
            DJANGO_SETTINGS_MODULE="scene_chat_live_settings",
            PYTHONPATH=os.pathsep.join([cls.server_dir.name, str(settings.BASE_DIR)]),
        )
        cls.server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "daphne",
                "-b",
                cls.host,
                "-p",
                str(port),
                "scene_chat_live_asgi:application",
            ],
            cwd=settings.BASE_DIR,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cls.live_server_url = f"http://{cls.host}:{port}"
        deadline = time.monotonic() + 30
        while True:
            try:
                socket.create_connection((cls.host, port), timeout=1).close()
                return
            except OSError as exc:
                if cls.server.poll() is not None or time.monotonic() > deadline:
                    cls.server.kill()
                    raise RuntimeError("The Daphne test server did not start") from exc
                time.sleep(0.1)

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Live chronicle")
        line = Gameline.objects.create(name="World of Darkness")
        self.alice = User.objects.create_user("alice", password="pw")
        self.bob = User.objects.create_user("bob", password="pw")
        STRelationship.objects.create(user=self.bob, chronicle=self.chronicle, gameline=line)
        self.hero = Human.objects.create(name="Hero", owner=self.alice, chronicle=self.chronicle)
        self.narrator = Human.objects.create(
            name="Narrator", owner=self.bob, chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(name="Live scene", chronicle=self.chronicle)
        self.scene.characters.add(self.hero, self.narrator)
        self.contexts = []
        self.errors = []

    def tearDown(self):
        for context in self.contexts:
            context.close()

    # Helpers ---------------------------------------------------------------

    def browser_for(self, user, expected_errors=()):
        """A signed-in page; console errors are collected unless expected."""
        client = Client()
        client.force_login(user)
        context = self.browser.new_context()
        self.contexts.append(context)
        context.add_cookies(
            [
                {
                    "name": "sessionid",
                    "value": client.cookies["sessionid"].value,
                    "url": self.live_server_url,
                }
            ]
        )
        # Only the live server is reachable (no CDNs), as in the chargen tests.
        context.route(
            "**/*",
            lambda route: (
                route.continue_()
                if route.request.url.startswith(self.live_server_url)
                else route.abort()
            ),
        )
        page = context.new_page()
        page.set_default_timeout(10000)
        page.on(
            "pageerror",
            lambda error: "boot/js/bootstrap" not in (error.stack or "")
            and self.errors.append(str(error)),
        )
        page.on(
            "console",
            lambda message: message.type == "error"
            and not message.text.startswith("Failed to load resource")
            and not any(text in message.text for text in expected_errors)
            and self.errors.append(message.text),
        )
        return page

    def open(self, page, wait_live=True, wait_until="load"):
        page.goto(self.live_server_url + self.scene.get_absolute_url(), wait_until=wait_until)
        if wait_live:
            page.wait_for_selector('[data-ws-state="open"]', state="attached")

    def say(self, page, text):
        page.fill("#message-input", text)
        page.press("#message-input", "Enter")

    def wait_for_post(self, page, text):
        page.wait_for_selector(f'#posts-container .post-item:has-text("{text}")')

    def post_ids(self, page):
        return page.eval_on_selector_all(
            "#posts-container [data-post-id]", "posts => posts.map(p => +p.dataset.postId)"
        )

    def wait_until(self, condition, timeout=10):
        deadline = time.monotonic() + timeout
        while not condition():
            if time.monotonic() > deadline:
                self.fail("Timed out waiting")
            self.contexts[0].pages[0].wait_for_timeout(50)

    def create_post(self, text):
        """A post the server never broadcasts (written from the test process)."""
        return Post.objects.create(
            scene=self.scene, character=self.narrator, display_name="Narrator", message=text
        )

    # Tests -----------------------------------------------------------------

    def test_a_post_from_one_player_appears_for_the_other(self):
        alice, bob = self.browser_for(self.alice), self.browser_for(self.bob)
        self.open(alice)
        self.open(bob)
        self.assertTrue(bob.is_visible("#no-posts-message"))

        self.say(alice, "The door creaks open.")
        self.wait_for_post(bob, "The door creaks open.")
        self.wait_for_post(alice, "The door creaks open.")

        # Rendered per viewer: Alice's own post is marked as hers only for her.
        self.assertEqual(alice.locator("#posts-container article.tl-turn--mine").count(), 1)
        self.assertEqual(bob.locator("#posts-container article.tl-turn--mine").count(), 0)
        # The message field was reset by the server and keeps the focus.
        alice.wait_for_function("document.querySelector('#message-input').value === ''")
        self.assertEqual(alice.evaluate("document.activeElement.id"), "message-input")
        self.assertTrue(bob.is_hidden("#no-posts-message"))
        self.assertEqual(Post.objects.filter(scene=self.scene).count(), 1)

        # And back: Bob storytells this chronicle, so his post is styled as an ST's.
        self.say(bob, 'Rain begins. "Hurry."')
        self.wait_for_post(alice, "Rain begins.")
        self.assertEqual(alice.locator("#posts-container article.tl-turn--st").count(), 1)
        self.assertEqual(alice.locator("#posts-container span.quote").count(), 1)
        self.assertEqual(self.errors, [])

    def test_a_refused_post_keeps_the_text_and_shows_why(self):
        alice = self.browser_for(self.alice)
        self.open(alice)
        self.say(alice, "Leap /extended nonsense")
        alice.wait_for_selector("#scene-chat-notice .tl-message--error")
        self.assertIn("Command does not match", alice.inner_text("#scene-chat-notice"))
        self.assertEqual(alice.input_value("#message-input"), "Leap /extended nonsense")
        self.assertFalse(alice.is_disabled("#post-submit-btn"))
        self.assertFalse(Post.objects.filter(scene=self.scene).exists())
        # Shift+Enter is a newline, not a send.
        alice.fill("#message-input", "Line one")
        alice.press("#message-input", "Shift+Enter")
        self.assertIn("\n", alice.input_value("#message-input"))
        self.assertEqual(self.errors, [])

    def test_posts_made_before_the_socket_opened_are_caught_up(self):
        held = []
        bob = self.browser_for(self.bob)
        bob.route("**/ws.min.js", lambda route: held.append(route))
        # Deferred scripts run before DOMContentLoaded, so only wait for the response.
        self.open(bob, wait_live=False, wait_until="commit")
        bob.wait_for_function("window.htmx !== undefined")
        missed = self.create_post("Missed while loading")
        held[0].continue_()
        self.wait_for_post(bob, "Missed while loading")
        self.assertEqual(self.post_ids(bob), [missed.pk])
        self.assertEqual(self.errors, [])

    def test_a_reconnect_catches_up_without_duplicates(self):
        connections = []

        def proxy(ws):
            connections.append(ws)
            if len(connections) == 2:
                # Made while Bob was disconnected, so never broadcast to him.
                self.create_post("Missed while away")
            ws.connect_to_server()

        alice, bob = self.browser_for(self.alice), self.browser_for(self.bob)
        bob.route_web_socket("**/ws/scene/**", proxy)
        self.open(alice)
        self.open(bob)
        self.say(alice, "Before the drop")
        self.wait_for_post(bob, "Before the drop")

        connections[0].close(code=1012, reason="Service restart")  # retried by htmx
        bob.wait_for_function(
            "document.querySelector('[data-scene-live]').dataset.wsState !== 'open'"
        )
        self.wait_for_post(bob, "Missed while away")
        bob.wait_for_selector('[data-ws-state="open"]', state="attached")
        self.say(alice, "After the return")
        self.wait_for_post(bob, "After the return")

        self.assertEqual(len(connections), 2)
        ids = self.post_ids(bob)
        self.assertEqual(ids, sorted(Post.objects.values_list("pk", flat=True)))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.errors, [])

    def test_duplicate_and_late_posts_keep_one_copy_in_id_order(self):
        routes = []

        def proxy(ws):
            routes.append(ws)
            ws.connect_to_server()

        alice, bob = self.browser_for(self.alice), self.browser_for(self.bob)
        bob.route_web_socket("**/ws/scene/**", proxy)
        self.open(alice)
        self.open(bob)
        self.say(alice, "First")
        self.wait_for_post(bob, "First")
        late = self.create_post("Late")  # committed before Second, delivered after it
        self.say(alice, "Second")
        self.wait_for_post(bob, "Second")
        first, second = Post.objects.exclude(pk=late.pk).order_by("pk")

        # One frame with a post Bob already has and the late one, as a sync
        # reply racing a broadcast would deliver them.
        frame = render_to_string(
            "game/scene/ws/_posts.html",
            {"posts": [scene_post(self.scene, first.pk), scene_post(self.scene, late.pk)]},
        )
        routes[0].send(frame)
        self.wait_for_post(bob, "Late")
        self.assertEqual(self.post_ids(bob), [first.pk, late.pk, second.pk])
        self.assertEqual(self.errors, [])

    def test_posting_falls_back_to_http_when_the_socket_is_refused(self):
        refused = []
        alice = self.browser_for(self.alice)
        # Not connected to the server: Playwright answers for it. (Closing
        # inside the handler would deadlock the sync API.)
        alice.route_web_socket("**/ws/scene/**", lambda ws: refused.append(ws))
        self.open(alice, wait_live=False)
        alice.wait_for_function("() => document.querySelector('[data-ws-state]') !== null")
        self.wait_until(lambda: refused)
        refused[0].close(code=4403, reason="Denied")
        alice.wait_for_selector('[data-ws-state="closed"]', state="attached")
        self.assertIn("Live updates are unavailable", alice.text_content("#status-indicator"))
        with alice.expect_navigation():
            self.say(alice, "Sent the old way")
        self.wait_for_post(alice, "Sent the old way")
        self.assertEqual(Post.objects.get(scene=self.scene).message, "Sent the old way")
        self.assertEqual(self.errors, [])

    def test_closing_the_scene_ends_live_posting_for_everyone(self):
        alice, bob = self.browser_for(self.alice), self.browser_for(self.bob)
        self.open(alice)
        self.open(bob)
        with bob.expect_navigation():
            bob.click('button:has-text("Close scene")')
        alice.wait_for_selector("#scene-actions:has-text('This scene is closed.')")
        alice.wait_for_selector('[data-ws-state="closed"]', state="attached")
        self.assertEqual(alice.locator("#post-form").count(), 0)
        self.assertEqual(self.errors, [])

    def test_earlier_posts_load_in_place(self):
        posts = [self.create_post(f"Numbered post {n}") for n in range(105)]
        alice = self.browser_for(self.alice)
        self.open(alice)
        url = alice.url
        self.assertEqual(self.post_ids(alice)[0], posts[5].pk)
        alice.click("#earlier-posts")
        alice.wait_for_selector(f"#post-{posts[0].pk}", state="attached")
        self.assertEqual(alice.url, url)
        self.assertEqual(self.post_ids(alice), [post.pk for post in posts])
        self.assertEqual(alice.locator("#earlier-posts").count(), 0)
        self.assertEqual(self.errors, [])
