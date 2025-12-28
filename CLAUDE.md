# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

Django 5.1.7 web application for managing World of Darkness tabletop RPG characters, items, and locations. Supports multiple game lines: Vampire (VtM), Werewolf (WtA), Mage (MtA), Wraith (WtO), Changeling (CtD), Demon (DtF), Mummy (MtR), and Hunter (HtR).

## Skills Reference

This project has domain-specific skills. Read the appropriate SKILL.md before working in that area:

| Skill | When to Use | Location |
|-------|-------------|----------|
| **model-standards** | Creating/editing models, views, forms, URLs | `.claude/skills/model-standards/SKILL.md` |
| **tg-frontend** | Template styling, TG components, gameline theming | `.claude/skills/tg-frontend/SKILL.md` |
| **tg-permissions** | Permission checks, access control, limited forms | `.claude/skills/tg-permissions/SKILL.md` |
| **tg-testing** | Writing/running tests, test file locations | `.claude/skills/tg-testing/SKILL.md` |
| **tg-domain** | WoD terminology (ST, Disciplines, Spheres, etc.) | `.claude/skills/tg-domain/SKILL.md` |

## Common Commands

```bash
# Setup
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic

# Development
python manage.py runserver 7000

# Testing (see tg-testing skill for details)
python manage.py test                     # All tests
python manage.py test characters          # App-specific

# Database seeding
bash setup_db.sh                          # Loads all game data
```

## Architecture

### Polymorphic Model Inheritance

Core pattern: `core.models.Model` extends Django Polymorphic. Three inheritance trees:
- **Character** → gameline-specific (VtMHuman, Garou, Mage, Wraith, etc.)
- **ItemModel** → gameline-specific items
- **LocationModel** → gameline-specific locations

See **model-standards** skill for implementation patterns.

### App Structure

| App | Purpose |
|-----|---------|
| **characters/** | Character models, forms, views by gameline |
| **items/** | Equipment and artifacts |
| **locations/** | Places and locations |
| **game/** | Chronicle, Scene, Story, Week, Journal |
| **accounts/** | User profiles, preferences, ST relationships |
| **core/** | Shared utilities, base models, template tags |

### Key Patterns

**User Profile** - One-to-one with Django User. Key methods: `is_st()`, `st_relations()`, `objects_to_approve()`.

**Chronicle System** - `Chronicle` defines campaigns. `Scene` handles sessions. `Story` groups scenes.

**XP Tracking** - Characters have `xp` (earned) and `spent_xp` (JSONField). Storytellers approve via `WeeklyXPRequest`.

**Character Status** - `Un` (Unfinished), `Sub` (Submitted), `App` (Approved), `Ret` (Retired), `Dec` (Deceased).

## Important Files

| File | Purpose |
|------|---------|
| `tg/settings.py` | Django config, gameline settings |
| `core/models.py` | Base polymorphic models |
| `core/mixins.py` | All view mixins |
| `core/permissions.py` | PermissionManager |
| `accounts/models.py` | Profile with ST logic |
| `populate_db/` | Game data loading scripts |
| `docs/` | Design docs, guides, deployment |

## Coding Standards

### Gameline Configuration

Always use settings for gameline data:

```python
from django.conf import settings
gameline_name = settings.GAMELINES.get(gameline, {}).get('name', gameline)

# For model choices
gameline = models.CharField(choices=settings.GAMELINE_CHOICES, ...)
```

### View Mixins

Import all mixins from `core.mixins`:

```python
from core.mixins import (
    ViewPermissionMixin, EditPermissionMixin, MessageMixin,
    VisibilityFilterMixin, STRequiredMixin, SpecialUserMixin,
)
```

See **tg-permissions** skill for complete mixin list and usage patterns.

### Preventing N+1 Queries

Always use `select_related()` and `prefetch_related()`:

```python
# Good
characters = Character.objects.select_related('owner').prefetch_related('merits_and_flaws')
```

### Error Handling

Use `get_object_or_404()` instead of `.get()`:

```python
from django.shortcuts import get_object_or_404
character = get_object_or_404(Character, pk=pk)
```

## Template Standards

See **tg-frontend** skill for complete styling guide.

**Quick Reference:**
- Use `tg-card`, `tg-table`, `tg-badge` (not Bootstrap defaults)
- Use `{{ object.get_heading }}` for gameline-specific styling
- Load `{% load sanitize_text dots %}` for template tags
- Dots: `{{ rating|dots }}` → `●●●○○`
