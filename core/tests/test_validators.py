"""Tests for shared validators in core/validators.py."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from core.validators import validate_gameline, validate_non_empty_name


class ValidateNonEmptyNameTests(TestCase):
    """Tests for validate_non_empty_name validator."""

    def test_valid_name(self):
        """Valid names should not raise errors."""
        validate_non_empty_name("Test Name")  # Should not raise

    def test_valid_name_with_whitespace(self):
        """Names with leading/trailing whitespace are valid if non-empty."""
        validate_non_empty_name("  Test Name  ")  # Should not raise

    def test_empty_string(self):
        """Empty strings should raise ValidationError."""
        with self.assertRaises(ValidationError) as context:
            validate_non_empty_name("")
        self.assertEqual(context.exception.code, "required")

    def test_whitespace_only(self):
        """Whitespace-only strings should raise ValidationError."""
        with self.assertRaises(ValidationError) as context:
            validate_non_empty_name("   ")
        self.assertEqual(context.exception.code, "required")

    def test_none_value(self):
        """None values should raise ValidationError."""
        with self.assertRaises(ValidationError) as context:
            validate_non_empty_name(None)
        self.assertEqual(context.exception.code, "required")

    def test_custom_field_name_in_message(self):
        """Error message should include custom field name."""
        with self.assertRaises(ValidationError) as context:
            validate_non_empty_name("", "Custom field")
        self.assertIn("Custom field is required", str(context.exception))

    def test_default_field_name_in_message(self):
        """Error message should use 'Name' as default field name."""
        with self.assertRaises(ValidationError) as context:
            validate_non_empty_name("")
        self.assertIn("Name is required", str(context.exception))


class ValidateGamelineTests(TestCase):
    """Tests for validate_gameline validator."""

    def test_valid_gameline(self):
        """Valid gameline codes should not raise errors."""
        # Get first valid gameline from settings
        valid_code = settings.GAMELINE_CHOICES[0][0]
        validate_gameline(valid_code)  # Should not raise

    def test_all_valid_gamelines(self):
        """All gameline codes from settings should be valid."""
        for code, _ in settings.GAMELINE_CHOICES:
            validate_gameline(code)  # Should not raise

    def test_invalid_gameline(self):
        """Invalid gameline codes should raise ValidationError."""
        with self.assertRaises(ValidationError) as context:
            validate_gameline("invalid_code")
        self.assertEqual(context.exception.code, "invalid_choice")

    def test_error_message_includes_invalid_code(self):
        """Error message should mention the invalid code."""
        with self.assertRaises(ValidationError) as context:
            validate_gameline("xyz123")
        self.assertIn("xyz123", str(context.exception))

    def test_error_message_includes_valid_options(self):
        """Error message should list valid options."""
        with self.assertRaises(ValidationError) as context:
            validate_gameline("invalid")
        # Check that at least one valid code is mentioned
        valid_code = settings.GAMELINE_CHOICES[0][0]
        self.assertIn(valid_code, str(context.exception))

    def test_empty_string_gameline(self):
        """Empty string should raise ValidationError if not a valid choice."""
        # Check if empty string is a valid choice
        valid_codes = [code for code, _ in settings.GAMELINE_CHOICES]
        if "" not in valid_codes:
            with self.assertRaises(ValidationError):
                validate_gameline("")

    def test_none_gameline(self):
        """None should raise ValidationError."""
        with self.assertRaises(ValidationError):
            validate_gameline(None)
