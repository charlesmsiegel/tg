from django.test import TestCase
from django.urls import reverse
from locations.models.core import LocationModel


# Create your tests here.
class TestLocation(TestCase):
    def setUp(self) -> None:
        self.location = LocationModel.objects.create(name="Location 1")
        self.child = LocationModel.objects.create(
            name="Location 2", parent=self.location
        )

    def test_location_parent(self):
        self.assertEqual(self.child.parent, self.location)
        self.assertIn(self.child, self.location.children.all())


class TestLocationDetailView(TestCase):
    def setUp(self) -> None:
        self.location = LocationModel.objects.create(
            name="Location 1", description="Test description", reality_zone="Test RZ"
        )
        self.url = self.location.get_absolute_url()

    def test_location_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_location_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/detail.html")

    def test_detail_view_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.location.name)
        self.assertContains(response, self.location.description)
        self.assertContains(response, self.location.gauntlet)
        self.assertContains(response, self.location.reality_zone)


class TestLocationCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Name",
            "description": "Test Description",
            "reality_zone": "Test RZ",
            "gauntlet": 6,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        self.invalid_data = {"name": "", "description": ""}
        self.url = reverse("locations:create:location")

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LocationModel.objects.count(), 1)
        self.assertEqual(LocationModel.objects.first().name, "Test Name")


class TestLocationUpdateView(TestCase):
    def setUp(self):
        self.location = LocationModel.objects.create(
            name="Location 1", description="Test description", reality_zone="Test RZ"
        )
        self.valid_data = {
            "name": "Test Name Updated",
            "description": "Test Description Updated",
            "reality_zone": "Test RZ Updated",
            "gauntlet": 6,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        self.url = self.location.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Test Name Updated")
        self.assertEqual(self.location.description, "Test Description Updated")
