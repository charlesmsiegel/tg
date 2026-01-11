from django.test import TestCase

from characters.models.mage import Effect
from items.models.mage import Artifact


class TestArtifact(TestCase):
    def setUp(self):
        self.artifact = Artifact.objects.create(name="Test Artifact")
        self.power = Effect.objects.create(name="Power")

    def test_set_power(self):
        self.assertFalse(self.artifact.has_power())
        self.assertTrue(self.artifact.set_power(self.power))
        self.assertTrue(self.artifact.has_power())

    def test_has_power(self):
        self.assertFalse(self.artifact.has_power())
        self.artifact.set_power(self.power)
        self.assertTrue(self.artifact.has_power())


class TestArtifactDetailView(TestCase):
    def setUp(self) -> None:
        self.artifact = Artifact.objects.create(name="Test Artifact")
        self.url = self.artifact.get_absolute_url()

    def test_object_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/artifact/detail.html")


class TestArtifactCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Artifact",
            "description": "A test description for the artifact.",
            "rank": 2,
            "background_cost": 3,
            "quintessence_max": 5,
        }
        self.url = Artifact.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/artifact/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Artifact.objects.count(), 1)
        self.assertEqual(Artifact.objects.first().name, "Test Artifact")


class TestArtifactUpdateView(TestCase):
    def setUp(self):
        self.artifact = Artifact.objects.create(
            name="Test Artifact",
            description="Test description",
        )
        self.valid_data = {
            "name": "Test Artifact Updated",
            "description": "A test description for the artifact.",
            "rank": 2,
            "background_cost": 3,
            "quintessence_max": 5,
        }
        self.url = self.artifact.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/artifact/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.artifact.refresh_from_db()
        self.assertEqual(self.artifact.name, "Test Artifact Updated")
        self.assertEqual(self.artifact.description, "A test description for the artifact.")
