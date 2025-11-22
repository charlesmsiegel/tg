# Core App

The `core` app provides foundational components used throughout the TG project. It contains base models, shared utilities, permissions, constants, and template tags used by all other apps.

## Purpose

Core serves as the foundation layer for the entire application, providing:
- Base polymorphic models for Characters, Items, and Locations
- Shared utilities and helper functions
- Permission systems and decorators
- Template tags and filters
- Common constants and enumerations
- Context processors for global template data

## Key Components

### Models (`models.py`)
- **Model**: Base polymorphic model extending Django Polymorphic
- **Book**: Source book references for game content
- **HouseRule**: Custom rules for chronicles
- **Language**: Language system for character creation
- **MeritFlaw**: Character advantages and disadvantages (shared across gamelines)
- **Specialty**: Ability specializations
- **ArchetypeModel**: Base for Natures and Demeanors

### Utilities (`utils.py`)
Helper functions for common operations across the project.

### Permissions (`permissions.py`)
- Object-level permissions
- Storyteller verification
- Approval workflows

### Decorators (`decorators.py`)
Custom decorators for views, including permission checks.

### Constants (`constants.py`)
Shared enumerations and constant values:
- `ATTRIBUTES`: Physical/Social/Mental attribute lists
- `ABILITIES`: Talents, Skills, Knowledges
- `STATUS_CHOICES`: Character/Item/Location status options

### Template Tags (`templatetags/`)
- `dots`: Display WoD-style ratings (●●●○○)
- `sanitize_text`: Safe HTML rendering
- Custom filters for common data transformations

### Context Processors (`context_processors.py`)
Global context data available in all templates.

## Directory Structure

```
core/
├── __init__.py
├── admin.py                    # Admin configuration
├── apps.py                     # App configuration
├── constants.py                # Shared constants and enumerations
├── context_processors.py       # Global template context
├── decorators.py               # Custom decorators
├── migrations/                 # Database migrations
├── mixins.py                   # Reusable model/view mixins
├── models.py                   # Base polymorphic models
├── permissions.py              # Permission system
├── templates/
│   └── core/
│       ├── base.html          # Base template for entire site
│       └── ...
├── templatetags/              # Custom template filters/tags
│   ├── __init__.py
│   ├── dots.py               # WoD rating display (●●●○○)
│   └── sanitize_text.py      # Safe HTML rendering
├── tests/                     # Unit and integration tests
├── urls.py                    # URL routing
├── utils.py                   # Helper functions
└── views.py                   # Core views
```

## Usage Examples

### Using Base Models

```python
from core.models import Model

class MyCustomModel(Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "My Custom Model"
        verbose_name_plural = "My Custom Models"
```

### Using Template Tags

```html
{% load dots sanitize_text %}

<!-- Display WoD-style ratings -->
{{ character.strength|dots }}  <!-- Output: ●●●○○ -->

<!-- Safe HTML rendering -->
{{ user_content|sanitize_html }}
```

### Using Permissions

```python
from core.permissions import user_can_edit_object
from core.decorators import require_storyteller

@require_storyteller
def storyteller_only_view(request):
    # Only accessible to storytellers
    pass

def edit_view(request, pk):
    obj = MyModel.objects.get(pk=pk)
    if not user_can_edit_object(request.user, obj):
        raise PermissionDenied
    # ... editing logic
```

## Testing

Run core app tests:
```bash
pytest core/tests/
pytest -v core/test_permissions.py
```

## Dependencies

- Django 5.1.7
- django-polymorphic (for model inheritance)

## Related Documentation

- See `docs/CODE_STYLE.md` for coding standards
- See `docs/MODELS.md` for model design patterns
- See `docs/TEMPLATE_TAGS.md` for template tag usage
- See `/CLAUDE.md` for project-wide conventions
