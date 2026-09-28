"""Pages migrated to the Spread shell (core/tl_base.html)."""

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from characters.models.core import Human
from game.models import Chronicle, Post, Scene


class HomeContinueScenesTest(TestCase):
    def setUp(self):
        cache.clear()
        self.player = User.objects.create_user("player", password="pw")
        self.other = User.objects.create_user("other", password="pw")
        self.chronicle = Chronicle.objects.create(name="Ashes of Hyde Park", headings="mta_heading")
        self.character = Human.objects.create(
            name="Marisol", owner=self.player, chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(
            name="The Map Room at Midnight", chronicle=self.chronicle, gameline="mta"
        )
        self.scene.characters.add(self.character)
        for text in ("One", "Two"):
            Post.objects.create(
                scene=self.scene, character=self.character, display_name="Marisol", message=text
            )

    def test_player_sees_their_live_scene(self):
        self.client.force_login(self.player)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "The Map Room at Midnight")
        self.assertContains(response, "2 posts")
        self.assertContains(response, 'data-gameline="mta"')

    def test_finished_scenes_are_left_out(self):
        self.scene.finished = True
        self.scene.save()
        self.client.force_login(self.player)
        response = self.client.get(reverse("core:home"))
        self.assertNotContains(response, "The Map Room at Midnight")
        self.assertContains(response, "No live scenes right now.")

    def test_other_players_do_not_see_it(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("core:home"))
        self.assertNotContains(response, "The Map Room at Midnight")


class HomeCacheIsolationTest(TestCase):
    def setUp(self):
        cache.clear()

    def test_cached_home_page_is_not_shared_between_visitors(self):
        first = User.objects.create_user("firstvisitor", password="pw")
        second = User.objects.create_user("secondvisitor", password="pw")
        self.client.force_login(first)
        self.assertContains(self.client.get(reverse("core:home")), "firstvisitor")

        self.client.force_login(second)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "secondvisitor")
        self.assertNotContains(response, "firstvisitor")

        self.client.logout()
        response = self.client.get(reverse("core:home"))
        self.assertNotContains(response, "secondvisitor")
        self.assertContains(response, "Log in to see your scenes.")


class CharacterIndexSelectionTest(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user("staff", password="pw", is_staff=True)
        self.first = Chronicle.objects.create(name="First Chronicle", headings="vtm_heading")
        self.second = Chronicle.objects.create(name="Second Chronicle", headings="mta_heading")
        Human.objects.create(
            name="Active Alice", owner=self.staff, chronicle=self.first, status="App"
        )
        Human.objects.create(
            name="Retired Rob", owner=self.staff, chronicle=self.first, status="Ret"
        )
        Human.objects.create(
            name="Second Sam", owner=self.staff, chronicle=self.second, status="App"
        )
        self.client.force_login(self.staff)

    def test_defaults_to_first_chronicle_with_characters_and_active(self):
        response = self.client.get(reverse("characters:index"))
        self.assertEqual(response.context["selected_chronicle"], self.first)
        self.assertEqual(response.context["selected_status"], "active")
        self.assertContains(response, "Active Alice")
        self.assertNotContains(response, "Retired Rob")
        self.assertNotContains(response, "Second Sam")
        self.assertContains(response, 'data-gameline="vtm"')

    def test_querystring_picks_chronicle_and_status(self):
        response = self.client.get(
            reverse("characters:index"), {"chronicle": self.first.pk, "status": "retired"}
        )
        self.assertContains(response, "Retired Rob")
        self.assertNotContains(response, "Active Alice")

        response = self.client.get(reverse("characters:index"), {"chronicle": self.second.pk})
        self.assertContains(response, "Second Sam")
        self.assertContains(response, 'data-gameline="mta"')

    def test_status_counts_and_switch_links(self):
        response = self.client.get(reverse("characters:index"))
        counts = {tab["key"]: tab["count"] for tab in response.context["status_tabs"]}
        self.assertEqual(counts, {"active": 1, "retired": 1, "deceased": 0, "npc": 0})
        self.assertContains(response, f"?chronicle={self.second.pk}&amp;status=active")

    def test_unknown_values_fall_back(self):
        response = self.client.get(
            reverse("characters:index"), {"chronicle": "999999", "status": "bogus"}
        )
        self.assertEqual(response.context["selected_chronicle"], self.first)
        self.assertEqual(response.context["selected_status"], "active")


class SpreadShellPagesTest(TestCase):
    def test_auth_pages_use_the_spread_shell(self):
        pages = {
            "login": reverse("login"),
            "password_reset": reverse("password_reset"),
            "password_reset_done": reverse("password_reset_done"),
            "password_reset_complete": reverse("password_reset_complete"),
            "password_reset_confirm": reverse(
                "password_reset_confirm", kwargs={"uidb64": "xx", "token": "bad-token"}
            ),
            "signup": reverse("accounts:signup"),
        }
        for name, url in pages.items():
            with self.subTest(page=name):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "core/tl_auth.html")
                self.assertTemplateNotUsed(response, "admin/base.html")
                self.assertNotContains(response, "bootstrap")

    def test_invalid_reset_link_offers_a_new_one(self):
        url = reverse("password_reset_confirm", kwargs={"uidb64": "xx", "token": "bad-token"})
        response = self.client.get(url)
        self.assertContains(response, "The password reset link was invalid")
        self.assertContains(response, reverse("password_reset"))

    def test_logout_uses_the_spread_shell(self):
        user = User.objects.create_user("leaver", password="pw")
        self.client.force_login(user)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("core:home"))

    def test_signup_field_errors_render_inline(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "mira",
                "email": "mira@example.com",
                "password1": "a-long-passphrase-1",
                "password2": "different-passphrase-2",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tl-field is-invalid")

    def test_404_uses_the_error_shell(self):
        response = self.client.get("/no-such-page-anywhere/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "core/errors/error.html")
        self.assertContains(response, "404", status_code=404)

    def test_logged_in_nav_shows_user_menu(self):
        user = User.objects.create_user("navuser", password="pw")
        self.client.force_login(user)
        cache.clear()
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "navuser")
        self.assertContains(response, reverse("logout"))
