"""Tests that chargen pages render the client-side validation hooks."""

from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse

from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.core.background_block import Background
from characters.models.core.human import Human
from characters.models.mage.mtahuman import MtAHuman
from characters.models.vampire.vampire import Vampire
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.wtohuman import WtOHuman
from characters.tests.utils import human_setup


class TestChargenValidationRendering(TestCase):
    """The validation include and shared utilities must reach the page."""

    def setUp(self):
        human_setup()
        self.owner = User.objects.create_user(username="owner", password="password")

    def test_abilities_step_renders_validation(self):
        char = Human.objects.create(
            name="Ability Human", owner=self.owner, creation_status=2
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(char.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "abilities-validation-status")
        self.assertContains(response, "TG.validation")

    def test_abilities_step_renders_validation_other_gameline(self):
        char = VtMHuman.objects.create(
            name="Vampire Ability Human", owner=self.owner, creation_status=2
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(char.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "abilities-validation-status")
        self.assertContains(response, "TG.validation")

    def test_abilities_step_renders_validation_third_gameline(self):
        char = WtAHuman.objects.create(
            name="Werewolf Ability Human", owner=self.owner, creation_status=2
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(char.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "abilities-validation-status")
        self.assertContains(response, "TG.validation")

    def test_abilities_step_renders_validation_fourth_gameline(self):
        char = CtDHuman.objects.create(
            name="Changeling Ability Human", owner=self.owner, creation_status=2
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(char.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "abilities-validation-status")
        self.assertContains(response, "TG.validation")

    def test_abilities_step_renders_validation_all_gamelines(self):
        """WtOHuman and MtAHuman work now that their ability views set
        is_approved_user (two #1459 instances fixed in this PR)."""
        for model, name in [(WtOHuman, "Wraith"), (MtAHuman, "Mage")]:
            char = model.objects.create(
                name=f"{name} Ability Human", owner=self.owner, creation_status=2
            )
            self.client.login(username="owner", password="password")
            response = self.client.get(char.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "abilities-validation-status")
            self.assertContains(response, "TG.validation")

    def test_backgrounds_step_renders_validation(self):
        # The plain-Human step 3 template (core/human/chargen.html) has no
        # backgrounds block (pre-existing gap), so exercise a flow whose
        # template includes background_block/form.html: the Wraith human.
        char = WtOHuman.objects.create(
            name="Background Human", owner=self.owner, creation_status=3
        )
        self.client.login(username="owner", password="password")
        response = self.client.get(char.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "backgrounds-validation-status")
        self.assertContains(response, "TG.validation")
        # The multiplier map must render with real data, not fall back empty
        bg = Background.objects.filter(
            property_name__in=char.allowed_backgrounds
        ).first()
        self.assertIsNotNone(bg)
        self.assertContains(response, f'"{bg.pk}": {bg.multiplier}')

    def test_virtues_step_renders_validation(self):
        char = Vampire.objects.create(
            name="Virtue Vampire", owner=self.owner, creation_status=5
        )
        self.client.login(username="owner", password="password")
        # Vampire.get_absolute_url targets the plain detail view; chargen is
        # reached through the generic character dispatcher.
        response = self.client.get(
            reverse("characters:character", kwargs={"pk": char.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "virtues-validation-status")
        self.assertContains(response, "TG.validation")
