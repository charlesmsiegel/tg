from characters.models.werewolf.renownincident import RenownIncident
from django.test import TestCase


class TestRenownIncidentDetailView(TestCase):
    def setUp(self) -> None:
        self.renownincident = RenownIncident.objects.create(name="Test RenownIncident")
        self.url = self.renownincident.get_absolute_url()

    def test_renownincident_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_renownincident_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/renownincident/detail.html")


class TestRenownIncidentCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "RenownIncident",
            "description": "Test",
            "glory": 1,
            "honor": 1,
            "wisdom": 1,
            "posthumous": False,
            "only_once": False,
            "breed": "homid",
        }
        self.url = RenownIncident.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/renownincident/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RenownIncident.objects.count(), 1)
        self.assertEqual(RenownIncident.objects.first().name, "RenownIncident")


class TestRenownIncidentUpdateView(TestCase):
    def setUp(self):
        self.renownincident = RenownIncident.objects.create(
            name="Test RenownIncident",
            description="Test description",
        )
        self.valid_data = {
            "name": "RenownIncident Updated",
            "description": "Test",
            "glory": 1,
            "honor": 1,
            "wisdom": 1,
            "posthumous": False,
            "only_once": False,
            "breed": "homid",
        }
        self.url = self.renownincident.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/renownincident/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.renownincident.refresh_from_db()
        self.assertEqual(self.renownincident.name, "RenownIncident Updated")
        self.assertEqual(self.renownincident.description, "Test")
