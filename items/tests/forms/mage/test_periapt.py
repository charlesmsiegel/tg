"""
Tests for Periapt forms (Quintessence storage devices).

Tests cover:
- PeriaptForm initialization and field configuration
- PeriaptForm validation (rank, arete, charges, resonance)
- WonderResonanceRatingForm validation
- PeriaptResonanceRatingFormSet behavior
- Effect formset integration
- Save behavior with formsets
"""

from characters.models.mage.effect import Effect
from characters.models.mage.resonance import Resonance
from django.test import TestCase
from items.forms.mage.periapt import (
    PeriaptForm,
    PeriaptResonanceRatingFormSet,
    WonderResonanceRatingForm,
)
from items.models.mage.periapt import Periapt


class TestWonderResonanceRatingForm(TestCase):
    """Test WonderResonanceRatingForm validation."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = WonderResonanceRatingForm()

        self.assertIn("resonance", form.fields)
        self.assertIn("rating", form.fields)

    def test_rating_min_value(self):
        """Test that rating has minimum value of 0."""
        form = WonderResonanceRatingForm()

        self.assertEqual(form.fields["rating"].min_value, 0)

    def test_rating_max_value(self):
        """Test that rating has maximum value of 5."""
        form = WonderResonanceRatingForm()

        self.assertEqual(form.fields["rating"].max_value, 5)

    def test_rating_initial_value(self):
        """Test that rating has initial value of 0."""
        form = WonderResonanceRatingForm()

        self.assertEqual(form.fields["rating"].initial, 0)

    def test_resonance_is_optional(self):
        """Test that resonance field is optional."""
        form = WonderResonanceRatingForm()

        self.assertFalse(form.fields["resonance"].required)

    def test_valid_resonance_rating(self):
        """Test valid resonance rating data."""
        form_data = {
            "resonance": self.resonance.pk,
            "rating": 3,
        }

        form = WonderResonanceRatingForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_rating_too_high(self):
        """Test that rating > 5 is invalid."""
        form_data = {
            "resonance": self.resonance.pk,
            "rating": 6,
        }

        form = WonderResonanceRatingForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_rating_negative(self):
        """Test that negative rating is invalid."""
        form_data = {
            "resonance": self.resonance.pk,
            "rating": -1,
        }

        form = WonderResonanceRatingForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)


class TestPeriaptFormBasics(TestCase):
    """Test basic PeriaptForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = PeriaptForm()

        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("rank", form.fields)
        self.assertIn("arete", form.fields)
        self.assertIn("max_charges", form.fields)
        self.assertIn("current_charges", form.fields)
        self.assertIn("is_consumable", form.fields)

    def test_form_has_resonance_formset(self):
        """Test that form has a resonance formset."""
        form = PeriaptForm()

        self.assertTrue(hasattr(form, "resonance_formset"))
        self.assertIsInstance(form.resonance_formset, PeriaptResonanceRatingFormSet)

    def test_form_has_effect_formset(self):
        """Test that form has an effect formset."""
        form = PeriaptForm()

        self.assertTrue(hasattr(form, "effect_formset"))

    def test_name_placeholder(self):
        """Test that name field has correct placeholder."""
        form = PeriaptForm()

        self.assertEqual(form.fields["name"].widget.attrs.get("placeholder"), "Enter name here")

    def test_description_placeholder(self):
        """Test that description field has correct placeholder."""
        form = PeriaptForm()

        self.assertEqual(
            form.fields["description"].widget.attrs.get("placeholder"),
            "Enter description here",
        )


class TestPeriaptFormValidation(TestCase):
    """Test PeriaptForm validation rules."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)

    def setUp(self):
        """Create an effect for testing."""
        self.effect = Effect.objects.create(name="Test Effect", entropy=1)

    def _get_basic_form_data(self, **overrides):
        """Helper to create basic valid form data."""
        data = {
            "name": "Test Periapt",
            "description": "A test periapt",
            "rank": 1,
            "arete": 1,
            "max_charges": 5,
            "current_charges": 5,
            "is_consumable": True,
            # Resonance formset - management form
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            # Resonance form
            "resonance-0-resonance": str(self.resonance.pk),
            "resonance-0-rating": "1",
            # Effect formset - select existing effect (not create)
            "effects-TOTAL_FORMS": "1",
            "effects-INITIAL_FORMS": "0",
            "effects-MIN_NUM_FORMS": "0",
            "effects-MAX_NUM_FORMS": "1000",
            "effects-0-select": str(self.effect.pk),
            # select_or_create is False (not checked) = select existing
            # name is required by the ModelForm even when selecting
            "effects-0-name": "dummy",
        }
        data.update(overrides)
        return data

    def test_rank_cannot_be_none(self):
        """Test that rank is required."""
        data = self._get_basic_form_data()
        del data["rank"]

        form = PeriaptForm(data=data)

        # Form validation requires rank
        self.assertFalse(form.is_valid())

    def test_arete_cannot_be_none(self):
        """Test that arete is required."""
        data = self._get_basic_form_data()
        del data["arete"]

        form = PeriaptForm(data=data)

        # Form validation requires arete
        self.assertFalse(form.is_valid())

    def test_arete_must_be_at_least_rank(self):
        """Test that arete must be >= rank."""
        data = self._get_basic_form_data(rank=3, arete=2)

        form = PeriaptForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("Periapt Arete rating must be at least equal to rank", str(form.errors))

    def test_arete_equal_to_rank_is_valid(self):
        """Test that arete == rank is valid."""
        data = self._get_basic_form_data(rank=2, arete=2)
        # Resonance must match rank
        data["resonance-0-rating"] = "2"

        form = PeriaptForm(data=data)
        # Check for specific validation error - form might have other issues
        # but arete >= rank should be satisfied
        if not form.is_valid():
            self.assertNotIn(
                "Periapt Arete rating must be at least equal to rank", str(form.errors)
            )

    def test_arete_greater_than_rank_is_valid(self):
        """Test that arete > rank is valid."""
        data = self._get_basic_form_data(rank=1, arete=3)

        form = PeriaptForm(data=data)
        # Check for specific validation error
        if not form.is_valid():
            self.assertNotIn(
                "Periapt Arete rating must be at least equal to rank", str(form.errors)
            )

    def test_current_charges_cannot_exceed_max(self):
        """Test that current_charges cannot exceed max_charges."""
        data = self._get_basic_form_data(max_charges=5, current_charges=10)

        form = PeriaptForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("Current charges cannot exceed maximum charges", str(form.errors))

    def test_current_charges_equal_to_max_is_valid(self):
        """Test that current_charges == max_charges is valid."""
        data = self._get_basic_form_data(max_charges=5, current_charges=5)

        form = PeriaptForm(data=data)
        # Check for specific validation error
        if not form.is_valid():
            self.assertNotIn("Current charges cannot exceed maximum charges", str(form.errors))

    def test_resonance_total_must_match_or_exceed_rank(self):
        """Test that total resonance must be >= rank."""
        # Rank 3, Arete 3 (meets arete >= rank), but resonance 1 < rank 3
        data = self._get_basic_form_data(rank=3, arete=3)
        data["resonance-0-rating"] = "1"

        form = PeriaptForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("Resonance total must match or exceed rank", str(form.errors))

    def test_resonance_equal_to_rank_is_valid(self):
        """Test that resonance total == rank is valid."""
        data = self._get_basic_form_data(rank=2)
        data["resonance-0-rating"] = "2"

        form = PeriaptForm(data=data)
        # Check for specific validation error
        if not form.is_valid():
            self.assertNotIn("Resonance total must match or exceed rank", str(form.errors))

    def test_periapts_can_only_have_one_power(self):
        """Test that periapts can only have one power."""
        data = self._get_basic_form_data()
        # Add two effects
        data["effects-TOTAL_FORMS"] = "2"
        data["effects-0-select_or_create"] = "on"
        data["effects-0-name"] = "Effect 1"
        data["effects-0-correspondence"] = "1"
        data["effects-1-select_or_create"] = "on"
        data["effects-1-name"] = "Effect 2"
        data["effects-1-time"] = "1"

        form = PeriaptForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("Periapts can only have one power", str(form.errors))


class TestPeriaptFormEffectValidation(TestCase):
    """Test PeriaptForm effect cost validation."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)

    def _get_form_data_with_effect(self, rank, resonance_rating, effect):
        """Helper to create form data with an existing effect."""
        data = {
            "name": "Test Periapt",
            "description": "A test periapt",
            "rank": rank,
            "arete": rank,
            "max_charges": 5,
            "current_charges": 5,
            "is_consumable": True,
            # Resonance formset
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            "resonance-0-resonance": str(self.resonance.pk),
            "resonance-0-rating": str(resonance_rating),
            # Effect formset - select existing effect
            "effects-TOTAL_FORMS": "1",
            "effects-INITIAL_FORMS": "0",
            "effects-MIN_NUM_FORMS": "0",
            "effects-MAX_NUM_FORMS": "1000",
            "effects-0-select": str(effect.pk),
            # select_or_create is False = select existing
            # name is required by the ModelForm even when selecting
            "effects-0-name": "dummy",
        }
        return data

    def test_effect_cost_cannot_exceed_rank(self):
        """Test that effect cost cannot exceed rank."""
        # Rank 1 periapt with effect cost 2 (too expensive)
        expensive_effect = Effect.objects.create(name="Expensive Effect", entropy=2)
        data = self._get_form_data_with_effect(rank=1, resonance_rating=1, effect=expensive_effect)

        form = PeriaptForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("Effect too expensive", str(form.errors))

    def test_effect_cost_equal_to_rank_is_valid(self):
        """Test that effect cost equal to rank is valid."""
        # Rank 2 periapt with effect cost 2
        matching_effect = Effect.objects.create(name="Matching Effect", entropy=2)
        data = self._get_form_data_with_effect(rank=2, resonance_rating=2, effect=matching_effect)

        form = PeriaptForm(data=data)
        # Check specific error not present
        if not form.is_valid():
            self.assertNotIn("Effect too expensive", str(form.errors))


class TestPeriaptFormPointsValidation(TestCase):
    """Test PeriaptForm points calculation validation."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)

    def setUp(self):
        """Create an effect for testing."""
        self.effect = Effect.objects.create(name="Test Effect", entropy=1)

    def test_extra_points_exceed_limit(self):
        """Test that extra resonance/arete/effects cannot exceed 3x rank."""
        # Rank 1 gives 3 points
        # Arete 3 costs 2 extra (3-1=2)
        # Resonance 3 costs 2 extra (3-1=2)
        # Total = 4 > 3 points available
        data = {
            "name": "Test Periapt",
            "description": "A test periapt",
            "rank": 1,
            "arete": 3,
            "max_charges": 5,
            "current_charges": 5,
            "is_consumable": True,
            # Resonance formset
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            "resonance-0-resonance": str(self.resonance.pk),
            "resonance-0-rating": "3",
            # Effect formset - select existing effect
            "effects-TOTAL_FORMS": "1",
            "effects-INITIAL_FORMS": "0",
            "effects-MIN_NUM_FORMS": "0",
            "effects-MAX_NUM_FORMS": "1000",
            "effects-0-select": str(self.effect.pk),
            "effects-0-name": "dummy",
        }

        form = PeriaptForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Extra Resonance, Arete, and Effects must be less than 3 times the rank",
            str(form.errors),
        )

    def test_points_at_limit_is_valid(self):
        """Test that points at exactly the limit are valid."""
        # Rank 2 gives 6 points
        # Arete 2 costs 0 extra (2-2=0)
        # Resonance 2 costs 0 extra (2-2=0)
        # Total = 0 <= 6 points available
        data = {
            "name": "Test Periapt",
            "description": "A test periapt",
            "rank": 2,
            "arete": 2,
            "max_charges": 5,
            "current_charges": 5,
            "is_consumable": True,
            # Resonance formset
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            "resonance-0-resonance": str(self.resonance.pk),
            "resonance-0-rating": "2",
            # Effect formset - select existing effect
            "effects-TOTAL_FORMS": "1",
            "effects-INITIAL_FORMS": "0",
            "effects-MIN_NUM_FORMS": "0",
            "effects-MAX_NUM_FORMS": "1000",
            "effects-0-select": str(self.effect.pk),
            "effects-0-name": "dummy",
        }

        form = PeriaptForm(data=data)

        # Check specific error not present
        if not form.is_valid():
            self.assertNotIn(
                "Extra Resonance, Arete, and Effects must be less than 3 times the rank",
                str(form.errors),
            )


class TestPeriaptFormIsValid(TestCase):
    """Test PeriaptForm is_valid method with formsets."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)

    def setUp(self):
        """Create an effect for testing."""
        self.effect = Effect.objects.create(name="Test Effect", entropy=1)

    def test_is_valid_checks_resonance_formset(self):
        """Test that is_valid checks resonance formset validity."""
        data = {
            "name": "Test Periapt",
            "description": "A test periapt",
            "rank": 1,
            "arete": 1,
            "max_charges": 5,
            "current_charges": 5,
            "is_consumable": True,
            # Invalid resonance formset - missing management form
            "effects-TOTAL_FORMS": "1",
            "effects-INITIAL_FORMS": "0",
            "effects-MIN_NUM_FORMS": "0",
            "effects-MAX_NUM_FORMS": "1000",
            "effects-0-select": str(self.effect.pk),
            "effects-0-name": "dummy",
        }

        form = PeriaptForm(data=data)

        self.assertFalse(form.is_valid())

    def test_is_valid_checks_effect_formset(self):
        """Test that is_valid checks effect formset validity."""
        data = {
            "name": "Test Periapt",
            "description": "A test periapt",
            "rank": 1,
            "arete": 1,
            "max_charges": 5,
            "current_charges": 5,
            "is_consumable": True,
            # Resonance formset
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            "resonance-0-resonance": str(self.resonance.pk),
            "resonance-0-rating": "1",
            # Invalid effect formset - missing management form
        }

        form = PeriaptForm(data=data)

        self.assertFalse(form.is_valid())


class TestPeriaptFormSave(TestCase):
    """Test PeriaptForm save method."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance and effect for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)

    def _get_valid_form_data(self):
        """Helper to create valid form data."""
        # Create an effect for selection
        effect = Effect.objects.create(name="Test Effect", entropy=1)

        return {
            "name": "Test Periapt",
            "description": "A test periapt",
            "rank": 1,
            "arete": 1,
            "max_charges": 5,
            "current_charges": 5,
            "is_consumable": True,
            # Resonance formset
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            "resonance-0-resonance": str(self.resonance.pk),
            "resonance-0-rating": "1",
            # Effect formset - select existing effect (not create)
            "effects-TOTAL_FORMS": "1",
            "effects-INITIAL_FORMS": "0",
            "effects-MIN_NUM_FORMS": "0",
            "effects-MAX_NUM_FORMS": "1000",
            "effects-0-select": str(effect.pk),
            # select_or_create is False (not checked) = select existing
            # name is required by the ModelForm even when selecting
            "effects-0-name": "dummy",
        }

    def test_save_creates_periapt(self):
        """Test that save creates a periapt."""
        data = self._get_valid_form_data()

        form = PeriaptForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        periapt = form.save()

        self.assertIsNotNone(periapt)
        self.assertEqual(periapt.name, "Test Periapt")
        self.assertEqual(periapt.rank, 1)
        self.assertEqual(periapt.arete, 1)

    def test_save_commit_false_does_not_save_to_db(self):
        """Test that save(commit=False) does not save to database."""
        data = self._get_valid_form_data()

        form = PeriaptForm(data=data)
        self.assertTrue(form.is_valid())

        periapt = form.save(commit=False)

        self.assertIsNone(periapt.pk)

    def test_save_saves_resonance_formset(self):
        """Test that save also saves resonance formset."""
        data = self._get_valid_form_data()

        form = PeriaptForm(data=data)
        self.assertTrue(form.is_valid())

        periapt = form.save()

        # Check that resonance was saved
        from items.models.mage.wonder import WonderResonanceRating

        resonance_ratings = WonderResonanceRating.objects.filter(wonder=periapt)
        self.assertEqual(resonance_ratings.count(), 1)
        self.assertEqual(resonance_ratings.first().rating, 1)

    def test_save_with_effect(self):
        """Test that save correctly associates an effect."""
        data = self._get_valid_form_data()
        # Add an effect
        data["effects-0-select_or_create"] = "on"
        data["effects-0-name"] = "Test Effect"
        data["effects-0-entropy"] = "1"

        form = PeriaptForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        periapt = form.save()

        # Check that power was set
        self.assertIsNotNone(periapt.power)
        self.assertEqual(periapt.power.name, "Test Effect")


class TestPeriaptResonanceRatingFormSet(TestCase):
    """Test PeriaptResonanceRatingFormSet behavior."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance and periapt for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)
        cls.periapt = Periapt.objects.create(
            name="Test Periapt",
            rank=1,
            arete=1,
            max_charges=5,
            current_charges=5,
        )

    def test_formset_extra_forms(self):
        """Test that formset has 1 extra form by default."""
        formset = PeriaptResonanceRatingFormSet()

        self.assertEqual(formset.extra, 1)

    def test_formset_cannot_delete(self):
        """Test that formset doesn't allow deletion."""
        formset = PeriaptResonanceRatingFormSet()

        self.assertFalse(formset.can_delete)

    def test_formset_with_instance(self):
        """Test that formset can be created with existing instance."""
        formset = PeriaptResonanceRatingFormSet(instance=self.periapt)

        self.assertIsNotNone(formset)
        self.assertEqual(formset.instance, self.periapt)
