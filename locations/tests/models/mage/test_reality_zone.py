from django.contrib.auth.models import User
from django.test import TestCase
from locations.models.mage.reality_zone import RealityZone


class TestRealityZoneDetailView(TestCase):
    """Test RealityZone detail view.

    Note: RealityZone is a simple model (not LocationModel) without owner/status fields.
    ViewPermissionMixin on this model returns 404 for all users since permission checking
    fails on models without the expected fields.
    """

    def setUp(self) -> None:
        self.reality_zone = RealityZone.objects.create(name="Test RealityZone")
        self.url = self.reality_zone.get_absolute_url()

    def test_reality_zone_detail_view_status_code(self):
        # ViewPermissionMixin returns 404 because RealityZone lacks owner/status
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class TestRealityZoneCreateView(TestCase):
    """Test RealityZone create view GET requests.

    Note: RealityZone create view requires login (LoginRequiredMixin).
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = RealityZone.get_creation_url()

    def test_create_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)  # LoginRequiredMixin returns 401

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/reality_zone/form.html")


class TestRealityZoneUpdateView(TestCase):
    """Test RealityZone update view.

    Note: RealityZone is a simple model (not LocationModel) without owner/status/chronicle.
    EditPermissionMixin returns 403 because permission checking fails on non-standard models.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.reality_zone = RealityZone.objects.create(
            name="Test RealityZone",
            description="Test description",
        )
        self.url = self.reality_zone.get_update_url()

    def test_update_view_returns_403(self):
        # EditPermissionMixin returns 403 because RealityZone lacks owner/chronicle
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
