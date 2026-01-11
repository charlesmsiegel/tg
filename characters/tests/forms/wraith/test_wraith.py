"""Tests for Wraith forms."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.wraith.wraith import WraithCreationForm
from characters.models.wraith.guild import Guild
from characters.models.wraith.wraith import Wraith
from game.models import Chronicle


class WraithCreationFormTestCase(TestCase):
    """Base test case with common setup for WraithCreationForm tests."""

    def setUp(self):
        """Set up test user and guild."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.guild = Guild.objects.create(
            name="Masquers",
            guild_type="greater",
            willpower=6,
        )


class TestWraithCreationFormInitialization(WraithCreationFormTestCase):
    """Tests for WraithCreationForm initialization."""

    def test_form_requires_user(self):
        """Form requires user parameter."""
        form = WraithCreationForm(user=self.user)
        self.assertEqual(form.user, self.user)

    def test_form_has_expected_fields(self):
        """Form has all expected fields."""
        form = WraithCreationForm(user=self.user)
        expected_fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "chronicle",
            "image",
            "guild",
            "npc",
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_guild_field_required(self):
        """Guild field is required."""
        form = WraithCreationForm(user=self.user)
        self.assertTrue(form.fields["guild"].required)

    def test_image_field_not_required(self):
        """Image field is not required."""
        form = WraithCreationForm(user=self.user)
        self.assertFalse(form.fields["image"].required)

    def test_guild_queryset(self):
        """Guild field queryset includes all guilds."""
        form = WraithCreationForm(user=self.user)
        self.assertIn(self.guild, form.fields["guild"].queryset)

    def test_name_placeholder(self):
        """Name field has placeholder."""
        form = WraithCreationForm(user=self.user)
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Enter name here",
        )

    def test_concept_placeholder(self):
        """Concept field has placeholder."""
        form = WraithCreationForm(user=self.user)
        self.assertEqual(
            form.fields["concept"].widget.attrs.get("placeholder"),
            "Enter concept here",
        )


class TestWraithCreationFormValidation(WraithCreationFormTestCase):
    """Tests for WraithCreationForm validation."""

    def test_valid_data(self):
        """Form is valid with required fields."""
        data = {
            "name": "Test Wraith",
            "guild": self.guild.pk,
        }
        form = WraithCreationForm(data=data, user=self.user)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_missing_name_invalid(self):
        """Form is invalid without name."""
        data = {
            "guild": self.guild.pk,
        }
        form = WraithCreationForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_guild_invalid(self):
        """Form is invalid without guild."""
        data = {
            "name": "Test Wraith",
        }
        form = WraithCreationForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("guild", form.errors)


class TestWraithCreationFormSave(WraithCreationFormTestCase):
    """Tests for WraithCreationForm save behavior."""

    def test_save_sets_owner(self):
        """Save assigns user as owner."""
        data = {
            "name": "Test Wraith",
            "guild": self.guild.pk,
        }
        form = WraithCreationForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        wraith = form.save()
        self.assertEqual(wraith.owner, self.user)

    def test_save_creates_wraith(self):
        """Save creates Wraith object."""
        data = {
            "name": "Test Wraith",
            "guild": self.guild.pk,
        }
        form = WraithCreationForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        wraith = form.save()
        self.assertIsInstance(wraith, Wraith)
        self.assertEqual(wraith.name, "Test Wraith")
        self.assertEqual(wraith.guild, self.guild)

    def test_save_with_optional_fields(self):
        """Save works with optional fields."""
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        data = {
            "name": "Test Wraith",
            "guild": self.guild.pk,
            "concept": "A restless spirit",
            "chronicle": chronicle.pk,
            "npc": True,
        }
        form = WraithCreationForm(data=data, user=self.user)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        wraith = form.save()
        self.assertEqual(wraith.concept, "A restless spirit")
        self.assertEqual(wraith.chronicle, chronicle)
        self.assertTrue(wraith.npc)

    def test_save_commit_false(self):
        """Save with commit=False doesn't save to database."""
        initial_count = Wraith.objects.count()
        data = {
            "name": "Test Wraith",
            "guild": self.guild.pk,
        }
        form = WraithCreationForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())
        wraith = form.save(commit=False)
        self.assertEqual(Wraith.objects.count(), initial_count)
        self.assertEqual(wraith.owner, self.user)


class TestWraithCreationFormMultipleGuilds(WraithCreationFormTestCase):
    """Tests for WraithCreationForm with multiple guilds."""

    def setUp(self):
        super().setUp()
        self.guild2 = Guild.objects.create(
            name="Haunters",
            guild_type="greater",
            willpower=5,
        )
        self.guild3 = Guild.objects.create(
            name="Solicitors",
            guild_type="greater",
            willpower=6,
        )

    def test_guild_queryset_contains_all_guilds(self):
        """Guild queryset includes all created guilds."""
        form = WraithCreationForm(user=self.user)
        queryset = form.fields["guild"].queryset
        self.assertIn(self.guild, queryset)
        self.assertIn(self.guild2, queryset)
        self.assertIn(self.guild3, queryset)

    def test_can_select_different_guilds(self):
        """Form accepts different guild selections."""
        for guild in [self.guild, self.guild2, self.guild3]:
            data = {
                "name": f"Wraith of {guild.name}",
                "guild": guild.pk,
            }
            form = WraithCreationForm(data=data, user=self.user)
            self.assertTrue(form.is_valid(), f"Form errors for {guild.name}: {form.errors}")
            wraith = form.save()
            self.assertEqual(wraith.guild, guild)
            wraith.delete()  # Clean up for next iteration
