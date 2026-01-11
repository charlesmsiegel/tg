"""Tests for Changeling forms."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.changeling.changeling import ChangelingCreationForm
from characters.models.changeling.changeling import Changeling
from characters.models.changeling.house import House
from characters.models.changeling.kith import Kith
from characters.models.changeling.legacy import Legacy
from game.models import Chronicle


class TestChangelingCreationForm(TestCase):
    """Tests for ChangelingCreationForm."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Create test data for form fields
        self.seelie_legacy = Legacy.objects.create(name="Seelie Legacy", court="seelie")
        self.unseelie_legacy = Legacy.objects.create(name="Unseelie Legacy", court="unseelie")
        self.kith = Kith.objects.create(name="Test Kith")
        self.house = House.objects.create(name="Test House", court="seelie")

    def test_form_with_valid_data(self):
        """Test form with valid data."""
        form_data = {
            "name": "Test Changeling",
            "concept": "A wandering dreamer",
            "court": "seelie",
            "seeming": "wilder",
        }
        form = ChangelingCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_requires_name(self):
        """Test that form requires name."""
        form_data = {
            "concept": "A wandering dreamer",
            "court": "seelie",
        }
        form = ChangelingCreationForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_form_sets_owner_on_save(self):
        """Test that form sets owner when saved."""
        form_data = {
            "name": "Test Changeling",
        }
        form = ChangelingCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        changeling = form.save()
        self.assertEqual(changeling.owner, self.user)

    def test_form_saves_without_user(self):
        """Test that form can save when user is None."""
        form_data = {
            "name": "Test Changeling",
        }
        form = ChangelingCreationForm(data=form_data, user=None)
        self.assertTrue(form.is_valid(), form.errors)
        changeling = form.save()
        self.assertIsNone(changeling.owner)

    def test_seelie_legacy_queryset_filters_by_court(self):
        """Test that seelie_legacy field only shows seelie legacies."""
        form = ChangelingCreationForm(user=self.user)
        seelie_legacies = form.fields["seelie_legacy"].queryset
        for legacy in seelie_legacies:
            self.assertEqual(legacy.court, "seelie")

    def test_unseelie_legacy_queryset_filters_by_court(self):
        """Test that unseelie_legacy field only shows unseelie legacies."""
        form = ChangelingCreationForm(user=self.user)
        unseelie_legacies = form.fields["unseelie_legacy"].queryset
        for legacy in unseelie_legacies:
            self.assertEqual(legacy.court, "unseelie")

    def test_form_has_placeholder_for_name(self):
        """Test that name field has placeholder."""
        form = ChangelingCreationForm(user=self.user)
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Enter name here",
        )

    def test_form_has_placeholder_for_concept(self):
        """Test that concept field has placeholder."""
        form = ChangelingCreationForm(user=self.user)
        self.assertEqual(
            form.fields["concept"].widget.attrs.get("placeholder"),
            "Enter concept here",
        )

    def test_image_field_not_required(self):
        """Test that image field is not required."""
        form = ChangelingCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)

    def test_form_with_all_fields(self):
        """Test form with all fields filled."""
        form_data = {
            "name": "Full Changeling",
            "concept": "A complete character",
            "chronicle": self.chronicle.pk,
            "court": "seelie",
            "seelie_legacy": self.seelie_legacy.pk,
            "unseelie_legacy": self.unseelie_legacy.pk,
            "house": self.house.pk,
            "seeming": "grump",
            "kith": self.kith.pk,
            "npc": False,
        }
        form = ChangelingCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        changeling = form.save()
        self.assertEqual(changeling.name, "Full Changeling")
        self.assertEqual(changeling.concept, "A complete character")
        self.assertEqual(changeling.court, "seelie")
        self.assertEqual(changeling.seeming, "grump")
        self.assertEqual(changeling.kith, self.kith)
        self.assertEqual(changeling.house, self.house)

    def test_form_with_unseelie_court(self):
        """Test form with unseelie court."""
        unseelie_house = House.objects.create(name="Unseelie House", court="unseelie")
        form_data = {
            "name": "Unseelie Changeling",
            "court": "unseelie",
            "house": unseelie_house.pk,
        }
        form = ChangelingCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        changeling = form.save()
        self.assertEqual(changeling.court, "unseelie")
        self.assertEqual(changeling.house, unseelie_house)

    def test_form_model_is_changeling(self):
        """Test that form's model is Changeling."""
        form = ChangelingCreationForm(user=self.user)
        self.assertEqual(form.Meta.model, Changeling)

    def test_form_includes_expected_fields(self):
        """Test that form includes all expected fields."""
        expected_fields = [
            "name",
            "concept",
            "chronicle",
            "image",
            "court",
            "seelie_legacy",
            "unseelie_legacy",
            "house",
            "seeming",
            "kith",
            "npc",
        ]
        form = ChangelingCreationForm(user=self.user)
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_form_commit_false(self):
        """Test form save with commit=False."""
        form_data = {
            "name": "Uncommitted Changeling",
        }
        form = ChangelingCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        changeling = form.save(commit=False)
        self.assertIsNone(changeling.pk)  # Not saved to database yet
        self.assertEqual(changeling.owner, self.user)
        self.assertEqual(changeling.name, "Uncommitted Changeling")

    def test_form_with_all_seemings(self):
        """Test form with each seeming option."""
        for seeming in ["childling", "wilder", "grump"]:
            form_data = {
                "name": f"{seeming.title()} Changeling",
                "seeming": seeming,
            }
            form = ChangelingCreationForm(data=form_data, user=self.user)
            self.assertTrue(form.is_valid(), form.errors)
            changeling = form.save()
            self.assertEqual(changeling.seeming, seeming)

    def test_form_with_npc_true(self):
        """Test form with NPC flag set to true."""
        form_data = {
            "name": "NPC Changeling",
            "npc": True,
        }
        form = ChangelingCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        changeling = form.save()
        self.assertTrue(changeling.npc)

    def test_form_with_empty_optional_fields(self):
        """Test form with empty optional fields."""
        form_data = {
            "name": "Minimal Changeling",
            "concept": "",
            "court": "",
            "seeming": "",
        }
        form = ChangelingCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        changeling = form.save()
        self.assertEqual(changeling.name, "Minimal Changeling")
        self.assertEqual(changeling.concept, "")
        self.assertEqual(changeling.court, "")
        self.assertEqual(changeling.seeming, "")
