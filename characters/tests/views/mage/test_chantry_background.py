"""Regression tests for the Chantry background step in the Mage-family wizards."""

from unittest import mock

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.companion import Companion
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.views.mage.mage import MageChantryView
from game.models import Chronicle
from locations.forms.mage.chantry import ChantrySelectOrCreateForm
from locations.models.mage.chantry import Chantry
from locations.services import chantry_points


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
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
            creation_status=2,
            total_points=10,
        )
        response = self.client.post(self.url, {"existing_chantry": existing.pk, "name": "Ignored"})
        self.assertEqual(response.status_code, 302)
        existing.refresh_from_db()
        self.assertEqual(existing.total_points, 13)
        self.assertEqual(existing.owner, self.owner)
        self.assertEqual(existing.chronicle, self.chronicle)
        self.assertEqual(existing.status, "Un")
        self.assertEqual(existing.creation_status, 2)
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

    def test_another_players_approved_chantry_cannot_be_joined(self):
        """Pooling points into someone else's chantry would raise its rank unspendably."""
        existing = Chantry.objects.create(
            name="Their Tower",
            owner=self.other,
            chronicle=self.chronicle,
            status="App",
            creation_status=7,
            total_points=10,
        )
        response = self.client.post(self.url, {"existing_chantry": existing.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn("existing_chantry", response.context["form"].errors)
        existing.refresh_from_db()
        self.assertEqual(existing.total_points, 10)
        self.assertFalse(existing.members.filter(pk=self.character.pk).exists())
        self.rating.refresh_from_db()
        self.assertFalse(self.rating.complete)

    def test_another_players_draft_cannot_be_joined(self):
        draft = Chantry.objects.create(
            name="Their Draft", owner=self.other, chronicle=self.chronicle, status="Un"
        )
        response = self.client.post(self.url, {"existing_chantry": draft.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn("existing_chantry", response.context["form"].errors)
        draft.refresh_from_db()
        self.assertEqual(draft.total_points, 0)

    def test_a_join_refused_at_save_time_is_a_form_error_and_claims_nothing(self):
        """A chantry approved between validation and save leaves the step unfinished."""
        existing = Chantry.objects.create(
            name="Closing", owner=self.owner, chronicle=self.chronicle, status="Un", total_points=10
        )
        with mock.patch.object(
            chantry_points, "add_points", side_effect=ValidationError("No longer being built.")
        ):
            response = self.client.post(self.url, {"existing_chantry": existing.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn("No longer being built.", response.context["form"].non_field_errors())
        existing.refresh_from_db()
        self.assertEqual(existing.total_points, 10)
        self.assertFalse(existing.members.filter(pk=self.character.pk).exists())
        self.rating.refresh_from_db()
        self.assertFalse(self.rating.complete)
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


class TestChantryStepDoubleSubmit(TestCase):
    """A second POST that lost the claim race must not double-apply the background."""

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="racer", password="password")
        cls.chronicle = Chronicle.objects.create(name="Race Chronicle")
        cls.chantry_bg, _ = Background.objects.get_or_create(
            property_name="chantry", defaults={"name": "Chantry"}
        )
        cls.character = Mage.objects.create(
            name="Race Mage",
            owner=cls.owner,
            chronicle=cls.chronicle,
            creation_status=20,
            arete=1,
        )

    def setUp(self):
        self.rating = BackgroundRating.objects.create(
            char=self.character, bg=self.chantry_bg, rating=3, complete=False
        )

    def _stale_rating(self):
        """A rating whose DB row is already claimed, but this in-memory copy is not."""
        BackgroundRating.objects.filter(pk=self.rating.pk).update(complete=True)
        stale = BackgroundRating.objects.get(pk=self.rating.pk)
        stale.complete = False
        return stale

    def _build_view(self):
        view = MageChantryView()
        view.object = self.character
        view.kwargs = {"pk": self.character.pk}
        return view

    def test_stale_rating_join_does_not_double_add_points(self):
        existing = Chantry.objects.create(
            name="Race Tower",
            owner=self.owner,
            chronicle=self.chronicle,
            status="Un",
            total_points=10,
        )
        view = self._build_view()
        view.current_background = self._stale_rating()
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": existing.pk}, character=self.character, points=3
        )
        self.assertTrue(form.is_valid())

        response = view.form_valid(form)

        self.assertEqual(response.status_code, 302)
        existing.refresh_from_db()
        self.assertEqual(existing.total_points, 10)
        self.assertFalse(existing.members.filter(pk=self.character.pk).exists())
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, 20)

    def test_stale_rating_create_does_not_create_chantry(self):
        view = self._build_view()
        view.current_background = self._stale_rating()
        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "Ghost Chantry"},
            character=self.character,
            points=3,
        )
        self.assertTrue(form.is_valid())

        response = view.form_valid(form)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Chantry.objects.filter(name="Ghost Chantry").exists())
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, 20)


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
