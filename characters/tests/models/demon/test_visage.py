"""Tests for Visage model."""

from characters.models.demon.apocalyptic_form import ApocalypticForm
from characters.models.demon.house import DemonHouse
from characters.models.demon.visage import Visage
from django.contrib.auth.models import User
from django.test import TestCase


class VisageModelTests(TestCase):
    """Tests for Visage model functionality."""

    def setUp(self):
        """Create a test user for ownership."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.visage = Visage.objects.create(
            name="Bel",
            owner=self.user,
        )

    def test_type_is_visage(self):
        """Test that type is 'visage'."""
        self.assertEqual(self.visage.type, "visage")

    def test_gameline_is_dtf(self):
        """Test that gameline is 'dtf'."""
        self.assertEqual(self.visage.gameline, "dtf")

    def test_str_representation(self):
        """Test string representation is the name."""
        self.assertEqual(str(self.visage), "Bel")

    def test_default_house_is_none(self):
        """Test default house is None."""
        self.assertIsNone(self.visage.house)

    def test_default_apocalyptic_form_is_none(self):
        """Test default apocalyptic form is None."""
        self.assertIsNone(self.visage.default_apocalyptic_form)

    def test_ordering_by_name(self):
        """Visages should be ordered by name by default."""
        visage_c = Visage.objects.create(name="Qingu", owner=self.user)
        visage_a = Visage.objects.create(name="Dagan", owner=self.user)
        visage_b = Visage.objects.create(name="Nusku", owner=self.user)

        visages = list(Visage.objects.filter(pk__in=[visage_a.pk, visage_b.pk, visage_c.pk]))

        self.assertEqual(visages[0], visage_a)  # Dagan
        self.assertEqual(visages[1], visage_b)  # Nusku
        self.assertEqual(visages[2], visage_c)  # Qingu

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL."""
        url = self.visage.get_absolute_url()
        self.assertEqual(url, f"/characters/demon/visage/{self.visage.pk}/")

    def test_get_update_url(self):
        """Test get_update_url returns correct URL."""
        url = self.visage.get_update_url()
        self.assertEqual(url, f"/characters/demon/update/visage/{self.visage.pk}/")

    def test_get_creation_url(self):
        """Test get_creation_url returns correct URL."""
        url = Visage.get_creation_url()
        self.assertEqual(url, "/characters/demon/create/visage/")

    def test_get_heading(self):
        """Test get_heading returns DTF heading."""
        self.assertEqual(self.visage.get_heading(), "dtf_heading")


class VisageVerboseNameTests(TestCase):
    """Tests for Visage verbose names."""

    def test_verbose_name(self):
        """Test verbose_name is correct."""
        self.assertEqual(Visage._meta.verbose_name, "Visage")

    def test_verbose_name_plural(self):
        """Test verbose_name_plural is correct."""
        self.assertEqual(Visage._meta.verbose_name_plural, "Visages")


class VisageHouseRelationshipTests(TestCase):
    """Tests for Visage-House relationship."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        self.visage = Visage.objects.create(name="Bel", owner=self.user)

    def test_visage_can_have_house(self):
        """Visage can be associated with a house."""
        self.visage.house = self.house
        self.visage.save()
        self.assertEqual(self.visage.house, self.house)

    def test_house_visages_related_name(self):
        """House can access its visages via related_name."""
        self.visage.house = self.house
        self.visage.save()
        self.assertIn(self.visage, self.house.visages.all())

    def test_house_can_have_multiple_visages(self):
        """House can have multiple visages associated."""
        visage2 = Visage.objects.create(name="Anshar", owner=self.user, house=self.house)
        self.visage.house = self.house
        self.visage.save()

        self.assertEqual(self.house.visages.count(), 2)

    def test_visage_house_set_null_on_delete(self):
        """Deleting house sets visage.house to NULL."""
        self.visage.house = self.house
        self.visage.save()

        house_id = self.house.id
        self.house.delete()

        self.visage.refresh_from_db()
        self.assertIsNone(self.visage.house)


class VisageDefaultApocalypticFormTests(TestCase):
    """Tests for Visage default apocalyptic form relationship."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.form = ApocalypticForm.objects.create(name="Bel Default Form", owner=self.user)
        self.visage = Visage.objects.create(name="Bel", owner=self.user)

    def test_visage_can_have_default_form(self):
        """Visage can have a default apocalyptic form."""
        self.visage.default_apocalyptic_form = self.form
        self.visage.save()
        self.assertEqual(self.visage.default_apocalyptic_form, self.form)

    def test_form_visages_related_name(self):
        """Form can access visages using it as default via related_name."""
        self.visage.default_apocalyptic_form = self.form
        self.visage.save()
        self.assertIn(self.visage, self.form.visages_using_as_default.all())

    def test_multiple_visages_same_default_form(self):
        """Multiple visages can share the same default form."""
        visage2 = Visage.objects.create(name="Anshar", owner=self.user)
        self.visage.default_apocalyptic_form = self.form
        visage2.default_apocalyptic_form = self.form
        self.visage.save()
        visage2.save()

        self.assertEqual(self.form.visages_using_as_default.count(), 2)

    def test_visage_form_set_null_on_delete(self):
        """Deleting form sets visage.default_apocalyptic_form to NULL."""
        self.visage.default_apocalyptic_form = self.form
        self.visage.save()

        form_id = self.form.id
        self.form.delete()

        self.visage.refresh_from_db()
        self.assertIsNone(self.visage.default_apocalyptic_form)


class VisageAllRelationshipsTests(TestCase):
    """Tests for Visage with all relationships set."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        self.form = ApocalypticForm.objects.create(name="Bel Default Form", owner=self.user)
        self.visage = Visage.objects.create(
            name="Bel",
            house=self.house,
            default_apocalyptic_form=self.form,
            owner=self.user,
        )

    def test_visage_with_all_relationships(self):
        """Visage can have both house and default form set."""
        self.assertEqual(self.visage.house, self.house)
        self.assertEqual(self.visage.default_apocalyptic_form, self.form)

    def test_visage_accessible_from_house(self):
        """Visage is accessible from its house."""
        self.assertIn(self.visage, self.house.visages.all())

    def test_visage_accessible_from_form(self):
        """Visage is accessible from its default form."""
        self.assertIn(self.visage, self.form.visages_using_as_default.all())
