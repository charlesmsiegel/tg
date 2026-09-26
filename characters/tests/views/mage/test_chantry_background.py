"""Regression tests for the Chantry background step in the Mage-family wizards."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.companion import Companion
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from game.models import Chronicle
from locations.models.mage.chantry import Chantry


class ChantryBackgroundStepMixin:
    """Build a character sitting on its wizard's Chantry step."""

    chantry_step = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="owner", password="password")
        cls.other = User.objects.create_user(username="other", password="password")
        cls.chronicle = Chronicle.objects.create(name="Chantry Chronicle")
        cls.chantry_bg, _ = Background.objects.get_or_create(
            property_name="chantry", defaults={"name": "Chantry"}
        )

    def make_character(self):
        raise NotImplementedError

    def setUp(self):
        self.character = self.make_character()
        self.rating = BackgroundRating.objects.create(
            char=self.character, bg=self.chantry_bg, rating=3
        )
        self.client.login(username="owner", password="password")
        self.url = self.character.get_absolute_url()

    def test_step_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chantry Background")
        self.assertContains(response, 'name="existing_chantry"')
        self.assertNotContains(response, 'name="total_points"')

    def test_create_makes_unfinished_player_owned_chantry(self):
        response = self.client.post(
            self.url,
            {"create_new": "on", "name": "House of Winds", "description": "Windy"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.character.get_absolute_url())
        chantry = Chantry.objects.get(name="House of Winds")
        self.assertEqual(chantry.owner, self.owner)
        self.assertEqual(chantry.chronicle, self.chronicle)
        self.assertEqual(chantry.status, "Un")
        self.assertEqual(chantry.creation_status, 1)
        self.assertEqual(chantry.total_points, 3)
        self.assertIn(self.character.pk, chantry.members.values_list("pk", flat=True))
        self.rating.refresh_from_db()
        self.assertTrue(self.rating.complete)
        self.assertEqual(self.rating.note, "House of Winds")
        self.assertEqual(self.rating.url, chantry.get_absolute_url())
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, self.chantry_step + 1)

    def test_join_existing_only_adds_points_and_membership(self):
        existing = Chantry.objects.create(
            name="Old Tower",
            owner=self.other,
            chronicle=self.chronicle,
            status="App",
            creation_status=7,
            total_points=10,
        )
        response = self.client.post(self.url, {"existing_chantry": existing.pk, "name": "Ignored"})
        self.assertEqual(response.status_code, 302)
        existing.refresh_from_db()
        self.assertEqual(existing.total_points, 13)
        self.assertEqual(existing.owner, self.other)
        self.assertEqual(existing.chronicle, self.chronicle)
        self.assertEqual(existing.status, "App")
        self.assertEqual(existing.creation_status, 7)
        self.assertEqual(existing.name, "Old Tower")
        self.assertIn(self.character.pk, existing.members.values_list("pk", flat=True))
        self.assertFalse(Chantry.objects.filter(name="Ignored").exists())
        self.rating.refresh_from_db()
        self.assertTrue(self.rating.complete)
        self.assertEqual(self.rating.note, "Old Tower")
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, self.chantry_step + 1)

    def test_create_without_name_is_form_error(self):
        response = self.client.post(self.url, {"create_new": "on", "name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        self.assertFalse(Chantry.objects.exists())
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, self.chantry_step)

    def test_select_without_choice_is_form_error(self):
        response = self.client.post(self.url, {"existing_chantry": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("existing_chantry", response.context["form"].errors)
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, self.chantry_step)

    def test_retired_chantry_cannot_be_joined(self):
        retired = Chantry.objects.create(
            name="Ruin", owner=self.other, chronicle=self.chronicle, status="Ret", total_points=5
        )
        response = self.client.post(self.url, {"existing_chantry": retired.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn("existing_chantry", response.context["form"].errors)
        retired.refresh_from_db()
        self.assertEqual(retired.total_points, 5)


class TestMageChantryStep(ChantryBackgroundStepMixin, TestCase):
    chantry_step = 20

    def make_character(self):
        return Mage.objects.create(
            name="Chantry Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=self.chantry_step,
            arete=1,
        )


class TestMtAHumanChantryStep(ChantryBackgroundStepMixin, TestCase):
    chantry_step = 13

    def make_character(self):
        return MtAHuman.objects.create(
            name="Chantry Human",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=self.chantry_step,
        )


class TestCompanionChantryStep(ChantryBackgroundStepMixin, TestCase):
    chantry_step = 13

    def make_character(self):
        return Companion.objects.create(
            name="Chantry Companion",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=self.chantry_step,
        )


class TestSorcererChantryStep(ChantryBackgroundStepMixin, TestCase):
    chantry_step = 17

    def make_character(self):
        return Sorcerer.objects.create(
            name="Chantry Sorcerer",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=self.chantry_step,
            sorcerer_type="hedge_mage",
        )
