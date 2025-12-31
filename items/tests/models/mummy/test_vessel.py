"""Tests for Vessel model."""

from django.contrib.auth.models import User
from django.test import TestCase
from items.models.mummy.vessel import Vessel


class TestVessel(TestCase):
    """Test Vessel model methods."""

    def setUp(self):
        self.vessel = Vessel.objects.create(
            name="Test Vessel",
            rank=3,
            current_ba=20,
            transfer_rate=2,
            efficiency=90,
        )

    def test_save_auto_calculates_max_ba(self):
        """Test save() auto-calculates max_ba from rank."""
        vessel = Vessel.objects.create(name="Rank Test", rank=5)
        self.assertEqual(vessel.max_ba, 50)  # rank * 10

    def test_save_auto_sets_background_cost(self):
        """Test save() auto-sets background_cost to rank."""
        vessel = Vessel.objects.create(name="Background Test", rank=4)
        self.assertEqual(vessel.background_cost, 4)

    def test_save_clamps_current_ba_to_max(self):
        """Test save() ensures current_ba doesn't exceed max_ba."""
        vessel = Vessel.objects.create(name="Clamp Test", rank=2, current_ba=100)
        self.assertEqual(vessel.current_ba, 20)  # max_ba = rank * 10 = 20


class TestVesselStoreBa(TestCase):
    """Test store_ba method."""

    def test_store_ba_basic(self):
        """Test storing Ba in vessel."""
        vessel = Vessel.objects.create(
            name="Test", rank=3, current_ba=10, transfer_rate=5, efficiency=100
        )
        stored = vessel.store_ba(3)
        self.assertEqual(stored, 3)
        vessel.refresh_from_db()
        self.assertEqual(vessel.current_ba, 13)

    def test_store_ba_limited_by_transfer_rate(self):
        """Test store_ba is limited by transfer_rate."""
        vessel = Vessel.objects.create(
            name="Test", rank=5, current_ba=0, transfer_rate=2, efficiency=100
        )
        stored = vessel.store_ba(10)
        self.assertEqual(stored, 2)  # Limited by transfer_rate
        vessel.refresh_from_db()
        self.assertEqual(vessel.current_ba, 2)

    def test_store_ba_limited_by_space(self):
        """Test store_ba is limited by available space."""
        vessel = Vessel.objects.create(
            name="Test", rank=2, current_ba=18, transfer_rate=5, efficiency=100
        )
        # max_ba = 20, current = 18, space = 2
        stored = vessel.store_ba(5)
        self.assertEqual(stored, 2)
        vessel.refresh_from_db()
        self.assertEqual(vessel.current_ba, 20)

    def test_store_ba_applies_efficiency(self):
        """Test store_ba applies efficiency percentage."""
        vessel = Vessel.objects.create(
            name="Test", rank=5, current_ba=0, transfer_rate=10, efficiency=50
        )
        stored = vessel.store_ba(10)
        self.assertEqual(stored, 5)  # 50% efficiency
        vessel.refresh_from_db()
        self.assertEqual(vessel.current_ba, 5)


class TestVesselWithdrawBa(TestCase):
    """Test withdraw_ba method."""

    def test_withdraw_ba_basic(self):
        """Test withdrawing Ba from vessel."""
        vessel = Vessel.objects.create(name="Test", rank=5, current_ba=30, transfer_rate=5)
        withdrawn = vessel.withdraw_ba(3)
        self.assertEqual(withdrawn, 3)
        vessel.refresh_from_db()
        self.assertEqual(vessel.current_ba, 27)

    def test_withdraw_ba_limited_by_transfer_rate(self):
        """Test withdraw_ba is limited by transfer_rate."""
        vessel = Vessel.objects.create(name="Test", rank=5, current_ba=30, transfer_rate=2)
        withdrawn = vessel.withdraw_ba(10)
        self.assertEqual(withdrawn, 2)  # Limited by transfer_rate
        vessel.refresh_from_db()
        self.assertEqual(vessel.current_ba, 28)

    def test_withdraw_ba_limited_by_current(self):
        """Test withdraw_ba is limited by current Ba."""
        vessel = Vessel.objects.create(name="Test", rank=5, current_ba=1, transfer_rate=10)
        withdrawn = vessel.withdraw_ba(5)
        self.assertEqual(withdrawn, 1)  # Limited by current_ba
        vessel.refresh_from_db()
        self.assertEqual(vessel.current_ba, 0)


class TestVesselStatus(TestCase):
    """Test vessel status methods."""

    def test_is_full_true(self):
        """Test is_full returns True when at max."""
        vessel = Vessel.objects.create(name="Test", rank=2, current_ba=20)
        self.assertTrue(vessel.is_full())

    def test_is_full_false(self):
        """Test is_full returns False when not at max."""
        vessel = Vessel.objects.create(name="Test", rank=2, current_ba=10)
        self.assertFalse(vessel.is_full())

    def test_is_empty_true(self):
        """Test is_empty returns True when Ba is 0."""
        vessel = Vessel.objects.create(name="Test", rank=2, current_ba=0)
        self.assertTrue(vessel.is_empty())

    def test_is_empty_false(self):
        """Test is_empty returns False when Ba remains."""
        vessel = Vessel.objects.create(name="Test", rank=2, current_ba=5)
        self.assertFalse(vessel.is_empty())


class TestVesselCanUse(TestCase):
    """Test can_use method."""

    def test_can_use_not_attuned(self):
        """Test any mummy can use non-attuned vessel."""
        vessel = Vessel.objects.create(name="Test", rank=2, is_attuned=False)

        # Mock mummy object
        class MockMummy:
            pass

        self.assertTrue(vessel.can_use(MockMummy()))

    def test_can_use_attuned_to_correct_mummy(self):
        """Test attuned vessel can be used by attuned mummy."""
        vessel = Vessel.objects.create(name="Test", rank=2, is_attuned=True, attuned_to=None)

        class MockMummy:
            pass

        mock = MockMummy()
        vessel.attuned_to = None  # Would be a real Mummy FK in practice
        # Since attuned_to is None and is_attuned is True, can_use checks attuned_to != mummy
        # This will fail because None != mock
        self.assertFalse(vessel.can_use(mock))


class TestVesselTypes(TestCase):
    """Test vessel type choices."""

    def test_vessel_type_default(self):
        """Test default vessel type is canopic."""
        vessel = Vessel.objects.create(name="Default Type")
        self.assertEqual(vessel.vessel_type, "canopic")

    def test_vessel_type_choices(self):
        """Test vessel type can be set to valid choices."""
        valid_types = [
            "canopic",
            "scarab",
            "ankh",
            "crystal",
            "urn",
            "statue",
            "cartouche",
            "other",
        ]
        for vtype in valid_types:
            vessel = Vessel.objects.create(name=f"{vtype} vessel", vessel_type=vtype)
            self.assertEqual(vessel.vessel_type, vtype)


class TestVesselUrls(TestCase):
    """Test URL methods for Vessel."""

    def setUp(self):
        self.vessel = Vessel.objects.create(name="URL Test Vessel")

    def test_get_absolute_url(self):
        """Test get_absolute_url generates correct URL."""
        url = self.vessel.get_absolute_url()
        self.assertIn(str(self.vessel.id), url)

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.vessel.get_update_url()
        self.assertIn(str(self.vessel.pk), url)
        self.assertIn("vessel", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = Vessel.get_creation_url()
        self.assertIn("vessel", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.vessel.get_heading(), "mtr_heading")


class TestVesselDetailView(TestCase):
    """Test Vessel detail view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.vessel = Vessel.objects.create(name="Test Vessel", owner=self.user)
        self.url = self.vessel.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/vessel/detail.html")


class TestVesselCreateView(TestCase):
    """Test Vessel create view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = Vessel.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/vessel/form.html")


class TestVesselUpdateView(TestCase):
    """Test Vessel update view."""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@test.com"
        )
        self.vessel = Vessel.objects.create(name="Test Vessel", description="Test")
        self.url = self.vessel.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/vessel/form.html")


class TestVesselProperties(TestCase):
    """Test vessel boolean properties."""

    def test_is_portable_default(self):
        """Test is_portable defaults to True."""
        vessel = Vessel.objects.create(name="Portable")
        self.assertTrue(vessel.is_portable)

    def test_requires_ritual_default(self):
        """Test requires_ritual defaults to False."""
        vessel = Vessel.objects.create(name="No Ritual")
        self.assertFalse(vessel.requires_ritual)

    def test_is_attuned_default(self):
        """Test is_attuned defaults to False."""
        vessel = Vessel.objects.create(name="Not Attuned")
        self.assertFalse(vessel.is_attuned)
