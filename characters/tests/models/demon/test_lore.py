"""Tests for Lore model."""

from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from django.contrib.auth.models import User
from django.test import TestCase


class LoreModelTests(TestCase):
    """Tests for Lore model functionality."""

    def setUp(self):
        """Create a test user for ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.lore = Lore.objects.create(
            name="Lore of Flame",
            property_name="flame",
            description="Control and create fire",
            owner=self.user,
        )

    def test_type_is_lore(self):
        """Test that type is 'lore'."""
        self.assertEqual(self.lore.type, "lore")

    def test_gameline_is_dtf(self):
        """Test that gameline is 'dtf'."""
        self.assertEqual(self.lore.gameline, "dtf")

    def test_str_representation(self):
        """Test string representation is the name."""
        self.assertEqual(str(self.lore), "Lore of Flame")

    def test_property_name_unique(self):
        """Test that property_name must be unique."""
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Lore.objects.create(
                name="Other Fire Lore",
                property_name="flame",  # Same property name
                owner=self.user,
            )

    def test_default_description(self):
        """Test default description is empty."""
        lore = Lore.objects.create(
            name="Test Lore",
            property_name="test",
            owner=self.user,
        )
        self.assertEqual(lore.description, "")

    def test_ordering_by_name(self):
        """Lores should be ordered by name by default."""
        lore_c = Lore.objects.create(
            name="Lore of the Wild", property_name="wild", owner=self.user
        )
        lore_a = Lore.objects.create(
            name="Lore of Death", property_name="death", owner=self.user
        )
        lore_b = Lore.objects.create(
            name="Lore of Light", property_name="light", owner=self.user
        )

        lores = list(Lore.objects.filter(pk__in=[lore_a.pk, lore_b.pk, lore_c.pk]))

        self.assertEqual(lores[0], lore_a)  # Death
        self.assertEqual(lores[1], lore_b)  # Light
        self.assertEqual(lores[2], lore_c)  # Wild

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.lore.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/lore/{self.lore.pk}/")

    def test_get_update_url(self):
        """Test get_update_url returns correct URL."""
        url = self.lore.get_update_url()
        self.assertEqual(url, f"/characters/demon/update/lore/{self.lore.pk}/")

    def test_get_creation_url(self):
        """Test get_creation_url returns correct URL."""
        url = Lore.get_creation_url()
        self.assertEqual(url, "/characters/demon/create/lore/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.lore.get_heading(), "dtf_heading")


class LoreVerboseNameTests(TestCase):
    """Tests for Lore verbose names."""

    def test_verbose_name(self):
        """Test verbose_name is correct."""
        self.assertEqual(Lore._meta.verbose_name, "Lore")

    def test_verbose_name_plural(self):
        """Test verbose_name_plural is correct."""
        self.assertEqual(Lore._meta.verbose_name_plural, "Lores")


class LoreHouseRelationshipTests(TestCase):
    """Tests for Lore-House many-to-many relationship."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.house_devils = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        self.house_scourges = DemonHouse.objects.create(
            name="Scourges", celestial_name="Asharu", owner=self.user
        )
        self.lore = Lore.objects.create(
            name="Lore of Flame",
            property_name="flame",
            owner=self.user,
        )

    def test_lore_can_have_no_houses(self):
        """Lore can exist without any house associations."""
        self.assertEqual(self.lore.houses.count(), 0)

    def test_lore_can_have_one_house(self):
        """Lore can be associated with one house."""
        self.lore.houses.add(self.house_devils)
        self.assertEqual(self.lore.houses.count(), 1)
        self.assertIn(self.house_devils, self.lore.houses.all())

    def test_lore_can_have_multiple_houses(self):
        """Lore can be associated with multiple houses."""
        self.lore.houses.add(self.house_devils, self.house_scourges)
        self.assertEqual(self.lore.houses.count(), 2)
        self.assertIn(self.house_devils, self.lore.houses.all())
        self.assertIn(self.house_scourges, self.lore.houses.all())

    def test_house_lores_related_name(self):
        """House can access its lores via related_name."""
        self.lore.houses.add(self.house_devils)
        self.assertIn(self.lore, self.house_devils.lores.all())

    def test_house_can_have_multiple_lores(self):
        """House can have multiple lores associated."""
        lore2 = Lore.objects.create(
            name="Lore of Light",
            property_name="light",
            owner=self.user,
        )
        self.lore.houses.add(self.house_devils)
        lore2.houses.add(self.house_devils)

        self.assertEqual(self.house_devils.lores.count(), 2)


class LoreTwentyThreeLoresTests(TestCase):
    """Tests for creating all 23 canonical lores."""

    def setUp(self):
        """Create test user."""
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_can_create_all_23_lores(self):
        """Test that all 23 canonical lores can be created."""
        lores = [
            ("Lore of Awakening", "awakening"),
            ("Lore of the Beast", "beast"),
            ("Lore of the Celestials", "celestials"),
            ("Lore of Death", "death"),
            ("Lore of the Earth", "earth"),
            ("Lore of Flame", "flame"),
            ("Lore of the Firmament", "firmament"),
            ("Lore of the Flesh", "flesh"),
            ("Lore of the Forge", "forge"),
            ("Lore of the Fundament", "fundament"),
            ("Lore of Humanity", "humanity"),
            ("Lore of Light", "light"),
            ("Lore of Longing", "longing"),
            ("Lore of Paths", "paths"),
            ("Lore of Patterns", "patterns"),
            ("Lore of Portals", "portals"),
            ("Lore of Radiance", "radiance"),
            ("Lore of the Realms", "realms"),
            ("Lore of the Spirit", "spirit"),
            ("Lore of Storms", "storms"),
            ("Lore of Transfiguration", "transfiguration"),
            ("Lore of the Wild", "wild"),
            ("Lore of the Winds", "winds"),
        ]

        created_lores = []
        for name, property_name in lores:
            lore = Lore.objects.create(
                name=name,
                property_name=property_name,
                owner=self.user,
            )
            created_lores.append(lore)

        self.assertEqual(len(created_lores), 23)
        self.assertEqual(Lore.objects.count(), 23)
