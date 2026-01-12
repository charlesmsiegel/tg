"""
Shared constants for character forms.

This module contains reusable constants used across multiple form modules
to avoid duplication and ensure consistency.
"""

# Base category choices for freebie spending forms
BASE_CATEGORY_CHOICES = [
    ("-----", "-----"),
    ("Attribute", "Attribute"),
    ("Ability", "Ability"),
    ("Background", "Background"),
    ("Willpower", "Willpower"),
    ("MeritFlaw", "MeritFlaw"),
]

# Extended category choices for XP spending forms (includes Image)
XP_CATEGORY_CHOICES = [
    ("-----", "-----"),
    ("Image", "Image"),
    ("Attribute", "Attribute"),
    ("Ability", "Ability"),
    ("Background", "Background"),
    ("Willpower", "Willpower"),
    ("MeritFlaw", "MeritFlaw"),
]
