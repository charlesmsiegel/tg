from django.contrib.auth.models import User
from django.test import TestCase

from game.models import Chronicle
from items.models.core import ItemModel


class TestItemDetailView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="password")
        self.item = ItemModel.objects.create(
            name="Test Item",
            owner=self.user,
            status="App",
        )
        self.url = self.item.get_absolute_url()

    def test_object_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/item/detail.html")


class TestItemCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.valid_data = {
            "name": "Test Item",
            "description": "A test description for the item.",
        }
        self.url = ItemModel.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/item/form.html")

    def test_create_view_successful_post(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ItemModel.objects.count(), 1)
        self.assertEqual(ItemModel.objects.first().name, "Test Item")


class TestItemUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.item = ItemModel.objects.create(
            name="Test Item",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.valid_data = {
            "name": "Test Item Updated",
            "description": "A test description for the item.",
        }
        self.url = self.item.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/core/item/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="st_user", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Test Item Updated")
        self.assertEqual(self.item.description, "A test description for the item.")
