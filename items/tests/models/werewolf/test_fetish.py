from django.test import TestCase
from items.models.werewolf.fetish import Fetish


class TestFetish(TestCase):
    def test_save(self):
        fetish = Fetish.objects.create(name="Test Fetish", rank=2)
        self.assertEqual(fetish.background_cost, 2)


class TestFetishDetailView(TestCase):
    def setUp(self) -> None:
        self.fetish = Fetish.objects.create(name="Test Fetish")
        self.url = self.fetish.get_absolute_url()

    def test_fetish_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fetish_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/werewolf/fetish/detail.html")


class TestFetishCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Fetish",
            "rank": 2,
            "background_cost": 2,
            "quintessence_max": 2,
            "description": "Test",
            "gnosis": 2,
            "spirit": "Test",
        }
        self.url = Fetish.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/werewolf/fetish/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Fetish.objects.count(), 1)
        self.assertEqual(Fetish.objects.first().name, "Fetish")


class TestFetishUpdateView(TestCase):
    def setUp(self):
        self.fetish = Fetish.objects.create(
            name="Test Fetish",
            description="Test description",
        )
        self.valid_data = {
            "name": "Fetish Updated",
            "rank": 2,
            "background_cost": 2,
            "quintessence_max": 2,
            "description": "Test",
            "gnosis": 2,
            "spirit": "Test",
        }
        self.url = self.fetish.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/werewolf/fetish/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.fetish.refresh_from_db()
        self.assertEqual(self.fetish.name, "Fetish Updated")
        self.assertEqual(self.fetish.description, "Test")
