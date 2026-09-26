from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from characters.chargen.transitions import advance, previous_position
from characters.models.core import Character
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.sorcerer import Sorcerer
from characters.models.vampire.vampire import Vampire


class TransitionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username="transition-owner")
        cls.other = get_user_model().objects.create_user(username="transition-other")

    def vampire(self, **kwargs):
        return Vampire.objects.create(name="Transition", owner=self.owner, **kwargs)

    def test_unapproved_zero_freebies_are_not_skipped(self):
        character = self.vampire(creation_status=6, freebies=0)
        self.assertEqual(advance(character, user=self.owner), 7)
        self.assertFalse(character.languages.exists())

    def test_skips_consecutive_empty_steps_and_adds_default_language(self):
        character = self.vampire(creation_status=7, freebies=0, freebies_approved=True)
        self.assertEqual(advance(character, user=self.owner), 13)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 13)
        self.assertEqual(list(character.languages.values_list("name", flat=True)), ["English"])

    def test_stops_at_first_incomplete_background(self):
        character = self.vampire(creation_status=7, freebies=0, freebies_approved=True)
        bg = Background.objects.create(name="Mentor", property_name="mentor")
        BackgroundRating.objects.create(char=character, bg=bg, rating=1)
        self.assertEqual(advance(character, user=self.owner), 10)

    def test_authorization_precedes_language_side_effects(self):
        character = self.vampire(creation_status=7, freebies=0, freebies_approved=True)
        with self.assertRaises(PermissionDenied):
            advance(character, user=self.other)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 7)
        self.assertFalse(character.languages.exists())

    def test_submitted_characters_cannot_advance(self):
        character = self.vampire(creation_status=7, status="Sub")
        with self.assertRaises(PermissionDenied):
            advance(character, user=self.owner)

    def test_bad_position_cannot_mutate(self):
        character = self.vampire(creation_status=99)
        with self.assertRaises(ValueError):
            advance(character, user=self.owner)
        character.refresh_from_db()
        self.assertEqual(character.creation_status, 99)

    def test_sorcerer_branches(self):
        for kind, start, expected in (("hedge_mage", 3, 5), ("psychic", 4, 7)):
            with self.subTest(kind=kind):
                character = Sorcerer.objects.create(
                    name=kind, owner=self.owner, sorcerer_type=kind, creation_status=start
                )
                self.assertEqual(advance(character, user=self.owner), expected)

    def test_previous_position_skips_empty_steps_without_side_effects(self):
        character = self.vampire(creation_status=13)
        self.assertEqual(previous_position(character), 7)
        self.assertFalse(character.languages.exists())

    def test_freebie_filter_uses_registry_positions_and_concrete_content_types(self):
        from characters.models.core import Human
        from characters.models.demon.demon import Demon
        from characters.models.werewolf.bastet import Bastet
        from characters.models.werewolf.fomor import Fomor
        from characters.models.werewolf.garou import Werewolf
        from characters.models.wraith.wraith import Wraith

        for model, correct, wrong in (
            (Werewolf, 7, 5),
            (Wraith, 9, 7),
            (Demon, 8, 7),
            (Fomor, 6, 5),
            (Bastet, 8, 5),
            (Human, 5, 4),
        ):
            with self.subTest(model=model.__name__):
                character = model.objects.create(
                    name="Freebies", owner=self.owner, creation_status=correct
                )
                self.assertEqual(character.freebie_step, correct)
                self.assertEqual(model.freebie_step, correct)
                self.assertTrue(
                    Character.objects.at_freebie_step().filter(pk=character.pk).exists()
                )
                Character.objects.filter(pk=character.pk).update(creation_status=wrong)
                self.assertFalse(
                    Character.objects.at_freebie_step().filter(pk=character.pk).exists()
                )
