"""Tests for NodeForm forms."""

from characters.models.mage.focus import Practice
from characters.models.mage.resonance import Resonance
from django.test import TestCase
from locations.forms.mage.node import NodeForm, NodeResonanceRatingForm


class TestNodeResonanceRatingForm(TestCase):
    """Test NodeResonanceRatingForm validation."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = NodeResonanceRatingForm()

        self.assertIn("resonance", form.fields)
        self.assertIn("rating", form.fields)

    def test_rating_min_value(self):
        """Test that rating has minimum value of 0."""
        form = NodeResonanceRatingForm()

        self.assertEqual(form.fields["rating"].min_value, 0)

    def test_rating_max_value(self):
        """Test that rating has maximum value of 5."""
        form = NodeResonanceRatingForm()

        self.assertEqual(form.fields["rating"].max_value, 5)

    def test_rating_initial_value(self):
        """Test that rating has initial value of 0."""
        form = NodeResonanceRatingForm()

        self.assertEqual(form.fields["rating"].initial, 0)

    def test_resonance_is_optional(self):
        """Test that resonance field is optional."""
        form = NodeResonanceRatingForm()

        self.assertFalse(form.fields["resonance"].required)


class TestNodeFormBasics(TestCase):
    """Test basic NodeForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = NodeForm()

        self.assertIn("name", form.fields)
        self.assertIn("rank", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("ratio", form.fields)
        self.assertIn("size", form.fields)
        self.assertIn("quintessence_form", form.fields)
        self.assertIn("tass_form", form.fields)
        self.assertIn("contained_within", form.fields)
        self.assertIn("gauntlet", form.fields)
        self.assertIn("shroud", form.fields)
        self.assertIn("dimension_barrier", form.fields)

    def test_form_has_resonance_formset(self):
        """Test that form has a resonance formset."""
        form = NodeForm()

        self.assertTrue(hasattr(form, "resonance_formset"))

    def test_form_has_merit_flaw_formset(self):
        """Test that form has a merit/flaw formset."""
        form = NodeForm()

        self.assertTrue(hasattr(form, "merit_flaw_formset"))

    def test_form_has_reality_zone_formset(self):
        """Test that form has a reality zone formset."""
        form = NodeForm()

        self.assertTrue(hasattr(form, "reality_zone_formset"))

    def test_name_placeholder(self):
        """Test that name field has correct placeholder."""
        form = NodeForm()

        self.assertEqual(form.fields["name"].widget.attrs.get("placeholder"), "Enter name here")

    def test_description_placeholder(self):
        """Test that description field has correct placeholder."""
        form = NodeForm()

        self.assertEqual(
            form.fields["description"].widget.attrs.get("placeholder"),
            "Enter description here",
        )


class TestNodeFormValidation(TestCase):
    """Test NodeForm validation rules."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance and practices for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)
        cls.practice1 = Practice.objects.create(name="High Ritual Magick")
        cls.practice2 = Practice.objects.create(name="Chaos Magick")

    def _get_basic_form_data(self, rank=1, **overrides):
        """Helper to create basic valid form data."""
        data = {
            "name": "Test Node",
            "description": "A test node",
            "rank": rank,
            "ratio": 0,
            "size": 0,
            "quintessence_form": "Golden light",
            "tass_form": "Crystals",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            # Resonance formset - management form
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            # Resonance form
            "resonance-0-resonance": "Dynamic",
            "resonance-0-rating": str(rank),
            # Merit/Flaw formset - management form
            "merit_flaw-TOTAL_FORMS": "0",
            "merit_flaw-INITIAL_FORMS": "0",
            "merit_flaw-MIN_NUM_FORMS": "0",
            "merit_flaw-MAX_NUM_FORMS": "1000",
            # Reality Zone formset - with practices and ratings that sum to 0
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": str(rank),
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": str(-rank),
        }
        data.update(overrides)
        return data

    def test_rank_cannot_be_none(self):
        """Test that rank is required."""
        data = self._get_basic_form_data()
        del data["rank"]

        form = NodeForm(data=data)

        self.assertFalse(form.is_valid())

    def test_resonance_total_must_match_or_exceed_rank(self):
        """Test that total resonance must be >= rank."""
        data = self._get_basic_form_data(rank=3)
        data["resonance-0-rating"] = "1"

        form = NodeForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("Resonance total must match or exceed rank", str(form.errors))


class TestNodeFormSave(TestCase):
    """Test NodeForm save method."""

    @classmethod
    def setUpTestData(cls):
        """Create resonance and practices for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)
        cls.practice1 = Practice.objects.create(name="High Ritual Magick")
        cls.practice2 = Practice.objects.create(name="Chaos Magick")

    def _get_valid_form_data(self, rank=1):
        """Helper to create valid form data."""
        return {
            "name": "Test Node",
            "description": "A test node",
            "rank": rank,
            "ratio": 0,
            "size": 0,
            "quintessence_form": "Golden light",
            "tass_form": "Crystals",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            # Resonance formset - management form
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            # Resonance form
            "resonance-0-resonance": "Dynamic",
            "resonance-0-rating": str(rank),
            # Merit/Flaw formset - management form
            "merit_flaw-TOTAL_FORMS": "0",
            "merit_flaw-INITIAL_FORMS": "0",
            "merit_flaw-MIN_NUM_FORMS": "0",
            "merit_flaw-MAX_NUM_FORMS": "1000",
            # Reality Zone formset - with practices and ratings that sum to 0
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": str(rank),
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": str(-rank),
        }

    def test_save_without_validation_does_not_raise_attribute_error(self):
        """Test that save() without clean() does not raise AttributeError.

        This test verifies the fix for issue #1054: the save() method was using
        self.tass_per_week and self.quintessence_per_week which are only set
        during clean(). If save() is called without clean(), this would raise
        an AttributeError.
        """
        form = NodeForm(data=self._get_valid_form_data())
        # Do NOT call is_valid() - this simulates calling save without validation
        # The form should handle this gracefully

        # This should not raise an AttributeError
        try:
            node = form.save(commit=False)
            # If we get here, attributes were calculated properly
            self.assertIsNotNone(node)
        except AttributeError as e:
            if "tass_per_week" in str(e) or "quintessence_per_week" in str(e):
                self.fail(
                    "save() raised AttributeError for undefined attributes - "
                    "clean() was not called first"
                )
            raise

    def test_save_creates_node_after_validation(self):
        """Test that save creates a node after proper validation."""
        data = self._get_valid_form_data()

        form = NodeForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        node = form.save()

        self.assertIsNotNone(node)
        self.assertEqual(node.name, "Test Node")
        self.assertEqual(node.rank, 1)

    def test_save_commit_false_does_not_save_to_db(self):
        """Test that save(commit=False) does not save to database."""
        data = self._get_valid_form_data()

        form = NodeForm(data=data)
        self.assertTrue(form.is_valid())

        node = form.save(commit=False)

        self.assertIsNone(node.pk)

    def test_save_calculates_tass_and_quintessence(self):
        """Test that save correctly calculates tass and quintessence per week."""
        data = self._get_valid_form_data(rank=2)
        # Update resonance to match rank
        data["resonance-0-rating"] = "2"
        # Update reality zone to match rank (positive must sum to rank)
        data["reality_zone-0-rating"] = "2"
        data["reality_zone-1-rating"] = "-2"

        form = NodeForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        node = form.save()

        # With rank 2, ratio 0 (50%), size 0, and no merits/flaws:
        # points_remaining = 3*2 - (2-2) - 0 - 0 - 0 = 6
        # With ratio=0 -> 0.5, quintessence = int(6 * 0.5) = 3
        # tass = 6 - 3 = 3
        self.assertEqual(node.quintessence_per_week, 3)
        self.assertEqual(node.tass_per_week, 3)

    def test_save_saves_resonance_formset(self):
        """Test that save also saves resonance formset."""
        data = self._get_valid_form_data()

        form = NodeForm(data=data)
        self.assertTrue(form.is_valid())

        node = form.save()

        # Check that resonance was saved
        from locations.models.mage.node import NodeResonanceRating

        resonance_ratings = NodeResonanceRating.objects.filter(node=node)
        self.assertEqual(resonance_ratings.count(), 1)
        self.assertEqual(resonance_ratings.first().rating, 1)


class TestNodeFormIsValid(TestCase):
    """Test NodeForm is_valid method with formsets."""

    def test_is_valid_checks_resonance_formset(self):
        """Test that is_valid checks resonance formset validity."""
        data = {
            "name": "Test Node",
            "description": "A test node",
            "rank": 1,
            "ratio": 0,
            "size": 0,
            "quintessence_form": "Golden light",
            "tass_form": "Crystals",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            # Missing resonance management form - invalid
            # Merit/Flaw formset - management form
            "merit_flaw-TOTAL_FORMS": "0",
            "merit_flaw-INITIAL_FORMS": "0",
            "merit_flaw-MIN_NUM_FORMS": "0",
            "merit_flaw-MAX_NUM_FORMS": "1000",
            # Reality Zone formset - management form
            "reality_zone-TOTAL_FORMS": "0",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
        }

        form = NodeForm(data=data)

        self.assertFalse(form.is_valid())


class TestNodeFormFormsetErrorPropagation(TestCase):
    """Test that formset errors are properly propagated to form errors.

    Issue #1067: When nested formsets have validation errors, those errors
    should be clearly communicated to the user through the parent form's
    error system.
    """

    @classmethod
    def setUpTestData(cls):
        """Create resonance and practices for testing."""
        cls.resonance = Resonance.objects.create(name="Dynamic", entropy=True)
        cls.practice1 = Practice.objects.create(name="High Ritual Magick")
        cls.practice2 = Practice.objects.create(name="Chaos Magick")

    def _get_valid_form_data(self, rank=1):
        """Helper to create valid form data."""
        return {
            "name": "Test Node",
            "description": "A test node",
            "rank": rank,
            "ratio": 0,
            "size": 0,
            "quintessence_form": "Golden light",
            "tass_form": "Crystals",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            # Resonance formset - management form
            "resonance-TOTAL_FORMS": "1",
            "resonance-INITIAL_FORMS": "0",
            "resonance-MIN_NUM_FORMS": "0",
            "resonance-MAX_NUM_FORMS": "1000",
            # Resonance form
            "resonance-0-resonance": "Dynamic",
            "resonance-0-rating": str(rank),
            # Merit/Flaw formset - management form
            "merit_flaw-TOTAL_FORMS": "0",
            "merit_flaw-INITIAL_FORMS": "0",
            "merit_flaw-MIN_NUM_FORMS": "0",
            "merit_flaw-MAX_NUM_FORMS": "1000",
            # Reality Zone formset - with practices and ratings that sum to 0
            "reality_zone-TOTAL_FORMS": "2",
            "reality_zone-INITIAL_FORMS": "0",
            "reality_zone-MIN_NUM_FORMS": "0",
            "reality_zone-MAX_NUM_FORMS": "1000",
            "reality_zone-0-practice": str(self.practice1.pk),
            "reality_zone-0-rating": str(rank),
            "reality_zone-1-practice": str(self.practice2.pk),
            "reality_zone-1-rating": str(-rank),
        }

    def test_invalid_resonance_formset_propagates_error(self):
        """Test that invalid resonance formset adds an error to the form.

        When the resonance formset is invalid, the form should have a
        clear error message about resonance errors.
        """
        data = self._get_valid_form_data()
        # Make resonance formset invalid with bad rating
        data["resonance-0-rating"] = "999"  # Invalid: max is 5

        form = NodeForm(data=data)

        self.assertFalse(form.is_valid())
        # Check that there's an error message about resonance
        all_errors = str(form.errors) + str(form.non_field_errors())
        self.assertTrue(
            "resonance" in all_errors.lower(),
            f"Expected resonance error in form.errors, got: {form.errors}, non_field_errors: {form.non_field_errors()}",
        )

    def test_invalid_reality_zone_formset_propagates_error(self):
        """Test that invalid reality zone formset adds an error to the form.

        When the reality zone formset is invalid, the form should have a
        clear error message about reality zone errors.
        """
        data = self._get_valid_form_data()
        # Make reality zone formset invalid by removing management form
        del data["reality_zone-TOTAL_FORMS"]

        form = NodeForm(data=data)

        self.assertFalse(form.is_valid())
        # Check that there's an error message about reality zone
        all_errors = str(form.errors) + str(form.non_field_errors())
        self.assertTrue(
            "reality" in all_errors.lower() or "zone" in all_errors.lower(),
            f"Expected reality zone error in form.errors, got: {form.errors}, non_field_errors: {form.non_field_errors()}",
        )
