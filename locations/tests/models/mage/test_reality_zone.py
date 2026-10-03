from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from locations.models.mage.reality_zone import RealityZone
from locations.models.mage.sanctum import Sanctum
from locations.registry import registry


class TestRealityZoneDetailView(TestCase):
    """RealityZone is publicly readable reference data, without owner/status fields."""

    def setUp(self) -> None:
        self.reality_zone = RealityZone.objects.create(name="Test RealityZone")
        self.url = self.reality_zone.get_absolute_url()

    def test_reality_zone_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.reality_zone.name)


class RealityZoneAppliedToTests(TestCase):
    def test_every_registered_zone_bearing_location_is_included(self):
        zone = RealityZone.objects.create(name="Shared Zone")
        places = []
        for entry in registry:
            if any(field.name == "reality_zone" for field in entry.model._meta.fields):
                places.append(entry.model.objects.create(name=entry.slug, reality_zone=zone))
        self.assertCountEqual(zone.get_applied_to(), places)

    def test_every_zone_link_is_classified_as_player_data(self):
        for entry in registry:
            if any(field.name == "reality_zone" for field in entry.model._meta.fields):
                with self.subTest(model=entry.model):
                    zone = RealityZone.objects.create(name="Staff reference")
                    entry.model.objects.create(name=entry.slug, reality_zone=zone)
                    zone.refresh_from_db()
                    self.assertTrue(zone.is_player_zone)

    def test_failed_place_save_does_not_classify_an_unlinked_reference(self):
        zone = RealityZone.objects.create(name="Staff reference")
        with self.assertRaises(ValidationError):
            Sanctum.objects.create(name="Invalid place", gauntlet=11, reality_zone=zone)
        zone.refresh_from_db()
        self.assertFalse(zone.is_player_zone)
        self.assertFalse(zone.get_applied_to())

    def test_unsaved_link_does_not_classify_a_different_reference(self):
        original = RealityZone.objects.create(name="Original reference")
        replacement = RealityZone.objects.create(name="Unused reference")
        place = Sanctum.objects.create(name="Place", reality_zone=original)
        place.reality_zone = replacement
        place.description = "Description-only edit"
        place.save(update_fields=["description"])
        place.refresh_from_db()
        replacement.refresh_from_db()
        self.assertEqual(place.reality_zone_id, original.pk)
        self.assertFalse(replacement.is_player_zone)

    def test_positional_update_fields_does_not_classify_an_unsaved_link(self):
        original = RealityZone.objects.create(name="Original reference")
        replacement = RealityZone.objects.create(name="Unused reference")
        place = Sanctum.objects.create(name="Place", reality_zone=original)
        place.reality_zone = replacement
        place.description = "Description-only edit"
        place.save(False, False, None, ["description"])
        place.refresh_from_db()
        replacement.refresh_from_db()
        self.assertEqual(place.description, "Description-only edit")
        self.assertEqual(place.reality_zone_id, original.pk)
        self.assertFalse(replacement.is_player_zone)

    def test_generator_update_fields_keeps_description_edit_and_reference_public(self):
        original = RealityZone.objects.create(name="Original reference")
        replacement = RealityZone.objects.create(name="Unused reference")
        place = Sanctum.objects.create(name="Place", reality_zone=original)
        place.reality_zone = replacement
        place.description = "Description-only edit"
        place.save(update_fields=(name for name in ["description"]))
        place.refresh_from_db()
        replacement.refresh_from_db()
        self.assertEqual(place.description, "Description-only edit")
        self.assertEqual(place.reality_zone_id, original.pk)
        self.assertFalse(replacement.is_player_zone)


class TestRealityZoneCreateView(TestCase):
    """Test RealityZone create view GET requests.

    Note: RealityZone create view requires login (LoginRequiredMixin).
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password", is_staff=True
        )
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
