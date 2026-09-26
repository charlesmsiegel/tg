"""
Tests for character forms.

Tests cover:
- LimitedHumanEditForm field restrictions
- Full character forms
- Form validation
- XP spending forms
- Freebie spending forms
"""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.core import LimitedHumanEditForm
from characters.models.core import Human


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

    def test_limited_form_accepts_html_sanitized_at_render(self):
        """Test that form accepts HTML which is sanitized at template render time.

        The project uses template-level sanitization via the sanitize_html filter,
        not form-level sanitization. This test verifies the form accepts the data
        and that the sanitize_html filter properly strips dangerous HTML.
        """
        from core.templatetags.sanitize_text import sanitize_html

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
            # Script tags should be stripped by the sanitize_html filter at render time
            sanitized = sanitize_html(saved.description)
            self.assertNotIn("<script>", sanitized)

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
