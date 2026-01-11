from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core import Character
from locations.models.core import City


class TestCity(TestCase):
    """Manage Tests for City"""

    def test_add_character(self):
        city = City.objects.create(name="New York City", population=28000000)
        player = User.objects.create_user(username="User")
        char = Character.objects.create(name="NPC 1", owner=player)
        city.add_character(char)
        self.assertIn(char, city.characters.all())


class TestCityDetailView(TestCase):
    def setUp(self) -> None:
        self.location = City.objects.create(name="Test Location")
        self.url = self.location.get_absolute_url()

    def test_location_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_location_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/city/detail.html")


class TestCityCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test City",
            "description": "A test description for the city.",
            "status": "App",
            "gauntlet": 6,
            "shroud": 5,
            "dimension_barrier": 5,
            "population": 800000,
            "mood": "None",
            "theme": "Test theme",
            "media": "Only National",
            "politicians": "White dudes",
        }
        self.url = City.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/city/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(City.objects.first().name, "Test City")


class TestCityUpdateView(TestCase):
    def setUp(self):
        self.location = City.objects.create(
            name="Location 1",
            description="Test description",
            population=10000,
        )
        self.valid_data = {
            "name": "Test City Updated",
            "description": "A test description for the city.",
            "status": "App",
            "gauntlet": 6,
            "shroud": 5,
            "dimension_barrier": 5,
            "population": 2,
            "mood": "None",
            "theme": "Test theme",
            "media": "Only National",
            "politicians": "White dudes",
        }
        self.url = self.location.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/city/form.html")

    def test_update_view_successful_post(self):
        self.assertEqual(self.location.population, 10000)
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Test City Updated")
        self.assertEqual(self.location.description, "A test description for the city.")
        self.assertEqual(self.location.population, 2)
