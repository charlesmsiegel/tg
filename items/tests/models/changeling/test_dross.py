"""Tests for Dross model."""
from django.test import TestCase
from items.models.changeling.dross import Dross


class TestDross(TestCase):
    """Test Dross model methods."""

    def setUp(self):
        self.dross = Dross.objects.create(
            name="Test Dross",
            quality="fine",
            glamour_value=5,
            physical_form="crystal",
        )

    def test_str_with_name(self):
        """Test __str__ returns name with glamour value."""
        expected = f"{self.dross.name} ({self.dross.glamour_value} Glamour)"
        self.assertEqual(str(self.dross), expected)

    def test_str_without_name(self):
        """Test __str__ without name shows quality."""
        dross = Dross.objects.create(name="Temp Dross", quality="common", glamour_value=3)
        # Need to clear the name to test fallback
        Dross.objects.filter(pk=dross.pk).update(name="")
        dross.refresh_from_db()
        self.assertIn("Glamour", str(dross))

    def test_get_quality_multiplier(self):
        """Test get_quality_multiplier returns correct values."""
        quality_multipliers = {
            "ephemeral": 0.5,
            "common": 1.0,
            "fine": 2.0,
            "exquisite": 4.0,
            "legendary": 10.0,
        }
        for quality, expected in quality_multipliers.items():
            dross = Dross.objects.create(name=f"{quality} dross", quality=quality)
            self.assertEqual(dross.get_quality_multiplier(), expected)


class TestDrossDefaults(TestCase):
    """Test Dross default values."""

    def test_quality_default(self):
        """Test quality defaults to common."""
        dross = Dross.objects.create(name="Default Quality")
        self.assertEqual(dross.quality, "common")

    def test_glamour_value_default(self):
        """Test glamour_value defaults to 2."""
        dross = Dross.objects.create(name="Default Glamour")
        self.assertEqual(dross.glamour_value, 2)

    def test_physical_form_default(self):
        """Test physical_form defaults to crystal."""
        dross = Dross.objects.create(name="Default Form")
        self.assertEqual(dross.physical_form, "crystal")

    def test_source_default(self):
        """Test source defaults to natural."""
        dross = Dross.objects.create(name="Default Source")
        self.assertEqual(dross.source, "natural")

    def test_is_stable_default(self):
        """Test is_stable defaults to True."""
        dross = Dross.objects.create(name="Default Stable")
        self.assertTrue(dross.is_stable)

    def test_is_consumable_default(self):
        """Test is_consumable defaults to True."""
        dross = Dross.objects.create(name="Default Consumable")
        self.assertTrue(dross.is_consumable)


class TestDrossQuality(TestCase):
    """Test quality choices."""

    def test_quality_choices(self):
        """Test quality can be set to valid choices."""
        valid_qualities = ["ephemeral", "common", "fine", "exquisite", "legendary"]
        for quality in valid_qualities:
            dross = Dross.objects.create(name=f"{quality} dross", quality=quality)
            self.assertEqual(dross.quality, quality)


class TestDrossPhysicalForm(TestCase):
    """Test physical form choices."""

    def test_physical_form_choices(self):
        """Test physical_form can be set to valid choices."""
        valid_forms = ["crystal", "liquid", "vapor", "object", "other"]
        for form in valid_forms:
            dross = Dross.objects.create(name=f"{form} dross", physical_form=form)
            self.assertEqual(dross.physical_form, form)


class TestDrossSource(TestCase):
    """Test source choices."""

    def test_source_choices(self):
        """Test source can be set to valid choices."""
        valid_sources = ["balefire", "dream", "art", "natural", "refined", "unknown"]
        for source in valid_sources:
            dross = Dross.objects.create(name=f"{source} dross", source=source)
            self.assertEqual(dross.source, source)


class TestDrossUrls(TestCase):
    """Test URL methods for Dross."""

    def setUp(self):
        self.dross = Dross.objects.create(name="URL Test Dross")

    def test_get_absolute_url(self):
        """Test get_absolute_url generates correct URL."""
        url = self.dross.get_absolute_url()
        self.assertIn(str(self.dross.id), url)

    def test_get_update_url(self):
        """Test get_update_url generates correct URL."""
        url = self.dross.get_update_url()
        self.assertIn(str(self.dross.id), url)
        self.assertIn("dross", url)

    def test_get_creation_url(self):
        """Test get_creation_url generates correct URL."""
        url = Dross.get_creation_url()
        self.assertIn("dross", url)
        self.assertIn("create", url)

    def test_get_heading(self):
        """Test get_heading returns correct heading class."""
        self.assertEqual(self.dross.get_heading(), "ctd_heading")


class TestDrossDetailView(TestCase):
    """Test Dross detail view."""

    def setUp(self):
        self.dross = Dross.objects.create(name="Test Dross")
        self.url = self.dross.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/changeling/dross/detail.html")


class TestDrossCreateView(TestCase):
    """Test Dross create view."""

    def setUp(self):
        self.url = Dross.get_creation_url()

    def test_create_view_status_code(self):
        """Test create view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/changeling/dross/form.html")


class TestDrossUpdateView(TestCase):
    """Test Dross update view."""

    def setUp(self):
        self.dross = Dross.objects.create(name="Test Dross", description="Test")
        self.url = self.dross.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/changeling/dross/form.html")


class TestDrossOptionalFields(TestCase):
    """Test optional text fields."""

    def test_color_can_be_set(self):
        """Test color can be set."""
        dross = Dross.objects.create(name="Colored Dross", color="Iridescent blue")
        self.assertEqual(dross.color, "Iridescent blue")

    def test_resonance_can_be_set(self):
        """Test resonance can be set."""
        dross = Dross.objects.create(name="Resonant Dross", resonance="Joy")
        self.assertEqual(dross.resonance, "Joy")

    def test_restricted_to_can_be_set(self):
        """Test restricted_to can be set."""
        dross = Dross.objects.create(name="Restricted Dross", restricted_to="Sluagh only")
        self.assertEqual(dross.restricted_to, "Sluagh only")
