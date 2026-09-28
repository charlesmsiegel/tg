"""Tests for Ritual views."""

from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from characters.models.demon.ritual import Ritual


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
            secondary_lore_requirements=[{"lore_id": cls.other.pk, "rating": 2}],
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
