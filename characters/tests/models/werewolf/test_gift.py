from django.test import TestCase

from characters.models.werewolf.gift import Gift


class TestGift(TestCase):
    def setUp(self):
        self.gift = Gift.objects.create()


class TestGiftDetailView(TestCase):
    def setUp(self) -> None:
        self.gift = Gift.objects.create(name="Test Gift")
        self.url = self.gift.get_absolute_url()

    def test_gift_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_gift_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/gift/detail.html")


class TestGiftCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Gift",
            "description": "Test",
            "rank": 2,
        }
        self.url = Gift.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/gift/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Gift.objects.count(), 1)
        self.assertEqual(Gift.objects.first().name, "Gift")


class TestGiftUpdateView(TestCase):
    def setUp(self):
        self.gift = Gift.objects.create(
            name="Test Gift",
            description="Test description",
        )
        self.valid_data = {
            "name": "Gift Updated",
            "description": "Test",
            "rank": 2,
        }
        self.url = self.gift.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/gift/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.gift.refresh_from_db()
        self.assertEqual(self.gift.name, "Gift Updated")
        self.assertEqual(self.gift.description, "Test")
