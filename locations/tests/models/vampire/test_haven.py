"""Tests for Haven model."""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.vampire.haven import Haven, HavenSizeChoices


class TestHavenModel(TestCase):
    """Test Haven model methods and properties."""

    def setUp(self):
        self.haven = Haven.objects.create(name="Test Haven")

    def test_haven_type(self):
        """Test haven type is correctly set."""
        self.assertEqual(self.haven.type, "haven")

    def test_haven_gameline(self):
        """Test haven gameline is vtm."""
        self.assertEqual(self.haven.gameline, "vtm")

    def test_get_heading(self):
        """Test get_heading returns vtm_heading."""
        self.assertEqual(self.haven.get_heading(), "vtm_heading")

    def test_default_size(self):
        """Test default size is 1 (Cramped)."""
        self.assertEqual(self.haven.size, 1)

    def test_default_security(self):
        """Test default security is 0."""
        self.assertEqual(self.haven.security, 0)

    def test_default_location(self):
        """Test default location quality is 0."""
        self.assertEqual(self.haven.location, 0)


class TestHavenSizeChoices(TestCase):
    """Test HavenSizeChoices enum."""

    def test_cramped_value(self):
        """Test Cramped is 1."""
        self.assertEqual(HavenSizeChoices.CRAMPED, 1)

    def test_small_value(self):
        """Test Small is 2."""
        self.assertEqual(HavenSizeChoices.SMALL, 2)

    def test_average_value(self):
        """Test Average is 3."""
        self.assertEqual(HavenSizeChoices.AVERAGE, 3)

    def test_spacious_value(self):
        """Test Spacious is 4."""
        self.assertEqual(HavenSizeChoices.SPACIOUS, 4)

    def test_luxurious_value(self):
        """Test Luxurious is 5."""
        self.assertEqual(HavenSizeChoices.LUXURIOUS, 5)


class TestHavenTotalRating(TestCase):
    """Test calculate_total_rating method."""

    def test_basic_rating_calculation(self):
        """Test basic rating calculation."""
        haven = Haven.objects.create(name="Test", size=3, security=2, location=1)
        self.assertEqual(haven.total_rating, 6)

    def test_rating_with_guardian(self):
        """Test rating increases with guardian."""
        haven = Haven.objects.create(name="Test", size=3, security=2, location=1, has_guardian=True)
        self.assertEqual(haven.total_rating, 7)

    def test_rating_with_luxury(self):
        """Test rating increases with luxury."""
        haven = Haven.objects.create(name="Test", size=3, security=2, location=1, has_luxury=True)
        self.assertEqual(haven.total_rating, 7)

    def test_rating_with_hidden(self):
        """Test rating increases when hidden."""
        haven = Haven.objects.create(name="Test", size=3, security=2, location=1, is_hidden=True)
        self.assertEqual(haven.total_rating, 7)

    def test_rating_with_library(self):
        """Test rating increases with library."""
        haven = Haven.objects.create(name="Test", size=3, security=2, location=1, has_library=True)
        self.assertEqual(haven.total_rating, 7)

    def test_rating_with_workshop(self):
        """Test rating increases with workshop."""
        haven = Haven.objects.create(name="Test", size=3, security=2, location=1, has_workshop=True)
        self.assertEqual(haven.total_rating, 7)

    def test_rating_with_all_features(self):
        """Test rating with all special features."""
        haven = Haven.objects.create(
            name="Test",
            size=3,
            security=2,
            location=1,
            has_guardian=True,
            has_luxury=True,
            is_hidden=True,
            has_library=True,
            has_workshop=True,
        )
        self.assertEqual(haven.total_rating, 11)

    def test_save_recalculates_rating(self):
        """Test save method recalculates total rating."""
        haven = Haven.objects.create(name="Test", size=1, security=0, location=0)
        self.assertEqual(haven.total_rating, 1)
        haven.size = 3
        haven.security = 2
        haven.save()
        self.assertEqual(haven.total_rating, 5)


class TestHavenDetailView(TestCase):
    """Test Haven detail view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.haven = Haven.objects.create(
            name="Test Haven",
            owner=self.user,
            status="App",
        )
        self.url = self.haven.get_absolute_url()

    def test_haven_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_haven_detail_view_templates(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/vampire/haven/detail.html")


class TestHavenCreateView(TestCase):
    """Test Haven create view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = Haven.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/vampire/haven/form.html")


class TestHavenUpdateView(TestCase):
    """Test Haven update view."""

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.haven = Haven.objects.create(
            name="Test Haven",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.haven.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/vampire/haven/form.html")
