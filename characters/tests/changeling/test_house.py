from characters.models.changeling.house import House
from django.test import TestCase


class TestHouseDetailView(TestCase):
    def setUp(self) -> None:
        self.house = House.objects.create(name="Test House")
        self.url = self.house.get_absolute_url()

    def test_house_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_house_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/house/detail.html")


class TestHouseCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "House",
            "description": "Test",
            "court": "seelie",
            "boon": "test boom",
            "flaw": "test flaw",
        }
        self.url = House.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/house/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(House.objects.count(), 1)
        self.assertEqual(House.objects.first().name, "House")


class TestHouseUpdateView(TestCase):
    def setUp(self):
        self.house = House.objects.create(
            name="Test House",
            description="Test description",
        )
        self.valid_data = {
            "name": "House Updated",
            "description": "Test",
            "court": "seelie",
            "boon": "test boom",
            "flaw": "test flaw",
        }
        self.url = self.house.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/house/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.house.refresh_from_db()
        self.assertEqual(self.house.name, "House Updated")
        self.assertEqual(self.house.description, "Test")
