"""Tests for json_filters template tags."""

from django.test import TestCase

from core.templatetags.json_filters import pprint


class PPrintFilterTest(TestCase):
    """Tests for pprint filter."""

    def test_pretty_prints_dict(self):
        """Test filter pretty prints dictionary."""
        data = {"name": "Test", "value": 123}
        result = pprint(data)

        # Should have proper indentation
        self.assertIn('"name"', result)
        self.assertIn('"value"', result)
        self.assertIn("123", result)
        # Check for indentation (2 spaces)
        self.assertIn("  ", result)

    def test_pretty_prints_list(self):
        """Test filter pretty prints list."""
        data = [1, 2, 3]
        result = pprint(data)

        self.assertIn("1", result)
        self.assertIn("2", result)
        self.assertIn("3", result)

    def test_pretty_prints_nested_structure(self):
        """Test filter pretty prints nested structures."""
        data = {"outer": {"inner": "value"}}
        result = pprint(data)

        self.assertIn('"outer"', result)
        self.assertIn('"inner"', result)
        self.assertIn('"value"', result)

    def test_handles_json_string_input(self):
        """Test filter handles JSON string input."""
        json_str = '{"key": "value"}'
        result = pprint(json_str)

        # Should parse and re-format the JSON string
        self.assertIn('"key"', result)
        self.assertIn('"value"', result)

    def test_handles_invalid_json_string(self):
        """Test filter handles invalid JSON string gracefully."""
        invalid_json = "not valid json"
        result = pprint(invalid_json)

        # Should return string representation
        self.assertEqual(result, invalid_json)

    def test_handles_none(self):
        """Test filter handles None value."""
        result = pprint(None)
        self.assertEqual(result, "null")

    def test_handles_integer(self):
        """Test filter handles integer value."""
        result = pprint(42)
        self.assertEqual(result, "42")

    def test_handles_boolean(self):
        """Test filter handles boolean values."""
        result = pprint(True)
        self.assertEqual(result, "true")

        result = pprint(False)
        self.assertEqual(result, "false")

    def test_preserves_unicode(self):
        """Test filter preserves unicode characters."""
        data = {"name": "Teszt"}
        result = pprint(data)

        self.assertIn("Teszt", result)

    def test_handles_empty_dict(self):
        """Test filter handles empty dictionary."""
        result = pprint({})
        self.assertEqual(result, "{}")

    def test_handles_empty_list(self):
        """Test filter handles empty list."""
        result = pprint([])
        self.assertEqual(result, "[]")

    def test_handles_type_error(self):
        """Test filter handles objects that can't be serialized."""

        class NonSerializable:
            pass

        result = pprint(NonSerializable())

        # Should return string representation
        self.assertIn("NonSerializable", result)
