"""CharacterTemplate.apply_to_character, clean() and theming (U15)."""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.models.mage.mtahuman import MtAHuman
from core.models import CharacterTemplate, Language, TemplateApplication
from core.templatetags.tl import gameline_code


class CharacterTemplateApplyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="player")
        Archetype.objects.create(name="Visionary")
        Background.objects.create(name="Resources", property_name="resources")
        MeritFlaw.objects.create(name="Acute Sense")
        Ability.objects.create(name="Alertness", property_name="alertness")
        Language.objects.create(name="Latin")
        cls.template = CharacterTemplate.objects.create(
            name="Hedge Scholar",
            gameline="mta",
            character_type="mage",
            basic_info={"nature": "FK:Archetype:Visionary", "concept": "Scholar"},
            attributes={"intelligence": 4},
            abilities={"alertness": 2},
            backgrounds=[{"name": "Resources", "rating": 2}],
            merits_flaws=[{"name": "Acute Sense", "rating": 1}],
            specialties=["Alertness (Traps)"],
            languages=["Latin"],
        )

    def test_apply_sets_traits_and_creates_related_rows(self):
        character = MtAHuman.objects.create(name="Applied", owner=self.user)

        self.template.apply_to_character(character)

        character.refresh_from_db()
        self.assertEqual(character.nature.name, "Visionary")
        self.assertEqual(character.concept, "Scholar")
        self.assertEqual(character.intelligence, 4)
        self.assertEqual(character.alertness, 2)
        rating = BackgroundRating.objects.get(char=character)
        self.assertEqual((rating.bg.name, rating.rating), ("Resources", 2))
        mf = MeritFlawRating.objects.get(character=character)
        self.assertEqual((mf.mf.name, mf.rating), ("Acute Sense", 1))
        specialty = character.specialties.get()
        self.assertEqual((specialty.name, specialty.stat), ("Traps", "alertness"))
        self.assertEqual([x.name for x in character.languages.all()], ["Latin"])
        self.assertTrue(
            TemplateApplication.objects.filter(character=character, template=self.template).exists()
        )
        self.template.refresh_from_db()
        self.assertEqual(self.template.times_used, 1)

    def test_specialty_rows_are_shared(self):
        first = MtAHuman.objects.create(name="First", owner=self.user)
        second = MtAHuman.objects.create(name="Second", owner=self.user)
        self.template.apply_to_character(first)
        self.template.apply_to_character(second)
        self.assertEqual(first.specialties.get(), second.specialties.get())


class CharacterTemplateGamelineTests(TestCase):
    def test_clean_accepts_every_configured_gameline(self):
        for gameline in ("mtr", "htr"):
            with self.subTest(gameline=gameline):
                template = CharacterTemplate(
                    name=f"{gameline} template", gameline=gameline, character_type="mortal"
                )
                template.full_clean()

    def test_clean_rejects_unknown_gameline(self):
        template = CharacterTemplate(name="Bad", gameline="xyz", character_type="mortal")
        with self.assertRaises(ValidationError) as ctx:
            template.full_clean()
        self.assertIn("gameline", ctx.exception.message_dict)

    def test_theme_follows_the_template_gameline(self):
        template = CharacterTemplate(name="Themed", gameline="wta", character_type="werewolf")
        self.assertEqual(template.get_gameline(), "wta")
        self.assertEqual(template.get_heading(), "wta_heading")
        self.assertEqual(gameline_code(template), "wta")
