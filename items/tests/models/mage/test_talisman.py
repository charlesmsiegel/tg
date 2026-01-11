
from django.test import TestCase

from characters.models.mage import Effect
from items.models.mage.talisman import Talisman


class TestTalisman(TestCase):
    def setUp(self):
        self.effect1 = Effect.objects.create(name="Effect 1", forces=3)
        self.effect2 = Effect.objects.create(name="Effect 2", life=2)
        self.effect3 = Effect.objects.create(name="Effect 3", time=3)

    def test_add_power(self):
        talisman = Talisman.objects.create(name="Test Talisman", rank=2)
        self.assertEqual(talisman.powers.count(), 0)
        talisman.add_power(self.effect1)
        self.assertEqual(talisman.powers.count(), 1)
        talisman.add_power(self.effect2)
        self.assertEqual(talisman.powers.count(), 2)

    def test_has_powers(self):
        talisman = Talisman.objects.create(name="Test Talisman 2", rank=2)
        self.assertFalse(talisman.has_powers())
        talisman.add_power(self.effect1)
        self.assertFalse(talisman.has_powers())
        talisman.add_power(self.effect2)
        self.assertTrue(talisman.has_powers())


class TestTalismanDetailView(TestCase):
    def setUp(self) -> None:
        self.talisman = Talisman.objects.create(name="Test Talisman")
        self.url = self.talisman.get_absolute_url()

    def test_object_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/talisman/detail.html")


class TestTalismanCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Talisman",
            "description": "A test description for the talisman.",
            "rank": 2,
            "background_cost": 3,
            "quintessence_max": 5,
            "arete": 2,
        }
        self.url = Talisman.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/talisman/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Talisman.objects.count(), 1)
        self.assertEqual(Talisman.objects.first().name, "Test Talisman")


class TestTalismanUpdateView(TestCase):
    def setUp(self):
        self.talisman = Talisman.objects.create(
            name="Test Talisman",
            description="Test description",
        )
        self.valid_data = {
            "name": "Test Talisman Updated",
            "description": "A test description for the talisman.",
            "rank": 2,
            "background_cost": 3,
            "quintessence_max": 5,
            "arete": 2,
        }
        self.url = self.talisman.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/talisman/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.talisman.refresh_from_db()
        self.assertEqual(self.talisman.name, "Test Talisman Updated")
        self.assertEqual(self.talisman.description, "A test description for the talisman.")
