from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.mage.realm import HorizonRealm


class TestHorizonRealmDetailView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="password")
        self.realm = HorizonRealm.objects.create(
            name="Test HorizonRealm",
            owner=self.user,
            status="App",
        )
        self.url = self.realm.get_absolute_url()

    def test_realm_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_realm_detail_view_templates(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/detail.html")


class TestHorizonRealmCreateView(TestCase):
    """Test HorizonRealm create view GET requests.

    Note: POST tests require complex form validation which is beyond the scope
    of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = HorizonRealm.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/form.html")


class TestHorizonRealmUpdateView(TestCase):
    """Test HorizonRealm update view GET requests.

    Note: POST tests require complex form validation which is beyond the scope
    of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.realm = HorizonRealm.objects.create(
            name="Test HorizonRealm",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.realm.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/realm/form.html")
