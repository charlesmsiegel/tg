"""Tests for Mage Sector model."""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.mage.reality_zone import RealityZone
from locations.models.mage.sector import Sector


class TestSectorModel(TestCase):
    """Test Sector model methods and properties."""

    def setUp(self):
        self.sector = Sector.objects.create(name="Test Sector")

    def test_sector_str(self):
        """Test string representation includes name and class."""
        expected = f"Test Sector ({self.sector.get_sector_class_display()})"
        self.assertEqual(str(self.sector), expected)

    def test_sector_type(self):
        """Test sector type is correctly set."""
        self.assertEqual(self.sector.type, "sector")

    def test_sector_gameline(self):
        """Test sector gameline is mta."""
        self.assertEqual(self.sector.gameline, "mta")

    def test_get_heading(self):
        """Test get_heading returns mta_heading."""
        self.assertEqual(self.sector.get_heading(), "mta_heading")

    def test_default_sector_class(self):
        """Test default sector class is grid."""
        self.assertEqual(self.sector.sector_class, "grid")

    def test_default_access_level(self):
        """Test default access level is free."""
        self.assertEqual(self.sector.access_level, "free")


class TestSectorEffectiveDifficulty(TestCase):
    """Test get_effective_difficulty method."""

    def test_base_difficulty(self):
        """Test base difficulty is 6."""
        sector = Sector.objects.create(name="Test")
        difficulty = sector.get_effective_difficulty()
        self.assertEqual(difficulty, 6)

    def test_difficulty_with_reality_zone(self):
        """Test difficulty modified by reality zone."""
        rz = RealityZone.objects.create(name="Test RZ")
        sector = Sector.objects.create(
            name="Test", reality_zone=rz, difficulty_modifier=2
        )
        difficulty = sector.get_effective_difficulty()
        self.assertEqual(difficulty, 8)

    def test_difficulty_incompatible_paradigm(self):
        """Test additional penalty for incompatible paradigm."""
        sector = Sector.objects.create(name="Test", constraints="Cyberpunk only")
        difficulty = sector.get_effective_difficulty(paradigm_match=False)
        self.assertEqual(difficulty, 7)

    def test_difficulty_capped_at_minimum(self):
        """Test difficulty doesn't go below 3."""
        sector = Sector.objects.create(name="Test", difficulty_modifier=-5)
        rz = RealityZone.objects.create(name="Test RZ")
        sector.reality_zone = rz
        sector.save()
        difficulty = sector.get_effective_difficulty()
        self.assertEqual(difficulty, 3)

    def test_difficulty_capped_at_maximum(self):
        """Test difficulty doesn't go above 10."""
        rz = RealityZone.objects.create(name="Test RZ")
        sector = Sector.objects.create(
            name="Test",
            reality_zone=rz,
            difficulty_modifier=6,
            constraints="Very strict",
        )
        difficulty = sector.get_effective_difficulty(paradigm_match=False)
        self.assertEqual(difficulty, 10)


class TestSectorParadoxGeneration(TestCase):
    """Test generates_paradox_for_power method."""

    def test_no_paradox_within_power_rating(self):
        """Test no extra paradox when effect within power rating."""
        sector = Sector.objects.create(name="Test", power_rating=5)
        paradox = sector.generates_paradox_for_power(3)
        self.assertEqual(paradox, 0)

    def test_no_paradox_at_power_rating(self):
        """Test no extra paradox when effect equals power rating."""
        sector = Sector.objects.create(name="Test", power_rating=5)
        paradox = sector.generates_paradox_for_power(5)
        self.assertEqual(paradox, 0)

    def test_paradox_exceeds_power_rating(self):
        """Test extra paradox when effect exceeds power rating."""
        sector = Sector.objects.create(name="Test", power_rating=5)
        paradox = sector.generates_paradox_for_power(8)
        self.assertEqual(paradox, 3)


class TestSectorAccessibility(TestCase):
    """Test is_accessible_to method."""

    def test_free_sector_always_accessible(self):
        """Test free sectors are accessible without credentials."""
        sector = Sector.objects.create(name="Test", access_level="free")
        self.assertTrue(sector.is_accessible_to())
        self.assertTrue(sector.is_accessible_to("any_credentials"))

    def test_restricted_without_credentials(self):
        """Test restricted sectors need credentials."""
        sector = Sector.objects.create(name="Test", access_level="restricted")
        self.assertFalse(sector.is_accessible_to())

    def test_restricted_with_approved_credentials(self):
        """Test restricted sectors accessible with approved credentials."""
        sector = Sector.objects.create(
            name="Test",
            access_level="restricted",
            approved_users="admin\nviewer\noperator",
        )
        self.assertTrue(sector.is_accessible_to("admin"))
        self.assertTrue(sector.is_accessible_to("viewer"))

    def test_restricted_with_unapproved_credentials(self):
        """Test restricted sectors not accessible with wrong credentials."""
        sector = Sector.objects.create(
            name="Test",
            access_level="restricted",
            approved_users="admin\nviewer",
        )
        self.assertFalse(sector.is_accessible_to("hacker"))


class TestSectorWhiteoutRisk(TestCase):
    """Test get_whiteout_risk method."""

    def test_low_risk(self):
        """Test low risk with small paradox pool."""
        sector = Sector.objects.create(name="Test")
        self.assertEqual(sector.get_whiteout_risk(0), "low")
        self.assertEqual(sector.get_whiteout_risk(2), "low")

    def test_moderate_risk(self):
        """Test moderate risk with medium paradox pool."""
        sector = Sector.objects.create(name="Test")
        self.assertEqual(sector.get_whiteout_risk(3), "moderate")
        self.assertEqual(sector.get_whiteout_risk(5), "moderate")

    def test_high_risk(self):
        """Test high risk with large paradox pool."""
        sector = Sector.objects.create(name="Test")
        self.assertEqual(sector.get_whiteout_risk(6), "high")
        self.assertEqual(sector.get_whiteout_risk(10), "high")

    def test_critical_risk(self):
        """Test critical risk with very large paradox pool."""
        sector = Sector.objects.create(name="Test")
        self.assertEqual(sector.get_whiteout_risk(11), "critical")
        self.assertEqual(sector.get_whiteout_risk(20), "critical")


class TestSectorBaseParadox(TestCase):
    """Test calculate_base_paradox method."""

    def test_coincidental_magic_no_paradox(self):
        """Test coincidental magic generates no base paradox."""
        sector = Sector.objects.create(name="Test")
        paradox = sector.calculate_base_paradox(is_vulgar=False)
        self.assertEqual(paradox, 0)

    def test_vulgar_magic_in_free_sector(self):
        """Test vulgar magic in free sector without witnesses."""
        sector = Sector.objects.create(name="Test", access_level="free")
        paradox = sector.calculate_base_paradox(is_vulgar=True, has_witnesses=False)
        self.assertEqual(paradox, 0)

    def test_vulgar_magic_with_witnesses(self):
        """Test vulgar magic with witnesses."""
        sector = Sector.objects.create(name="Test")
        paradox = sector.calculate_base_paradox(is_vulgar=True, has_witnesses=True)
        self.assertEqual(paradox, 1)

    def test_vulgar_magic_in_restricted_sector(self):
        """Test vulgar magic in restricted sector."""
        sector = Sector.objects.create(name="Test", access_level="restricted")
        paradox = sector.calculate_base_paradox(is_vulgar=True)
        self.assertEqual(paradox, 1)

    def test_paradox_risk_modifier_applied(self):
        """Test paradox risk modifier is applied."""
        sector = Sector.objects.create(name="Test", paradox_risk_modifier=2)
        paradox = sector.calculate_base_paradox()
        self.assertEqual(paradox, 2)

    def test_corrupted_sector_adds_paradox(self):
        """Test corrupted sectors add to paradox."""
        sector = Sector.objects.create(name="Test", sector_class="corrupted")
        paradox = sector.calculate_base_paradox()
        self.assertEqual(paradox, 1)

    def test_corrupted_sector_with_vulgar_magic(self):
        """Test corrupted sector with vulgar magic stacks."""
        sector = Sector.objects.create(name="Test", sector_class="corrupted")
        paradox = sector.calculate_base_paradox(is_vulgar=True, has_witnesses=True)
        self.assertEqual(paradox, 2)


class TestSectorNavigationDifficulty(TestCase):
    """Test get_navigation_difficulty method."""

    def test_base_navigation(self):
        """Test base navigation difficulty is 6."""
        sector = Sector.objects.create(name="Test")
        self.assertEqual(sector.get_navigation_difficulty(), 6)

    def test_restricted_sector_harder(self):
        """Test restricted sectors are harder to navigate to."""
        sector = Sector.objects.create(name="Test", access_level="restricted")
        self.assertEqual(sector.get_navigation_difficulty(), 8)

    def test_security_adds_difficulty(self):
        """Test security level adds to difficulty."""
        sector = Sector.objects.create(name="Test", security_level=5)
        self.assertEqual(sector.get_navigation_difficulty(), 7)

    def test_corrupted_sector_harder(self):
        """Test corrupted sectors are harder to navigate."""
        sector = Sector.objects.create(name="Test", sector_class="corrupted")
        self.assertEqual(sector.get_navigation_difficulty(), 7)

    def test_junklands_harder(self):
        """Test junklands are harder to navigate."""
        sector = Sector.objects.create(name="Test", sector_class="junklands")
        self.assertEqual(sector.get_navigation_difficulty(), 7)

    def test_difficulty_capped_at_10(self):
        """Test navigation difficulty capped at 10."""
        sector = Sector.objects.create(
            name="Test",
            access_level="restricted",
            security_level=10,
            sector_class="corrupted",
        )
        self.assertEqual(sector.get_navigation_difficulty(), 10)


class TestSectorDeRezType(TestCase):
    """Test get_de_rez_type method."""

    def test_minor_violation_soft_de_rez(self):
        """Test minor violations cause soft de-rez."""
        sector = Sector.objects.create(name="Test")
        self.assertEqual(sector.get_de_rez_type("minor"), "soft")

    def test_major_violation_hard_de_rez(self):
        """Test major violations cause hard de-rez."""
        sector = Sector.objects.create(name="Test")
        self.assertEqual(sector.get_de_rez_type("major"), "hard")

    def test_critical_violation_hard_de_rez(self):
        """Test critical violations cause hard de-rez."""
        sector = Sector.objects.create(name="Test")
        self.assertEqual(sector.get_de_rez_type("critical"), "hard")

    def test_corrupted_always_hard_de_rez(self):
        """Test corrupted sectors always cause hard de-rez."""
        sector = Sector.objects.create(name="Test", sector_class="corrupted")
        self.assertEqual(sector.get_de_rez_type("minor"), "hard")

    def test_restricted_major_violation(self):
        """Test major violations in restricted sectors cause hard de-rez."""
        sector = Sector.objects.create(name="Test", access_level="restricted")
        self.assertEqual(sector.get_de_rez_type("major"), "hard")


class TestSectorTimeDilation(TestCase):
    """Test time_in_sector method."""

    def test_normal_time(self):
        """Test normal time flow (1.0 ratio)."""
        sector = Sector.objects.create(name="Test", time_dilation=1.0)
        self.assertEqual(sector.time_in_sector(60), 60.0)

    def test_faster_time(self):
        """Test faster time flow."""
        sector = Sector.objects.create(name="Test", time_dilation=2.0)
        self.assertEqual(sector.time_in_sector(60), 120.0)

    def test_slower_time(self):
        """Test slower time flow."""
        sector = Sector.objects.create(name="Test", time_dilation=0.5)
        self.assertEqual(sector.time_in_sector(60), 30.0)


class TestSectorDetailView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="password")
        self.sector = Sector.objects.create(
            name="Test Sector",
            owner=self.user,
            status="App",
        )
        self.url = self.sector.get_absolute_url()

    def test_sector_detail_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_sector_detail_view_templates(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sector/detail.html")


class TestSectorCreateView(TestCase):
    """Test Sector create view GET requests.

    Note: POST tests require complex form validation which is beyond the scope
    of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = Sector.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sector/form.html")


class TestSectorUpdateView(TestCase):
    """Test Sector update view GET requests.

    Note: POST tests require complex form validation which is beyond the scope
    of basic CRUD view tests. GET tests verify accessibility.
    """

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.sector = Sector.objects.create(
            name="Test Sector",
            description="Test description",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.sector.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/sector/form.html")
