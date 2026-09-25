from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from characters.models.core.human import Human
from game.models import Chronicle, Gameline, Journal, Scene, STRelationship


class RelationshipSecurityTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("scene_owner")
        self.st = users.objects.create_user("scene_st")
        self.wrong_st = users.objects.create_user("wrong_scene_st")
        self.first = Chronicle.objects.create(name="First chronicle")
        self.second = Chronicle.objects.create(name="Second chronicle")
        wod = Gameline.objects.create(name="World of Darkness")
        vtm = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(user=self.st, chronicle=self.first, gameline=wod)
        STRelationship.objects.create(user=self.wrong_st, chronicle=self.second, gameline=wod)
        self.other_line_st = users.objects.create_user("other_line_scene_st")
        STRelationship.objects.create(
            user=self.other_line_st, chronicle=self.first, gameline=vtm
        )
        self.character = Human.objects.create(
            name="First hero", owner=self.owner, chronicle=self.first
        )
        self.other_character = Human.objects.create(
            name="Second hero", owner=self.owner, chronicle=self.second
        )
        self.scene = Scene.objects.create(name="First scene", chronicle=self.first)

    def test_scene_rejects_character_from_another_chronicle(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            f"/game/scene/{self.scene.pk}/",
            {"character_to_add": str(self.other_character.pk)},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.scene.characters.filter(pk=self.other_character.pk).exists())

    def test_matching_st_and_staff_can_add_another_players_character(self):
        for user in (self.st, get_user_model().objects.create_user(
            "scene_staff", is_staff=True
        )):
            with self.subTest(user=user.username):
                self.scene.characters.clear()
                self.client.force_login(user)
                response = self.client.post(
                    f"/game/scene/{self.scene.pk}/",
                    {"character_to_add": str(self.character.pk)},
                )
                self.assertEqual(response.status_code, 302)
                self.assertTrue(
                    self.scene.characters.filter(pk=self.character.pk).exists()
                )

    def test_other_gameline_st_cannot_add_another_players_character(self):
        self.client.force_login(self.other_line_st)
        response = self.client.post(
            f"/game/scene/{self.scene.pk}/",
            {"character_to_add": str(self.character.pk)},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.scene.characters.filter(pk=self.character.pk).exists())

    def test_scene_rejects_malformed_character_id(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            f"/game/scene/{self.scene.pk}/", {"character_to_add": "bad-id"}
        )
        self.assertEqual(response.status_code, 400)

    def test_finished_scene_rejects_character_addition(self):
        self.scene.finished = True
        self.scene.save(update_fields=["finished"])
        self.client.force_login(self.owner)
        response = self.client.post(
            f"/game/scene/{self.scene.pk}/",
            {"character_to_add": str(self.character.pk)},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.scene.characters.filter(pk=self.character.pk).exists())

    def test_st_from_another_chronicle_cannot_close_scene(self):
        self.client.force_login(self.wrong_st)
        response = self.client.post(
            f"/game/scene/{self.scene.pk}/", {"close_scene": "1"}
        )
        self.assertEqual(response.status_code, 404)
        self.scene.refresh_from_db()
        self.assertFalse(self.scene.finished)

    def test_journal_response_must_target_entry_in_this_journal(self):
        journal = Journal.objects.get(character=self.character)
        other_journal = Journal.objects.get(character=self.other_character)
        entry = other_journal.add_post(timezone.now(), "private other journal entry")
        self.client.force_login(self.st)
        response = self.client.post(
            f"/game/journal/{journal.pk}/",
            {"submit_response": str(entry.pk), f"entry-{entry.pk}-st_message": "Leaked"},
        )
        self.assertEqual(response.status_code, 404)
        entry.refresh_from_db()
        self.assertEqual(entry.st_message, "")

    def test_journal_response_rejects_malformed_entry_id(self):
        journal = Journal.objects.get(character=self.character)
        self.client.force_login(self.st)
        response = self.client.post(
            f"/game/journal/{journal.pk}/",
            {"submit_response": "bad-id", "entry-bad-id-st_message": "No"},
        )
        self.assertEqual(response.status_code, 404)

    def test_st_of_other_gameline_cannot_publish_scene(self):
        self.client.force_login(self.other_line_st)
        response = self.client.post(
            f"/game/scene-manage/{self.scene.pk}/update/",
            {"name": "Published", "gameline": "wod", "visibility": "PUBLIC"},
        )
        self.assertEqual(response.status_code, 403)
        self.scene.refresh_from_db()
        self.assertEqual(self.scene.visibility, Scene.Visibility.CHRONICLE)

    def test_other_gameline_st_post_does_not_clear_waiting_flag(self):
        character = Human.objects.create(
            name="Other line ST character", owner=self.other_line_st,
            chronicle=self.first,
        )
        self.scene.characters.add(character)
        self.scene.waiting_for_st = True
        self.scene.save(update_fields=["waiting_for_st"])

        self.scene.add_post(character, character.name, "A character response")

        self.scene.refresh_from_db()
        self.assertTrue(self.scene.waiting_for_st)
