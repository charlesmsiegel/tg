from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.core import LocationModel


class TestLocation(TestCase):
    def setUp(self) -> None:
        self.location = LocationModel.objects.create(name="Location 1")
        self.child = LocationModel.objects.create(name="Location 2", parent=self.location)

    def test_location_parent(self):
        self.assertEqual(self.child.parent, self.location)
        self.assertIn(self.child, self.location.children.all())


class TestLocationDetailView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="password")
        self.location = LocationModel.objects.create(
            name="Location 1",
            description="Test description",
            owner=self.user,
            status="App",
        )
        self.url = self.location.get_absolute_url()

    def test_location_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_location_detail_view_templates(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/detail.html")

    def test_detail_view_content(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertContains(response, self.location.name)
        self.assertContains(response, self.location.description)
        self.assertContains(response, self.location.gauntlet)


class TestLocationCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.valid_data = {
            "name": "Test Name",
            "description": "Test Description",
            "gauntlet": 6,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        self.invalid_data = {"name": "", "description": ""}
        self.url = LocationModel.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/form.html")

    def test_create_view_successful_post(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LocationModel.objects.count(), 1)
        self.assertEqual(LocationModel.objects.first().name, "Test Name")


class TestLocationUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.location = LocationModel.objects.create(
            name="Location 1",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.valid_data = {
            "name": "Test Name Updated",
            "description": "Test Description Updated",
            "gauntlet": 6,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        self.url = self.location.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/core/location/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="st_user", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Test Name Updated")
        self.assertEqual(self.location.description, "Test Description Updated")
