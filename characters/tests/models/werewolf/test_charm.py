from characters.models.werewolf import SpiritCharm
from django.test import TestCase


class TestSpiritCharmDetailView(TestCase):
    def setUp(self) -> None:
        self.charm = SpiritCharm.objects.create(name="Test SpiritCharm")
        self.url = self.charm.get_absolute_url()

    def test_charm_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_charm_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/charm/detail.html")


class TestSpiritCharmCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "SpiritCharm",
            "description": "Test",
        }
        self.url = SpiritCharm.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/charm/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SpiritCharm.objects.count(), 1)
        self.assertEqual(SpiritCharm.objects.first().name, "SpiritCharm")


class TestSpiritCharmUpdateView(TestCase):
    def setUp(self):
        self.charm = SpiritCharm.objects.create(
            name="Test SpiritCharm",
            description="Test description",
        )
        self.valid_data = {
            "name": "SpiritCharm Updated",
            "description": "Test",
        }
        self.url = self.charm.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/charm/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.charm.refresh_from_db()
        self.assertEqual(self.charm.name, "SpiritCharm Updated")
        self.assertEqual(self.charm.description, "Test")
