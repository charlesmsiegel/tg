"""Tests for the Freehold views."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core import Human
from locations.models.changeling import Freehold


class TestFreeholdCreateView(TestCase):
    """The direct (all-at-once) create view saves and owns the freehold (U10)."""

    def setUp(self):
        self.user = User.objects.create_user(username="creator", password="password")
        self.client.login(username="creator", password="password")
        self.url = reverse("locations:changeling:create:freehold_direct")
        self.data = {
            "name": "Direct Freehold",
            "description": "Made in one go",
            "archetype": "stronghold",
            "balefire": 2,
            "size": 2,
            "sanctuary": 1,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

    def test_post_creates_freehold_owned_by_creator(self):
        response = self.client.post(self.url, self.data)
        freehold = Freehold.objects.get(name="Direct Freehold")
        self.assertRedirects(response, freehold.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual(freehold.owner, self.user)
        self.assertIsNone(freehold.owned_by)

    def test_post_defaults_owned_by_to_first_character(self):
        character = Human.objects.create(name="Keeper", owner=self.user)
        self.client.post(self.url, self.data)
        freehold = Freehold.objects.get(name="Direct Freehold")
        self.assertEqual(freehold.owned_by_id, character.pk)

    def test_post_keeps_chosen_owned_by(self):
        Human.objects.create(name="First", owner=self.user)
        chosen = Human.objects.create(name="Chosen", owner=self.user)
        self.client.post(self.url, {**self.data, "owned_by": chosen.pk})
        freehold = Freehold.objects.get(name="Direct Freehold")
        self.assertEqual(freehold.owned_by_id, chosen.pk)

    def test_anonymous_post_is_denied(self):
        self.client.logout()
        response = self.client.post(self.url, self.data)
        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Freehold.objects.filter(name="Direct Freehold").exists())


class TestFreeholdBasicsView(TestCase):
    """The first wizard step makes the creator the owner so later steps admit them."""

    def setUp(self):
        self.user = User.objects.create_user(username="creator", password="password")
        self.client.login(username="creator", password="password")

    def test_basics_sets_owner_and_next_step_loads(self):
        self.client.post(
            reverse("locations:changeling:create:freehold"),
            {"name": "Wizard Freehold", "archetype": "hearth", "description": "Step one"},
        )
        freehold = Freehold.objects.get(name="Wizard Freehold")
        self.assertEqual(freehold.owner, self.user)
        response = self.client.get(freehold.get_update_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/changeling/freehold/chargen/features.html")
