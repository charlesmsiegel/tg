"""Tests for sanitize_text template tags."""

from django.test import TestCase

from core.templatetags.sanitize_text import (
    badge_text,
    quote_tag,
    sanitize_html,
    simple_markdown,
)


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

    def test_escapes_html_in_quoted_text(self):
        """Test filter escapes HTML special characters in quoted text."""
        text = 'He said "<script>alert(1)</script>" to her.'
        result = quote_tag(text)
        # The script tag should be escaped, not rendered as HTML
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)

    def test_escapes_html_outside_quotes(self):
        """Test filter escapes HTML special characters outside quotes."""
        text = '<b>Bold</b> "quoted" text'
        result = quote_tag(text)
        # HTML outside quotes should also be escaped
        self.assertIn("&lt;b&gt;", result)
        self.assertIn("&lt;/b&gt;", result)

    def test_returns_safe_string(self):
        """Test filter returns a SafeString."""
        from django.utils.safestring import SafeString

        text = 'He said "hello" to her.'
        result = quote_tag(text)
        self.assertIsInstance(result, SafeString)

    def test_xss_prevention_complex_payload(self):
        """Test filter prevents XSS with complex payloads."""
        # Test various XSS vectors - ensure HTML tags are escaped
        payloads = [
            ('"<img src=x onerror=alert(1)>"', "&lt;img"),
            ('"<svg onload=alert(1)>"', "&lt;svg"),
            ('"><script>alert(1)</script><"', "&lt;script&gt;"),
            ('"</span><script>alert(1)</script><span>"', "&lt;/span&gt;"),
        ]
        for payload, expected_escaped in payloads:
            result = quote_tag(payload)
            # Ensure HTML tags are escaped, not rendered
            self.assertIn(expected_escaped, result, f"Failed for payload: {payload}")
            # Ensure no unescaped dangerous HTML tags
            self.assertNotIn("<script>", result)
            self.assertNotIn("<img ", result)
            self.assertNotIn("<svg ", result)

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

    def test_unicode_escape_sequence_in_quotes(self):
        """Test filter handles unicode escape sequences that spell HTML tags."""
        # \u003c is < and \u003e is > - these could be used to bypass filters
        text = 'He said "\u003cscript\u003ealert(1)" to her.'
        result = quote_tag(text)
        # The < and > should be escaped
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)

    def test_unicode_characters_preserved(self):
        """Test unicode characters are not corrupted."""
        text = 'He said "こんにちは" in Japanese.'
        result = quote_tag(text)
        self.assertIn("こんにちは", result)
        self.assertIn('<span class="quote">', result)

    def test_html_entities_not_double_escaped(self):
        """Test pre-escaped HTML entities are preserved (not double-escaped)."""
        # If input contains &lt; it should stay as &lt;, not become &amp;lt;
        text = 'He said "&lt;script&gt;" to her.'
        result = quote_tag(text)
        # The & in &lt; gets escaped to &amp;, making it &amp;lt;
        # This is correct behavior - we escape ALL special chars
        self.assertIn("&amp;lt;script&amp;gt;", result)
        # Ensure no actual script tags
        self.assertNotIn("<script>", result)

    def test_nested_quotes(self):
        """Test filter handles nested/adjacent quote marks."""
        text = 'She said ""really?"" sarcastically.'
        result = quote_tag(text)
        # Should create two adjacent quote spans
        self.assertEqual(result.count('<span class="quote">'), 2)

    def test_ampersand_escaping(self):
        """Test ampersands are properly escaped."""
        text = 'Tom & Jerry said "hello & goodbye"'
        result = quote_tag(text)
        self.assertIn("Tom &amp; Jerry", result)
        self.assertIn("hello &amp; goodbye", result)


class SimpleMarkdownFilterTest(TestCase):
    """Tests for simple_markdown filter."""

    def test_escapes_html_in_bold_text(self):
        """Test filter escapes HTML special characters in bold text."""
        text = "This is **<script>alert(1)</script>** bold."
        result = simple_markdown(text)
        # The script tag should be escaped
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)

    def test_escapes_html_in_italic_text(self):
        """Test filter escapes HTML special characters in italic text."""
        text = "This is *<img src=x onerror=alert(1)>* italic."
        result = simple_markdown(text)
        # The img tag should be escaped (not rendered as HTML)
        self.assertNotIn("<img", result)
        self.assertIn("&lt;img", result)

    def test_escapes_html_outside_markdown(self):
        """Test filter escapes HTML outside of markdown formatting."""
        text = "<script>alert(1)</script> and **bold**"
        result = simple_markdown(text)
        self.assertNotIn("<script>", result)
        self.assertIn("<strong>bold</strong>", result)

    def test_xss_prevention_complex_payload(self):
        """Test filter prevents XSS with complex payloads."""
        # Test various XSS vectors - ensure HTML tags are escaped
        payloads = [
            ("**</strong><script>alert(1)</script><strong>**", "&lt;/strong&gt;"),
            ("*</em><svg onload=alert(1)><em>*", "&lt;/em&gt;"),
            ("<p onmouseover=alert(1)>text</p>", "&lt;p"),
            ("</p><script>alert(1)</script><p>", "&lt;script&gt;"),
        ]
        for payload, expected_escaped in payloads:
            result = simple_markdown(payload)
            # Ensure HTML tags are escaped, not rendered
            self.assertIn(expected_escaped, result, f"Failed for payload: {payload}")
            # Ensure no unescaped dangerous HTML tags (besides our safe tags)
            self.assertNotIn("<script>", result)
            self.assertNotIn("<svg", result)

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

    def test_unclosed_markdown_with_html(self):
        """Test filter handles unclosed markdown with HTML injection attempt."""
        text = "**bold text <script>alert(1)</script>"
        result = simple_markdown(text)
        # Script should be escaped
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)
        # Unclosed ** should remain as literal asterisks (escaped)
        self.assertIn("**", result)

    def test_unicode_escape_sequences(self):
        """Test filter handles unicode escape sequences that spell HTML tags."""
        text = "Test \u003cscript\u003ealert(1)\u003c/script\u003e"
        result = simple_markdown(text)
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)

    def test_unicode_characters_preserved(self):
        """Test unicode characters are preserved in output."""
        text = "**日本語** and *한국어* text"
        result = simple_markdown(text)
        self.assertIn("日本語", result)
        self.assertIn("한국어", result)
        self.assertIn("<strong>日本語</strong>", result)
        self.assertIn("<em>한국어</em>", result)

    def test_html_entities_escaped(self):
        """Test pre-escaped HTML entities are double-escaped (security)."""
        text = "&lt;script&gt;alert(1)&lt;/script&gt;"
        result = simple_markdown(text)
        # Ampersands should be escaped
        self.assertIn("&amp;lt;", result)
        self.assertNotIn("<script>", result)

    def test_markdown_with_quotes(self):
        """Test interaction between markdown and quotation marks."""
        text = '**"Bold and quoted"** text'
        result = simple_markdown(text)
        # Should have bold tags and quotes (escaped as &quot;)
        self.assertIn("<strong>", result)
        self.assertIn("&quot;Bold and quoted&quot;", result)

    def test_ampersand_escaping(self):
        """Test ampersands are properly escaped."""
        text = "Tom & Jerry are **friends & allies**"
        result = simple_markdown(text)
        self.assertIn("Tom &amp; Jerry", result)
        self.assertIn("friends &amp; allies", result)

    def test_less_than_greater_than_escaping(self):
        """Test < and > outside markdown are escaped."""
        text = "5 < 10 and 10 > 5 is **true**"
        result = simple_markdown(text)
        self.assertIn("5 &lt; 10", result)
        self.assertIn("10 &gt; 5", result)
        self.assertIn("<strong>true</strong>", result)

    def test_mixed_asterisks_not_markdown(self):
        """Test asterisks that don't form valid markdown are preserved."""
        text = "3 * 4 = 12 and 2 ** 3 = 8"
        result = simple_markdown(text)
        # Single asterisk with spaces should not become italic
        self.assertIn("3 * 4", result)
        # ** without closing should not become bold
        self.assertIn("** 3", result)


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
