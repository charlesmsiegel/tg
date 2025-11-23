# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 5.1.7 web application for managing World of Darkness (WoD) tabletop RPG characters, items, and locations. Supports multiple game lines: Vampire (VtM), Werewolf (WtA), Mage (MtA), Wraith (WtO), Changeling (CtD), and Demon (DtF).

## Common Commands

```bash
# Setup
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

# Run development server
python manage.py runserver

# Testing
pytest                                    # Run all tests
pytest characters/tests/                  # Run app-specific tests
pytest -v accounts/tests.py::TestClass::test_method  # Run single test

# Database seeding
bash setup_db.sh                          # Loads all game data from populate_db/
```

## Architecture

### Polymorphic Model Inheritance
Core pattern: `core.models.Model` extends Django Polymorphic. Three main inheritance trees:
- **Character** → gameline-specific implementations (VtMHuman, Garou, Mage, Wraith, etc.)
- **ItemModel** → gameline-specific items
- **LocationModel** → gameline-specific locations

Each gameline has its own module under `characters/models/{gameline}/`, `items/models/{gameline}/`, etc.

### App Structure
- **characters/** - Character models, forms, views organized by gameline
- **items/** - Equipment and artifacts (mirrors characters structure)
- **locations/** - Places and locations (mirrors characters structure)
- **game/** - Chronicle, Scene, Story, Week, Journal management
- **accounts/** - User profiles, preferences, ST relationships
- **core/** - Shared utilities, base models, constants, template tags

### Key Patterns

**User Profile** - One-to-one with Django User. Tracks theme preferences, ST status, approval queues. Key methods: `is_st()`, `st_relations()`, `objects_to_approve()`.

**Chronicle System** - `Chronicle` defines campaigns with storytellers and players. `Scene` handles sessions with participants and XP. `Story` groups multiple scenes.

**XP Tracking** - Characters have `xp` (earned) and `spent_xp` (JSONField with approval status). Storytellers approve spending via `WeeklyXPRequest`.

**Character Status** - `Un` (Unfinished), `Sub` (Submitted), `App` (Approved), `Ret` (Retired), `Dec` (Deceased).

## Domain Terminology

- **ST** - Storyteller (game master)
- **Attributes** - Physical/Social/Mental base traits (1-5)
- **Abilities** - Skills and knowledges
- **Backgrounds** - Character advantages
- **Freebie Points** - Character creation points
- **Angst** - Wraith's Shadow power measure
- **Passions/Fetters** - Wraith emotional connections
- **Disciplines/Gifts/Spheres/Arts/Lores** - Game-specific supernatural powers

## Important Files

- `tg/settings.py` - Django configuration (uses .env), gameline configuration
- `core/models.py` - Base polymorphic models, Book, HouseRule
- `core/mixins.py` - All view mixins (permission, message, user checks)
- `characters/models/core/character.py` - Base Character class
- `accounts/models.py` - Profile model with ST logic
- `SOURCES/STYLE.md` - UI design guide (use `tg-card` not Bootstrap `card`)
- `TODO.md` - Known technical debt and planned improvements
- `populate_db/` - 80+ scripts for loading game mechanics data
- `docs/design/` - Design documentation (permissions, validation)
- `docs/guides/` - Implementation guides (migrations, permissions)

## Coding Standards

### Gameline Configuration
Gameline data is centralized in `tg/settings.py`. **Always use settings for gameline data**:

```python
# tg/settings.py defines:
GAMELINES = {
    'wod': {'name': 'World of Darkness', 'short': '', 'app_name': 'wod'},
    'vtm': {'name': 'Vampire: the Masquerade', 'short': 'VtM', 'app_name': 'vampire'},
    'wta': {'name': 'Werewolf: the Apocalypse', 'short': 'WtA', 'app_name': 'werewolf'},
    'mta': {'name': 'Mage: the Ascension', 'short': 'MtA', 'app_name': 'mage'},
    'wto': {'name': 'Wraith: the Oblivion', 'short': 'WtO', 'app_name': 'wraith'},
    'ctd': {'name': 'Changeling: the Dreaming', 'short': 'CtD', 'app_name': 'changeling'},
    'dtf': {'name': 'Demon: the Fallen', 'short': 'DtF', 'app_name': 'demon'},
}
GAMELINE_CHOICES = [(key, val['name']) for key, val in GAMELINES.items()]

# In your code - use settings, don't hardcode:
from django.conf import settings
gameline_name = settings.GAMELINES.get(gameline, {}).get('name', gameline)

# For model choices:
gameline = models.CharField(choices=settings.GAMELINE_CHOICES, ...)
```

### View Mixins
All view mixins are consolidated in `core/mixins.py`. **Always import from `core.mixins`**:

```python
# Correct - consolidated imports
from core.mixins import (
    ViewPermissionMixin,      # Requires VIEW_FULL permission
    EditPermissionMixin,      # Requires EDIT_FULL permission
    MessageMixin,             # Success/error messages
    SpecialUserMixin,         # Special user access
)

# Deprecated - old scattered imports (still work but avoid)
from core.views.message_mixin import SuccessMessageMixin
from core.views.approved_user_mixin import SpecialUserMixin
```

**Available Mixins:**
- **Permission Mixins**: `ViewPermissionMixin`, `EditPermissionMixin`, `SpendXPPermissionMixin`, `SpendFreebiesPermissionMixin`, `VisibilityFilterMixin`, `OwnerRequiredMixin`, `STRequiredMixin`
- **Message Mixins**: `SuccessMessageMixin`, `ErrorMessageMixin`, `MessageMixin`, `DeleteMessageMixin`
- **User Check Mixins**: `SpecialUserMixin`

### Permission Patterns
Two permission systems exist - use the right one for the context:

**Use PermissionManager (object-level):**
```python
# In views - checking permissions on specific objects
class CharacterDetailView(ViewPermissionMixin, DetailView):
    # ViewPermissionMixin automatically checks VIEW_FULL permission
    pass

# In code - explicit permission checks
from core.permissions import PermissionManager
pm = PermissionManager()
if pm.check_permission(user, character, 'edit_full'):
    # Allow editing
```

**Use is_st() (role-based):**
```python
# In forms - to determine available options
if user.profile.is_st():
    # Show ST-only form fields

# In templates - to show/hide UI elements
{% if user.profile.is_st %}
    <!-- ST-only controls -->
{% endif %}

# General storyteller checks (not object-specific)
if request.user.profile.is_st():
    # Allow ST-only actions
```

**Guidelines:**
- Use **PermissionManager** for detail/update/delete views and object-specific permissions
- Use **is_st()** for general role checks, forms, and templates
- Permission mixins handle view-level checks automatically
- See `docs/design/permissions_system.md` for comprehensive documentation

### View Class Patterns
Follow Django's class-based view patterns:

```python
from django.views.generic import DetailView, UpdateView
from core.mixins import ViewPermissionMixin, MessageMixin

# Good - proper CBV pattern
class CharacterDetailView(ViewPermissionMixin, DetailView):
    model = Character
    template_name = 'characters/character/detail.html'

    def get_queryset(self):
        # Use select_related/prefetch_related to prevent N+1 queries
        return super().get_queryset().select_related('owner').prefetch_related('merits_and_flaws')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['additional_data'] = self.get_additional_data()
        return context

# Good - update view with messages
class CharacterUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    success_message = "Character updated successfully"
```

### Preventing N+1 Queries
Always use `select_related()` and `prefetch_related()` in querysets:

```python
# Bad - causes N+1 queries
characters = Character.objects.all()
for char in characters:
    print(char.owner.username)  # Query per character!

# Good - single query with join
characters = Character.objects.select_related('owner')
for char in characters:
    print(char.owner.username)  # No additional queries

# Good - prefetch related objects
chronicle = Chronicle.objects.prefetch_related('storytellers', 'allowed_objects').get(pk=pk)
```

### Error Handling in Views
Use `get_object_or_404()` instead of `.get()`:

```python
# Bad - raises 500 error
character = Character.objects.get(pk=pk)  # DoesNotExist = 500 error

# Good - returns proper 404
from django.shortcuts import get_object_or_404
character = get_object_or_404(Character, pk=pk)  # DoesNotExist = 404 response
```

## Template Styling Conventions

### Core Component Classes
Use custom TG classes instead of Bootstrap defaults:
- `tg-card`, `tg-card-header`, `tg-card-body`, `tg-card-title`, `tg-card-subtitle` (not Bootstrap `card-*`)
- `tg-table` (not Bootstrap `table`)
- `tg-badge` with `badge-pill` for status indicators (not Bootstrap `badge`)

### Gameline-Specific Styling
Headers use gameline classes for consistent theming:
```html
<div class="tg-card header-card mb-4" data-gameline="mta">
    <div class="tg-card-header">
        <h1 class="tg-card-title mta_heading">{{ object.name }}</h1>
    </div>
</div>
```

Available heading classes: `vtm_heading`, `wta_heading`, `mta_heading`, `wto_heading`, `ctd_heading`, `dtf_heading`

In templates, use `{{ object.get_heading }}` to get the appropriate class dynamically.

### Stat Box Pattern (Inline Label)
For key statistics with label beside value:
```html
<div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
    <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Label:</span>
    <span style="font-weight: 700; color: var(--theme-text-primary);">{{ value }}</span>
</div>
```

### Large Stat Display (Label Above)
For prominent numbers:
```html
<div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
    <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ value }}</div>
    <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Label</div>
</div>
```

### Template Tags
Load custom filters at top of template:
```html
{% load sanitize_text dots %}
```

**Dots filter** - Displays WoD-style ratings: `{{ rating|dots }}` → `●●●○○`
- Default maximum is 5, auto-expands to 10 if value exceeds 5
- Also available: `{{ value|boxes }}` → `■■■□□`

**Sanitize filter** - `{{ content|sanitize_html }}` for safe HTML rendering

### Template Inheritance
- Base template: `core/templates/core/base.html`
- Detail pages extend gameline base: `{% extends "locations/core/location/detail.html" %}`
- Common blocks: `{% block objectname %}`, `{% block model_specific %}`, `{% block reality_zone %}`

### Display Includes Pattern
Reusable component fragments in `display_includes/` subdirectories:
```html
{% include "locations/mage/node/display_includes/basics.html" %}
{% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
```

### Spacing Standards
- Card body padding: `padding: 20px;` (standard) to `24px-32px` (spacious)
- Between sections: `mb-4` or `mb-5`
- Between related items: `mb-3`
- Inline label-value spacing: `margin-right: 8px`

### Status Badge Classes
```html
<span class="tg-badge badge-{{ object.status|lower }}">{{ object.get_status_display }}</span>
```
- `badge-un` (gray) - Unfinished
- `badge-sub` (blue) - Submitted
- `badge-app` (green) - Approved
- `badge-ret` (orange) - Retired
- `badge-dec` (red) - Deceased

### CSS Variables
Use theme-aware variables for colors:
- `var(--theme-text-primary)` - main text
- `var(--theme-text-secondary)` - labels and muted text
- Backgrounds: `rgba(0,0,0,0.05)` for stat boxes, `rgba(0,0,0,0.02)` for content boxes

### Responsive Grid Layouts
Two-column for stats:
```html
<div class="row">
    <div class="col-md-6 mb-3"><!-- Left --></div>
    <div class="col-md-6 mb-3"><!-- Right --></div>
</div>
```

Use `h-100` on cards within grid for equal heights.

### Typography Standards
- Section headers in cards: `<h6>` with gameline class
- Subsection labels: `font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px`
- Large numbers: `font-size: 1.5rem; font-weight: 700`
- Standard text: `line-height: 1.6`

See `SOURCES/STYLE.md` for complete style guide with examples.

## Testing

Tests organized by app and gameline: `characters/tests/vampire/`, `items/tests/mage/`, etc. Uses pytest-django. Run `pytest -v` for verbose output.
