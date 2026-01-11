"""Tests for json_filters template tags."""

from django.test import TestCase

from core.templatetags.json_filters import get_item, pprint


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


class GetItemFilterTest(TestCase):
    """Tests for get_item filter."""

    def test_gets_item_from_dict(self):
        """Test filter gets item from dictionary by key."""
        data = {"name": "Test", "value": 123}

        result = get_item(data, "name")
        self.assertEqual(result, "Test")

        result = get_item(data, "value")
        self.assertEqual(result, 123)

    def test_returns_none_for_missing_key(self):
        """Test filter returns None for missing key."""
        data = {"name": "Test"}

        result = get_item(data, "missing")
        self.assertIsNone(result)

    def test_returns_none_for_none_dict(self):
        """Test filter returns None when dictionary is None."""
        result = get_item(None, "key")
        self.assertIsNone(result)

    def test_returns_none_for_non_dict(self):
        """Test filter returns None for non-dictionary values."""
        result = get_item("not a dict", "key")
        self.assertIsNone(result)

        result = get_item([1, 2, 3], "key")
        self.assertIsNone(result)

        result = get_item(123, "key")
        self.assertIsNone(result)

    def test_handles_nested_dict(self):
        """Test filter handles nested dictionary access."""
        data = {"outer": {"inner": "value"}}

        outer = get_item(data, "outer")
        self.assertEqual(outer, {"inner": "value"})

        # Can then get inner value
        inner = get_item(outer, "inner")
        self.assertEqual(inner, "value")

    def test_handles_various_key_types(self):
        """Test filter handles various key types."""
        data = {"string_key": 1, 123: 2, (1, 2): 3}

        result = get_item(data, "string_key")
        self.assertEqual(result, 1)

        result = get_item(data, 123)
        self.assertEqual(result, 2)

    def test_handles_none_value_in_dict(self):
        """Test filter correctly returns None when value is None."""
        data = {"key": None}

        result = get_item(data, "key")
        self.assertIsNone(result)

    def test_handles_empty_dict(self):
        """Test filter handles empty dictionary."""
        result = get_item({}, "key")
        self.assertIsNone(result)

    def test_handles_falsy_values(self):
        """Test filter correctly returns falsy values."""
        data = {"zero": 0, "empty_str": "", "false": False, "empty_list": []}

        result = get_item(data, "zero")
        self.assertEqual(result, 0)

        result = get_item(data, "empty_str")
        self.assertEqual(result, "")

        result = get_item(data, "false")
        self.assertFalse(result)

        result = get_item(data, "empty_list")
        self.assertEqual(result, [])
