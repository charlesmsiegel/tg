"""Tests for Domain model."""

from django.contrib.auth.models import User
from django.test import TestCase

from game.models import Chronicle
from locations.models.vampire.domain import Domain


class TestDomainBasics(TestCase):
    """Test basic Domain model functionality."""

    def test_domain_creation(self):
        """Test creating a domain."""
        domain = Domain.objects.create(
            name="Downtown District",
            size=3,
            population=2,
            control=2,
        )
        self.assertEqual(domain.name, "Downtown District")
        self.assertEqual(domain.size, 3)
        self.assertEqual(domain.population, 2)
        self.assertEqual(domain.control, 2)
        self.assertEqual(domain.type, "domain")
        self.assertEqual(domain.gameline, "vtm")

    def test_domain_defaults(self):
        """Test domain default values."""
        domain = Domain.objects.create(name="Test Domain")
        self.assertEqual(domain.size, 0)
        self.assertEqual(domain.population, 0)
        self.assertEqual(domain.control, 0)
        self.assertFalse(domain.is_elysium)
        self.assertFalse(domain.has_rack)
        self.assertFalse(domain.is_disputed)
        self.assertEqual(domain.domain_type, "")

    def test_domain_get_heading(self):
        """Test get_heading returns vtm_heading."""
        domain = Domain.objects.create(name="Test")
        self.assertEqual(domain.get_heading(), "vtm_heading")

    def test_domain_get_update_url(self):
        """Test get_update_url returns valid URL."""
        domain = Domain.objects.create(name="Test")
        url = domain.get_update_url()
        self.assertIn(str(domain.id), url)
        self.assertIn("domain", url)

    def test_domain_get_creation_url(self):
        """Test get_creation_url returns valid URL."""
        url = Domain.get_creation_url()
        self.assertIn("domain", url)


class TestDomainTotalRating(TestCase):
    """Test Domain total rating calculation."""

    def test_calculate_total_rating_basic(self):
        """Test basic total rating calculation."""
        domain = Domain.objects.create(
            name="Test",
            size=2,
            population=3,
            control=1,
        )
        # Total = size + population + control = 2 + 3 + 1 = 6
        self.assertEqual(domain.total_rating, 6)

    def test_calculate_total_rating_with_rack(self):
        """Test total rating with rack bonus."""
        domain = Domain.objects.create(
            name="Test",
            size=2,
            population=2,
            control=2,
            has_rack=True,
        )
        # Total = 2 + 2 + 2 + 1 (rack) = 7
        self.assertEqual(domain.total_rating, 7)

    def test_calculate_total_rating_disputed(self):
        """Test total rating with disputed penalty."""
        domain = Domain.objects.create(
            name="Test",
            size=2,
            population=2,
            control=2,
            is_disputed=True,
        )
        # Total = 2 + 2 + 2 - 1 (disputed) = 5
        self.assertEqual(domain.total_rating, 5)

    def test_calculate_total_rating_rack_and_disputed(self):
        """Test total rating with rack and disputed."""
        domain = Domain.objects.create(
            name="Test",
            size=2,
            population=2,
            control=2,
            has_rack=True,
            is_disputed=True,
        )
        # Total = 2 + 2 + 2 + 1 (rack) - 1 (disputed) = 6
        self.assertEqual(domain.total_rating, 6)

    def test_calculate_total_rating_no_negative(self):
        """Test total rating cannot go negative."""
        domain = Domain.objects.create(
            name="Test",
            size=0,
            population=0,
            control=0,
            is_disputed=True,
        )
        # Total = 0 + 0 + 0 - 1 (disputed) = -1, but should be clamped to 0
        self.assertEqual(domain.total_rating, 0)

    def test_save_recalculates_total_rating(self):
        """Test save() recalculates total rating."""
        domain = Domain.objects.create(
            name="Test",
            size=1,
            population=1,
            control=1,
        )
        self.assertEqual(domain.total_rating, 3)

        domain.size = 3
        domain.population = 3
        domain.control = 3
        domain.save()
        domain.refresh_from_db()
        self.assertEqual(domain.total_rating, 9)


class TestDomainFeatures(TestCase):
    """Test Domain special features."""

    def test_is_elysium(self):
        """Test is_elysium feature."""
        domain = Domain.objects.create(name="Test", is_elysium=True)
        self.assertTrue(domain.is_elysium)

    def test_has_rack(self):
        """Test has_rack feature."""
        domain = Domain.objects.create(name="Test", has_rack=True)
        self.assertTrue(domain.has_rack)

    def test_is_disputed(self):
        """Test is_disputed feature."""
        domain = Domain.objects.create(name="Test", is_disputed=True)
        self.assertTrue(domain.is_disputed)

    def test_domain_type(self):
        """Test domain_type field."""
        domain = Domain.objects.create(
            name="Test",
            domain_type="Nightclub district",
        )
        self.assertEqual(domain.domain_type, "Nightclub district")


class TestDomainViews(TestCase):
    """Test Domain views integration."""

    def test_domain_list_view(self):
        """Test domain list view."""
        Domain.objects.create(name="Domain 1")
        Domain.objects.create(name="Domain 2")
        response = self.client.get("/locations/vampire/list/domains/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Domain 1")
        self.assertContains(response, "Domain 2")

    def test_domain_detail_view(self):
        """Test domain detail view."""
        user = User.objects.create_user(username="testuser", password="password")
        domain = Domain.objects.create(
            name="Test Domain",
            size=3,
            population=2,
            control=2,
            owner=user,
            status="App",
        )
        self.client.login(username="testuser", password="password")
        response = self.client.get(domain.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Domain")

    def test_domain_create_view(self):
        """Test domain create view."""
        user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        response = self.client.get(Domain.get_creation_url())
        self.assertEqual(response.status_code, 200)

    def test_domain_create_post(self):
        """Test creating domain via POST."""
        user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Domain",
            "description": "A new domain",
            "size": 2,
            "population": 3,
            "control": 2,
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        response = self.client.post(Domain.get_creation_url(), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Domain.objects.filter(name="New Domain").exists())
        domain = Domain.objects.get(name="New Domain")
        self.assertEqual(domain.total_rating, 7)  # 2 + 3 + 2

    def test_domain_update_view(self):
        """Test domain update view."""
        st = User.objects.create_user(username="st_user", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        chronicle.storytellers.add(st)
        domain = Domain.objects.create(
            name="Existing Domain",
            size=1,
            population=1,
            control=1,
            owner=st,
            chronicle=chronicle,
            status="App",
        )
        self.client.login(username="st_user", password="password")
        response = self.client.get(domain.get_update_url())
        self.assertEqual(response.status_code, 200)

    def test_domain_update_post(self):
        """Test updating domain via POST."""
        st = User.objects.create_user(username="st_user", password="password")
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        chronicle.storytellers.add(st)
        domain = Domain.objects.create(
            name="Existing Domain",
            size=1,
            population=1,
            control=1,
            owner=st,
            chronicle=chronicle,
            status="App",
        )
        self.client.login(username="st_user", password="password")
        data = {
            "name": "Updated Domain",
            "description": "Updated description",
            "size": 4,
            "population": 4,
            "control": 4,
            "has_rack": True,
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        response = self.client.post(domain.get_update_url(), data=data)
        self.assertEqual(response.status_code, 302)
        domain.refresh_from_db()
        self.assertEqual(domain.name, "Updated Domain")
        self.assertEqual(domain.total_rating, 13)  # 4 + 4 + 4 + 1 (rack)


class TestDomainMeta(TestCase):
    """Test Domain Meta class."""

    def test_verbose_name(self):
        """Test verbose name."""
        self.assertEqual(Domain._meta.verbose_name, "Domain")

    def test_verbose_name_plural(self):
        """Test verbose name plural."""
        self.assertEqual(Domain._meta.verbose_name_plural, "Domains")
