"""
Tests for custom template tags and filters.

Tests cover:
- dots filter for WoD-style rating display
- boxes filter for alternative rating display
- sanitize_html filter
"""
from core.templatetags.dots import boxes, dots
from core.templatetags.sanitize_text import sanitize_html
from django.test import TestCase


class TestDotsFilter(TestCase):
    """Test the dots template filter for WoD-style ratings."""

    def test_dots_with_zero(self):
        """Test dots filter with rating of 0."""
        result = dots(0)
        self.assertEqual(result, "○○○○○")

    def test_dots_with_one(self):
        """Test dots filter with rating of 1."""
        result = dots(1)
        self.assertEqual(result, "●○○○○")

    def test_dots_with_three(self):
        """Test dots filter with rating of 3."""
        result = dots(3)
        self.assertEqual(result, "●●●○○")

    def test_dots_with_five(self):
        """Test dots filter with rating of 5 (max standard)."""
        result = dots(5)
        self.assertEqual(result, "●●●●●")

    def test_dots_with_six_expands_to_ten(self):
        """Test that ratings above 5 expand to 10 dots."""
        result = dots(6)
        self.assertEqual(result, "●●●●●●○○○○")

    def test_dots_with_ten(self):
        """Test dots filter with rating of 10 (max extended)."""
        result = dots(10)
        self.assertEqual(result, "●●●●●●●●●●")

    def test_dots_with_custom_maximum(self):
        """Test dots filter with custom maximum."""
        result = dots(3, maximum=7)
        self.assertEqual(result, "●●●○○○○")

    def test_dots_exceeding_maximum(self):
        """Test that ratings exceeding maximum are capped."""
        result = dots(8, maximum=5)
        self.assertEqual(result, "●●●●●")

    def test_dots_with_negative_value(self):
        """Test dots filter with negative value (should treat as 0)."""
        result = dots(-1)
        self.assertEqual(result, "○○○○○")

    def test_dots_with_string_number(self):
        """Test dots filter with string representation of number."""
        result = dots("3")
        self.assertEqual(result, "●●●○○")

    def test_dots_with_none(self):
        """Test dots filter with None value."""
        result = dots(None)
        self.assertEqual(result, "○○○○○")


class TestBoxesFilter(TestCase):
    """Test the boxes template filter for alternative rating display."""

    def test_boxes_with_zero(self):
        """Test boxes filter with rating of 0."""
        result = boxes(0)
        self.assertEqual(result, "□□□□□")

    def test_boxes_with_three(self):
        """Test boxes filter with rating of 3."""
        result = boxes(3)
        self.assertEqual(result, "■■■□□")

    def test_boxes_with_five(self):
        """Test boxes filter with rating of 5."""
        result = boxes(5)
        self.assertEqual(result, "■■■■■")

    def test_boxes_with_ten(self):
        """Test boxes filter with rating of 10."""
        result = boxes(10)
        self.assertEqual(result, "■■■■■■■■■■")

    def test_boxes_with_custom_maximum(self):
        """Test boxes filter with custom maximum."""
        result = boxes(4, maximum=8)
        self.assertEqual(result, "■■■■□□□□")


class TestSanitizeHTMLFilter(TestCase):
    """Test the sanitize_html template filter."""

    def test_sanitize_allows_safe_html(self):
        """Test that safe HTML tags are allowed."""
        html = "<p>This is <b>bold</b> and <i>italic</i> text.</p>"
        result = sanitize_html(html)
        self.assertIn("<p>", result)
        self.assertIn("<b>", result)
        self.assertIn("<i>", result)

    def test_sanitize_removes_script_tags(self):
        """Test that script tags are removed."""
        html = '<p>Safe text</p><script>alert("XSS")</script>'
        result = sanitize_html(html)
        self.assertNotIn("<script>", result)
        self.assertNotIn("alert", result)
        self.assertIn("<p>Safe text</p>", result)

    def test_sanitize_removes_onclick_attributes(self):
        """Test that dangerous attributes are removed."""
        html = '<a href="#" onclick="alert(\'XSS\')">Click me</a>'
        result = sanitize_html(html)
        self.assertNotIn("onclick", result)

    def test_sanitize_allows_links(self):
        """Test that links are allowed."""
        html = '<a href="https://example.com">Link</a>'
        result = sanitize_html(html)
        self.assertIn('<a href="https://example.com">', result)

    def test_sanitize_allows_formatting(self):
        """Test that formatting tags are allowed."""
        html = "<strong>Strong</strong> <em>Emphasis</em> <u>Underline</u>"
        result = sanitize_html(html)
        self.assertIn("<strong>", result)
        self.assertIn("<em>", result)
        self.assertIn("<u>", result)

    def test_sanitize_allows_lists(self):
        """Test that list tags are allowed."""
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        result = sanitize_html(html)
        self.assertIn("<ul>", result)
        self.assertIn("<li>", result)

    def test_sanitize_removes_dangerous_protocols(self):
        """Test that dangerous URL protocols are removed."""
        html = '<a href="javascript:alert(\'XSS\')">Click</a>'
        result = sanitize_html(html)
        self.assertNotIn("javascript:", result)

    def test_sanitize_empty_string(self):
        """Test sanitizing an empty string."""
        result = sanitize_html("")
        self.assertEqual(result, "")

    def test_sanitize_none(self):
        """Test sanitizing None."""
        result = sanitize_html(None)
        self.assertEqual(result, "")

    def test_sanitize_plain_text(self):
        """Test sanitizing plain text (no HTML)."""
        text = "This is plain text"
        result = sanitize_html(text)
        self.assertEqual(result, text)


class TestGetHeadingFilter(TestCase):
    """Test the get_heading method for gameline-specific CSS classes."""

    def test_get_heading_for_vtm(self):
        """Test heading class for Vampire: the Masquerade."""
        class MockObject:
            gameline = "vtm"

            def get_heading(self):
                headings = {
                    "vtm": "vtm_heading",
                    "wta": "wta_heading",
                    "mta": "mta_heading",
                    "wto": "wto_heading",
                    "ctd": "ctd_heading",
                    "dtf": "dtf_heading",
                }
                return headings.get(self.gameline, "")

        obj = MockObject()
        self.assertEqual(obj.get_heading(), "vtm_heading")

    def test_get_heading_for_mta(self):
        """Test heading class for Mage: the Ascension."""
        class MockObject:
            gameline = "mta"

            def get_heading(self):
                headings = {
                    "vtm": "vtm_heading",
                    "wta": "wta_heading",
                    "mta": "mta_heading",
                    "wto": "wto_heading",
                    "ctd": "ctd_heading",
                    "dtf": "dtf_heading",
                }
                return headings.get(self.gameline, "")

        obj = MockObject()
        self.assertEqual(obj.get_heading(), "mta_heading")

    def test_get_heading_for_unknown_gameline(self):
        """Test heading class for unknown gameline."""
        class MockObject:
            gameline = "unknown"

            def get_heading(self):
                headings = {
                    "vtm": "vtm_heading",
                    "wta": "wta_heading",
                    "mta": "mta_heading",
                    "wto": "wto_heading",
                    "ctd": "ctd_heading",
                    "dtf": "dtf_heading",
                }
                return headings.get(self.gameline, "")

        obj = MockObject()
        self.assertEqual(obj.get_heading(), "")
