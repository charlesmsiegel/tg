"""
Tests for VampireCreationForm.

Tests cover:
- Form initialization with user
- Queryset setup for clan, sect, path, sire fields
- Field configuration (required fields, placeholders)
- Form validation with valid and invalid data
- Owner assignment on save
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.vampire.vampire import VampireCreationForm
from characters.models.core.archetype import Archetype
from characters.models.vampire.clan import VampireClan
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.path import Path
from characters.models.vampire.sect import VampireSect
from characters.models.vampire.vampire import Vampire
from game.models import Chronicle


class VampireCreationFormTestCase(TestCase):
    """Base test case with common setup for VampireCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create disciplines
        cls.potence = Discipline.objects.create(name="Potence", property_name="potence")
        cls.celerity = Discipline.objects.create(name="Celerity", property_name="celerity")
        cls.presence = Discipline.objects.create(name="Presence", property_name="presence")
        cls.dominate = Discipline.objects.create(name="Dominate", property_name="dominate")

        # Create clans
        cls.brujah = VampireClan.objects.create(
            name="Brujah",
            nickname="Rabble",
            is_bloodline=False,
        )
        cls.brujah.disciplines.add(cls.potence, cls.celerity, cls.presence)

        cls.ventrue = VampireClan.objects.create(
            name="Ventrue",
            nickname="Blue Bloods",
            is_bloodline=False,
        )
        cls.ventrue.disciplines.add(cls.dominate, cls.potence, cls.presence)

        # Create a bloodline (should be excluded from default queryset)
        cls.true_brujah = VampireClan.objects.create(
            name="True Brujah",
            is_bloodline=True,
            parent_clan=cls.brujah,
        )

        # Create sects
        cls.camarilla = VampireSect.objects.create(name="Camarilla")
        cls.sabbat = VampireSect.objects.create(name="Sabbat")

        # Create paths
        cls.path_of_caine = Path.objects.create(
            name="Path of Caine",
            requires_conviction=True,
            requires_instinct=True,
        )

        # Create archetypes
        cls.survivor = Archetype.objects.create(name="Survivor")
        cls.bravo = Archetype.objects.create(name="Bravo")

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")


class TestVampireCreationFormInitialization(VampireCreationFormTestCase):
    """Test form initialization."""

    def test_form_initializes_with_user(self):
        """Form initializes correctly with user parameter."""
        form = VampireCreationForm(user=self.user)
        self.assertEqual(form.user, self.user)

    def test_form_has_expected_fields(self):
        """Form has all expected fields."""
        form = VampireCreationForm(user=self.user)
        expected_fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "clan",
            "sect",
            "sire",
            "path",
            "chronicle",
            "image",
            "npc",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_clan_queryset_excludes_bloodlines(self):
        """Clan queryset only includes main clans, not bloodlines."""
        form = VampireCreationForm(user=self.user)
        clan_qs = form.fields["clan"].queryset
        self.assertIn(self.brujah, clan_qs)
        self.assertIn(self.ventrue, clan_qs)
        self.assertNotIn(self.true_brujah, clan_qs)

    def test_sect_queryset_includes_all_sects(self):
        """Sect queryset includes all sects."""
        form = VampireCreationForm(user=self.user)
        sect_qs = form.fields["sect"].queryset
        self.assertIn(self.camarilla, sect_qs)
        self.assertIn(self.sabbat, sect_qs)

    def test_path_queryset_includes_all_paths(self):
        """Path queryset includes all paths."""
        form = VampireCreationForm(user=self.user)
        path_qs = form.fields["path"].queryset
        self.assertIn(self.path_of_caine, path_qs)

    def test_sire_queryset_empty_initially(self):
        """Sire queryset is empty when form is not bound."""
        form = VampireCreationForm(user=self.user)
        sire_qs = form.fields["sire"].queryset
        self.assertEqual(sire_qs.count(), 0)


class TestVampireCreationFormFieldConfiguration(VampireCreationFormTestCase):
    """Test form field configuration."""

    def test_name_has_placeholder(self):
        """Name field has placeholder."""
        form = VampireCreationForm(user=self.user)
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Enter name here",
        )

    def test_concept_has_placeholder(self):
        """Concept field has placeholder."""
        form = VampireCreationForm(user=self.user)
        self.assertEqual(
            form.fields["concept"].widget.attrs.get("placeholder"),
            "Enter concept here",
        )

    def test_image_not_required(self):
        """Image field is not required."""
        form = VampireCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)

    def test_sire_not_required(self):
        """Sire field is not required."""
        form = VampireCreationForm(user=self.user)
        self.assertFalse(form.fields["sire"].required)

    def test_path_not_required(self):
        """Path field is not required."""
        form = VampireCreationForm(user=self.user)
        self.assertFalse(form.fields["path"].required)


class TestVampireCreationFormBoundData(VampireCreationFormTestCase):
    """Test form behavior when bound with data."""

    def test_sire_queryset_populated_when_bound(self):
        """Sire queryset includes all vampires when form is bound."""
        # Create a potential sire
        sire = Vampire.objects.create(
            name="Elder Brujah",
            owner=self.user,
            clan=self.brujah,
        )

        form = VampireCreationForm(
            data={
                "name": "New Vampire",
                "concept": "Warrior",
            },
            user=self.user,
        )
        sire_qs = form.fields["sire"].queryset
        self.assertIn(sire, sire_qs)


class TestVampireCreationFormValidation(VampireCreationFormTestCase):
    """Test form validation."""

    def test_valid_minimal_submission(self):
        """Valid submission with minimal required data."""
        form = VampireCreationForm(
            data={
                "name": "Test Vampire",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.bravo.pk),
                "concept": "Warrior",
                "clan": str(self.brujah.pk),
                "sect": str(self.camarilla.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_full_submission(self):
        """Valid submission with all fields filled."""
        sire = Vampire.objects.create(
            name="Elder",
            owner=self.user,
            clan=self.brujah,
        )

        form = VampireCreationForm(
            data={
                "name": "Test Vampire",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.bravo.pk),
                "concept": "Warrior",
                "clan": str(self.brujah.pk),
                "sect": str(self.camarilla.pk),
                "sire": str(sire.pk),
                "path": str(self.path_of_caine.pk),
                "chronicle": str(self.chronicle.pk),
                "npc": False,
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_invalid_without_name(self):
        """Form is invalid without name."""
        form = VampireCreationForm(
            data={
                "concept": "Warrior",
                "clan": str(self.brujah.pk),
            },
            user=self.user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TestVampireCreationFormSave(VampireCreationFormTestCase):
    """Test form save functionality."""

    def test_save_assigns_owner(self):
        """Saving form assigns owner to vampire."""
        form = VampireCreationForm(
            data={
                "name": "Test Vampire",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.bravo.pk),
                "concept": "Warrior",
                "clan": str(self.brujah.pk),
                "sect": str(self.camarilla.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        vampire = form.save()
        self.assertEqual(vampire.owner, self.user)

    def test_save_commit_false(self):
        """Saving with commit=False returns unsaved instance."""
        form = VampireCreationForm(
            data={
                "name": "Test Vampire",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.bravo.pk),
                "concept": "Warrior",
                "clan": str(self.brujah.pk),
                "sect": str(self.camarilla.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        vampire = form.save(commit=False)
        self.assertIsNone(vampire.pk)
        self.assertEqual(vampire.owner, self.user)

    def test_save_creates_vampire_with_correct_data(self):
        """Saving form creates vampire with correct data."""
        form = VampireCreationForm(
            data={
                "name": "Marcus Brujah",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.bravo.pk),
                "concept": "Philosopher Warrior",
                "clan": str(self.brujah.pk),
                "sect": str(self.camarilla.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        vampire = form.save()

        self.assertEqual(vampire.name, "Marcus Brujah")
        self.assertEqual(vampire.concept, "Philosopher Warrior")
        self.assertEqual(vampire.clan, self.brujah)
        self.assertEqual(vampire.sect, self.camarilla)
        self.assertEqual(vampire.owner, self.user)

    def test_save_with_path_sets_path_rating(self):
        """Saving form with a path sets path_rating to 4."""
        form = VampireCreationForm(
            data={
                "name": "Test Vampire",
                "nature": str(self.survivor.pk),
                "demeanor": str(self.bravo.pk),
                "concept": "Warrior",
                "clan": str(self.brujah.pk),
                "sect": str(self.sabbat.pk),
                "path": str(self.path_of_caine.pk),
                "chronicle": str(self.chronicle.pk),
            },
            user=self.user,
        )
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        vampire = form.save()
        self.assertEqual(vampire.path, self.path_of_caine)
        self.assertEqual(vampire.path_rating, 4)
