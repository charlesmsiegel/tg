"""Tests for sanitize_text template tags."""

from core.templatetags.sanitize_text import (
    badge_text,
    quote_tag,
    sanitize_html,
    simple_markdown,
)
from django.test import TestCase


class SanitizeHTMLFilterTest(TestCase):
    """Tests for sanitize_html filter."""

    def test_returns_empty_string_for_none(self):
        """Test filter returns empty string for None input."""
        result = sanitize_html(None)
        self.assertEqual(result, "")

    def test_returns_empty_string_for_empty_string(self):
        """Test filter returns empty string for empty input."""
        result = sanitize_html("")
        self.assertEqual(result, "")

    def test_converts_non_string_to_string(self):
        """Test filter converts non-string types to string."""
        result = sanitize_html(123)
        self.assertEqual(result, "123")

    def test_preserves_allowed_tags(self):
        """Test filter preserves allowed HTML tags."""
        allowed_tags = ["a", "b", "i", "em", "strong", "u", "p", "br", "strike", "ul", "li", "span"]
        for tag in allowed_tags:
            html = f"<{tag}>content</{tag}>"
            result = sanitize_html(html)
            self.assertIn(f"<{tag}>", result, f"Tag {tag} should be preserved")

    def test_allows_anchor_href(self):
        """Test filter allows href attribute on anchor tags."""
        html = '<a href="https://example.com">Link</a>'
        result = sanitize_html(html)
        self.assertIn('href="https://example.com"', result)

    def test_allows_span_with_quote_class(self):
        """Test filter allows span with class='quote'."""
        html = '<span class="quote">Quoted text</span>'
        result = sanitize_html(html)
        self.assertIn('class="quote"', result)

    def test_strips_disallowed_span_classes(self):
        """Test filter strips span classes other than 'quote'."""
        html = '<span class="danger">Text</span>'
        result = sanitize_html(html)
        self.assertNotIn('class="danger"', result)
        self.assertIn("<span>", result)

    def test_removes_script_tags(self):
        """Test filter removes script tags."""
        html = '<script>alert("XSS")</script>Safe text'
        result = sanitize_html(html)
        self.assertNotIn("<script>", result)
        self.assertIn("Safe text", result)

    def test_removes_onclick_attributes(self):
        """Test filter removes dangerous onclick attributes."""
        html = '<a href="#" onclick="alert(1)">Click</a>'
        result = sanitize_html(html)
        self.assertNotIn("onclick", result)

    def test_allows_http_protocol(self):
        """Test filter allows http protocol in links."""
        html = '<a href="http://example.com">Link</a>'
        result = sanitize_html(html)
        self.assertIn("http://example.com", result)

    def test_allows_https_protocol(self):
        """Test filter allows https protocol in links."""
        html = '<a href="https://example.com">Link</a>'
        result = sanitize_html(html)
        self.assertIn("https://example.com", result)

    def test_allows_mailto_protocol(self):
        """Test filter allows mailto protocol in links."""
        html = '<a href="mailto:test@example.com">Email</a>'
        result = sanitize_html(html)
        self.assertIn("mailto:test@example.com", result)

    def test_strips_javascript_protocol(self):
        """Test filter strips javascript protocol from links."""
        html = '<a href="javascript:alert(1)">Click</a>'
        result = sanitize_html(html)
        self.assertNotIn("javascript:", result)

    def test_strips_data_protocol(self):
        """Test filter strips data protocol from links."""
        html = '<a href="data:text/html,<script>alert(1)</script>">Link</a>'
        result = sanitize_html(html)
        self.assertNotIn("data:", result)

    def test_returns_marked_safe_html(self):
        """Test filter returns marked safe HTML."""
        from django.utils.safestring import SafeString

        html = "<p>Test</p>"
        result = sanitize_html(html)
        self.assertIsInstance(result, SafeString)

    def test_preserves_plain_text(self):
        """Test filter preserves plain text without HTML."""
        text = "This is plain text"
        result = sanitize_html(text)
        self.assertEqual(result, text)


class QuoteTagFilterTest(TestCase):
    """Tests for quote_tag filter."""

    def test_wraps_quoted_text_in_span(self):
        """Test filter wraps quoted text in span tags."""
        text = 'He said "hello" to her.'
        result = quote_tag(text)
        self.assertIn('<span class="quote">"hello"</span>', result)

    def test_wraps_multiple_quotes(self):
        """Test filter wraps multiple quoted sections."""
        text = '"First" and "Second" quotes.'
        result = quote_tag(text)
        self.assertIn('<span class="quote">"First"</span>', result)
        self.assertIn('<span class="quote">"Second"</span>', result)

    def test_returns_non_string_unchanged(self):
        """Test filter returns non-string values unchanged."""
        result = quote_tag(123)
        self.assertEqual(result, 123)

        result = quote_tag(None)
        self.assertIsNone(result)

    def test_handles_empty_quotes(self):
        """Test filter handles empty quotes."""
        text = 'Empty "" quotes'
        result = quote_tag(text)
        self.assertIn('<span class="quote">""</span>', result)

    def test_preserves_text_outside_quotes(self):
        """Test filter preserves text outside quotes."""
        text = 'Before "quoted" after'
        result = quote_tag(text)
        self.assertIn("Before", result)
        self.assertIn("after", result)

    def test_handles_text_without_quotes(self):
        """Test filter handles text without any quotes."""
        text = "No quotes here"
        result = quote_tag(text)
        self.assertEqual(result, text)


class SimpleMarkdownFilterTest(TestCase):
    """Tests for simple_markdown filter."""

    def test_returns_empty_string_for_none(self):
        """Test filter returns empty string for None input."""
        result = simple_markdown(None)
        self.assertEqual(result, "")

    def test_returns_empty_string_for_empty_string(self):
        """Test filter returns empty string for empty input."""
        result = simple_markdown("")
        self.assertEqual(result, "")

    def test_converts_non_string_to_string(self):
        """Test filter converts non-string types to string."""
        result = simple_markdown(123)
        self.assertIn("123", result)

    def test_converts_bold_markdown(self):
        """Test filter converts **bold** to <strong>."""
        text = "This is **bold** text."
        result = simple_markdown(text)
        self.assertIn("<strong>bold</strong>", result)

    def test_converts_italic_markdown(self):
        """Test filter converts *italic* to <em>."""
        text = "This is *italic* text."
        result = simple_markdown(text)
        self.assertIn("<em>italic</em>", result)

    def test_bold_not_confused_with_italic(self):
        """Test filter handles bold and italic together correctly."""
        text = "**bold** and *italic* text"
        result = simple_markdown(text)
        self.assertIn("<strong>bold</strong>", result)
        self.assertIn("<em>italic</em>", result)

    def test_converts_line_breaks(self):
        """Test filter converts newlines to <br> tags."""
        text = "Line 1\nLine 2"
        result = simple_markdown(text)
        self.assertIn("<br>", result)

    def test_converts_double_newlines_to_paragraphs(self):
        """Test filter converts double newlines to paragraph breaks."""
        text = "Paragraph 1\n\nParagraph 2"
        result = simple_markdown(text)
        self.assertIn("</p>", result)
        self.assertIn("<p>", result)

    def test_wraps_in_paragraph_tags(self):
        """Test filter wraps content in paragraph tags."""
        text = "Some text"
        result = simple_markdown(text)
        self.assertTrue(result.startswith("<p>"))
        self.assertTrue(result.endswith("</p>"))

    def test_normalizes_windows_line_endings(self):
        """Test filter normalizes Windows line endings."""
        text = "Line 1\r\nLine 2"
        result = simple_markdown(text)
        self.assertNotIn("\r", result)

    def test_returns_marked_safe_html(self):
        """Test filter returns marked safe HTML."""
        from django.utils.safestring import SafeString

        text = "Test"
        result = simple_markdown(text)
        self.assertIsInstance(result, SafeString)


class BadgeTextFilterTest(TestCase):
    """Tests for badge_text filter."""

    def test_returns_empty_string_for_none(self):
        """Test filter returns empty string for None input."""
        result = badge_text(None)
        self.assertEqual(result, "")

    def test_returns_empty_string_for_empty_string(self):
        """Test filter returns empty string for empty input."""
        result = badge_text("")
        self.assertEqual(result, "")

    def test_converts_non_string_to_string(self):
        """Test filter converts non-string types to string."""
        result = badge_text(123)
        self.assertEqual(result, "123")

    def test_replaces_underscores_with_spaces(self):
        """Test filter replaces underscores with spaces."""
        text = "some_text_here"
        result = badge_text(text)
        self.assertNotIn("_", result)
        self.assertIn(" ", result)

    def test_capitalizes_each_word(self):
        """Test filter capitalizes each word (title case)."""
        text = "hello_world"
        result = badge_text(text)
        self.assertEqual(result, "Hello World")

    def test_handles_multiple_underscores(self):
        """Test filter handles multiple underscores."""
        text = "one_two_three_four"
        result = badge_text(text)
        self.assertEqual(result, "One Two Three Four")

    def test_handles_already_capitalized(self):
        """Test filter handles already capitalized text."""
        text = "ALREADY_CAPS"
        result = badge_text(text)
        self.assertEqual(result, "Already Caps")

    def test_handles_single_word(self):
        """Test filter handles single word without underscores."""
        text = "word"
        result = badge_text(text)
        self.assertEqual(result, "Word")

    def test_example_autumn_person(self):
        """Test filter with example from docstring."""
        text = "autumn_person"
        result = badge_text(text)
        self.assertEqual(result, "Autumn Person")
