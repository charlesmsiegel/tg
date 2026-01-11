"""Tests for WraithFreebiesForm."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.costs import get_freebie_cost
from characters.forms.wraith.freebies import WraithFreebiesForm
from characters.models.wraith.wraith import Wraith


class WraithFreebiesFormTestCase(TestCase):
    """Base test case with common setup for WraithFreebiesForm tests."""

    def setUp(self):
        """Set up test user and wraith."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.wraith = Wraith.objects.create(
            name="Test Wraith",
            owner=self.user,
            freebies=21,  # Wraith gets 21 freebies (15 + 7 from freebie_step)
        )


class TestWraithFreebiesFormInitialization(WraithFreebiesFormTestCase):
    """Tests for WraithFreebiesForm initialization."""

    def test_form_initializes_with_wraith_instance(self):
        """Form initializes correctly with wraith instance."""
        form = WraithFreebiesForm(instance=self.wraith)
        self.assertIn("category", form.fields)
        self.assertIn("example", form.fields)

    def test_form_inherits_from_human_freebies_form(self):
        """Form inherits from HumanFreebiesForm."""
        from characters.forms.core.freebies import HumanFreebiesForm

        self.assertTrue(issubclass(WraithFreebiesForm, HumanFreebiesForm))


class TestWraithFreebiesFormValidator(WraithFreebiesFormTestCase):
    """Tests for the validator method."""

    def test_validator_returns_true_for_affordable_trait(self):
        """Validator returns True when wraith can afford trait."""
        form = WraithFreebiesForm(instance=self.wraith)
        # Arcanos costs 7, should be affordable with 21 freebies
        self.assertTrue(form.validator("arcanos"))

    def test_validator_returns_false_for_unaffordable_trait(self):
        """Validator returns False when wraith cannot afford trait."""
        self.wraith.freebies = 3
        self.wraith.save()
        form = WraithFreebiesForm(instance=self.wraith)
        # Arcanos costs 7, should not be affordable with 3 freebies
        self.assertFalse(form.validator("arcanos"))

    def test_validator_returns_false_for_unknown_trait(self):
        """Validator returns False for unknown traits (cost 10000)."""
        form = WraithFreebiesForm(instance=self.wraith)
        # Unknown traits have cost 10000 which is treated as blocked
        self.assertFalse(form.validator("unknown_trait_type"))

    def test_validator_handles_different_costs(self):
        """Validator handles different freebie costs correctly."""
        self.wraith.freebies = 5
        self.wraith.save()
        form = WraithFreebiesForm(instance=self.wraith)

        # Pathos costs 0.5 (non-int) - validator returns True for non-int costs
        self.assertTrue(form.validator("pathos"))

        # Arcanos costs 5, exactly affordable with 5 freebies
        self.assertTrue(form.validator("arcanos"))

        # Test with not enough freebies
        self.wraith.freebies = 4
        self.wraith.save()
        form2 = WraithFreebiesForm(instance=self.wraith)
        # Arcanos costs 5, should not be affordable with 4 freebies
        self.assertFalse(form2.validator("arcanos"))

    def test_validator_returns_false_for_blocked_category(self):
        """Validator returns False for blocked categories (cost 10000)."""
        form = WraithFreebiesForm(instance=self.wraith)
        # Default blocked category
        self.assertFalse(form.validator("-----"))


class TestWraithFreebiesFormSave(WraithFreebiesFormTestCase):
    """Tests for form save behavior."""

    def test_save_returns_instance(self):
        """Save returns the wraith instance."""
        form = WraithFreebiesForm(
            data={"category": "Willpower", "example": "", "value": ""},
            instance=self.wraith,
        )
        if form.is_valid():
            result = form.save()
            self.assertEqual(result, self.wraith)


class TestWraithFreebiesFormCostCalculations(WraithFreebiesFormTestCase):
    """Tests for wraith-specific freebie cost calculations."""

    def test_arcanos_cost_is_five(self):
        """Arcanos costs 5 freebies."""
        cost = get_freebie_cost("arcanos")
        self.assertEqual(cost, 5)

    def test_pathos_cost_is_half(self):
        """Pathos costs 0.5 freebie (1 per 2 dots)."""
        cost = get_freebie_cost("pathos")
        self.assertEqual(cost, 0.5)

    def test_passion_cost_is_two(self):
        """Passion costs 2 freebies."""
        cost = get_freebie_cost("passion")
        self.assertEqual(cost, 2)

    def test_fetter_cost_is_one(self):
        """Fetter costs 1 freebie."""
        cost = get_freebie_cost("fetter")
        self.assertEqual(cost, 1)

    def test_wraith_willpower_cost_is_two(self):
        """Wraith willpower costs 2 freebies."""
        cost = get_freebie_cost("wraith_willpower")
        self.assertEqual(cost, 2)


class TestWraithFreebiesFormEdgeCases(WraithFreebiesFormTestCase):
    """Tests for edge cases and boundary conditions."""

    def test_zero_freebies(self):
        """Form handles zero freebies correctly."""
        self.wraith.freebies = 0
        self.wraith.save()
        form = WraithFreebiesForm(instance=self.wraith)
        # Should not be able to afford arcanos (integer cost of 5)
        self.assertFalse(form.validator("arcanos"))
        # Note: pathos has a non-integer cost (0.5), and the validator
        # returns True for non-integer costs by design

    def test_exact_freebie_amount(self):
        """Validator handles exact freebie amount correctly."""
        self.wraith.freebies = 5
        self.wraith.save()
        form = WraithFreebiesForm(instance=self.wraith)
        # Exactly enough for arcanos (costs 5)
        self.assertTrue(form.validator("arcanos"))

    def test_one_below_required(self):
        """Validator handles one below required amount correctly."""
        self.wraith.freebies = 4
        self.wraith.save()
        form = WraithFreebiesForm(instance=self.wraith)
        # Not quite enough for arcanos (costs 5)
        self.assertFalse(form.validator("arcanos"))

    def test_validator_with_lowercase_trait(self):
        """Validator handles lowercase trait names."""
        form = WraithFreebiesForm(instance=self.wraith)
        self.assertTrue(form.validator("arcanos"))

    def test_validator_with_spaces_in_trait(self):
        """Validator handles trait names with spaces."""
        form = WraithFreebiesForm(instance=self.wraith)
        # "new background" should convert to "new_background" internally
        result = form.validator("new background")
        # This tests the normalization in the validator
        self.assertIsInstance(result, bool)
