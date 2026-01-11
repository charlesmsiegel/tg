"""Tests for Arcanos model."""

from django.test import TestCase

from characters.models.wraith.arcanos import Arcanos


class TestArcanosModel(TestCase):
    """Tests for Arcanos model creation and attributes."""

    def test_arcanos_creation(self):
        """Arcanos can be created with basic attributes."""
        arcanos = Arcanos.objects.create(
            name="Argos",
            level=1,
            description="The art of navigation in the Underworld.",
        )
        self.assertEqual(arcanos.name, "Argos")
        self.assertEqual(arcanos.level, 1)

    def test_arcanos_default_values(self):
        """Arcanos has correct default values."""
        arcanos = Arcanos.objects.create(
            name="Test Arcanos",
            description="Test description",
        )
        self.assertEqual(arcanos.arcanos_type, "standard")
        self.assertEqual(arcanos.level, 1)
        self.assertEqual(arcanos.pathos_cost, 0)
        self.assertEqual(arcanos.angst_cost, 0)
        self.assertEqual(arcanos.difficulty, 6)

    def test_arcanos_type_choices(self):
        """Arcanos can have standard or dark type."""
        standard = Arcanos.objects.create(
            name="Standard",
            arcanos_type="standard",
            description="Standard arcanos",
        )
        dark = Arcanos.objects.create(
            name="Dark",
            arcanos_type="dark",
            description="Dark arcanos",
        )
        self.assertEqual(standard.arcanos_type, "standard")
        self.assertEqual(dark.arcanos_type, "dark")

    def test_arcanos_gameline(self):
        """Arcanos has correct gameline."""
        arcanos = Arcanos.objects.create(name="Test", description="Test description")
        self.assertEqual(arcanos.gameline, "wto")

    def test_arcanos_type_attribute(self):
        """Arcanos has correct type attribute."""
        arcanos = Arcanos.objects.create(name="Test", description="Test description")
        self.assertEqual(arcanos.type, "arcanos")

    def test_arcanos_parent_relationship(self):
        """Arcanos can have a parent arcanos for leveled abilities."""
        parent = Arcanos.objects.create(
            name="Argos",
            level=0,
            description="Parent arcanos",
        )
        child = Arcanos.objects.create(
            name="Enshroud",
            level=1,
            parent_arcanos=parent,
            description="Child arcanos",
        )
        self.assertEqual(child.parent_arcanos, parent)
        self.assertIn(child, parent.levels.all())

    def test_arcanos_pathos_and_angst_costs(self):
        """Arcanos can have pathos and angst costs."""
        arcanos = Arcanos.objects.create(
            name="Blighted Insight",
            arcanos_type="dark",
            pathos_cost=2,
            angst_cost=1,
            description="Dark arcanos ability",
        )
        self.assertEqual(arcanos.pathos_cost, 2)
        self.assertEqual(arcanos.angst_cost, 1)


class TestArcanosUrls(TestCase):
    """Tests for Arcanos URL methods."""

    def setUp(self):
        self.arcanos = Arcanos.objects.create(
            name="Test Arcanos",
            description="Test description",
        )

    def test_get_absolute_url_method_exists(self):
        """Arcanos has get_absolute_url method."""
        self.assertTrue(hasattr(self.arcanos, "get_absolute_url"))
        self.assertTrue(callable(self.arcanos.get_absolute_url))

    def test_get_heading(self):
        """Arcanos returns correct heading class."""
        self.assertEqual(self.arcanos.get_heading(), "wto_heading")


class TestArcanosHierarchy(TestCase):
    """Tests for Arcanos hierarchy with parent relationships."""

    def test_multiple_levels_under_parent(self):
        """Parent arcanos can have multiple levels."""
        parent = Arcanos.objects.create(
            name="Castigate",
            level=0,
            description="Parent",
        )
        level1 = Arcanos.objects.create(
            name="Soulsight",
            level=1,
            parent_arcanos=parent,
            description="Level 1",
        )
        level2 = Arcanos.objects.create(
            name="Tainted Touch",
            level=2,
            parent_arcanos=parent,
            description="Level 2",
        )
        level3 = Arcanos.objects.create(
            name="Condemn",
            level=3,
            parent_arcanos=parent,
            description="Level 3",
        )

        self.assertEqual(parent.levels.count(), 3)
        self.assertIn(level1, parent.levels.all())
        self.assertIn(level2, parent.levels.all())
        self.assertIn(level3, parent.levels.all())

    def test_deleting_parent_nullifies_children(self):
        """Deleting parent arcanos sets children's parent to null."""
        parent = Arcanos.objects.create(name="Parent", level=0, description="Parent")
        child = Arcanos.objects.create(
            name="Child",
            level=1,
            parent_arcanos=parent,
            description="Child",
        )
        child_id = child.id

        parent.delete()
        child.refresh_from_db()
        self.assertIsNone(child.parent_arcanos)

    def test_arcanos_str_representation(self):
        """Arcanos uses name for string representation (from Model base)."""
        arcanos = Arcanos.objects.create(name="Phantasm", description="Test")
        self.assertEqual(str(arcanos), "Phantasm")


class TestArcanosMetaOptions(TestCase):
    """Tests for Arcanos Meta options."""

    def test_verbose_name(self):
        """Arcanos has correct verbose_name."""
        self.assertEqual(Arcanos._meta.verbose_name, "Arcanos")

    def test_verbose_name_plural(self):
        """Arcanos has correct verbose_name_plural (Arcanoi)."""
        self.assertEqual(Arcanos._meta.verbose_name_plural, "Arcanoi")
