from django.test import TestCase
from items.models.core import (
    Weapon,
)


class TestWeaponDetailView(TestCase):
    def setUp(self) -> None:
        self.item = Weapon.objects.create(name="Test Weapon")
        self.url = self.item.get_absolute_url()

    def test_object_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/weapon/detail.html")


class TestWeaponCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Weapon",
            "description": "A test description for the weapon.",
            "difficulty": 6,
            "damage": 2,
            "damage_type": "L",
            "conceal": "P",
        }
        self.url = Weapon.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/weapon/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Weapon.objects.count(), 1)
        self.assertEqual(Weapon.objects.first().name, "Test Weapon")


class TestWeaponUpdateView(TestCase):
    def setUp(self):
        self.item = Weapon.objects.create(
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
        }
        self.url = self.item.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/weapon/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Test Weapon 2")
        self.assertEqual(self.item.description, "A test description for the weapon.")
