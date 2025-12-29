"""Tests for Demon Relic model."""
from django.test import TestCase
from items.models.demon.relic import Relic


class TestRelic(TestCase):
    """Test Relic model methods."""

    def setUp(self):
        self.relic = Relic.objects.create(
            name="Test Relic",
            relic_type="enhanced",
            complexity=3,
        )

    def test_str(self):
        """Test __str__ returns name with type display."""
        expected = f"{self.relic.name} ({self.relic.get_relic_type_display()})"
        self.assertEqual(str(self.relic), expected)

    def test_set_complexity_valid(self):
        """Test set_complexity with valid values."""
        for complexity in range(1, 11):
            result = self.relic.set_complexity(complexity)
            self.assertTrue(result)
            self.relic.refresh_from_db()
            self.assertEqual(self.relic.complexity, complexity)

    def test_set_complexity_invalid_low(self):
        """Test set_complexity rejects values below 1."""
        original = self.relic.complexity
        result = self.relic.set_complexity(0)
        self.assertFalse(result)
        self.relic.refresh_from_db()
        self.assertEqual(self.relic.complexity, original)

    def test_set_complexity_invalid_high(self):
        """Test set_complexity rejects values above 10."""
        original = self.relic.complexity
        result = self.relic.set_complexity(11)
        self.assertFalse(result)
        self.relic.refresh_from_db()
        self.assertEqual(self.relic.complexity, original)

    def test_has_complexity_true(self):
        """Test has_complexity returns True when complexity > 0."""
        self.assertTrue(self.relic.has_complexity())

    def test_has_complexity_false(self):
        """Test has_complexity returns False when complexity is 0."""
        relic = Relic.objects.create(name="No Complexity", complexity=0)
        self.assertFalse(relic.has_complexity())

    def test_set_difficulty_valid(self):
        """Test set_difficulty with valid values."""
        result = self.relic.set_difficulty(8)
        self.assertTrue(result)
        self.relic.refresh_from_db()
        self.assertEqual(self.relic.difficulty, 8)

    def test_set_difficulty_invalid(self):
        """Test set_difficulty rejects values below 2."""
        original = self.relic.difficulty
        result = self.relic.set_difficulty(1)
        self.assertFalse(result)
        self.relic.refresh_from_db()
        self.assertEqual(self.relic.difficulty, original)


class TestRelicDefaults(TestCase):
    """Test Relic default values."""

    def test_relic_type_default(self):
        """Test relic_type defaults to enhanced."""
        relic = Relic.objects.create(name="Default Type")
        self.assertEqual(relic.relic_type, "enhanced")

    def test_complexity_default(self):
        """Test complexity defaults to 1."""
        relic = Relic.objects.create(name="Default Complexity")
        self.assertEqual(relic.complexity, 1)

    def test_difficulty_default(self):
        """Test difficulty defaults to 6."""
        relic = Relic.objects.create(name="Default Difficulty")
        self.assertEqual(relic.difficulty, 6)

    def test_is_permanent_default(self):
        """Test is_permanent defaults to False."""
        relic = Relic.objects.create(name="Default Permanent")
        self.assertFalse(relic.is_permanent)

    def test_dice_pool_default(self):
        """Test dice_pool defaults to 0."""
        relic = Relic.objects.create(name="Default Dice Pool")
        self.assertEqual(relic.dice_pool, 0)


class TestRelicType(TestCase):
    """Test relic type choices."""

    def test_relic_type_choices(self):
        """Test relic_type can be set to valid choices."""
        valid_types = ["enhanced", "enchanted", "house_specific", "demonic", "ancient"]
        for rtype in valid_types:
            relic = Relic.objects.create(name=f"{rtype} relic", relic_type=rtype)
            self.assertEqual(relic.relic_type, rtype)


class TestRelicUrls(TestCase):
    """Test URL methods for Relic."""

    def setUp(self):
        self.relic = Relic.objects.create(name="URL Test Relic")

    def test_get_absolute_url(self):
        """Test get_absolute_url generates correct URL."""
        url = self.relic.get_absolute_url()
        self.assertIn(str(self.relic.pk), url)

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.relic.get_update_url()
        self.assertIn(str(self.relic.id), url)
        self.assertIn("relic", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = Relic.get_creation_url()
        self.assertIn("relic", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.relic.get_heading(), "dtf_heading")


class TestRelicDetailView(TestCase):
    """Test Relic detail view."""

    def setUp(self):
        self.relic = Relic.objects.create(name="Test Relic")
        self.url = self.relic.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/demon/relic/detail.html")


class TestRelicCreateView(TestCase):
    """Test Relic create view."""

    def setUp(self):
        self.url = Relic.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/demon/relic/form.html")


class TestRelicUpdateView(TestCase):
    """Test Relic update view."""

    def setUp(self):
        self.relic = Relic.objects.create(name="Test Relic", description="Test")
        self.url = self.relic.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/demon/relic/form.html")
