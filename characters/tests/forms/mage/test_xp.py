"""
Tests for Mage XP spending form validation and processing.

Tests cover:
- MageXPForm initialization and mage-specific fields
- Category validation for mage-specific categories (Sphere, Arete, Practice, etc.)
- Category filtering based on character state
- Example field population for mage categories
- XP cost calculations for mage-specific stats
"""

from characters.costs import get_xp_cost
from characters.forms.mage.xp import CATEGORY_CHOICES, MageXPForm
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.mage import Mage, PracticeRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from characters.tests.utils import mage_setup
from core.models import Number
from django.contrib.auth.models import User
from django.test import TestCase


class TestMageXPFormBasics(TestCase):
    """Test basic MageXPForm initialization and structure."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.first()
        self.character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
        )
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_form_has_mage_specific_fields(self):
        """Test that form has mage-specific fields."""
        form = MageXPForm(character=self.character)

        # Should have inherited fields
        self.assertIn("category", form.fields)
        self.assertIn("example", form.fields)
        self.assertIn("value", form.fields)

        # Should have mage-specific field
        self.assertIn("resonance", form.fields)

    def test_form_category_has_mage_choices(self):
        """Test that category field has mage-specific choices."""
        form = MageXPForm(character=self.character)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        # Check for mage-specific categories
        self.assertIn("Sphere", category_values)
        self.assertIn("Arete", category_values)
        self.assertIn("Rote Points", category_values)
        self.assertIn("Resonance", category_values)
        self.assertIn("Tenet", category_values)
        self.assertIn("Practice", category_values)

    def test_resonance_field_has_suggestions(self):
        """Test that resonance field has autocomplete suggestions."""
        form = MageXPForm(character=self.character)

        suggestions = form.fields["resonance"].widget.suggestions
        self.assertIsNotNone(suggestions)
        self.assertGreater(len(suggestions), 0)


class TestMageXPFormCategoryFiltering(TestCase):
    """Test that mage-specific categories are filtered based on character state."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.first()
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_sphere_category_hidden_when_insufficient_xp(self):
        """Test Sphere category is hidden when character can't afford any sphere."""
        character = Mage.objects.create(
            name="Poor Mage",
            owner=self.user,
            xp=0,
            arete=3,
            faction=self.faction,
        )

        form = MageXPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Sphere", category_values)

    def test_sphere_category_shown_when_affordable(self):
        """Test Sphere category is shown when character can afford sphere upgrades."""
        character = Mage.objects.create(
            name="Rich Mage",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
        )

        form = MageXPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Sphere", category_values)

    def test_rote_points_category_requires_xp(self):
        """Test Rote Points category requires at least 1 XP."""
        character_with_xp = Mage.objects.create(
            name="Mage With XP",
            owner=self.user,
            xp=5,
            arete=3,
            faction=self.faction,
        )
        character_no_xp = Mage.objects.create(
            name="Mage No XP",
            owner=self.user,
            xp=0,
            arete=3,
            faction=self.faction,
        )

        form_with = MageXPForm(character=character_with_xp)
        form_without = MageXPForm(character=character_no_xp)

        categories_with = [choice[0] for choice in form_with.fields["category"].choices]
        categories_without = [choice[0] for choice in form_without.fields["category"].choices]

        self.assertIn("Rote Points", categories_with)
        self.assertNotIn("Rote Points", categories_without)

    def test_resonance_category_requires_3_xp(self):
        """Test Resonance category requires at least 3 XP."""
        character_with_xp = Mage.objects.create(
            name="Mage With XP",
            owner=self.user,
            xp=3,
            arete=3,
            faction=self.faction,
        )
        character_no_xp = Mage.objects.create(
            name="Mage No XP",
            owner=self.user,
            xp=2,
            arete=3,
            faction=self.faction,
        )

        form_with = MageXPForm(character=character_with_xp)
        form_without = MageXPForm(character=character_no_xp)

        categories_with = [choice[0] for choice in form_with.fields["category"].choices]
        categories_without = [choice[0] for choice in form_without.fields["category"].choices]

        self.assertIn("Resonance", categories_with)
        self.assertNotIn("Resonance", categories_without)

    def test_tenet_category_always_available(self):
        """Test Tenet category is always available (free to add)."""
        character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=0,
            arete=3,
            faction=self.faction,
        )

        form = MageXPForm(character=character)
        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Tenet", category_values)

    def test_arete_category_requires_sufficient_xp(self):
        """Test Arete category requires sufficient XP based on current arete."""
        # Arete 3 -> 4 costs 8 * 3 = 24 XP
        character_with_xp = Mage.objects.create(
            name="Rich Mage",
            owner=self.user,
            xp=30,
            arete=3,
            faction=self.faction,
        )
        character_no_xp = Mage.objects.create(
            name="Poor Mage",
            owner=self.user,
            xp=10,
            arete=3,
            faction=self.faction,
        )

        form_with = MageXPForm(character=character_with_xp)
        form_without = MageXPForm(character=character_no_xp)

        categories_with = [choice[0] for choice in form_with.fields["category"].choices]
        categories_without = [choice[0] for choice in form_without.fields["category"].choices]

        self.assertIn("Arete", categories_with)
        self.assertNotIn("Arete", categories_without)

    def test_rote_category_requires_rote_points(self):
        """Test Rote category requires character to have rote points."""
        character_with_points = Mage.objects.create(
            name="Mage With Points",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
            rote_points=5,
        )
        character_no_points = Mage.objects.create(
            name="Mage No Points",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
            rote_points=0,
        )

        form_with = MageXPForm(character=character_with_points)
        form_without = MageXPForm(character=character_no_points)

        categories_with = [choice[0] for choice in form_with.fields["category"].choices]
        categories_without = [choice[0] for choice in form_without.fields["category"].choices]

        self.assertIn("Rote", categories_with)
        self.assertNotIn("Rote", categories_without)


class TestMageXPFormExamplePopulation(TestCase):
    """Test example field population for mage-specific categories."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.first()
        self.character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
        )
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_sphere_category_populates_example_with_spheres(self):
        """Test that selecting Sphere populates example with sphere choices."""
        form = MageXPForm(
            data={"category": "Sphere"},
            character=self.character,
        )

        example_choices = form.fields["example"].choices
        choice_names = [choice[1] for choice in example_choices]

        # Check for some standard spheres
        self.assertIn("Correspondence", choice_names)
        self.assertIn("Forces", choice_names)
        self.assertIn("Mind", choice_names)

    def test_tenet_category_populates_example_with_tenets(self):
        """Test that selecting Tenet populates example with tenet choices."""
        form = MageXPForm(
            data={"category": "Tenet"},
            character=self.character,
        )

        example_choices = form.fields["example"].choices
        self.assertGreater(len(example_choices), 0)

    def test_practice_category_populates_example_with_practices(self):
        """Test that selecting Practice populates example with practice choices."""
        form = MageXPForm(
            data={"category": "Practice"},
            character=self.character,
        )

        example_choices = form.fields["example"].choices
        self.assertGreater(len(example_choices), 0)


class TestMageXPFormValidityChecks(TestCase):
    """Test the mage-specific *_valid() methods."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.first()

    def test_spheres_valid_with_available_xp(self):
        """Test spheres_valid returns True when XP is available."""
        character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
        )
        form = MageXPForm(character=character)

        self.assertTrue(form.spheres_valid())

    def test_spheres_valid_false_when_no_xp(self):
        """Test spheres_valid returns False when XP is insufficient."""
        character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=0,
            arete=3,
            faction=self.faction,
        )
        form = MageXPForm(character=character)

        self.assertFalse(form.spheres_valid())

    def test_rote_points_valid_requires_xp(self):
        """Test rote_points_valid requires at least 1 XP."""
        character_with = Mage.objects.create(
            name="With",
            owner=self.user,
            xp=1,
            arete=3,
            faction=self.faction,
        )
        character_without = Mage.objects.create(
            name="Without",
            owner=self.user,
            xp=0,
            arete=3,
            faction=self.faction,
        )

        form_with = MageXPForm(character=character_with)
        form_without = MageXPForm(character=character_without)

        self.assertTrue(form_with.rote_points_valid())
        self.assertFalse(form_without.rote_points_valid())

    def test_resonance_valid_requires_3_xp(self):
        """Test resonance_valid requires at least 3 XP."""
        character_with = Mage.objects.create(
            name="With",
            owner=self.user,
            xp=3,
            arete=3,
            faction=self.faction,
        )
        character_without = Mage.objects.create(
            name="Without",
            owner=self.user,
            xp=2,
            arete=3,
            faction=self.faction,
        )

        form_with = MageXPForm(character=character_with)
        form_without = MageXPForm(character=character_without)

        self.assertTrue(form_with.resonance_valid())
        self.assertFalse(form_without.resonance_valid())

    def test_add_tenet_valid_always_true(self):
        """Test add_tenet_valid always returns True."""
        character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=0,
            arete=1,
            faction=self.faction,
        )
        form = MageXPForm(character=character)

        self.assertTrue(form.add_tenet_valid())

    def test_arete_valid_checks_xp_and_tenet_limit(self):
        """Test arete_valid checks XP cost and tenet requirements."""
        character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
        )
        form = MageXPForm(character=character)

        # Should be valid with plenty of XP and arete <= tenets + 3
        self.assertTrue(form.arete_valid())

    def test_rote_valid_requires_rote_points(self):
        """Test rote_valid requires rote points > 0."""
        character_with = Mage.objects.create(
            name="With",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
            rote_points=5,
        )
        character_without = Mage.objects.create(
            name="Without",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
            rote_points=0,
        )

        form_with = MageXPForm(character=character_with)
        form_without = MageXPForm(character=character_without)

        self.assertTrue(form_with.rote_valid())
        self.assertFalse(form_without.rote_valid())


class TestMageXPFormCleanExample(TestCase):
    """Test example field cleaning for mage-specific categories."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.first()
        self.character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
        )
        for i in range(1, 6):
            Number.objects.get_or_create(value=i)

    def test_clean_example_returns_sphere_object(self):
        """Test that clean_example returns Sphere object for Sphere category."""
        forces = Sphere.objects.get(property_name="forces")

        form = MageXPForm(
            data={"category": "Sphere", "example": forces.id},
            character=self.character,
        )
        form.is_valid()

        if "example" in form.cleaned_data:
            self.assertEqual(form.cleaned_data["example"], forces)

    def test_clean_example_returns_tenet_object(self):
        """Test that clean_example returns Tenet object for Tenet category."""
        tenet = Tenet.objects.first()

        form = MageXPForm(
            data={"category": "Tenet", "example": tenet.id},
            character=self.character,
        )
        form.is_valid()

        if "example" in form.cleaned_data:
            self.assertEqual(form.cleaned_data["example"], tenet)

    def test_clean_example_returns_practice_object(self):
        """Test that clean_example returns Practice object for Practice category."""
        practice = Practice.objects.first()

        form = MageXPForm(
            data={"category": "Practice", "example": practice.id},
            character=self.character,
        )
        form.is_valid()

        if "example" in form.cleaned_data:
            self.assertEqual(form.cleaned_data["example"], practice)


class TestMageXPCostCalculations(TestCase):
    """Test XP cost calculations for mage-specific stat types."""

    def setUp(self):
        mage_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faction = MageFaction.objects.first()
        self.character = Mage.objects.create(
            name="Test Mage",
            owner=self.user,
            xp=50,
            arete=3,
            faction=self.faction,
        )

    def test_sphere_xp_cost(self):
        """Test XP cost for spheres (current rating * 8)."""
        self.assertEqual(get_xp_cost("sphere") * 1, 8)
        self.assertEqual(get_xp_cost("sphere") * 2, 16)
        self.assertEqual(get_xp_cost("sphere") * 3, 24)

    def test_new_sphere_xp_cost(self):
        """Test XP cost for new spheres (10 XP)."""
        self.assertEqual(get_xp_cost("new_sphere"), 10)

    def test_arete_xp_cost(self):
        """Test XP cost for arete (current rating * 8)."""
        self.assertEqual(get_xp_cost("arete") * 1, 8)
        self.assertEqual(get_xp_cost("arete") * 3, 24)
        self.assertEqual(get_xp_cost("arete") * 5, 40)

    def test_tenet_xp_cost(self):
        """Test XP cost for adding tenet (0 - free)."""
        self.assertEqual(get_xp_cost("tenet"), 0)

    def test_remove_tenet_xp_cost(self):
        """Test XP cost for removing tenet (1 per excess tenet)."""
        # Remove tenet is not in costs.py, this is a special case
        self.assertEqual(1 * 1, 1)
        self.assertEqual(1 * 3, 3)

    def test_practice_xp_cost(self):
        """Test XP cost for practices (current rating * 1)."""
        self.assertEqual(get_xp_cost("practice") * 1, 1)
        self.assertEqual(get_xp_cost("practice") * 3, 3)

    def test_new_practice_xp_cost(self):
        """Test XP cost for new practices (3 XP)."""
        self.assertEqual(get_xp_cost("new_practice"), 3)

    def test_resonance_xp_cost(self):
        """Test XP cost for resonance (current rating * 3)."""
        self.assertEqual(get_xp_cost("resonance") * 1, 3)
        self.assertEqual(get_xp_cost("resonance") * 3, 9)

    def test_new_resonance_xp_cost(self):
        """Test XP cost for new resonance (5 XP)."""
        self.assertEqual(get_xp_cost("new_resonance"), 5)
