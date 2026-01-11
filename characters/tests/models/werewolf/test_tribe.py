from django.test import TestCase

from characters.models.werewolf.tribe import Tribe


class TestTribeDetailView(TestCase):
    def setUp(self) -> None:
        self.tribe = Tribe.objects.create(name="Test Tribe")
        self.url = self.tribe.get_absolute_url()

    def test_tribe_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_tribe_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/tribe/detail.html")


class TestTribeCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Tribe",
            "description": "Test",
            "willpower": 3,
        }
        self.url = Tribe.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/tribe/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tribe.objects.count(), 1)
        self.assertEqual(Tribe.objects.first().name, "Tribe")


class TestTribeUpdateView(TestCase):
    def setUp(self):
        self.tribe = Tribe.objects.create(
            name="Test Tribe",
            description="Test description",
        )
        self.valid_data = {
            "name": "Tribe Updated",
            "description": "Test",
            "willpower": 3,
        }
        self.url = self.tribe.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/tribe/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.tribe.refresh_from_db()
        self.assertEqual(self.tribe.name, "Tribe Updated")
        self.assertEqual(self.tribe.description, "Test")
