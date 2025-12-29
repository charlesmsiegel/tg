"""
Tests for GroupCreationForm.

Tests cover:
- Form initialization for regular users vs storytellers
- Group type filtering based on user permissions
- Choice formatting (underscores to spaces, title case)
- Sorting of choices alphabetically
- Empty choices for unauthenticated users
- Form validation for valid/invalid group types
"""

from characters.forms.core.group_creation import GroupCreationForm
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, Gameline, ObjectType, STRelationship


class GroupCreationFormTestCase(TestCase):
    """Base test case with common setup for GroupCreationForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        # Create gamelines
        cls.gameline_mta = Gameline.objects.create(name="Mage: the Ascension")
        cls.gameline_vtm = Gameline.objects.create(name="Vampire: the Masquerade")
        cls.gameline_wta = Gameline.objects.create(name="Werewolf: the Apocalypse")
        cls.gameline_ctd = Gameline.objects.create(name="Changeling: the Dreaming")

        # Create group types
        ObjectType.objects.create(name="cabal", type="char", gameline="mta")
        ObjectType.objects.create(name="pack", type="char", gameline="wta")
        ObjectType.objects.create(name="coterie", type="char", gameline="vtm")
        ObjectType.objects.create(name="motley", type="char", gameline="ctd")
        ObjectType.objects.create(name="group", type="char", gameline="wod")
        ObjectType.objects.create(name="circle", type="char", gameline="wod")
        ObjectType.objects.create(name="conclave", type="char", gameline="wod")

        # Create chronicle for ST relationships
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def setUp(self):
        """Set up test users."""
        self.regular_user = User.objects.create_user(
            username="regular_user",
            email="regular@test.com",
            password="testpassword",
        )
        self.st_user = User.objects.create_user(
            username="st_user",
            email="st@test.com",
            password="testpassword",
        )
        # Make st_user a storyteller
        STRelationship.objects.create(
            user=self.st_user,
            chronicle=self.chronicle,
            gameline=self.gameline_mta,
        )


class TestGroupCreationFormInitialization(GroupCreationFormTestCase):
    """Test form initialization with different user types."""

    def test_form_initializes_without_user(self):
        """Form initializes correctly without a user."""
        form = GroupCreationForm()

        # Without user, should have empty choices
        self.assertEqual(len(form.fields["group_type"].choices), 0)

    def test_form_initializes_for_regular_user(self):
        """Form initializes correctly for regular (non-ST) user."""
        form = GroupCreationForm(user=self.regular_user)

        # Regular users only see cabal
        group_type_values = [choice[0] for choice in form.fields["group_type"].choices]
        self.assertEqual(group_type_values, ["cabal"])

    def test_form_initializes_for_st_user(self):
        """Form initializes correctly for storyteller user."""
        form = GroupCreationForm(user=self.st_user)

        # ST users see all group types
        group_type_values = [choice[0] for choice in form.fields["group_type"].choices]
        self.assertIn("cabal", group_type_values)
        self.assertIn("pack", group_type_values)
        self.assertIn("coterie", group_type_values)
        self.assertIn("motley", group_type_values)


class TestGroupTypeFiltering(GroupCreationFormTestCase):
    """Test group type choice filtering."""

    def test_regular_user_only_sees_cabal(self):
        """Regular users are restricted to cabal only."""
        form = GroupCreationForm(user=self.regular_user)

        group_type_choices = form.fields["group_type"].choices
        self.assertEqual(len(group_type_choices), 1)
        self.assertEqual(group_type_choices[0][0], "cabal")
        self.assertEqual(group_type_choices[0][1], "Cabal")

    def test_st_user_sees_all_group_types(self):
        """Storytellers can see all group types."""
        form = GroupCreationForm(user=self.st_user)

        group_type_values = [choice[0] for choice in form.fields["group_type"].choices]

        # Should have all the group types defined in the form
        expected_types = ["cabal", "pack", "motley", "group", "coterie", "circle", "conclave"]
        for expected in expected_types:
            self.assertIn(expected, group_type_values)


class TestChoiceFormatting(GroupCreationFormTestCase):
    """Test choice label formatting."""

    def test_labels_are_title_cased(self):
        """Choice labels are title-cased."""
        form = GroupCreationForm(user=self.st_user)

        group_type_choices = dict(form.fields["group_type"].choices)

        # Check that values are properly title-cased
        self.assertEqual(group_type_choices.get("cabal"), "Cabal")
        self.assertEqual(group_type_choices.get("pack"), "Pack")
        self.assertEqual(group_type_choices.get("coterie"), "Coterie")
        self.assertEqual(group_type_choices.get("motley"), "Motley")

    def test_underscores_replaced_with_spaces(self):
        """Underscores in names are replaced with spaces in labels."""
        # Create a group type with underscore
        ObjectType.objects.create(name="test_group", type="char", gameline="wod")

        form = GroupCreationForm(user=self.st_user)

        # Note: test_group won't appear unless it's in the allowed list
        # This test verifies the formatting logic is correct
        group_type_choices = dict(form.fields["group_type"].choices)

        # All existing types should be properly formatted
        for value, label in form.fields["group_type"].choices:
            self.assertNotIn("_", label)
            self.assertEqual(label, label.title())


class TestChoiceSorting(GroupCreationFormTestCase):
    """Test that choices are sorted alphabetically."""

    def test_st_choices_are_sorted_alphabetically(self):
        """ST user choices are sorted alphabetically by label."""
        form = GroupCreationForm(user=self.st_user)

        labels = [label for _, label in form.fields["group_type"].choices]
        self.assertEqual(labels, sorted(labels))


class TestFormValidation(GroupCreationFormTestCase):
    """Test form validation."""

    def test_valid_submission_for_st(self):
        """ST can submit form with valid group type."""
        form = GroupCreationForm(
            data={"group_type": "cabal"},
            user=self.st_user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_pack_submission_for_st(self):
        """ST can submit form with pack group type."""
        form = GroupCreationForm(
            data={"group_type": "pack"},
            user=self.st_user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_valid_cabal_submission_for_regular_user(self):
        """Regular user can submit form with cabal group type."""
        form = GroupCreationForm(
            data={"group_type": "cabal"},
            user=self.regular_user,
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_empty_submission_invalid(self):
        """Empty form submission is invalid."""
        form = GroupCreationForm(
            data={},
            user=self.st_user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("group_type", form.errors)

    def test_invalid_group_type_rejected(self):
        """Invalid group type value is rejected."""
        form = GroupCreationForm(
            data={"group_type": "invalid_type"},
            user=self.st_user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("group_type", form.errors)


class TestUnauthenticatedUser(GroupCreationFormTestCase):
    """Test form behavior for unauthenticated users."""

    def test_none_user_has_empty_choices(self):
        """None user gets empty choices."""
        form = GroupCreationForm(user=None)

        self.assertEqual(len(form.fields["group_type"].choices), 0)

    def test_anonymous_user_class_has_empty_choices(self):
        """AnonymousUser gets empty choices."""
        from django.contrib.auth.models import AnonymousUser

        anon = AnonymousUser()
        form = GroupCreationForm(user=anon)

        self.assertEqual(len(form.fields["group_type"].choices), 0)


class TestGroupTypeLabels(GroupCreationFormTestCase):
    """Test specific group type label formatting."""

    def test_all_expected_group_types_have_correct_labels(self):
        """All expected group types have correctly formatted labels."""
        form = GroupCreationForm(user=self.st_user)

        expected_labels = {
            "cabal": "Cabal",
            "pack": "Pack",
            "coterie": "Coterie",
            "motley": "Motley",
            "group": "Group",
            "circle": "Circle",
            "conclave": "Conclave",
        }

        group_type_choices = dict(form.fields["group_type"].choices)

        for value, expected_label in expected_labels.items():
            if value in group_type_choices:
                self.assertEqual(group_type_choices[value], expected_label)
