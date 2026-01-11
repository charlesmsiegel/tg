from django.test import TestCase

from characters.models.werewolf.camp import Camp


class TestCampDetailView(TestCase):
    def setUp(self) -> None:
        self.camp = Camp.objects.create(name="Test Camp")
        self.url = self.camp.get_absolute_url()

    def test_camp_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_camp_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/camp/detail.html")


class TestCampCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Camp",
            "description": "Test",
            "camp_type": "camp",
        }
        self.url = Camp.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/camp/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Camp.objects.count(), 1)
        self.assertEqual(Camp.objects.first().name, "Camp")


class TestCampUpdateView(TestCase):
    def setUp(self):
        self.camp = Camp.objects.create(
            name="Test Camp",
            description="Test description",
        )
        self.valid_data = {
            "name": "Camp Updated",
            "description": "Test",
            "camp_type": "camp",
        }
        self.url = self.camp.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/camp/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.camp.refresh_from_db()
        self.assertEqual(self.camp.name, "Camp Updated")
        self.assertEqual(self.camp.description, "Test")
