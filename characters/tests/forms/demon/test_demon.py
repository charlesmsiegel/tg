"""Tests for Demon creation form."""

from characters.forms.demon.demon import DemonCreationForm
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.visage import Visage
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle


class DemonCreationFormTests(TestCase):
    """Tests for DemonCreationForm functionality."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        self.faction = DemonFaction.objects.create(name="Cryptics", owner=self.user)
        self.visage = Visage.objects.create(name="Bel", owner=self.user)

    def test_form_has_expected_fields(self):
        """Test that form has all expected fields."""
        form = DemonCreationForm(user=self.user)
        expected_fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "house",
            "faction",
            "visage",
            "chronicle",
            "image",
            "npc",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_form_requires_user(self):
        """Test that form requires user parameter."""
        with self.assertRaises(KeyError):
            DemonCreationForm()

    def test_form_valid_with_minimal_data(self):
        """Test that form is valid with minimal required data."""
        form_data = {
            "name": "Test Demon",
            "nature": "Survivor",
            "demeanor": "Director",
            "concept": "Former angel of fire",
            "npc": False,
        }
        form = DemonCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_all_data(self):
        """Test that form is valid with all data provided."""
        form_data = {
            "name": "Test Demon",
            "nature": "Survivor",
            "demeanor": "Director",
            "concept": "Former angel of fire",
            "house": self.house.pk,
            "faction": self.faction.pk,
            "visage": self.visage.pk,
            "chronicle": self.chronicle.pk,
            "npc": False,
        }
        form = DemonCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_save_sets_owner(self):
        """Test that save sets owner from user parameter."""
        form_data = {
            "name": "Test Demon",
            "nature": "Survivor",
            "demeanor": "Director",
            "concept": "Former angel of fire",
            "npc": False,
        }
        form = DemonCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        demon = form.save()
        self.assertEqual(demon.owner, self.user)

    def test_optional_fields(self):
        """Test that optional fields can be empty."""
        form_data = {
            "name": "Test Demon",
            "nature": "",
            "demeanor": "",
            "concept": "",
            "npc": False,
        }
        form = DemonCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_house_queryset_contains_all_houses(self):
        """Test that house field queryset contains all houses."""
        DemonHouse.objects.create(
            name="Scourges", celestial_name="Asharu", owner=self.user
        )
        form = DemonCreationForm(user=self.user)
        self.assertEqual(form.fields["house"].queryset.count(), 2)

    def test_faction_queryset_contains_all_factions(self):
        """Test that faction field queryset contains all factions."""
        DemonFaction.objects.create(name="Faustians", owner=self.user)
        form = DemonCreationForm(user=self.user)
        self.assertEqual(form.fields["faction"].queryset.count(), 2)

    def test_visage_queryset_contains_all_visages(self):
        """Test that visage field queryset contains all visages."""
        Visage.objects.create(name="Anshar", owner=self.user)
        form = DemonCreationForm(user=self.user)
        self.assertEqual(form.fields["visage"].queryset.count(), 2)

    def test_name_placeholder(self):
        """Test that name field has placeholder."""
        form = DemonCreationForm(user=self.user)
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"), "Enter name here"
        )

    def test_concept_placeholder(self):
        """Test that concept field has placeholder."""
        form = DemonCreationForm(user=self.user)
        self.assertEqual(
            form.fields["concept"].widget.attrs.get("placeholder"),
            "Enter concept here",
        )

    def test_image_not_required(self):
        """Test that image field is not required."""
        form = DemonCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)

    def test_house_not_required(self):
        """Test that house field is not required."""
        form = DemonCreationForm(user=self.user)
        self.assertFalse(form.fields["house"].required)

    def test_faction_not_required(self):
        """Test that faction field is not required."""
        form = DemonCreationForm(user=self.user)
        self.assertFalse(form.fields["faction"].required)

    def test_visage_not_required(self):
        """Test that visage field is not required."""
        form = DemonCreationForm(user=self.user)
        self.assertFalse(form.fields["visage"].required)


class DemonCreationFormSaveTests(TestCase):
    """Tests for DemonCreationForm save behavior."""

    def setUp(self):
        """Create test fixtures."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.house = DemonHouse.objects.create(
            name="Devils", celestial_name="Namaru", owner=self.user
        )
        self.faction = DemonFaction.objects.create(name="Cryptics", owner=self.user)

    def test_save_commit_true(self):
        """Test save with commit=True saves to database."""
        form_data = {
            "name": "Test Demon",
            "nature": "Survivor",
            "demeanor": "Director",
            "concept": "Former angel of fire",
            "npc": False,
        }
        form = DemonCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        demon = form.save(commit=True)
        self.assertIsNotNone(demon.pk)

    def test_save_commit_false(self):
        """Test save with commit=False doesn't save to database."""
        form_data = {
            "name": "Test Demon",
            "nature": "Survivor",
            "demeanor": "Director",
            "concept": "Former angel of fire",
            "npc": False,
        }
        form = DemonCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        demon = form.save(commit=False)
        self.assertIsNone(demon.pk)

    def test_save_with_chronicle(self):
        """Test save with chronicle sets chronicle."""
        form_data = {
            "name": "Test Demon",
            "nature": "Survivor",
            "demeanor": "Director",
            "concept": "Former angel of fire",
            "chronicle": self.chronicle.pk,
            "npc": False,
        }
        form = DemonCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        demon = form.save()
        self.assertEqual(demon.chronicle, self.chronicle)

    def test_save_with_relationships(self):
        """Test save with house and faction sets relationships."""
        form_data = {
            "name": "Test Demon",
            "nature": "Survivor",
            "demeanor": "Director",
            "concept": "Former angel of fire",
            "house": self.house.pk,
            "faction": self.faction.pk,
            "npc": False,
        }
        form = DemonCreationForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        demon = form.save()
        self.assertEqual(demon.house, self.house)
        self.assertEqual(demon.faction, self.faction)
