"""Tests for Bloodstone model."""
from django.test import TestCase
from items.models.vampire.bloodstone import Bloodstone


class TestBloodstone(TestCase):
    """Test Bloodstone model methods."""

    def setUp(self):
        self.bloodstone = Bloodstone.objects.create(
            name="Test Bloodstone",
            blood_stored=5,
            max_blood=10,
        )

    def test_add_blood_success(self):
        """Test adding blood within capacity."""
        result = self.bloodstone.add_blood(3)
        self.assertTrue(result)
        self.assertEqual(self.bloodstone.blood_stored, 8)

    def test_add_blood_to_max(self):
        """Test adding blood up to max capacity."""
        result = self.bloodstone.add_blood(5)
        self.assertTrue(result)
        self.assertEqual(self.bloodstone.blood_stored, 10)

    def test_add_blood_exceeds_max(self):
        """Test adding blood that exceeds max returns False."""
        result = self.bloodstone.add_blood(10)
        self.assertFalse(result)
        self.assertEqual(self.bloodstone.blood_stored, 5)  # Unchanged

    def test_add_blood_when_inactive(self):
        """Test adding blood when bloodstone is inactive returns False."""
        self.bloodstone.is_active = False
        self.bloodstone.save()
        result = self.bloodstone.add_blood(2)
        self.assertFalse(result)
        self.assertEqual(self.bloodstone.blood_stored, 5)

    def test_remove_blood_success(self):
        """Test removing blood successfully."""
        result = self.bloodstone.remove_blood(3)
        self.assertTrue(result)
        self.assertEqual(self.bloodstone.blood_stored, 2)

    def test_remove_blood_all(self):
        """Test removing all blood."""
        result = self.bloodstone.remove_blood(5)
        self.assertTrue(result)
        self.assertEqual(self.bloodstone.blood_stored, 0)

    def test_remove_blood_exceeds_stored(self):
        """Test removing more blood than stored returns False."""
        result = self.bloodstone.remove_blood(10)
        self.assertFalse(result)
        self.assertEqual(self.bloodstone.blood_stored, 5)  # Unchanged

    def test_remove_blood_when_inactive(self):
        """Test removing blood when bloodstone is inactive returns False."""
        self.bloodstone.is_active = False
        self.bloodstone.save()
        result = self.bloodstone.remove_blood(2)
        self.assertFalse(result)
        self.assertEqual(self.bloodstone.blood_stored, 5)


class TestBloodstoneDefaults(TestCase):
    """Test Bloodstone default values."""

    def test_blood_stored_default(self):
        """Test blood_stored defaults to 0."""
        bloodstone = Bloodstone.objects.create(name="Default Blood")
        self.assertEqual(bloodstone.blood_stored, 0)

    def test_max_blood_default(self):
        """Test max_blood defaults to 10."""
        bloodstone = Bloodstone.objects.create(name="Default Max")
        self.assertEqual(bloodstone.max_blood, 10)

    def test_is_active_default(self):
        """Test is_active defaults to True."""
        bloodstone = Bloodstone.objects.create(name="Default Active")
        self.assertTrue(bloodstone.is_active)

    def test_created_by_generation_default(self):
        """Test created_by_generation defaults to 13."""
        bloodstone = Bloodstone.objects.create(name="Default Gen")
        self.assertEqual(bloodstone.created_by_generation, 13)


class TestBloodstoneUrls(TestCase):
    """Test URL methods for Bloodstone."""

    def setUp(self):
        self.bloodstone = Bloodstone.objects.create(name="URL Test Bloodstone")

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.bloodstone.get_update_url()
        self.assertIn(str(self.bloodstone.id), url)
        self.assertIn("bloodstone", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = Bloodstone.get_creation_url()
        self.assertIn("bloodstone", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.bloodstone.get_heading(), "vtm_heading")


class TestBloodstoneDetailView(TestCase):
    """Test Bloodstone detail view."""

    def setUp(self):
        self.bloodstone = Bloodstone.objects.create(name="Test Bloodstone")
        self.url = self.bloodstone.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/vampire/bloodstone/detail.html")


class TestBloodstoneCreateView(TestCase):
    """Test Bloodstone create view."""

    def setUp(self):
        self.url = Bloodstone.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/vampire/bloodstone/form.html")


class TestBloodstoneUpdateView(TestCase):
    """Test Bloodstone update view."""

    def setUp(self):
        self.bloodstone = Bloodstone.objects.create(name="Test Bloodstone", description="Test")
        self.url = self.bloodstone.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/vampire/bloodstone/form.html")


class TestBloodstoneEdgeCases(TestCase):
    """Test edge cases for Bloodstone."""

    def test_add_blood_zero(self):
        """Test adding zero blood."""
        bloodstone = Bloodstone.objects.create(name="Zero Add", blood_stored=5)
        result = bloodstone.add_blood(0)
        self.assertTrue(result)
        self.assertEqual(bloodstone.blood_stored, 5)

    def test_remove_blood_zero(self):
        """Test removing zero blood."""
        bloodstone = Bloodstone.objects.create(name="Zero Remove", blood_stored=5)
        result = bloodstone.remove_blood(0)
        self.assertTrue(result)
        self.assertEqual(bloodstone.blood_stored, 5)

    def test_add_blood_exactly_to_max(self):
        """Test adding blood to exactly reach max."""
        bloodstone = Bloodstone.objects.create(name="Exact Max", blood_stored=8, max_blood=10)
        result = bloodstone.add_blood(2)
        self.assertTrue(result)
        self.assertEqual(bloodstone.blood_stored, 10)

    def test_remove_all_blood(self):
        """Test removing exactly all stored blood."""
        bloodstone = Bloodstone.objects.create(name="Remove All", blood_stored=5)
        result = bloodstone.remove_blood(5)
        self.assertTrue(result)
        self.assertEqual(bloodstone.blood_stored, 0)
