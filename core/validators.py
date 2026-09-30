"""
Shared validators for Django models.

This module contains reusable validators for common validation patterns
across the application.
"""

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_non_empty_name(value, field_name="Name"):
    """
    Validate that a name field is not empty or whitespace-only.

    Args:
        value: The value to validate
        field_name: The field name for the error message (default: "Name")

    Raises:
        ValidationError: If the value is empty or whitespace-only
    """
    if value is None or not str(value).strip():
        raise ValidationError(f"{field_name} is required", code="required")


def validate_gameline(value):
    """
    Validate that a gameline value is in the valid choices.

    Args:
        value: The gameline code to validate

    Raises:
        ValidationError: If the gameline is None or not a valid choice
    """
    if value is None:
        raise ValidationError("Gameline is required", code="required")

    valid_gamelines = [code for code, _ in settings.GAMELINE_CHOICES]
    if value not in valid_gamelines:
        raise ValidationError(
            f"Invalid gameline '{value}'. Must be one of: {', '.join(valid_gamelines)}",
            code="invalid_choice",
        )


def validate_image_upload_size(value):
    """Reject a newly uploaded image larger than ``settings.MAX_IMAGE_UPLOAD_SIZE``.

    Files already stored are not re-checked, so saving an object never has to read its
    existing image from storage.
    """
    if not value or getattr(value, "_committed", False):
        return
    limit = settings.MAX_IMAGE_UPLOAD_SIZE
    size = getattr(value, "size", None)
    if size is not None and size > limit:
        raise ValidationError(
            f"Images may be at most {limit // (1024 * 1024)} MB.", code="file_too_large"
        )
