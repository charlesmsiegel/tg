"""CharacterTemplate clean() and theming (U15)."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import CharacterTemplate
from core.templatetags.tl import gameline_code


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
