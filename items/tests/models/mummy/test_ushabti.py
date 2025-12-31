"""Tests for Ushabti model."""
from django.contrib.auth.models import User
from django.test import TestCase
from items.models.mummy.ushabti import Ushabti


class TestUshabti(TestCase):
    """Test Ushabti model methods."""

    def setUp(self):
        self.ushabti = Ushabti.objects.create(
            name="Test Ushabti",
            rank=3,
            purpose="guardian",
            physical_rating=3,
            mental_rating=2,
        )

    def test_save_auto_sets_ba_to_animate(self):
        """Test save() auto-sets ba_to_animate to rank."""
        ushabti = Ushabti.objects.create(name="Auto BA Test", rank=4)
        self.assertEqual(ushabti.ba_to_animate, 4)

    def test_save_auto_sets_ba_per_day(self):
        """Test save() auto-sets ba_per_day to rank."""
        ushabti = Ushabti.objects.create(name="Auto BA Per Day Test", rank=5)
        self.assertEqual(ushabti.ba_per_day, 5)


class TestUshabtiDeactivate(TestCase):
    """Test deactivate method."""

    def test_deactivate(self):
        """Test deactivate sets is_currently_animated to False."""
        ushabti = Ushabti.objects.create(name="Deactivate Test", is_currently_animated=True)
        ushabti.deactivate()
        ushabti.refresh_from_db()
        self.assertFalse(ushabti.is_currently_animated)

    def test_deactivate_when_already_inactive(self):
        """Test deactivate when already inactive."""
        ushabti = Ushabti.objects.create(name="Already Inactive", is_currently_animated=False)
        ushabti.deactivate()
        ushabti.refresh_from_db()
        self.assertFalse(ushabti.is_currently_animated)


class TestUshabtiPurpose(TestCase):
    """Test purpose choices."""

    def test_purpose_default(self):
        """Test default purpose is servant."""
        ushabti = Ushabti.objects.create(name="Default Purpose")
        self.assertEqual(ushabti.purpose, "servant")

    def test_purpose_choices(self):
        """Test purpose can be set to valid choices."""
        valid_purposes = ["guardian", "servant", "laborer", "spy", "messenger", "craftsman", "scribe"]
        for purpose in valid_purposes:
            ushabti = Ushabti.objects.create(name=f"{purpose} ushabti", purpose=purpose)
            self.assertEqual(ushabti.purpose, purpose)


class TestUshabtiMaterial(TestCase):
    """Test material choices."""

    def test_material_default(self):
        """Test default material is clay."""
        ushabti = Ushabti.objects.create(name="Default Material")
        self.assertEqual(ushabti.material, "clay")

    def test_material_choices(self):
        """Test material can be set to valid choices."""
        valid_materials = ["clay", "wood", "stone", "gold", "bone", "wax"]
        for material in valid_materials:
            ushabti = Ushabti.objects.create(name=f"{material} ushabti", material=material)
            self.assertEqual(ushabti.material, material)


class TestUshabtiProperties(TestCase):
    """Test Ushabti boolean properties."""

    def test_is_currently_animated_default(self):
        """Test is_currently_animated defaults to False."""
        ushabti = Ushabti.objects.create(name="Not Animated")
        self.assertFalse(ushabti.is_currently_animated)

    def test_obeys_only_creator_default(self):
        """Test obeys_only_creator defaults to True."""
        ushabti = Ushabti.objects.create(name="Obeys Creator")
        self.assertTrue(ushabti.obeys_only_creator)


class TestUshabtiUrls(TestCase):
    """Test URL methods for Ushabti."""

    def setUp(self):
        self.ushabti = Ushabti.objects.create(name="URL Test Ushabti")

    def test_get_absolute_url(self):
        """Test get_absolute_url generates correct URL."""
        url = self.ushabti.get_absolute_url()
        self.assertIn(str(self.ushabti.id), url)

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.ushabti.get_update_url()
        self.assertIn(str(self.ushabti.pk), url)
        self.assertIn("ushabti", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = Ushabti.get_creation_url()
        self.assertIn("ushabti", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.ushabti.get_heading(), "mtr_heading")


class TestUshabtiDetailView(TestCase):
    """Test Ushabti detail view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.ushabti = Ushabti.objects.create(name="Test Ushabti", owner=self.user)
        self.url = self.ushabti.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/ushabti/detail.html")


class TestUshabtiCreateView(TestCase):
    """Test Ushabti create view."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = Ushabti.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/ushabti/form.html")


class TestUshabtiUpdateView(TestCase):
    """Test Ushabti update view."""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@test.com"
        )
        self.ushabti = Ushabti.objects.create(name="Test Ushabti", description="Test")
        self.url = self.ushabti.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mummy/ushabti/form.html")


class TestUshabtiRatings(TestCase):
    """Test physical and mental ratings."""

    def test_physical_rating_default(self):
        """Test physical_rating defaults to 1."""
        ushabti = Ushabti.objects.create(name="Physical Default")
        self.assertEqual(ushabti.physical_rating, 1)

    def test_mental_rating_default(self):
        """Test mental_rating defaults to 1."""
        ushabti = Ushabti.objects.create(name="Mental Default")
        self.assertEqual(ushabti.mental_rating, 1)

    def test_ratings_can_be_set(self):
        """Test ratings can be set to valid values."""
        ushabti = Ushabti.objects.create(
            name="Custom Ratings",
            physical_rating=4,
            mental_rating=3,
        )
        self.assertEqual(ushabti.physical_rating, 4)
        self.assertEqual(ushabti.mental_rating, 3)


class TestUshabtiAnimationProperties(TestCase):
    """Test animation-related properties."""

    def test_animation_duration_default(self):
        """Test animation_duration_hours defaults to 24."""
        ushabti = Ushabti.objects.create(name="Duration Default")
        self.assertEqual(ushabti.animation_duration_hours, 24)

    def test_size_description_default(self):
        """Test size_description has default value."""
        ushabti = Ushabti.objects.create(name="Size Default")
        self.assertEqual(ushabti.size_description, "Small statuette")
