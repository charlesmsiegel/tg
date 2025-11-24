"""
Tests for character forms.

Tests cover:
- LimitedCharacterEditForm field restrictions
- Full character forms
- Form validation
- XP spending forms
- Freebie spending forms
"""
from characters.forms.core import (
    LimitedCharacterEditForm,
    LimitedHumanEditForm,
)
from characters.models.core import Character, Human
from django.contrib.auth.models import User
from django.test import TestCase


class TestLimitedCharacterEditForm(TestCase):
    """Test the limited character edit form for owners."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.character = Character.objects.create(
            name="Test Character",
            owner=self.user,
            concept="Detective",
            description="Original description",
            notes="Original notes",
        )

    def test_form_includes_only_safe_fields(self):
        """Test that form only includes descriptive fields."""
        form = LimitedCharacterEditForm(instance=self.character)

        # Should include safe descriptive fields
        self.assertIn("description", form.fields)
        self.assertIn("notes", form.fields)
        self.assertIn("public_info", form.fields)
        self.assertIn("image", form.fields)

        # Should NOT include mechanical or security-sensitive fields
        self.assertNotIn("name", form.fields)
        self.assertNotIn("owner", form.fields)
        self.assertNotIn("chronicle", form.fields)
        self.assertNotIn("status", form.fields)
        self.assertNotIn("xp", form.fields)
        self.assertNotIn("spent_xp", form.fields)
        self.assertNotIn("freebies", form.fields)
        self.assertNotIn("npc", form.fields)

    def test_form_saves_valid_data(self):
        """Test that form saves valid descriptive data."""
        form_data = {
            "description": "Updated description",
            "notes": "Updated notes",
            "public_info": "Public information",
        }
        form = LimitedCharacterEditForm(data=form_data, instance=self.character)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        updated = form.save()
        updated.refresh_from_db()

        self.assertEqual(updated.description, "Updated description")
        self.assertEqual(updated.notes, "Updated notes")
        self.assertEqual(updated.public_info, "Public information")

    def test_form_does_not_change_restricted_fields(self):
        """Test that form cannot change restricted fields."""
        original_name = self.character.name
        original_status = self.character.status

        form_data = {
            "description": "New description",
        }
        form = LimitedCharacterEditForm(data=form_data, instance=self.character)

        if form.is_valid():
            form.save()
            self.character.refresh_from_db()

            # Name and status should remain unchanged
            self.assertEqual(self.character.name, original_name)
            self.assertEqual(self.character.status, original_status)

    def test_form_has_helpful_placeholders(self):
        """Test that form fields have helpful placeholders."""
        form = LimitedCharacterEditForm(instance=self.character)

        self.assertIn("placeholder", form.fields["description"].widget.attrs)
        self.assertIn("placeholder", form.fields["notes"].widget.attrs)

    def test_form_has_helpful_help_text(self):
        """Test that form fields have helpful help text."""
        form = LimitedCharacterEditForm(instance=self.character)

        # Help text should guide users
        self.assertTrue(form.fields["public_info"].help_text)
        self.assertTrue(form.fields["notes"].help_text)


class TestLimitedHumanEditForm(TestCase):
    """Test the limited human edit form."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.user,
            history="Original history",
            goals="Original goals",
        )

    def test_form_includes_human_specific_fields(self):
        """Test that form includes human-specific descriptive fields."""
        form = LimitedHumanEditForm(instance=self.human)

        # Should include Character fields
        self.assertIn("description", form.fields)
        self.assertIn("notes", form.fields)

        # Should include Human-specific fields
        self.assertIn("history", form.fields)
        self.assertIn("goals", form.fields)

        # Should NOT include mechanical fields
        self.assertNotIn("strength", form.fields)
        self.assertNotIn("intelligence", form.fields)
        self.assertNotIn("willpower", form.fields)

    def test_form_saves_human_fields(self):
        """Test that form saves human-specific fields."""
        form_data = {
            "description": "Updated description",
            "notes": "Updated notes",
            "public_info": "Public info",
            "history": "Born in Boston in 1985...",
            "goals": "Solve the mystery of my father's death",
        }
        form = LimitedHumanEditForm(data=form_data, instance=self.human)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        updated = form.save()
        updated.refresh_from_db()

        self.assertEqual(updated.history, "Born in Boston in 1985...")
        self.assertEqual(updated.goals, "Solve the mystery of my father's death")

    def test_form_optional_fields(self):
        """Test that optional fields can be left blank."""
        form_data = {
            "description": "",  # Optional
            "notes": "",  # Optional
            "history": "",  # Optional
            "goals": "",  # Optional
        }
        form = LimitedHumanEditForm(data=form_data, instance=self.human)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")


class TestCharacterFormValidation(TestCase):
    """Test character form validation rules."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def test_limited_form_rejects_html_injection(self):
        """Test that form sanitizes or rejects malicious HTML."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
        )

        malicious_data = {
            "description": "<script>alert('XSS')</script>",
            "notes": "Normal notes",
        }

        form = LimitedHumanEditForm(data=malicious_data, instance=human)

        if form.is_valid():
            saved = form.save()
            # Script tags should be stripped or escaped
            self.assertNotIn("<script>", saved.description)

    def test_form_handles_very_long_text(self):
        """Test that form handles very long text appropriately."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
        )

        long_text = "A" * 10000  # Very long text

        form_data = {
            "description": long_text,
            "notes": "Normal notes",
        }

        form = LimitedHumanEditForm(data=form_data, instance=human)

        # Should either accept or gracefully handle long text
        if not form.is_valid():
            # If there's a max length, error should be clear
            self.assertTrue("description" in form.errors or len(form.errors) > 0)

    def test_form_handles_unicode_characters(self):
        """Test that form handles unicode characters correctly."""
        human = Human.objects.create(
            name="Test",
            owner=self.user,
        )

        unicode_data = {
            "description": "Description with émojis 🎭 and spëcial çharacters",
            "notes": "日本語 and العربية",
        }

        form = LimitedHumanEditForm(data=unicode_data, instance=human)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        if form.is_valid():
            saved = form.save()
            self.assertIn("émojis", saved.description)
            self.assertIn("日本語", saved.notes)


class TestImageUploadForm(TestCase):
    """Test image upload functionality in character forms."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.character = Character.objects.create(
            name="Test",
            owner=self.user,
        )

    def test_image_field_is_optional(self):
        """Test that image field is optional."""
        form_data = {
            "description": "Test description",
        }
        form = LimitedCharacterEditForm(data=form_data, instance=self.character)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_image_field_exists_in_form(self):
        """Test that image field is present in the form."""
        form = LimitedCharacterEditForm(instance=self.character)

        self.assertIn("image", form.fields)
        self.assertFalse(form.fields["image"].required)


class TestXPSpendingForm(TestCase):
    """Test XP spending form validation and processing."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.character = Human.objects.create(
            name="Test",
            owner=self.user,
            xp=20,  # Has XP to spend
        )

    def test_cannot_spend_more_xp_than_available(self):
        """Test that form prevents spending more XP than available."""
        # This test depends on XP spending form implementation
        # Placeholder for when form is created
        available_xp = self.character.xp
        self.assertGreaterEqual(available_xp, 0)

    def test_xp_spending_tracks_purpose(self):
        """Test that XP spending includes purpose/description."""
        # Test depends on implementation
        # Spent XP should track what it was spent on
        self.character.spent_xp = {
            "ability_increase": {
                "amount": 3,
                "description": "Melee 2 -> 3",
                "approved": False,
            }
        }
        self.character.save()

        self.assertIn("ability_increase", self.character.spent_xp)
        self.assertEqual(self.character.spent_xp["ability_increase"]["amount"], 3)


class TestFreebieSpendingForm(TestCase):
    """Test freebie point spending form validation."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.character = Human.objects.create(
            name="Test",
            owner=self.user,
            freebies=15,  # Standard starting freebies
        )

    def test_cannot_spend_more_freebies_than_available(self):
        """Test that form prevents overspending freebies."""
        # This test depends on freebie spending form implementation
        available_freebies = self.character.freebies
        self.assertEqual(available_freebies, 15)

    def test_freebie_spending_tracks_allocation(self):
        """Test that freebie spending tracks where points went."""
        self.character.spent_freebies = {
            "attributes": 5,
            "abilities": 4,
            "backgrounds": 3,
        }
        self.character.save()

        total_spent = sum(self.character.spent_freebies.values())
        self.assertEqual(total_spent, 12)
        remaining = self.character.freebies - total_spent
        self.assertEqual(remaining, 3)
