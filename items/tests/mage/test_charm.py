from characters.models.mage import Effect
from characters.models.mage.resonance import Resonance
from django.contrib.auth.models import User
from django.test import TestCase
from items.models.mage import Charm


class TestCharm(TestCase):
    def setUp(self):
        self.charm = Charm.objects.create(name="Test Charm")
        self.power = Effect.objects.create(name="Power")

    def test_set_power(self):
        self.assertFalse(self.charm.has_power())
        self.assertTrue(self.charm.set_power(self.power))
        self.assertTrue(self.charm.has_power())

    def test_has_power(self):
        self.assertFalse(self.charm.has_power())
        self.charm.set_power(self.power)
        self.assertTrue(self.charm.has_power())


class TestCharmDetailView(TestCase):
    def setUp(self) -> None:
        self.wonder = Charm.objects.create(name="Test Charm")
        self.url = self.wonder.get_absolute_url()

    def test_object_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/charm/detail.html")


class TestCharmCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Charm",
            "description": "A test description for the charm.",
            "rank": 2,
            "background_cost": 3,
            "quintessence_max": 5,
            "arete": 2,
        }
        self.url = Charm.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/charm/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Charm.objects.count(), 1)
        self.assertEqual(Charm.objects.first().name, "Test Charm")


class TestCharmUpdateView(TestCase):
    def setUp(self):
        self.wonder = Charm.objects.create(
            name="Test Charm",
            description="Test description",
        )
        self.valid_data = {
            "name": "Test Charm Updated",
            "description": "A test description for the wonder.",
            "rank": 2,
            "background_cost": 3,
            "quintessence_max": 5,
            "arete": 2,
        }
        self.url = self.wonder.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/charm/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.wonder.refresh_from_db()
        self.assertEqual(self.wonder.name, "Test Charm Updated")
        self.assertEqual(self.wonder.description, "A test description for the wonder.")
