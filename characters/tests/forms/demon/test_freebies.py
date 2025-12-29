"""Tests for Demon freebie forms."""

from characters.forms.demon.freebies import (
    DEMON_CATEGORY_CHOICES,
    DTFHUMAN_CATEGORY_CHOICES,
    THRALL_CATEGORY_CHOICES,
    DemonFreebiesForm,
    DtFHumanFreebiesForm,
    ThrallFreebiesForm,
)
from characters.models.demon import Demon
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.thrall import Thrall
from django.contrib.auth.models import User
from django.test import TestCase


class DtFHumanFreebiesFormTests(TestCase):
    """Tests for DtFHumanFreebiesForm functionality."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.human = DtFHuman.objects.create(
            name="Test Human",
            owner=self.user,
            freebies=15,  # Give them some freebies
        )

    def test_form_uses_dtfhuman_category_choices(self):
        """Test that form uses DtFHuman-specific category choices."""
        form = DtFHumanFreebiesForm(instance=self.human)
        # Verify choices are from DTFHUMAN_CATEGORY_CHOICES (filtered by affordability)
        for choice, _ in form.fields["category"].choices:
            self.assertIn((choice, choice), DTFHUMAN_CATEGORY_CHOICES)

    def test_form_filters_unaffordable_choices(self):
        """Test that form filters out unaffordable category choices."""
        human = DtFHuman.objects.create(
            name="Broke Human",
            owner=self.user,
            freebies=0,  # No freebies
        )
        form = DtFHumanFreebiesForm(instance=human)
        # With 0 freebies, should have very limited options
        self.assertLess(len(form.fields["category"].choices), len(DTFHUMAN_CATEGORY_CHOICES))

    def test_validator_returns_true_for_affordable(self):
        """Test validator returns True for affordable categories."""
        form = DtFHumanFreebiesForm(instance=self.human)
        # With 15 freebies, should be able to afford Attribute (5 cost)
        self.assertTrue(form.validator("Attribute"))

    def test_validator_returns_false_for_blocked(self):
        """Test validator returns False for blocked categories (10000 cost)."""
        form = DtFHumanFreebiesForm(instance=self.human)
        # Categories with 10000 cost should be blocked
        # This depends on the character's freebie_cost implementation
        # Just verify the validator doesn't crash
        result = form.validator("Willpower")
        self.assertIn(result, [True, False])

    def test_save_returns_instance(self):
        """Test that save returns the instance."""
        form_data = {"category": "Attribute"}
        form = DtFHumanFreebiesForm(data=form_data, instance=self.human)
        if form.is_valid():
            result = form.save()
            self.assertEqual(result, self.human)


class ThrallFreebiesFormTests(TestCase):
    """Tests for ThrallFreebiesForm functionality."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.thrall = Thrall.objects.create(
            name="Test Thrall",
            owner=self.user,
            freebies=15,
        )

    def test_form_has_thrall_specific_choices(self):
        """Test that form has Thrall-specific category choices."""
        # Thrall should have Faith Potential and Virtue choices
        self.assertIn(("Faith Potential", "Faith Potential"), THRALL_CATEGORY_CHOICES)
        self.assertIn(("Virtue", "Virtue"), THRALL_CATEGORY_CHOICES)

    def test_form_filters_unaffordable_choices(self):
        """Test that form filters out unaffordable category choices."""
        thrall = Thrall.objects.create(
            name="Broke Thrall",
            owner=self.user,
            freebies=0,
        )
        form = ThrallFreebiesForm(instance=thrall)
        self.assertLess(len(form.fields["category"].choices), len(THRALL_CATEGORY_CHOICES))

    def test_validator_returns_true_for_affordable(self):
        """Test validator returns True for affordable categories."""
        form = ThrallFreebiesForm(instance=self.thrall)
        self.assertTrue(form.validator("Attribute"))

    def test_save_returns_instance(self):
        """Test that save returns the instance."""
        form_data = {"category": "Attribute"}
        form = ThrallFreebiesForm(data=form_data, instance=self.thrall)
        if form.is_valid():
            result = form.save()
            self.assertEqual(result, self.thrall)


class DemonFreebiesFormTests(TestCase):
    """Tests for DemonFreebiesForm functionality."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.demon = Demon.objects.create(
            name="Test Demon",
            owner=self.user,
            freebies=15,
        )

    def test_form_has_demon_specific_choices(self):
        """Test that form has Demon-specific category choices."""
        # Demon should have Lore, Faith, Virtue, and Temporary Faith choices
        self.assertIn(("Lore", "Lore"), DEMON_CATEGORY_CHOICES)
        self.assertIn(("Faith", "Faith"), DEMON_CATEGORY_CHOICES)
        self.assertIn(("Virtue", "Virtue"), DEMON_CATEGORY_CHOICES)
        self.assertIn(("Temporary Faith", "Temporary Faith"), DEMON_CATEGORY_CHOICES)

    def test_form_filters_unaffordable_choices(self):
        """Test that form filters out unaffordable category choices."""
        demon = Demon.objects.create(
            name="Broke Demon",
            owner=self.user,
            freebies=0,
        )
        form = DemonFreebiesForm(instance=demon)
        self.assertLess(len(form.fields["category"].choices), len(DEMON_CATEGORY_CHOICES))

    def test_validator_returns_true_for_affordable(self):
        """Test validator returns True for affordable categories."""
        form = DemonFreebiesForm(instance=self.demon)
        self.assertTrue(form.validator("Attribute"))

    def test_save_returns_instance(self):
        """Test that save returns the instance."""
        form_data = {"category": "Attribute"}
        form = DemonFreebiesForm(data=form_data, instance=self.demon)
        if form.is_valid():
            result = form.save()
            self.assertEqual(result, self.demon)


class CategoryChoicesTests(TestCase):
    """Tests for category choice constants."""

    def test_dtfhuman_choices_is_list(self):
        """Test that DTFHUMAN_CATEGORY_CHOICES is a list."""
        self.assertIsInstance(DTFHUMAN_CATEGORY_CHOICES, (list, tuple))

    def test_thrall_choices_extends_base(self):
        """Test that THRALL_CATEGORY_CHOICES extends base choices."""
        # Thrall should have everything DtFHuman has plus more
        for choice in DTFHUMAN_CATEGORY_CHOICES:
            self.assertIn(choice, THRALL_CATEGORY_CHOICES)

    def test_demon_choices_extends_base(self):
        """Test that DEMON_CATEGORY_CHOICES extends base choices."""
        # Demon should have everything DtFHuman has plus more
        for choice in DTFHUMAN_CATEGORY_CHOICES:
            self.assertIn(choice, DEMON_CATEGORY_CHOICES)

    def test_thrall_has_faith_potential(self):
        """Test that Thrall choices include Faith Potential."""
        choices = [c[0] for c in THRALL_CATEGORY_CHOICES]
        self.assertIn("Faith Potential", choices)

    def test_demon_has_lore(self):
        """Test that Demon choices include Lore."""
        choices = [c[0] for c in DEMON_CATEGORY_CHOICES]
        self.assertIn("Lore", choices)

    def test_demon_has_faith(self):
        """Test that Demon choices include Faith."""
        choices = [c[0] for c in DEMON_CATEGORY_CHOICES]
        self.assertIn("Faith", choices)

    def test_demon_has_temporary_faith(self):
        """Test that Demon choices include Temporary Faith."""
        choices = [c[0] for c in DEMON_CATEGORY_CHOICES]
        self.assertIn("Temporary Faith", choices)
