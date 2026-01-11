from django.test import TestCase

from characters.models.changeling.legacy import Legacy


class TestLegacyDetailView(TestCase):
    def setUp(self) -> None:
        self.legacy = Legacy.objects.create(name="Test Legacy")
        self.url = self.legacy.get_absolute_url()

    def test_legacy_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_legacy_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/legacy/detail.html")


class TestLegacyCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Legacy",
            "description": "Test",
            "court": "seelie",
        }
        self.url = Legacy.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/legacy/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Legacy.objects.count(), 1)
        self.assertEqual(Legacy.objects.first().name, "Legacy")


class TestLegacyUpdateView(TestCase):
    def setUp(self):
        self.legacy = Legacy.objects.create(
            name="Test Legacy",
            description="Test description",
        )
        self.valid_data = {
            "name": "Legacy Updated",
            "description": "Test",
            "court": "seelie",
        }
        self.url = self.legacy.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/changeling/legacy/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.legacy.refresh_from_db()
        self.assertEqual(self.legacy.name, "Legacy Updated")
        self.assertEqual(self.legacy.description, "Test")
