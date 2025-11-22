# Core App - Code Style Guide

## Overview

This document outlines coding standards specific to the `core` app, which provides foundational components for the entire TG project.

## General Principles

1. **Minimal Dependencies**: Core should have minimal external dependencies since all other apps depend on it
2. **Backward Compatibility**: Changes to core affect all apps - maintain strict backward compatibility
3. **Generic Design**: Core components should be generic and reusable, not tied to specific gamelines
4. **Well-Tested**: Core utilities must have comprehensive test coverage

## File Organization

### Models (`models.py`)

All core models should extend Django Polymorphic's `PolymorphicModel`:

```python
from polymorphic.models import PolymorphicModel
from django.db import models

class Model(PolymorphicModel):
    """Base model for all polymorphic models in the project."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = False
        ordering = ['name']

    def __str__(self):
        return self.name
```

**Best Practices:**
- Always define `__str__()` method
- Use `blank=True, null=True` for optional text fields
- Add `verbose_name` and `verbose_name_plural` in Meta
- Include docstrings for complex models

### Utilities (`utils.py`)

Organize utility functions by purpose with clear docstrings:

```python
def get_gameline_display(gameline_code):
    """
    Convert gameline code to display name.

    Args:
        gameline_code (str): Short code like 'vtm', 'wta'

    Returns:
        str: Full name like 'Vampire: The Masquerade'
    """
    gameline_map = {
        'vtm': 'Vampire: The Masquerade',
        'wta': 'Werewolf: The Apocalypse',
        # ...
    }
    return gameline_map.get(gameline_code, gameline_code)
```

**Best Practices:**
- One utility per function (avoid multi-purpose utilities)
- Include type hints where helpful
- Add comprehensive docstrings with Args/Returns
- Group related utilities together
- Avoid dependencies on other apps

### Constants (`constants.py`)

Use uppercase for constants and organize by category:

```python
# Attributes
PHYSICAL_ATTRIBUTES = ['Strength', 'Dexterity', 'Stamina']
SOCIAL_ATTRIBUTES = ['Charisma', 'Manipulation', 'Appearance']
MENTAL_ATTRIBUTES = ['Perception', 'Intelligence', 'Wits']
ATTRIBUTES = PHYSICAL_ATTRIBUTES + SOCIAL_ATTRIBUTES + MENTAL_ATTRIBUTES

# Status choices
STATUS_UN = 'Un'
STATUS_SUB = 'Sub'
STATUS_APP = 'App'
STATUS_RET = 'Ret'
STATUS_DEC = 'Dec'

STATUS_CHOICES = [
    (STATUS_UN, 'Unfinished'),
    (STATUS_SUB, 'Submitted'),
    (STATUS_APP, 'Approved'),
    (STATUS_RET, 'Retired'),
    (STATUS_DEC, 'Deceased'),
]
```

**Best Practices:**
- Group related constants together
- Use descriptive names
- Provide both code and display values for choices
- Document any non-obvious constants

### Permissions (`permissions.py`)

Permission functions should return boolean values:

```python
def user_can_edit_object(user, obj):
    """
    Check if user has permission to edit an object.

    Args:
        user: Django User instance
        obj: Any model instance with 'owner' attribute

    Returns:
        bool: True if user can edit, False otherwise
    """
    if user.is_superuser:
        return True
    if hasattr(obj, 'owner') and obj.owner == user:
        return True
    if hasattr(obj, 'chronicle'):
        # Check if user is ST of the chronicle
        return obj.chronicle.storytellers.filter(id=user.id).exists()
    return False
```

**Best Practices:**
- Clear function names starting with `user_can_` or `has_`
- Return boolean only
- Check permissions in order: superuser → owner → storyteller → False
- Handle missing attributes gracefully

### Decorators (`decorators.py`)

Decorators should be reusable and well-documented:

```python
from functools import wraps
from django.core.exceptions import PermissionDenied

def require_storyteller(view_func):
    """
    Decorator that requires user to be a storyteller.

    Usage:
        @require_storyteller
        def my_view(request):
            # Only accessible to storytellers
            pass
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'profile'):
            raise PermissionDenied("User must have a profile")
        if not request.user.profile.is_st():
            raise PermissionDenied("User must be a storyteller")
        return view_func(request, *args, **kwargs)
    return wrapper
```

**Best Practices:**
- Always use `@wraps(view_func)` to preserve function metadata
- Raise appropriate exceptions (`PermissionDenied`, `Http404`)
- Include usage examples in docstring
- Keep decorators focused on single responsibility

### Template Tags

Template tag files should follow Django conventions:

```python
from django import template

register = template.Library()

@register.filter(name='dots')
def dots(value, max_dots=None):
    """
    Convert numeric rating to WoD-style dots.

    Usage:
        {{ character.strength|dots }}
        {{ trait.rating|dots:10 }}

    Args:
        value: Numeric rating (0-10)
        max_dots: Maximum dots to display (auto-expands if needed)

    Returns:
        str: Unicode dot characters (●●●○○)
    """
    if not isinstance(value, int):
        return ''

    if max_dots is None:
        max_dots = 10 if value > 5 else 5

    filled = '●' * value
    empty = '○' * (max_dots - value)
    return filled + empty
```

**Best Practices:**
- Register filters with descriptive names
- Include usage examples in docstrings
- Handle invalid input gracefully
- Return safe strings for HTML content

## Testing Standards

### Test Organization

```python
import pytest
from django.test import TestCase
from core.models import Book

class BookModelTest(TestCase):
    """Tests for Book model."""

    def setUp(self):
        """Set up test data."""
        self.book = Book.objects.create(
            name="Guide to the Traditions",
            gameline="mta"
        )

    def test_str_representation(self):
        """Test string representation."""
        self.assertEqual(str(self.book), "Guide to the Traditions")

    def test_gameline_display(self):
        """Test gameline display name."""
        self.assertEqual(
            self.book.get_gameline_display(),
            "Mage: The Ascension"
        )
```

**Best Practices:**
- One test class per model/utility
- Descriptive test names starting with `test_`
- Use `setUp()` for common test data
- Test edge cases and error conditions
- Aim for >80% code coverage

## Naming Conventions

- **Models**: PascalCase (e.g., `MeritFlaw`, `ArchetypeModel`)
- **Functions/Methods**: snake_case (e.g., `user_can_edit`, `get_gameline_display`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `STATUS_CHOICES`, `ATTRIBUTES`)
- **Template Tags**: lowercase, descriptive (e.g., `dots`, `sanitize_html`)

## Import Order

Follow this order for imports:

```python
# 1. Standard library
import json
from functools import wraps

# 2. Django imports
from django.db import models
from django.contrib.auth.models import User

# 3. Third-party packages
from polymorphic.models import PolymorphicModel

# 4. Local imports (from other TG apps)
from accounts.models import Profile

# 5. Relative imports (within core)
from .constants import STATUS_CHOICES
```

## Documentation

- All public functions/classes must have docstrings
- Use Google-style docstrings
- Include type hints for complex functions
- Document exceptions that can be raised

## Common Patterns

### Adding New Constants

When adding constants that other apps will use:

1. Add to `constants.py`
2. Export in `__init__.py` if needed
3. Document in this guide
4. Add tests
5. Update dependent apps if necessary

### Creating Reusable Mixins

```python
class TimeStampedMixin(models.Model):
    """Add creation and modification timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

Use `abstract = True` for mixins that should never be instantiated directly.

## Anti-Patterns to Avoid

- ❌ Importing from character/item/location apps in core
- ❌ Gameline-specific logic in core (belongs in respective apps)
- ❌ Hardcoding values that should be constants
- ❌ Creating utilities that only one app uses
- ❌ Breaking changes without migration path

## Code Review Checklist

- [ ] No imports from non-core apps
- [ ] All functions have docstrings
- [ ] Tests added for new functionality
- [ ] Constants used instead of magic values
- [ ] Backward compatible with existing code
- [ ] Generic and reusable design
- [ ] Follows project naming conventions
