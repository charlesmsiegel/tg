"""Tests for ParadoxRealm forms."""

from django.test import TestCase
from locations.forms.mage.paradox_realm import (
    ParadoxAtmosphereForm,
    ParadoxAtmosphereFormSet,
    ParadoxObstacleForm,
    ParadoxObstacleFormSet,
    ParadoxRealmForm,
)
from locations.models.mage.paradox_realm import (
    ParadoxAtmosphere,
    ParadoxObstacle,
    ParadoxRealm,
    ParadigmChoices,
    SphereChoices,
)


class TestParadoxObstacleForm(TestCase):
    """Test ParadoxObstacleForm."""

    def test_form_has_required_fields(self):
        """Test form has all required fields."""
        form = ParadoxObstacleForm()
        self.assertIn("sphere", form.fields)
        self.assertIn("obstacle_number", form.fields)
        self.assertIn("order", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)

    def test_name_placeholder(self):
        """Test name field has placeholder."""
        form = ParadoxObstacleForm()
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Enter obstacle name",
        )

    def test_description_placeholder(self):
        """Test description field has placeholder."""
        form = ParadoxObstacleForm()
        self.assertEqual(
            form.fields["description"].widget.attrs.get("placeholder"),
            "Enter obstacle description",
        )

    def test_valid_form(self):
        """Test form validates with valid data."""
        data = {
            "sphere": SphereChoices.FORCES,
            "obstacle_number": 4,
            "order": 1,
            "name": "Fire",
            "description": "A wall of flames",
        }
        form = ParadoxObstacleForm(data=data)
        self.assertTrue(form.is_valid())


class TestParadoxAtmosphereForm(TestCase):
    """Test ParadoxAtmosphereForm."""

    def test_form_has_required_fields(self):
        """Test form has all required fields."""
        form = ParadoxAtmosphereForm()
        self.assertIn("paradigm", form.fields)
        self.assertIn("atmosphere_number", form.fields)
        self.assertIn("description", form.fields)

    def test_description_placeholder(self):
        """Test description field has placeholder."""
        form = ParadoxAtmosphereForm()
        self.assertEqual(
            form.fields["description"].widget.attrs.get("placeholder"),
            "Enter atmosphere description",
        )

    def test_valid_form(self):
        """Test form validates with valid data."""
        data = {
            "paradigm": ParadigmChoices.CHAOS,
            "atmosphere_number": 1,
            "description": "Colors pulsating everywhere",
        }
        form = ParadoxAtmosphereForm(data=data)
        self.assertTrue(form.is_valid())


class TestParadoxRealmFormBasics(TestCase):
    """Test basic ParadoxRealmForm functionality."""

    def test_form_has_required_fields(self):
        """Test form has all required fields."""
        form = ParadoxRealmForm()
        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("primary_sphere", form.fields)
        self.assertIn("secondary_sphere", form.fields)
        self.assertIn("paradigm", form.fields)
        self.assertIn("secondary_paradigm", form.fields)
        self.assertIn("num_primary_obstacles", form.fields)
        self.assertIn("num_random_obstacles", form.fields)
        self.assertIn("final_obstacle_type", form.fields)
        self.assertIn("generate_random", form.fields)

    def test_name_placeholder(self):
        """Test name field has placeholder."""
        form = ParadoxRealmForm()
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Enter realm name",
        )

    def test_description_placeholder(self):
        """Test description field has placeholder."""
        form = ParadoxRealmForm()
        self.assertEqual(
            form.fields["description"].widget.attrs.get("placeholder"),
            "Enter description of the realm",
        )

    def test_secondary_fields_optional(self):
        """Test secondary fields are optional."""
        form = ParadoxRealmForm()
        self.assertFalse(form.fields["secondary_sphere"].required)
        self.assertFalse(form.fields["secondary_paradigm"].required)
        self.assertFalse(form.fields["parent"].required)

    def test_form_has_formsets(self):
        """Test form has obstacle and atmosphere formsets."""
        form = ParadoxRealmForm()
        self.assertTrue(hasattr(form, "obstacle_formset"))
        self.assertTrue(hasattr(form, "atmosphere_formset"))

    def test_generate_random_defaults_false(self):
        """Test generate_random field defaults to False."""
        form = ParadoxRealmForm()
        self.assertFalse(form.fields["generate_random"].initial)


class TestParadoxRealmFormValidation(TestCase):
    """Test ParadoxRealmForm validation."""

    def _get_basic_form_data(self, **overrides):
        """Helper to create basic form data."""
        data = {
            "name": "Test Realm",
            "description": "A test paradox realm",
            "primary_sphere": SphereChoices.FORCES,
            "paradigm": ParadigmChoices.CHAOS,
            "num_primary_obstacles": 2,
            "num_random_obstacles": 1,
            "final_obstacle_type": "maze",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            # Formset management forms
            "obstacles-TOTAL_FORMS": "0",
            "obstacles-INITIAL_FORMS": "0",
            "obstacles-MIN_NUM_FORMS": "0",
            "obstacles-MAX_NUM_FORMS": "1000",
            "atmospheres-TOTAL_FORMS": "0",
            "atmospheres-INITIAL_FORMS": "0",
            "atmospheres-MIN_NUM_FORMS": "0",
            "atmospheres-MAX_NUM_FORMS": "1000",
        }
        data.update(overrides)
        return data

    def test_valid_form(self):
        """Test form validates with valid data."""
        data = self._get_basic_form_data()
        form = ParadoxRealmForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_name_required(self):
        """Test name field is required."""
        data = self._get_basic_form_data(name="")
        form = ParadoxRealmForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TestParadoxRealmFormSave(TestCase):
    """Test ParadoxRealmForm save functionality."""

    def _get_valid_form_data(self):
        """Helper to create valid form data."""
        return {
            "name": "Saved Realm",
            "description": "A saved paradox realm",
            "primary_sphere": SphereChoices.ENTROPY,
            "paradigm": ParadigmChoices.ANTIMAGICK,
            "num_primary_obstacles": 1,
            "num_random_obstacles": 0,
            "final_obstacle_type": "maze",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            # Formset management forms
            "obstacles-TOTAL_FORMS": "0",
            "obstacles-INITIAL_FORMS": "0",
            "obstacles-MIN_NUM_FORMS": "0",
            "obstacles-MAX_NUM_FORMS": "1000",
            "atmospheres-TOTAL_FORMS": "0",
            "atmospheres-INITIAL_FORMS": "0",
            "atmospheres-MIN_NUM_FORMS": "0",
            "atmospheres-MAX_NUM_FORMS": "1000",
        }

    def test_save_creates_realm(self):
        """Test save creates a paradox realm."""
        data = self._get_valid_form_data()
        form = ParadoxRealmForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        realm = form.save()
        self.assertIsNotNone(realm.pk)
        self.assertEqual(realm.name, "Saved Realm")
        self.assertEqual(realm.primary_sphere, SphereChoices.ENTROPY)

    def test_save_with_generate_random(self):
        """Test save with generate_random creates random realm."""
        data = self._get_valid_form_data()
        data["generate_random"] = True
        data["name"] = "Random Generated Realm"
        form = ParadoxRealmForm(data=data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        realm = form.save()
        self.assertIsNotNone(realm.pk)
        self.assertEqual(realm.name, "Random Generated Realm")
        # When generate_random is true, it uses the random() method
        # which may set different values than form data

    def test_save_commit_false(self):
        """Test save with commit=False doesn't save to database."""
        data = self._get_valid_form_data()
        form = ParadoxRealmForm(data=data)
        self.assertTrue(form.is_valid())

        realm = form.save(commit=False)
        self.assertIsNone(realm.pk)


class TestParadoxRealmFormUpdate(TestCase):
    """Test ParadoxRealmForm for updating existing realms."""

    def setUp(self):
        self.realm = ParadoxRealm.objects.create(
            name="Existing Realm",
            primary_sphere=SphereChoices.MIND,
            paradigm=ParadigmChoices.FAITH,
        )

    def test_form_with_instance(self):
        """Test form loads instance data."""
        form = ParadoxRealmForm(instance=self.realm)
        self.assertEqual(form.initial["name"], "Existing Realm")
        self.assertEqual(form.initial["primary_sphere"], SphereChoices.MIND)

    def test_update_realm(self):
        """Test updating an existing realm."""
        data = {
            "name": "Updated Realm",
            "description": "Updated description",
            "primary_sphere": SphereChoices.TIME,
            "paradigm": ParadigmChoices.TECH,
            "num_primary_obstacles": 3,
            "num_random_obstacles": 2,
            "final_obstacle_type": "maze",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            "obstacles-TOTAL_FORMS": "0",
            "obstacles-INITIAL_FORMS": "0",
            "obstacles-MIN_NUM_FORMS": "0",
            "obstacles-MAX_NUM_FORMS": "1000",
            "atmospheres-TOTAL_FORMS": "0",
            "atmospheres-INITIAL_FORMS": "0",
            "atmospheres-MIN_NUM_FORMS": "0",
            "atmospheres-MAX_NUM_FORMS": "1000",
        }
        form = ParadoxRealmForm(data=data, instance=self.realm)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        realm = form.save()
        self.assertEqual(realm.pk, self.realm.pk)
        self.assertEqual(realm.name, "Updated Realm")
        self.assertEqual(realm.primary_sphere, SphereChoices.TIME)


class TestParadoxObstacleFormSet(TestCase):
    """Test ParadoxObstacleFormSet."""

    def test_formset_exists(self):
        """Test formset class exists and can be instantiated."""
        formset = ParadoxObstacleFormSet()
        self.assertIsNotNone(formset)

    def test_formset_allows_deletion(self):
        """Test formset allows deletion."""
        formset = ParadoxObstacleFormSet()
        self.assertTrue(formset.can_delete)


class TestParadoxAtmosphereFormSet(TestCase):
    """Test ParadoxAtmosphereFormSet."""

    def test_formset_exists(self):
        """Test formset class exists and can be instantiated."""
        formset = ParadoxAtmosphereFormSet()
        self.assertIsNotNone(formset)

    def test_formset_allows_deletion(self):
        """Test formset allows deletion."""
        formset = ParadoxAtmosphereFormSet()
        self.assertTrue(formset.can_delete)
