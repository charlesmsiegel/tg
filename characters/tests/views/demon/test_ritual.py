"""Tests for Ritual views."""

import json

from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from characters.models.demon.ritual import Ritual
from characters.views.demon.ritual import RitualCreateView


class TestRitualListView(TestCase):
    """The ritual reference list is public and shows each ritual's lore, cost and house."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="password")
        cls.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", starting_torment=3, owner=cls.user
        )
        cls.lore = Lore.objects.create(
            name="Lore of Flame", property_name="flame", description="Fire."
        )
        for index in range(3):
            Ritual.objects.create(
                name=f"Ritual {index}",
                description="A ritual.",
                house=cls.house,
                primary_lore=cls.lore,
                primary_lore_rating=2,
                base_cost=9,
            )

    def test_list_renders_without_login(self):
        response = self.client.get(reverse("characters:demon:list:ritual"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/demon/ritual/list.html")
        self.assertContains(response, "Ritual 0")
        self.assertContains(response, "Lore of Flame")
        self.assertContains(response, "9 XP")
        self.assertContains(response, "Devils")
        self.assertContains(response, 'data-filterable-item data-name="ritual 0"')

    def test_list_loads_house_and_lore_with_the_rituals(self):
        url = reverse("characters:demon:list:ritual")
        self.client.get(url)  # warm session / content-type caches
        with CaptureQueriesContext(connection) as queries:
            self.client.get(url)
        ritual_queries = [q["sql"] for q in queries if "characters_ritual" in q["sql"]]
        self.assertEqual(len(ritual_queries), 1)
        lore_queries = [
            q["sql"]
            for q in queries
            if 'FROM "characters_lore"' in q["sql"] and "characters_ritual" not in q["sql"]
        ]
        self.assertEqual(lore_queries, [])

    def test_empty_list_shows_empty_state(self):
        Ritual.objects.all().delete()
        response = self.client.get(reverse("characters:demon:list:ritual"))
        self.assertContains(response, "No rituals found.")


class TestRitualDetailView(TestCase):
    """The ritual detail page renders its lore requirements and prose sections."""

    @classmethod
    def setUpTestData(cls):
        cls.lore = Lore.objects.create(
            name="Lore of Flame", property_name="flame", description="Fire."
        )
        cls.other = Lore.objects.create(
            name="Lore of the Winds", property_name="winds", description="Air."
        )
        cls.ritual = Ritual.objects.create(
            name="Call the Pyre",
            description="A ritual.",
            primary_lore=cls.lore,
            primary_lore_rating=3,
            secondary_lore_requirements=[{"lore": cls.other.property_name, "rating": 2}],
            system="Roll Intelligence + Occult.",
            flavor_text="Old words.",
        )

    def test_detail_shows_lore_requirements(self):
        response = self.client.get(self.ritual.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lore of Flame")
        self.assertContains(response, "Lore of the Winds")
        self.assertContains(response, "5 dots across 2 paths")
        self.assertContains(response, "Roll Intelligence + Occult.")
        self.assertContains(response, "Old words.")

    def test_structured_citations_render_instead_of_legacy_text(self):
        self.ritual.add_source("Demon Players Guide", 187)
        self.ritual.source_page = "Legacy citation"
        self.ritual.save()
        response = self.client.get(self.ritual.get_absolute_url())
        self.assertContains(response, "Demon Players Guide p. 187")
        self.assertNotContains(response, "Legacy citation")

    def test_legacy_citation_still_renders(self):
        self.ritual.source_page = "Old custom book p. 42"
        self.ritual.save()
        response = self.client.get(self.ritual.get_absolute_url())
        self.assertContains(response, "Old custom book p. 42")


class TestRitualUpdateView(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username="staff", is_staff=True)
        self.player = User.objects.create_user(username="player")
        self.lore = Lore.objects.create(name="Flame", property_name="flame")
        self.ritual = Ritual.objects.create(name="Fire")
        self.data = {
            "name": "Fire",
            "primary_lore_rating": 2,
            "base_cost": 6,
            "minimum_casting_time": 10,
            "secondary_lore_requirements": json.dumps([{"lore": "flame", "rating": 2}]),
        }

    def test_staff_can_save_durable_requirement_keys(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.ritual.get_update_url(), self.data)
        self.assertEqual(response.status_code, 302)
        self.ritual.refresh_from_db()
        self.assertEqual(self.ritual.secondary_lore_requirements, [{"lore": "flame", "rating": 2}])

    def test_unknown_lore_returns_form_error_without_saving(self):
        self.client.force_login(self.staff)
        self.data["secondary_lore_requirements"] = json.dumps([{"lore": "missing", "rating": 2}])
        response = self.client.post(self.ritual.get_update_url(), self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("secondary_lore_requirements", response.context["form"].errors)
        self.ritual.refresh_from_db()
        self.assertEqual(self.ritual.secondary_lore_requirements, [])

    def test_player_cannot_edit_reference_requirements(self):
        self.client.force_login(self.player)
        response = self.client.post(self.ritual.get_update_url(), self.data)
        self.assertEqual(response.status_code, 403)
        self.ritual.refresh_from_db()
        self.assertEqual(self.ritual.secondary_lore_requirements, [])

    def test_staff_can_clear_secondary_requirements_with_blank_input(self):
        self.ritual.secondary_lore_requirements = [{"lore": "flame", "rating": 2}]
        self.ritual.save()
        self.client.force_login(self.staff)
        self.data["secondary_lore_requirements"] = ""
        response = self.client.post(self.ritual.get_update_url(), self.data)
        self.assertEqual(response.status_code, 302)
        self.ritual.refresh_from_db()
        self.assertEqual(self.ritual.secondary_lore_requirements, [])

    def test_creation_form_accepts_blank_secondary_requirements(self):
        # This view has no routed create endpoint; exercise its actual ModelForm.
        self.data["name"] = "Simple fire"
        self.data["secondary_lore_requirements"] = ""
        form = RitualCreateView().get_form_class()(data=self.data)
        self.assertTrue(form.is_valid(), form.errors)
        ritual = form.save()
        self.assertEqual(ritual.secondary_lore_requirements, [])
