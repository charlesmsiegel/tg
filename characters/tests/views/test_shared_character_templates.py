"""Shared character templates (characters/templates/characters/shared/)."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.specialty import Specialty
from characters.models.mage.mtahuman import MtAHuman
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.wtohuman import WtOHuman


class AbilitySectionsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="pw")

    def test_primary_abilities_are_grouped_and_alphabetical(self):
        character = WtAHuman.objects.create(name="Kin", owner=self.user, primal_urge=2)
        sections = dict(character.ability_sections())
        self.assertEqual(list(sections), ["Talents", "Skills", "Knowledges"])
        labels = [label for label, _rating, _spec in sections["Talents"]]
        self.assertEqual(labels, sorted(labels))
        self.assertIn(("Primal-Urge", 2, None), sections["Talents"])

    def test_rows_carry_the_specialty(self):
        character = WtAHuman.objects.create(name="Kin", owner=self.user, alertness=4)
        character.specialties.add(Specialty.objects.create(name="Keen Ears", stat="alertness"))
        talents = dict(character.ability_sections())["Talents"]
        self.assertIn(("Alertness", 4, "Keen Ears"), talents)

    def test_secondary_columns_are_padded_to_the_same_length(self):
        character = MtAHuman.objects.create(name="Sleeper", owner=self.user, cooking=2)
        sections = character.secondary_ability_sections()
        self.assertEqual(
            [heading for heading, _rows in sections],
            ["Secondary Talents", "Secondary Skills", "Secondary Knowledges"],
        )
        self.assertEqual(sections[0][1], [("Cooking", 2, None)])
        self.assertEqual(sections[1][1], [("", 0, None)])

    def test_no_secondary_abilities_means_no_secondary_section(self):
        character = WtAHuman.objects.create(name="Kin", owner=self.user)
        self.assertEqual(character.secondary_ability_sections(), [])


class WraithSheetAbilitiesTest(TestCase):
    """wtohuman/detail.html used to inline an ability block reading context variables
    no view supplied, so Wraith sheets never showed specialties."""

    def test_wto_human_sheet_shows_ability_specialties(self):
        user = User.objects.create_user("owner", password="pw")
        character = WtOHuman.objects.create(name="Shade", owner=user, alertness=4, status="App")
        character.specialties.add(Specialty.objects.create(name="Keen Ears", stat="alertness"))
        self.client.force_login(user)
        response = self.client.get(character.get_absolute_url(), follow=True)
        self.assertTemplateUsed(response, "characters/shared/human/ability_block_display.html")
        self.assertContains(
            response, 'Alertness <span class="tl-trait__spec">Keen Ears</span>', html=False
        )
