"""Tests for MummyRelic model."""

from django.contrib.auth.models import User
from django.test import TestCase

from items.models.mummy.relic import MummyRelic, RelicResonanceRating


class TestMummyRelic(TestCase):
    """Test MummyRelic model methods."""

    def setUp(self):
        self.relic = MummyRelic.objects.create(
            name="Test Relic",
            rank=3,
            relic_type="jewelry",
            ba_cost=2,
        )

    def test_save_auto_sets_background_cost(self):
        """Test save() auto-sets background_cost to rank if not set."""
        relic = MummyRelic.objects.create(name="Background Test", rank=4)
        self.assertEqual(relic.background_cost, 4)


class TestMummyRelicType(TestCase):
    """Test relic type choices."""

    def test_relic_type_default(self):
        """Test default relic_type is jewelry."""
        relic = MummyRelic.objects.create(name="Default Type")
        self.assertEqual(relic.relic_type, "jewelry")

    def test_relic_type_choices(self):
        """Test relic_type can be set to valid choices."""
        valid_types = [
            "weapon",
            "jewelry",
            "scroll",
            "canopic",
            "statue",
            "crown",
            "tool",
            "clothing",
            "other",
        ]
        for rtype in valid_types:
            relic = MummyRelic.objects.create(name=f"{rtype} relic", relic_type=rtype)
            self.assertEqual(relic.relic_type, rtype)


class TestMummyRelicEra(TestCase):
    """Test era choices."""

    def test_era_default(self):
        """Test default era is old_kingdom."""
        relic = MummyRelic.objects.create(name="Default Era")
        self.assertEqual(relic.era, "old_kingdom")

    def test_era_choices(self):
        """Test era can be set to valid choices."""
        valid_eras = [
            "predynastic",
            "old_kingdom",
            "middle_kingdom",
            "new_kingdom",
            "late_period",
            "ptolemaic",
            "unknown",
        ]
        for era in valid_eras:
            relic = MummyRelic.objects.create(name=f"{era} relic", era=era)
            self.assertEqual(relic.era, era)


class TestMummyRelicProperties(TestCase):
    """Test relic boolean properties."""

    def test_is_cursed_default(self):
        """Test is_cursed defaults to False."""
        relic = MummyRelic.objects.create(name="Not Cursed")
        self.assertFalse(relic.is_cursed)

    def test_is_unique_default(self):
        """Test is_unique defaults to False."""
        relic = MummyRelic.objects.create(name="Not Unique")
        self.assertFalse(relic.is_unique)

    def test_is_sentient_default(self):
        """Test is_sentient defaults to False."""
        relic = MummyRelic.objects.create(name="Not Sentient")
        self.assertFalse(relic.is_sentient)

    def test_requires_ritual_default(self):
        """Test requires_ritual defaults to False."""
        relic = MummyRelic.objects.create(name="No Ritual")
        self.assertFalse(relic.requires_ritual)


class TestMummyRelicUrls(TestCase):
    """Test URL methods for MummyRelic."""

    def setUp(self):
        self.relic = MummyRelic.objects.create(name="URL Test Relic")

    def test_get_absolute_url(self):
        """Test get_absolute_url generates correct URL."""
        url = self.relic.get_absolute_url()
        self.assertIn(str(self.relic.id), url)

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.relic.get_update_url()
        self.assertIn(str(self.relic.pk), url)
        self.assertIn("relic", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = MummyRelic.get_creation_url()
        self.assertIn("relic", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.relic.get_heading(), "mtr_heading")


class TestMummyRelicDetailView(TestCase):
    """Test MummyRelic detail view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.relic = MummyRelic.objects.create(name="Test Relic", owner=self.user)
        self.url = self.relic.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/relic/detail.html")


class TestMummyRelicCreateView(TestCase):
    """Test MummyRelic create view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = MummyRelic.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/relic/form.html")


class TestMummyRelicUpdateView(TestCase):
    """Test MummyRelic update view."""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@test.com"
        )
        self.relic = MummyRelic.objects.create(name="Test Relic", description="Test")
        self.url = self.relic.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/relic/form.html")


class TestMummyRelicCosts(TestCase):
    """Test Ba and Sekhem cost properties."""

    def test_ba_cost_default(self):
        """Test ba_cost defaults to 0."""
        relic = MummyRelic.objects.create(name="No BA Cost")
        self.assertEqual(relic.ba_cost, 0)

    def test_requires_sekhem_default(self):
        """Test requires_sekhem defaults to 0."""
        relic = MummyRelic.objects.create(name="No Sekhem Requirement")
        self.assertEqual(relic.requires_sekhem, 0)


class TestRelicResonanceRating(TestCase):
    """Test RelicResonanceRating through model."""

    def test_relic_resonance_rating_creation(self):
        """Test creating a RelicResonanceRating."""
        from characters.models.mage.resonance import Resonance

        relic = MummyRelic.objects.create(name="Resonance Test Relic")
        resonance = Resonance.objects.create(name="Test Resonance")
        rating = RelicResonanceRating.objects.create(
            relic=relic,
            resonance=resonance,
            rating=3,
        )
        self.assertEqual(rating.relic, relic)
        self.assertEqual(rating.resonance, resonance)
        self.assertEqual(rating.rating, 3)

    def test_relic_resonance_unique_together(self):
        """Test unique_together constraint on relic+resonance."""
        from django.db import IntegrityError

        from characters.models.mage.resonance import Resonance

        relic = MummyRelic.objects.create(name="Unique Test Relic")
        resonance = Resonance.objects.create(name="Unique Resonance")
        RelicResonanceRating.objects.create(relic=relic, resonance=resonance, rating=2)

        with self.assertRaises(IntegrityError):
            RelicResonanceRating.objects.create(relic=relic, resonance=resonance, rating=3)
