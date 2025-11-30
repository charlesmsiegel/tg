from django.test import TestCase
from locations.models.mage.reality_zone import RealityZone


class TestRealityZoneDetailView(TestCase):
    def setUp(self) -> None:
        self.reality_zone = RealityZone.objects.create(name="Test RealityZone")
        self.url = self.reality_zone.get_absolute_url()

    def test_reality_zone_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_reality_zone_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/reality_zone/detail.html")


class TestRealityZoneCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "RealityZone",
            "description": "Test RealityZone",
        }
        self.url = RealityZone.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/reality_zone/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RealityZone.objects.count(), 1)
        self.assertEqual(RealityZone.objects.first().name, "RealityZone")


class TestRealityZoneUpdateView(TestCase):
    def setUp(self):
        self.reality_zone = RealityZone.objects.create(
            name="Test RealityZone",
            description="Test description",
        )
        self.valid_data = {
            "name": "RealityZone Updated",
            "description": "Test RealityZone",
        }
        self.url = self.reality_zone.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/reality_zone/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.reality_zone.refresh_from_db()
        self.assertEqual(self.reality_zone.name, "RealityZone Updated")
        self.assertEqual(self.reality_zone.description, "Test RealityZone")
