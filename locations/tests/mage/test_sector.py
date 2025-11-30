from django.test import TestCase
from locations.models.mage.sector import Sector


class TestSectorDetailView(TestCase):
    def setUp(self) -> None:
        self.sector = Sector.objects.create(name="Test Sector")
        self.url = self.sector.get_absolute_url()

    def test_sector_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_sector_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sector/detail.html")


class TestSectorCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Sector",
            "reality_zone": "Test RZ",
            "description": "Test Sector",
            "sector_class": "virgin",
            "constraints": "test",
        }
        self.url = Sector.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sector/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Sector.objects.count(), 1)
        self.assertEqual(Sector.objects.first().name, "Sector")


class TestSectorUpdateView(TestCase):
    def setUp(self):
        self.sector = Sector.objects.create(
            name="Test Sector",
            description="Test description",
        )
        self.valid_data = {
            "name": "Sector Updated",
            "reality_zone": "Test RZ",
            "description": "Test Sector",
            "sector_class": "virgin",
            "constraints": "test",
        }
        self.url = self.sector.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sector/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.sector.refresh_from_db()
        self.assertEqual(self.sector.name, "Sector Updated")
        self.assertEqual(self.sector.description, "Test Sector")
