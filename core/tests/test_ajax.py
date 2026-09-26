"""Tests for AJAX utility functions in core.ajax module."""

import json

from django.test import SimpleTestCase

from core.ajax import dropdown_options_response


class MockObject:
    """Mock object for testing dropdown_options_response."""

    def __init__(self, pk, name, custom_attr=None):
        self.pk = pk
        self.name = name
        self.custom_attr = custom_attr

    def __str__(self):
        return f"Str: {self.name}"


class TestDropdownOptionsResponse(SimpleTestCase):
    """Tests for dropdown_options_response function."""

    def test_empty_queryset(self):
        """Test with empty queryset returns empty options list."""
        response = dropdown_options_response([])
        data = json.loads(response.content)
        self.assertEqual(data, {"options": []})

    def test_default_attributes(self):
        """Test with default pk and name attributes."""
        objects = [
            MockObject(pk=1, name="First"),
            MockObject(pk=2, name="Second"),
        ]
        response = dropdown_options_response(objects)
        data = json.loads(response.content)

        self.assertEqual(len(data["options"]), 2)
        self.assertEqual(data["options"][0], {"value": 1, "label": "First"})
        self.assertEqual(data["options"][1], {"value": 2, "label": "Second"})

    def test_str_label_attr(self):
        """Test using __str__ for label."""
        objects = [MockObject(pk=1, name="Test")]
        response = dropdown_options_response(objects, label_attr="__str__")
        data = json.loads(response.content)

        self.assertEqual(data["options"][0]["label"], "Str: Test")

    def test_custom_value_attr(self):
        """Test using custom attribute for value."""
        objects = [MockObject(pk=1, name="Test", custom_attr="custom_value")]
        response = dropdown_options_response(objects, value_attr="custom_attr")
        data = json.loads(response.content)

        self.assertEqual(data["options"][0]["value"], "custom_value")

    def test_custom_label_attr(self):
        """Test using custom attribute for label."""
        objects = [MockObject(pk=1, name="Test", custom_attr="Custom Label")]
        response = dropdown_options_response(objects, label_attr="custom_attr")
        data = json.loads(response.content)

        self.assertEqual(data["options"][0]["label"], "Custom Label")

    def test_returns_json_response(self):
        """Test that function returns a proper JsonResponse."""
        response = dropdown_options_response([])
        self.assertEqual(response["Content-Type"], "application/json")

    def test_preserves_order(self):
        """Test that options maintain queryset order."""
        objects = [
            MockObject(pk=3, name="Third"),
            MockObject(pk=1, name="First"),
            MockObject(pk=2, name="Second"),
        ]
        response = dropdown_options_response(objects)
        data = json.loads(response.content)

        # Order should be preserved
        self.assertEqual(data["options"][0]["label"], "Third")
        self.assertEqual(data["options"][1]["label"], "First")
        self.assertEqual(data["options"][2]["label"], "Second")
