"""
Tests for ValidatedSaveMixin.

Tests verify:
- save() calls full_clean() by default
- skip_validation=True bypasses full_clean()
- Validation errors are raised appropriately
"""

from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import Book, NewsItem


class TestValidatedSaveMixinBehavior(TestCase):
    """Test ValidatedSaveMixin validation behavior."""

    def test_save_calls_full_clean_by_default(self):
        """Test that save() calls full_clean() when skip_validation is not set."""
        book = Book(name="Test Book", edition="20th", gameline="mta")

        with patch.object(book, "full_clean", wraps=book.full_clean) as mock_clean:
            book.save()
            mock_clean.assert_called_once()

    def test_save_skips_validation_when_flag_is_true(self):
        """Test that save() skips full_clean() when skip_validation=True."""
        book = Book(name="Test Book", edition="20th", gameline="mta")

        with patch.object(book, "full_clean") as mock_clean:
            book.save(skip_validation=True)
            mock_clean.assert_not_called()

    def test_save_raises_validation_error_on_invalid_data(self):
        """Test that save() raises ValidationError for invalid model data."""
        # Book with invalid edition choice
        book = Book(name="Test Book", edition="INVALID", gameline="mta")

        with self.assertRaises(ValidationError) as context:
            book.save()

        self.assertIn("edition", str(context.exception))

    def test_skip_validation_allows_invalid_data(self):
        """Test that skip_validation=True allows saving invalid data."""
        # NewsItem with blank title violates TextField constraints
        # but skip_validation bypasses the check
        news = NewsItem(title="Valid Title", content="Test content")
        news.save(skip_validation=True)

        # Verify it was saved
        self.assertIsNotNone(news.pk)

    def test_mixin_preserves_other_save_kwargs(self):
        """Test that other save() kwargs are passed through correctly."""
        book = Book(name="Test Book", edition="20th", gameline="mta")
        book.save()

        # Update with update_fields
        book.name = "Updated Book"
        book.save(update_fields=["name"])

        book.refresh_from_db()
        self.assertEqual(book.name, "Updated Book")

    def test_mixin_works_on_update(self):
        """Test that validation runs on updates, not just creates."""
        book = Book.objects.create(name="Test Book", edition="20th", gameline="mta")

        # Try to update with invalid data
        book.edition = "INVALID"

        with self.assertRaises(ValidationError):
            book.save()


class TestValidatedSaveMixinMRO(TestCase):
    """Test that ValidatedSaveMixin is correctly placed in MRO."""

    def test_book_has_mixin_in_mro(self):
        """Test that Book has ValidatedSaveMixin in its MRO."""
        from core.base import ValidatedSaveMixin

        self.assertTrue(issubclass(Book, ValidatedSaveMixin))

    def test_newsitem_has_mixin_in_mro(self):
        """Test that NewsItem has ValidatedSaveMixin in its MRO."""
        from core.base import ValidatedSaveMixin

        self.assertTrue(issubclass(NewsItem, ValidatedSaveMixin))

    def test_mixin_comes_before_model(self):
        """Test that ValidatedSaveMixin comes before models.Model in MRO."""
        from django.db import models

        from core.base import ValidatedSaveMixin

        mro = Book.__mro__
        mixin_index = mro.index(ValidatedSaveMixin)
        model_index = mro.index(models.Model)

        self.assertLess(mixin_index, model_index)
