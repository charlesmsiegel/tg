"""
Base model mixins and utilities.

This module contains foundational mixins that need to be importable
without triggering circular imports with other model files.
"""


class ValidatedSaveMixin:
    """
    Mixin that calls full_clean() on save for non-polymorphic models.

    The polymorphic Model class already has save() with validation.
    This mixin provides the same behavior for standalone models like
    Book, NewsItem, Language, etc. that don't inherit from Model.

    Usage:
        class Book(ValidatedSaveMixin, models.Model):
            ...
    """

    def save(self, *args, **kwargs):
        if not kwargs.pop("skip_validation", False):
            self.full_clean()
        super().save(*args, **kwargs)
