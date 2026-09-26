"""
Tests for Chantry forms.

Tests cover:
- ChantryPointForm: Adding backgrounds and integrated effects
- ChantryEffectsForm: Selecting integrated effects for chantry
- ChantryCreateForm: Creating new chantries
- ChantrySelectOrCreateForm: Selecting existing or creating new chantry
"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.mage.effect import Effect
from characters.models.mage.mage import Mage
from characters.tests.utils import mage_setup
from game.models import Chronicle
from locations.forms.mage.chantry import (
    ChantryCreateForm,
    ChantryEffectsForm,
    ChantryPointForm,
    ChantrySelectOrCreateForm,
)
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating


class TestChantryPointFormSetup(TestCase):
    """Shared setup for ChantryPointForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantryPointForm tests."""
        mage_setup()
        cls.chantry = Chantry.objects.create(name="Test Chantry", total_points=20)
        cls.background = Background.objects.get(property_name="allies")


class TestChantryPointFormBasics(TestChantryPointFormSetup):
    """Test basic ChantryPointForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = ChantryPointForm(pk=self.chantry.pk)

        self.assertIn("category", form.fields)
        self.assertIn("example", form.fields)
        self.assertIn("note", form.fields)
        self.assertIn("display_alt_name", form.fields)

    def test_category_choices_include_integrated_effects(self):
        """Test that category includes Integrated Effects option."""
        form = ChantryPointForm(pk=self.chantry.pk)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Integrated Effects", category_values)
        self.assertIn("New Background", category_values)

    def test_category_excludes_existing_background_when_no_backgrounds(self):
        """Test that Existing Background is excluded when chantry has no backgrounds."""
        form = ChantryPointForm(pk=self.chantry.pk)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Existing Background", category_values)

    def test_category_includes_existing_background_when_has_backgrounds(self):
        """Test that Existing Background is included when chantry has backgrounds."""
        ChantryBackgroundRating.objects.create(bg=self.background, chantry=self.chantry, rating=1)
        form = ChantryPointForm(pk=self.chantry.pk)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertIn("Existing Background", category_values)

    def test_integrated_effects_excluded_at_max(self):
        """Test that Integrated Effects is excluded when score is at 10."""
        self.chantry.integrated_effects_score = 10
        self.chantry.save()

        form = ChantryPointForm(pk=self.chantry.pk)

        category_values = [choice[0] for choice in form.fields["category"].choices]

        self.assertNotIn("Integrated Effects", category_values)


class TestChantryPointFormValidation(TestChantryPointFormSetup):
    """Test ChantryPointForm validation logic."""

    def test_clean_requires_example_for_new_background(self):
        """Test that New Background requires an example to be selected."""
        form_data = {
            "category": "New Background",
            "example": "",
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)

        self.assertFalse(form.is_valid())

    def test_clean_requires_example_for_existing_background(self):
        """Test that Existing Background requires an example to be selected."""
        ChantryBackgroundRating.objects.create(bg=self.background, chantry=self.chantry, rating=1)

        form_data = {
            "category": "Existing Background",
            "example": "",
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)

        self.assertFalse(form.is_valid())

    def test_valid_integrated_effects_selection(self):
        """Test that Integrated Effects selection is valid."""
        form_data = {
            "category": "Integrated Effects",
            "example": "",
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)

        self.assertTrue(form.is_valid())


class TestChantryPointFormSave(TestChantryPointFormSetup):
    """Test ChantryPointForm save logic."""

    def test_save_integrated_effects_increases_score(self):
        """Test that saving Integrated Effects increases the score."""
        initial_score = self.chantry.integrated_effects_score

        form_data = {
            "category": "Integrated Effects",
            "example": "",
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)
        self.assertTrue(form.is_valid())
        form.save()

        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.integrated_effects_score, initial_score + 1)

    def test_save_new_background_creates_rating(self):
        """Test that saving New Background creates a ChantryBackgroundRating."""
        initial_count = ChantryBackgroundRating.objects.count()

        form_data = {
            "category": "New Background",
            "example": str(self.background.pk),
            "note": "Test Note",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(ChantryBackgroundRating.objects.count(), initial_count + 1)

    def test_save_existing_background_increases_rating(self):
        """Test that saving Existing Background increases the rating."""
        bg_rating = ChantryBackgroundRating.objects.create(
            bg=self.background, chantry=self.chantry, rating=1
        )

        form_data = {
            "category": "Existing Background",
            "example": str(bg_rating.pk),
            "note": "",
            "display_alt_name": False,
        }

        form = ChantryPointForm(data=form_data, pk=self.chantry.pk)
        self.assertTrue(form.is_valid())
        form.save()

        bg_rating.refresh_from_db()
        self.assertEqual(bg_rating.rating, 2)


class TestChantryEffectsFormSetup(TestCase):
    """Shared setup for ChantryEffectsForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantryEffectsForm tests."""
        mage_setup()
        cls.chantry = Chantry.objects.create(
            name="Test Chantry", total_points=50, integrated_effects_score=3
        )
        cls.effect = Effect.objects.filter(max_sphere__lte=cls.chantry.rank).first()


class TestChantryEffectsFormBasics(TestChantryEffectsFormSetup):
    """Test basic ChantryEffectsForm structure and fields."""

    def test_form_has_select_field(self):
        """Test that form has a select field."""
        form = ChantryEffectsForm(pk=self.chantry.pk)

        self.assertIn("select", form.fields)

    def test_queryset_excludes_existing_effects(self):
        """Test that queryset excludes effects already in chantry."""
        if self.effect:
            self.chantry.integrated_effects.add(self.effect)

            form = ChantryEffectsForm(pk=self.chantry.pk)

            self.assertNotIn(self.effect, form.fields["select"].queryset)

    def test_queryset_respects_rank_limit(self):
        """Test that queryset only includes effects within rank limit."""
        form = ChantryEffectsForm(pk=self.chantry.pk)

        for effect in form.fields["select"].queryset:
            self.assertLessEqual(effect.max_sphere, self.chantry.rank)


class TestChantryEffectsFormSave(TestChantryEffectsFormSetup):
    """Test ChantryEffectsForm save logic."""

    def test_save_adds_effect_to_chantry(self):
        """Test that saving adds the effect to chantry's integrated effects."""
        if self.effect:
            form_data = {
                "select_or_create": False,
                "select": str(self.effect.pk),
            }

            form = ChantryEffectsForm(data=form_data, pk=self.chantry.pk)
            if form.is_valid():
                form.save()
                self.assertIn(self.effect, self.chantry.integrated_effects.all())


class TestChantryCreateFormSetup(TestCase):
    """Shared setup for ChantryCreateForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantryCreateForm tests."""
        mage_setup()
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")


class TestChantryCreateFormBasics(TestChantryCreateFormSetup):
    """Test basic ChantryCreateForm structure and fields."""

    def test_form_has_required_fields(self):
        """Test that form has all required fields."""
        form = ChantryCreateForm()

        self.assertIn("name", form.fields)
        self.assertIn("chronicle", form.fields)
        self.assertIn("contained_within", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("faction", form.fields)
        self.assertIn("leadership_type", form.fields)
        self.assertIn("season", form.fields)
        self.assertIn("chantry_type", form.fields)
        self.assertIn("total_points", form.fields)

    def test_total_points_has_min_value(self):
        """Test that total_points has minimum value of 0."""
        form = ChantryCreateForm()

        self.assertEqual(form.fields["total_points"].min_value, 0)

    def test_name_widget_has_placeholder(self):
        """Test that name field has placeholder text."""
        form = ChantryCreateForm()

        self.assertIn("placeholder", form.fields["name"].widget.attrs)

    def test_description_widget_has_placeholder(self):
        """Test that description field has placeholder text."""
        form = ChantryCreateForm()

        self.assertIn("placeholder", form.fields["description"].widget.attrs)


class TestChantryCreateFormValidation(TestChantryCreateFormSetup):
    """Test ChantryCreateForm validation logic."""

    def test_valid_form_data(self):
        """Test that form validates with valid data."""
        form_data = {
            "name": "Test Chantry",
            "chronicle": self.chronicle.pk,
            "description": "A test chantry",
            "total_points": 10,
            "leadership_type": "panel",
            "season": "spring",
            "chantry_type": "exploration",
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = ChantryCreateForm(data=form_data)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_invalid_negative_total_points(self):
        """Test that negative total_points is invalid."""
        form_data = {
            "name": "Test Chantry",
            "total_points": -5,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = ChantryCreateForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("total_points", form.errors)


class TestChantryCreateFormSave(TestChantryCreateFormSetup):
    """Test ChantryCreateForm save logic."""

    def test_save_creates_chantry(self):
        """Test that saving creates a new Chantry."""
        initial_count = Chantry.objects.count()

        form_data = {
            "name": "New Chantry",
            "description": "A new chantry",
            "total_points": 15,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }

        form = ChantryCreateForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        chantry = form.save()

        self.assertEqual(Chantry.objects.count(), initial_count + 1)
        self.assertEqual(chantry.name, "New Chantry")
        self.assertEqual(chantry.total_points, 15)


class TestChantrySelectOrCreateFormSetup(TestCase):
    """Shared setup for ChantrySelectOrCreateForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantrySelectOrCreateForm tests."""
        mage_setup()
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.other = User.objects.create_user(username="other", password="password")
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")
        cls.character = Mage.objects.create(
            name="Test Mage", owner=cls.user, chronicle=cls.chronicle
        )
        cls.existing_chantry = Chantry.objects.create(
            name="Existing Chantry",
            owner=cls.other,
            chronicle=cls.chronicle,
            status="App",
            total_points=20,
        )


class TestChantrySelectOrCreateFormBasics(TestChantrySelectOrCreateFormSetup):
    """Test basic ChantrySelectOrCreateForm structure and fields."""

    def test_form_has_required_fields(self):
        """The form offers create/select and basics, but no points field."""
        form = ChantrySelectOrCreateForm(character=self.character, points=3)

        self.assertIn("create_new", form.fields)
        self.assertIn("existing_chantry", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertNotIn("total_points", form.fields)
        self.assertNotIn("chronicle", form.fields)

    def test_existing_chantry_queryset_filtered_by_chronicle(self):
        """Test that existing_chantry queryset is filtered by character's chronicle."""
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        other_chantry = Chantry.objects.create(name="Other Chantry", chronicle=other_chronicle)

        form = ChantrySelectOrCreateForm(character=self.character, points=3)

        self.assertIn(self.existing_chantry, form.fields["existing_chantry"].queryset)
        self.assertNotIn(other_chantry, form.fields["existing_chantry"].queryset)

    def test_existing_chantry_queryset_excludes_retired_and_deceased(self):
        retired = Chantry.objects.create(name="Retired", chronicle=self.chronicle, status="Ret")
        dead = Chantry.objects.create(name="Dead", chronicle=self.chronicle, status="Dec")

        queryset = (
            ChantrySelectOrCreateForm(character=self.character, points=3)
            .fields["existing_chantry"]
            .queryset
        )

        self.assertNotIn(retired, queryset)
        self.assertNotIn(dead, queryset)
        self.assertIn(self.existing_chantry, queryset)

    def test_all_fields_optional(self):
        """Test that all fields are optional."""
        form = ChantrySelectOrCreateForm(character=self.character, points=3)

        for field in form.fields.values():
            self.assertFalse(field.required)


class TestChantrySelectOrCreateFormValidation(TestChantrySelectOrCreateFormSetup):
    """Test ChantrySelectOrCreateForm validation logic."""

    def test_valid_select_existing(self):
        """Test that selecting existing chantry is valid."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": self.existing_chantry.pk},
            character=self.character,
            points=5,
        )

        self.assertTrue(form.is_valid())

    def test_invalid_no_selection_when_not_creating(self):
        """Test that not creating and no selection is invalid."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": ""}, character=self.character, points=5
        )

        self.assertFalse(form.is_valid())
        self.assertIn("existing_chantry", form.errors)

    def test_invalid_create_without_name(self):
        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "   "}, character=self.character, points=5
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_valid_create_new_with_valid_data(self):
        """Test that creating new with valid data is valid."""
        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "New Chantry", "description": "Test"},
            character=self.character,
            points=10,
        )

        self.assertTrue(form.is_valid())


class TestChantrySelectOrCreateFormSave(TestChantrySelectOrCreateFormSetup):
    """Test ChantrySelectOrCreateForm save logic."""

    def test_save_returns_existing_chantry(self):
        """Test that saving with existing selection returns the existing chantry."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": self.existing_chantry.pk},
            character=self.character,
            points=5,
        )
        self.assertTrue(form.is_valid())
        chantry = form.save()

        self.assertEqual(chantry.pk, self.existing_chantry.pk)

    def test_save_adds_points_to_existing_chantry_and_nothing_else(self):
        """Joining adds the points; owner, chronicle and status stay."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": self.existing_chantry.pk},
            character=self.character,
            points=5,
        )
        self.assertTrue(form.is_valid())
        form.save()

        self.existing_chantry.refresh_from_db()
        self.assertEqual(self.existing_chantry.total_points, 25)
        self.assertEqual(self.existing_chantry.owner, self.other)
        self.assertEqual(self.existing_chantry.status, "App")
        self.assertEqual(self.existing_chantry.chronicle, self.chronicle)

    def test_save_creates_new_chantry(self):
        """Creating makes an unfinished chantry owned by the character's player."""
        initial_count = Chantry.objects.count()

        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "Created Chantry", "description": "New"},
            character=self.character,
            points=15,
        )
        self.assertTrue(form.is_valid())
        chantry = form.save()

        self.assertEqual(Chantry.objects.count(), initial_count + 1)
        self.assertEqual(chantry.name, "Created Chantry")
        self.assertEqual(chantry.total_points, 15)
        self.assertEqual(chantry.owner, self.user)
        self.assertEqual(chantry.chronicle, self.chronicle)
        self.assertEqual(chantry.status, "Un")
        self.assertEqual(chantry.creation_status, 1)

    def test_save_join_adds_points_to_database_value_even_if_form_instance_stale(self):
        """The join is a single atomic UPDATE, so it uses the DB value, not a stale read."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": self.existing_chantry.pk},
            character=self.character,
            points=5,
        )
        self.assertTrue(form.is_valid())
        # Simulate another request changing total_points after this form validated but
        # before it saves (the instance the form's cleaned_data holds is now stale).
        Chantry.objects.filter(pk=self.existing_chantry.pk).update(total_points=100)

        chantry = form.save()

        self.assertEqual(chantry.total_points, 105)
        self.existing_chantry.refresh_from_db()
        self.assertEqual(self.existing_chantry.total_points, 105)


class TestChantrySelectOrCreateFormChronicleLess(TestCase):
    """A chronicle-less character may only join their own chronicle-less chantries."""

    @classmethod
    def setUpTestData(cls):
        mage_setup()
        cls.user = User.objects.create_user(username="homeless", password="password")
        cls.other = User.objects.create_user(username="other_homeless", password="password")
        cls.character = Mage.objects.create(name="Homeless Mage", owner=cls.user, chronicle=None)
        cls.own_chantry = Chantry.objects.create(
            name="Own Chantry-less",
            owner=cls.user,
            chronicle=None,
            status="App",
            total_points=5,
        )
        cls.other_chantry = Chantry.objects.create(
            name="Other Chantry-less",
            owner=cls.other,
            chronicle=None,
            status="App",
            total_points=5,
        )

    def test_own_chronicle_less_chantry_is_offered(self):
        queryset = (
            ChantrySelectOrCreateForm(character=self.character, points=3)
            .fields["existing_chantry"]
            .queryset
        )
        self.assertIn(self.own_chantry, queryset)

    def test_other_players_chronicle_less_chantry_is_not_offered(self):
        queryset = (
            ChantrySelectOrCreateForm(character=self.character, points=3)
            .fields["existing_chantry"]
            .queryset
        )
        self.assertNotIn(self.other_chantry, queryset)

    def test_post_choosing_other_players_chantry_is_invalid(self):
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": self.other_chantry.pk},
            character=self.character,
            points=3,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("existing_chantry", form.errors)
        self.other_chantry.refresh_from_db()
        self.assertEqual(self.other_chantry.total_points, 5)


class TestChantrySelectOrCreateFormTypeGrants(TestChantrySelectOrCreateFormSetup):
    def test_creating_library_type_grants_free_library_dots(self):
        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "Stacks", "chantry_type": "library"},
            character=self.character,
            points=4,
        )
        self.assertTrue(form.is_valid(), form.errors)
        chantry = form.save()
        rating = chantry.backgrounds.get(bg__property_name="library")
        self.assertEqual(rating.rating, 3)
        self.assertEqual(chantry.points, 4)


class TestChantryPointFormRules(TestChantryPointFormSetup):
    """Choices and validation follow the points service."""

    def form(self, data=None, **chantry_fields):
        Chantry.objects.filter(pk=self.chantry.pk).update(**chantry_fields)
        return ChantryPointForm(data=data, pk=self.chantry.pk)

    def examples(self, form, category):
        return {value for value, _ in form.fields["example"].choices_map[category]}

    def test_new_background_choices_are_allowed_and_affordable(self):
        form = self.form(total_points=4)
        examples = self.examples(form, "New Background")
        self.assertIn(str(self.background.pk), examples)
        requisitions = Background.objects.get(property_name="requisitions")
        self.assertIn(str(requisitions.pk), examples)
        for property_name in ["sanctum", "fame", "avatar"]:
            bg = Background.objects.get(property_name=property_name)
            self.assertNotIn(str(bg.pk), examples)

    def test_capped_rating_not_offered_as_existing(self):
        capped = ChantryBackgroundRating.objects.create(
            bg=self.background, chantry=self.chantry, rating=5
        )
        form = self.form()
        self.assertNotIn("Existing Background", dict(form.fields["category"].choices))
        self.assertNotIn(str(capped.pk), self.examples(form, "Existing Background"))
        self.assertNotIn(str(self.background.pk), self.examples(form, "New Background"))

    def test_no_points_leaves_only_placeholder(self):
        form = self.form(total_points=1)
        self.assertEqual([value for value, _ in form.fields["category"].choices], ["-----"])

    def test_forged_disallowed_background_fails(self):
        fame = Background.objects.get(property_name="fame")
        form = self.form({"category": "New Background", "example": str(fame.pk)})
        self.assertFalse(form.is_valid())

    def test_forged_unaffordable_background_fails(self):
        sanctum = Background.objects.get(property_name="sanctum")
        form = self.form({"category": "New Background", "example": str(sanctum.pk)}, total_points=4)
        self.assertFalse(form.is_valid())

    def test_forged_ie_at_cap_fails(self):
        form = self.form({"category": "Integrated Effects"}, integrated_effects_score=10)
        self.assertFalse(form.is_valid())

    def test_forged_other_chantrys_rating_fails(self):
        other = Chantry.objects.create(name="Other", total_points=20)
        foreign = ChantryBackgroundRating.objects.create(
            bg=self.background, chantry=other, rating=1
        )
        form = self.form({"category": "Existing Background", "example": str(foreign.pk)})
        self.assertFalse(form.is_valid())

    def test_forged_non_numeric_example_fails(self):
        form = self.form({"category": "New Background", "example": "allies"})
        self.assertFalse(form.is_valid())

    def test_save_new_background_keeps_note_and_alt_name(self):
        form = self.form(
            {
                "category": "New Background",
                "example": str(self.background.pk),
                "note": "Old friends",
                "display_alt_name": True,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        rating = form.save()
        self.assertEqual(
            (rating.rating, rating.note, rating.display_alt_name), (1, "Old friends", True)
        )
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.points, 18)

    def test_save_raises_when_points_were_spent_meanwhile(self):
        form = self.form({"category": "Integrated Effects"}, total_points=2)
        self.assertTrue(form.is_valid())
        Chantry.objects.filter(pk=self.chantry.pk).update(total_points=0)
        with self.assertRaises(ValidationError):
            form.save()


class TestChantryEffectsFormCostLimit(TestCase):
    """Only effects that fit the remaining IE points and chantry rank are offered."""

    @classmethod
    def setUpTestData(cls):
        mage_setup()
        cls.chantry = Chantry.objects.create(
            name="Ward Chantry", total_points=20, integrated_effects_score=1
        )  # rank 2, 4 IE points
        cls.fits = Effect.objects.create(name="Small Ward", forces=2, prime=2)  # cost 4
        cls.too_costly = Effect.objects.create(name="Big Ward", forces=2, prime=2, mind=1)

    def test_queryset_respects_remaining_ie_points(self):
        form = ChantryEffectsForm(pk=self.chantry.pk)
        self.assertIn(self.fits, form.fields["select"].queryset)
        self.assertNotIn(self.too_costly, form.fields["select"].queryset)
