from django.test import TestCase
from items.models.core import RangedWeapon


class TestRangedWeaponDetailView(TestCase):
    def setUp(self) -> None:
        self.item = RangedWeapon.objects.create(name="Test Weapon")
        self.url = self.item.get_absolute_url()

    def test_object_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/rangedweapon/detail.html")


class TestRangedWeaponCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Weapon",
            "description": "A test description for the weapon.",
            "difficulty": 6,
            "damage": 2,
            "damage_type": "L",
            "conceal": "P",
            "range": 100,
            "rate": 3,
            "clip": 17,
        }
        self.url = RangedWeapon.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/rangedweapon/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RangedWeapon.objects.count(), 1)
        self.assertEqual(RangedWeapon.objects.first().name, "Test Weapon")


class TestRangedWeaponUpdateView(TestCase):
    def setUp(self):
        self.item = RangedWeapon.objects.create(
            name="Weapon 1",
            description="Test description",
        )
        self.valid_data = {
            "name": "Test Weapon 2",
            "description": "A test description for the weapon.",
            "difficulty": 6,
            "damage": 2,
            "damage_type": "L",
            "conceal": "P",
            "range": 100,
            "rate": 3,
            "clip": 17,
        }
        self.url = self.item.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/rangedweapon/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Test Weapon 2")
        self.assertEqual(self.item.description, "A test description for the weapon.")
