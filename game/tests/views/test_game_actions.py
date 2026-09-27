"""Scene, journal and chronicle action endpoints (Step 5)."""

import datetime

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from core.tests.action_audience import AUDIENCE, ActionAudienceMixin
from game.models import Journal, JournalEntry, Post, Scene, Story
from locations.models.core import LocationModel


def _messages(response):
    return [str(m) for m in get_messages(response.wsgi_request)]


class GameActionTestBase(ActionAudienceMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.character = Human.objects.create(
            name="Scene Hero", owner=self.users["owner"], chronicle=self.chronicle, status="App"
        )
        self.scene = Scene.objects.create(name="Opening", chronicle=self.chronicle)

    def assert_matrix(self, expected, act, changed):
        """Run ``act()`` as each audience member; ``changed()`` reports a write."""
        self.assertEqual(set(expected), set(AUDIENCE))
        for who, status in expected.items():
            with self.subTest(who=who):
                self.reset()
                self.login_as(who)
                response = act()
                self.assertEqual(response.status_code, status)
                self.assertEqual(changed(), status == 302 and who in self.writers, who)

    def reset(self):
        pass


class SceneCloseTests(GameActionTestBase):
    writers = {"st", "staff"}

    def reset(self):
        Scene.objects.filter(pk=self.scene.pk).update(finished=False)

    def test_matrix(self):
        url = reverse("game:scene_close", kwargs={"pk": self.scene.pk})
        self.assert_matrix(
            {
                "owner": 403,
                "player": 404,
                "st": 302,
                "other_line_st": 403,
                "other_chronicle_st": 404,
                "staff": 302,
                "anonymous": 401,
            },
            lambda: self.client.post(url),
            lambda: Scene.objects.get(pk=self.scene.pk).finished,
        )

    def test_closing_twice_is_reported_not_repeated(self):
        url = reverse("game:scene_close", kwargs={"pk": self.scene.pk})
        self.login_as("st")
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(any("already closed" in m for m in _messages(response)))

    def test_get_and_old_button_are_rejected(self):
        self.login_as("st")
        self.assertEqual(
            self.client.get(reverse("game:scene_close", kwargs={"pk": self.scene.pk})).status_code,
            405,
        )
        response = self.client.post(self.scene.get_absolute_url(), {"close_scene": "Close Scene"})
        self.assertEqual(response.status_code, 405)
        self.scene.refresh_from_db()
        self.assertFalse(self.scene.finished)


class SceneAddCharacterTests(GameActionTestBase):
    writers = {"owner", "st", "staff"}

    def reset(self):
        self.scene.characters.clear()

    def test_matrix(self):
        url = reverse("game:scene_add_character", kwargs={"pk": self.scene.pk})
        self.assert_matrix(
            {
                "owner": 302,
                "player": 404,
                "st": 302,
                # Visible, but may enroll only their own characters: a form error.
                "other_line_st": 302,
                "other_chronicle_st": 404,
                "staff": 302,
                "anonymous": 401,
            },
            lambda: self.client.post(url, {"character_to_add": self.character.pk}),
            lambda: self.scene.characters.filter(pk=self.character.pk).exists(),
        )

    def test_character_from_another_chronicle_is_a_form_error(self):
        stranger = Human.objects.create(
            name="Elsewhere", owner=self.users["owner"], chronicle=self.other_chronicle
        )
        self.login_as("owner")
        response = self.client.post(
            reverse("game:scene_add_character", kwargs={"pk": self.scene.pk}),
            {"character_to_add": stranger.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(_messages(response))
        self.assertFalse(self.scene.characters.filter(pk=stranger.pk).exists())

    def test_finished_scene_is_read_only(self):
        Scene.objects.filter(pk=self.scene.pk).update(finished=True)
        self.login_as("owner")
        response = self.client.post(
            reverse("game:scene_add_character", kwargs={"pk": self.scene.pk}),
            {"character_to_add": self.character.pk},
        )
        self.assertEqual(response.status_code, 403)


class ScenePostTests(GameActionTestBase):
    writers = {"owner"}

    def setUp(self):
        super().setUp()
        self.scene.characters.add(self.character)

    def reset(self):
        Post.objects.filter(scene=self.scene).delete()

    def test_matrix(self):
        url = reverse("game:scene_post", kwargs={"pk": self.scene.pk})
        self.assert_matrix(
            {
                "owner": 302,
                "player": 404,
                "st": 403,
                "other_line_st": 403,
                "other_chronicle_st": 404,
                "staff": 403,
                "anonymous": 401,
            },
            lambda: self.client.post(url, {"message": "Hello", "display_name": ""}),
            lambda: Post.objects.filter(scene=self.scene).exists(),
        )

    def test_invalid_post_writes_nothing(self):
        self.login_as("owner")
        response = self.client.post(
            reverse("game:scene_post", kwargs={"pk": self.scene.pk}), {"message": "   "}
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("Failed to create post. Please check your input.", _messages(response))
        self.assertFalse(Post.objects.filter(scene=self.scene).exists())

    def test_old_message_post_to_detail_is_rejected(self):
        self.login_as("owner")
        response = self.client.post(self.scene.get_absolute_url(), {"message": "Hello"})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Post.objects.filter(scene=self.scene).exists())


class JournalActionTests(GameActionTestBase):
    def setUp(self):
        super().setUp()
        self.journal, _ = Journal.objects.get_or_create(character=self.character)

    def reset(self):
        JournalEntry.objects.filter(journal=self.journal).delete()

    def test_entry_matrix(self):
        self.writers = {"owner"}
        url = reverse("game:journal_add_entry", kwargs={"pk": self.journal.pk})
        self.assert_matrix(
            {
                "owner": 302,
                "player": 404,
                "st": 403,
                "other_line_st": 403,
                "other_chronicle_st": 404,
                "staff": 403,
                "anonymous": 401,
            },
            lambda: self.client.post(url, {"date": "2024-01-01", "message": "Dear diary"}),
            lambda: JournalEntry.objects.filter(journal=self.journal).exists(),
        )

    def test_entry_redirects_so_refresh_does_not_resubmit(self):
        self.login_as("owner")
        response = self.client.post(
            reverse("game:journal_add_entry", kwargs={"pk": self.journal.pk}),
            {"date": "2024-01-01", "message": "Dear diary"},
        )
        self.assertRedirects(response, self.journal.get_absolute_url())

    def new_entry(self):
        return JournalEntry.objects.create(
            journal=self.journal,
            date=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            message="Entry",
        )

    def test_response_matrix(self):
        self.writers = {"st", "staff"}
        entry = self.new_entry()
        url = reverse("game:journal_respond", kwargs={"pk": self.journal.pk, "entry_pk": entry.pk})

        def reset():
            JournalEntry.objects.filter(pk=entry.pk).update(st_message="")

        self.reset = reset
        self.assert_matrix(
            {
                "owner": 403,
                "player": 404,
                "st": 302,
                "other_line_st": 403,
                "other_chronicle_st": 404,
                "staff": 302,
                "anonymous": 401,
            },
            lambda: self.client.post(url, {f"entry-{entry.pk}-st_message": "Noted"}),
            lambda: JournalEntry.objects.get(pk=entry.pk).st_message == "Noted",
        )

    def test_draft_owner_cannot_write_an_st_response_regression(self):
        # D5: the old handler accepted EDIT_FULL, which a draft owner holds.
        Human.objects.filter(pk=self.character.pk).update(status="Un")
        entry = self.new_entry()
        self.login_as("owner")
        response = self.client.post(
            reverse("game:journal_respond", kwargs={"pk": self.journal.pk, "entry_pk": entry.pk}),
            {f"entry-{entry.pk}-st_message": "I approve of myself"},
        )
        self.assertEqual(response.status_code, 403)
        entry.refresh_from_db()
        self.assertEqual(entry.st_message, "")

    def test_entry_of_another_journal_is_404(self):
        other = Human.objects.create(
            name="Other", owner=self.users["player"], chronicle=self.chronicle, status="App"
        )
        other_journal, _ = Journal.objects.get_or_create(character=other)
        entry = JournalEntry.objects.create(
            journal=other_journal,
            date=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            message="Theirs",
        )
        self.login_as("st")
        response = self.client.post(
            reverse("game:journal_respond", kwargs={"pk": self.journal.pk, "entry_pk": entry.pk}),
            {f"entry-{entry.pk}-st_message": "Noted"},
        )
        self.assertEqual(response.status_code, 404)

    def test_old_buttons_are_rejected(self):
        entry = self.new_entry()
        self.login_as("st")
        response = self.client.post(
            self.journal.get_absolute_url(),
            {"submit_response": str(entry.pk), f"entry-{entry.pk}-st_message": "Noted"},
        )
        self.assertEqual(response.status_code, 405)


class ChronicleActionTests(GameActionTestBase):
    def setUp(self):
        super().setUp()
        self.head = get_user_model().objects.create_user("action_head")
        self.chronicle.head_st = self.head
        self.chronicle.save()
        self.location = LocationModel.objects.create(name="Harbour", chronicle=self.chronicle)

    def test_story_matrix(self):
        self.writers = {"staff"}
        url = reverse("game:chronicle_create_story", kwargs={"pk": self.chronicle.pk})

        def reset():
            Story.objects.all().delete()

        self.reset = reset
        self.assert_matrix(
            {
                "owner": 403,
                "player": 404,
                "st": 403,
                "other_line_st": 403,
                "other_chronicle_st": 404,
                "staff": 302,
                "anonymous": 401,
            },
            lambda: self.client.post(url, {"name": "Act One"}),
            lambda: Story.objects.filter(name="Act One").exists(),
        )
        self.client.force_login(self.head)
        self.assertEqual(self.client.post(url, {"name": "Act Two"}).status_code, 302)

    def scene_data(self, **overrides):
        data = {
            "name": "New scene",
            "location": self.location.pk,
            "date_of_scene": "2024-02-02",
            "gameline": "wod",
        }
        data.update(overrides)
        return data

    def test_scene_matrix(self):
        self.writers = {"st", "staff"}
        url = reverse("game:chronicle_create_scene", kwargs={"pk": self.chronicle.pk})

        def reset():
            Scene.objects.filter(name="New scene").delete()

        self.reset = reset
        self.assert_matrix(
            {
                "owner": 403,
                "player": 404,
                "st": 302,
                # Offered only their own gameline, so "wod" is a form error.
                "other_line_st": 200,
                "other_chronicle_st": 404,
                "staff": 302,
                "anonymous": 401,
            },
            lambda: self.client.post(url, self.scene_data()),
            lambda: Scene.objects.filter(name="New scene").exists(),
        )

    def test_scene_redirects_to_the_new_scene(self):
        self.login_as("st")
        response = self.client.post(
            reverse("game:chronicle_create_scene", kwargs={"pk": self.chronicle.pk}),
            self.scene_data(),
        )
        scene = Scene.objects.get(name="New scene")
        self.assertRedirects(response, scene.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual(scene.chronicle, self.chronicle)

    def test_invalid_scene_rerenders_the_chronicle_with_errors_regression(self):
        # D10: the old handler re-rendered with an unbound form.
        self.login_as("st")
        response = self.client.post(
            reverse("game:chronicle_create_scene", kwargs={"pk": self.chronicle.pk}),
            self.scene_data(name=""),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, "This field is required.")
        self.assertFalse(Scene.objects.filter(chronicle=self.chronicle, name="").exists())

    def test_old_buttons_and_navigation_posts_are_rejected(self):
        self.login_as("staff")
        for data in (
            {"create_story": "", "name": "Old"},
            {"create_character": "", "char_type": "human"},
        ):
            with self.subTest(data=data):
                response = self.client.post(self.chronicle.get_absolute_url(), data)
                self.assertEqual(response.status_code, 405)
        self.assertFalse(Story.objects.filter(name="Old").exists())

    def test_get_is_rejected(self):
        self.login_as("staff")
        for name in ("game:chronicle_create_story", "game:chronicle_create_scene"):
            with self.subTest(name=name):
                response = self.client.get(reverse(name, kwargs={"pk": self.chronicle.pk}))
                self.assertEqual(response.status_code, 405)
