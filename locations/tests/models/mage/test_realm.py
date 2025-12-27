from django.test import TestCase
from locations.models.mage.realm import HorizonRealm


class TestHorizonRealmDetailView(TestCase):
    def setUp(self) -> None:
        self.realm = HorizonRealm.objects.create(name="Test HorizonRealm")
        self.url = self.realm.get_absolute_url()

    def test_realm_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_realm_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/detail.html")


class TestHorizonRealmCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "HorizonRealm",
            "description": "Test",
        }
        self.url = HorizonRealm.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(HorizonRealm.objects.count(), 1)
        self.assertEqual(HorizonRealm.objects.first().name, "HorizonRealm")


class TestHorizonRealmUpdateView(TestCase):
    def setUp(self):
        self.realm = HorizonRealm.objects.create(
            name="Test HorizonRealm",
            description="Test description",
        )
        self.valid_data = {
            "name": "HorizonRealm Updated",
            "description": "Test",
        }
        self.url = self.realm.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.realm.refresh_from_db()
        self.assertEqual(self.realm.name, "HorizonRealm Updated")
        self.assertEqual(self.realm.description, "Test")
