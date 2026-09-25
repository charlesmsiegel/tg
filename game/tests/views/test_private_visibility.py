from django.contrib.auth import get_user_model
from django.test import TestCase

from characters.models.core.human import Human
from game.models import (
    Chronicle,
    FreebieSpendingRecord,
    Gameline,
    Journal,
    Scene,
    STRelationship,
)


class PrivateVisibilityTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("private_owner")
        self.other = users.objects.create_user("private_other")
        self.same_chronicle_player = users.objects.create_user("same_chronicle_player")
        self.chronicle = Chronicle.objects.create(name="Private chronicle")
        self.character = Human.objects.create(
            name="Private character", owner=self.owner, chronicle=self.chronicle
        )
        self.other_character = Human.objects.create(
            name="Other character", owner=self.same_chronicle_player,
            chronicle=self.chronicle,
        )
        self.journal = Journal.objects.get(character=self.character)
        self.record = FreebieSpendingRecord.objects.create(
            character=self.character, trait_name="Secret spend",
            trait_type="custom", trait_value=1, cost=1,
        )
        self.scene = Scene.objects.create(name="Hidden scene", chronicle=self.chronicle)

    def test_private_journal_existing_and_missing_ids_look_identical(self):
        self.client.force_login(self.other)
        existing = self.client.get(f"/game/journal/{self.journal.pk}/")
        missing = self.client.get("/game/journal/999999/")
        self.assertEqual((existing.status_code, existing.content),
                         (missing.status_code, missing.content))
        self.assertEqual(existing.status_code, 404)

    def test_private_spending_record_existing_and_missing_ids_look_identical(self):
        self.client.force_login(self.other)
        existing = self.client.get(f"/game/freebie-spending-record/{self.record.pk}/")
        missing = self.client.get("/game/freebie-spending-record/999999/")
        self.assertEqual((existing.status_code, existing.content),
                         (missing.status_code, missing.content))
        self.assertEqual(existing.status_code, 404)

    def test_outside_player_cannot_discover_scene(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f"/game/scene/{self.scene.pk}/").status_code, 404)
        response = self.client.get("/game/scenes/")
        self.assertNotContains(response, "Hidden scene")

    def test_same_chronicle_player_cannot_list_another_players_private_records(self):
        self.client.force_login(self.same_chronicle_player)
        self.assertEqual(
            self.client.get(f"/game/journal/{self.journal.pk}/").status_code, 404
        )
        self.assertNotContains(self.client.get("/game/journals/"), "Private character")
        self.assertNotContains(
            self.client.get("/game/freebie-spending-record/list/"), "Secret spend"
        )

    def test_chronicle_rich_tables_only_include_full_readable_objects(self):
        self.client.force_login(self.same_chronicle_player)
        response = self.client.get(f"/game/chronicle/{self.chronicle.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Other character")
        self.assertNotContains(response, "Private character")

    def test_participants_only_scene_hides_from_other_chronicle_players(self):
        self.scene.visibility = Scene.Visibility.PARTICIPANTS
        self.scene.save()
        self.scene.characters.add(self.character)
        self.client.force_login(self.same_chronicle_player)
        self.assertEqual(self.client.get(f"/game/scene/{self.scene.pk}/").status_code, 404)
        self.assertNotContains(self.client.get("/game/scenes/"), "Hidden scene")
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(f"/game/scene/{self.scene.pk}/").status_code, 200)

    def test_public_scene_is_readable_without_login(self):
        self.scene.visibility = Scene.Visibility.PUBLIC
        self.scene.save()
        self.assertEqual(self.client.get(f"/game/scene/{self.scene.pk}/").status_code, 200)
        self.assertContains(self.client.get("/game/scenes/"), "Hidden scene")
        self.assertEqual(
            self.client.post(f"/game/scene/{self.scene.pk}/", {"close_scene": "1"}).status_code,
            401,
        )

    def test_storyteller_can_read_participants_only_scene(self):
        st = get_user_model().objects.create_user("private_scene_st")
        wod = Gameline.objects.create(name="World of Darkness")
        STRelationship.objects.create(user=st, chronicle=self.chronicle, gameline=wod)
        self.scene.visibility = Scene.Visibility.PARTICIPANTS
        self.scene.save()
        self.client.force_login(st)
        self.assertEqual(self.client.get(f"/game/scene/{self.scene.pk}/").status_code, 200)

    def test_character_sheet_does_not_reveal_cross_chronicle_hidden_scene(self):
        head = get_user_model().objects.create_user("character_chronicle_head")
        Chronicle.objects.filter(pk=self.chronicle.pk).update(head_st=head)
        Human.objects.filter(pk=self.character.pk).update(status="App")
        other_chronicle = Chronicle.objects.create(name="Other scene chronicle")
        hidden = Scene.objects.create(
            name="Invisible cross-chronicle scene",
            chronicle=other_chronicle,
            visibility=Scene.Visibility.PARTICIPANTS,
        )
        hidden.characters.add(self.character)

        self.client.force_login(head)
        response = self.client.get(self.character.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, hidden.name)
        self.assertNotIn(hidden.pk, [scene.pk for scene in response.context["scenes"]])
