"""Tests for backgroundform module."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.core.backgroundform import (
    BackgroundRatingForm,
    BackgroundRatingFormSet,
)
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.human import Human
from characters.tests.utils import human_setup


class TestBackgroundRatingForm(TestCase):
    """Tests for BackgroundRatingForm."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(name="Test Human", owner=self.user)
        self.contacts = Background.objects.get(property_name="contacts")
        self.mentor = Background.objects.get(property_name="mentor")

    def test_form_has_required_fields(self):
        """Form includes bg, rating, note, display_alt_name, and pooled fields."""
        form = BackgroundRatingForm()
        self.assertIn("bg", form.fields)
        self.assertIn("rating", form.fields)
        self.assertIn("note", form.fields)
        self.assertIn("display_alt_name", form.fields)
        self.assertIn("pooled", form.fields)

    def test_form_bg_queryset_ordered_by_name(self):
        """Background queryset is ordered by name."""
        form = BackgroundRatingForm()
        queryset = form.fields["bg"].queryset
        names = list(queryset.values_list("name", flat=True))
        self.assertEqual(names, sorted(names))

    def test_form_rating_min_value(self):
        """Rating field has min_value of 0."""
        form = BackgroundRatingForm()
        self.assertEqual(form.fields["rating"].min_value, 0)

    def test_form_rating_max_value(self):
        """Rating field has max_value of 5."""
        form = BackgroundRatingForm()
        self.assertEqual(form.fields["rating"].max_value, 5)

    def test_form_rating_initial_value(self):
        """Rating field has initial value of 0."""
        form = BackgroundRatingForm()
        self.assertEqual(form.fields["rating"].initial, 0)

    def test_form_note_not_required(self):
        """Note field is not required."""
        form = BackgroundRatingForm()
        self.assertFalse(form.fields["note"].required)

    def test_form_display_alt_name_not_required(self):
        """Display alt name field is not required."""
        form = BackgroundRatingForm()
        self.assertFalse(form.fields["display_alt_name"].required)

    def test_form_pooled_not_required(self):
        """Pooled field is not required."""
        form = BackgroundRatingForm()
        self.assertFalse(form.fields["pooled"].required)

    def test_form_accepts_character_kwarg(self):
        """Form can be initialized with character kwarg."""
        form = BackgroundRatingForm(character=self.human)
        # Form should initialize without error
        self.assertIn("bg", form.fields)

    def test_form_valid_data(self):
        """Form validates with valid data."""
        data = {
            "bg": self.contacts.pk,
            "rating": 3,
            "note": "Test note",
            "display_alt_name": False,
            "pooled": False,
        }
        form = BackgroundRatingForm(data=data, character=self.human)
        self.assertTrue(form.is_valid())

    def test_form_invalid_rating_below_zero(self):
        """Form rejects rating below 0."""
        data = {
            "bg": self.contacts.pk,
            "rating": -1,
        }
        form = BackgroundRatingForm(data=data, character=self.human)
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_form_invalid_rating_above_five(self):
        """Form rejects rating above 5."""
        data = {
            "bg": self.contacts.pk,
            "rating": 6,
        }
        form = BackgroundRatingForm(data=data, character=self.human)
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_form_save_creates_background_rating(self):
        """Form save creates a BackgroundRating linked to the character."""
        data = {
            "bg": self.contacts.pk,
            "rating": 3,
            "note": "Test note",
            "display_alt_name": False,
            "pooled": False,
        }
        form = BackgroundRatingForm(data=data, character=self.human)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(instance.char, self.human)
        self.assertEqual(instance.bg, self.contacts)
        self.assertEqual(instance.rating, 3)
        self.assertEqual(instance.note, "Test note")

    def test_form_save_without_commit(self):
        """Form save with commit=False returns unsaved instance."""
        data = {
            "bg": self.contacts.pk,
            "rating": 2,
            "note": "",
            "display_alt_name": False,
            "pooled": False,
        }
        form = BackgroundRatingForm(data=data, character=self.human)
        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        self.assertEqual(instance.char, self.human)
        self.assertIsNone(instance.pk)  # Not saved yet


class TestBaseBackgroundRatingFormSet(TestCase):
    """Tests for BaseBackgroundRatingFormSet."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(name="Test Human", owner=self.user)
        self.contacts = Background.objects.get(property_name="contacts")
        self.mentor = Background.objects.get(property_name="mentor")

    def test_formset_accepts_character_kwarg(self):
        """Formset can be initialized with character kwarg."""
        formset = BackgroundRatingFormSet(instance=self.human, character=self.human)
        self.assertEqual(formset.character, self.human)

    def test_formset_get_form_kwargs_includes_character(self):
        """Formset passes character to individual forms."""
        formset = BackgroundRatingFormSet(instance=self.human, character=self.human)
        kwargs = formset.get_form_kwargs(0)
        self.assertEqual(kwargs["character"], self.human)

    def test_formset_add_fields_sets_bg_queryset(self):
        """Formset add_fields sets bg queryset ordered by name."""
        formset = BackgroundRatingFormSet(instance=self.human, character=self.human)
        for form in formset.forms:
            queryset = form.fields["bg"].queryset
            names = list(queryset.values_list("name", flat=True))
            self.assertEqual(names, sorted(names))


class TestBackgroundRatingFormSetFactory(TestCase):
    """Tests for BackgroundRatingFormSet factory."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(name="Test Human", owner=self.user)
        self.contacts = Background.objects.get(property_name="contacts")
        self.mentor = Background.objects.get(property_name="mentor")

    def test_formset_has_one_extra_form(self):
        """Formset has extra=1."""
        formset = BackgroundRatingFormSet(instance=self.human, character=self.human)
        # Should have at least one empty form
        self.assertGreaterEqual(len(formset.forms), 1)

    def test_formset_cannot_delete(self):
        """Formset has can_delete=False."""
        formset = BackgroundRatingFormSet(instance=self.human, character=self.human)
        # Check that delete field is not present
        for form in formset.forms:
            self.assertNotIn("DELETE", form.fields)

    def test_formset_save_with_valid_data(self):
        """Formset saves valid background ratings."""
        data = {
            "backgrounds-TOTAL_FORMS": "2",
            "backgrounds-INITIAL_FORMS": "0",
            "backgrounds-MIN_NUM_FORMS": "0",
            "backgrounds-MAX_NUM_FORMS": "1000",
            "backgrounds-0-bg": self.contacts.pk,
            "backgrounds-0-rating": 3,
            "backgrounds-0-note": "My contacts",
            "backgrounds-0-display_alt_name": "",
            "backgrounds-0-pooled": "",
            "backgrounds-1-bg": self.mentor.pk,
            "backgrounds-1-rating": 2,
            "backgrounds-1-note": "My mentor",
            "backgrounds-1-display_alt_name": "",
            "backgrounds-1-pooled": "",
        }
        formset = BackgroundRatingFormSet(data=data, instance=self.human, character=self.human)
        self.assertTrue(formset.is_valid(), formset.errors)
        formset.save()
        self.assertEqual(BackgroundRating.objects.filter(char=self.human).count(), 2)

    def test_formset_skips_empty_ratings(self):
        """Formset doesn't save entries with no rating or bg."""
        data = {
            "backgrounds-TOTAL_FORMS": "2",
            "backgrounds-INITIAL_FORMS": "0",
            "backgrounds-MIN_NUM_FORMS": "0",
            "backgrounds-MAX_NUM_FORMS": "1000",
            "backgrounds-0-bg": self.contacts.pk,
            "backgrounds-0-rating": 3,
            "backgrounds-0-note": "",
            "backgrounds-0-display_alt_name": "",
            "backgrounds-0-pooled": "",
            "backgrounds-1-bg": "",
            "backgrounds-1-rating": 0,
            "backgrounds-1-note": "",
            "backgrounds-1-display_alt_name": "",
            "backgrounds-1-pooled": "",
        }
        formset = BackgroundRatingFormSet(data=data, instance=self.human, character=self.human)
        self.assertTrue(formset.is_valid())
        formset.save()
        # Only the first form with valid data should be saved
        self.assertEqual(BackgroundRating.objects.filter(char=self.human).count(), 1)

    def test_formset_with_existing_background_ratings(self):
        """Formset properly handles existing background ratings."""
        # Create an existing background rating
        existing = BackgroundRating.objects.create(
            char=self.human, bg=self.contacts, rating=2, note="Existing"
        )
        formset = BackgroundRatingFormSet(instance=self.human, character=self.human)
        # Should have the existing form plus extra
        self.assertGreaterEqual(len(formset.forms), 1)
        # First form should have existing data
        initial_data = formset.forms[0].initial
        self.assertEqual(initial_data.get("bg"), self.contacts.pk)


class TestBackgroundRatingFormIntegration(TestCase):
    """Integration tests for background rating forms."""

    def setUp(self):
        human_setup()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.human = Human.objects.create(name="Test Human", owner=self.user)
        self.contacts = Background.objects.get(property_name="contacts")
        self.mentor = Background.objects.get(property_name="mentor")

    def test_form_creates_rating_that_can_be_queried(self):
        """Created ratings are properly queryable through the character."""
        data = {
            "bg": self.contacts.pk,
            "rating": 3,
            "note": "Integration test",
            "display_alt_name": False,
            "pooled": False,
        }
        form = BackgroundRatingForm(data=data, character=self.human)
        form.is_valid()
        form.save()

        # Query through the character's backgrounds relation
        ratings = self.human.backgrounds.filter(bg=self.contacts)
        self.assertEqual(ratings.count(), 1)
        self.assertEqual(ratings.first().rating, 3)

    def test_multiple_backgrounds_same_type(self):
        """Multiple background ratings of same type are allowed."""
        for i in range(3):
            data = {
                "bg": self.contacts.pk,
                "rating": i + 1,
                "note": f"Contact group {i + 1}",
                "display_alt_name": False,
                "pooled": False,
            }
            form = BackgroundRatingForm(data=data, character=self.human)
            form.is_valid()
            form.save()

        ratings = self.human.backgrounds.filter(bg=self.contacts)
        self.assertEqual(ratings.count(), 3)
