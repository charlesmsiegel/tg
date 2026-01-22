# UX Quick Wins: Performance and Visual Consistency

**Date:** 2026-01-22
**Status:** Design Complete
**Scope:** Quick wins to improve performance and visual consistency without major overhaul

## Problem Statement

The application has systemic issues with:
1. **Performance** - excessive database queries on every page load
2. **Visual consistency** - inline styles, mixed component classes, duplicated patterns

## Audit Findings

### Performance Issues

| Issue | Location | Impact |
|-------|----------|--------|
| notification_count() runs 15-20 queries per page | `accounts/context_processors.py:19-131` | Critical |
| N+1 query for active scenes in nav | `core/templates/core/base.html:195` | High |
| Duplicate jQuery (v3.5.1 + v1.7.1) | `core/templates/core/base.html:19,338` | Medium |
| Non-minified Bootstrap CSS | `core/templates/core/base.html:8-16` | Low |

### Visual Consistency Issues

| Issue | Location | Impact |
|-------|----------|--------|
| 3,012 inline styles across templates | All template files | Medium |
| Mixed button classes (btn vs tg-btn) | `characters/templates/` | Medium |
| Repeated collapsible card pattern | `accounts/templates/accounts/includes/` (19 files) | Medium |
| 119 lines CSS in base.html | `core/templates/core/base.html:40-158` | Low |

---

## Tier 1 Fixes (Highest Impact)

### Fix 1: Cache notification_count()

**Location:** `accounts/context_processors.py:19-131`

**Current Problem:**
- Executes 15-20 database queries on every page load for authenticated users
- Uses `len(list)` instead of `.count()`, loading full objects into memory

**Solution:**
```python
from django.core.cache import cache

def notification_count(request):
    if not request.user.is_authenticated:
        return {}

    cache_key = f'notification_count_{request.user.id}'
    cached = cache.get(cache_key)
    if cached:
        return cached

    profile = request.user.profile

    # Use .count() instead of len(list)
    result = {
        'unread_scenes': profile.unread_scenes().count(),
        'xp_requests': profile.xp_requests().count(),
        'rotes_to_approve': profile.rotes_to_approve().count(),  # was len()
        'freebies_to_approve': profile.freebies_to_approve().count(),  # was len()
        'xp_spend_requests': profile.xp_spend_requests().count(),  # was len()
        # ... other counts ...
    }

    cache.set(cache_key, result, 60)  # 60 second cache
    return result
```

**Cache Invalidation:**
- Add signal handlers to invalidate cache when relevant models are saved
- Key models: Scene (read status), WeeklyXPRequest, approval-related models

---

### Fix 2: Prefetch Active Scenes

**Location:**
- `accounts/context_processors.py` (chronicles query)
- `core/templates/core/base.html:195`

**Current Problem:**
```django
{% for chronicle in chronicles %}
    {% with active_scenes=chronicle.get_active_scenes %}
```
Calls `get_active_scenes()` per chronicle = N+1 query pattern.

**Solution:**

In context processor:
```python
from django.db.models import Prefetch
from game.models import Scene

chronicles = Chronicle.objects.filter(...).prefetch_related(
    Prefetch(
        'scene_set',
        queryset=Scene.objects.filter(finished=False),
        to_attr='active_scenes'
    )
)
```

In template:
```django
{% for chronicle in chronicles %}
    {% with active_scenes=chronicle.active_scenes %}
```

No method call - uses prefetched attribute directly.

---

### Fix 3: Delete Duplicate jQuery

**Location:** `core/templates/core/base.html:338`

**Current Problem:**
- Line 19: `<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>`
- Line 338: `<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.js"></script>`

jQuery v1.7.1 is from 2011, non-minified, and redundant.

**Solution:** Delete line 338.

---

## Tier 2 Fixes (Medium Impact)

### Fix 4: Switch to Minified Bootstrap

**Location:** `core/templates/core/base.html:8-16`

**Change:**
```html
<!-- Before -->
<link rel="stylesheet" href="{% static 'boot/css/bootstrap.css' %}">
<link rel="stylesheet" href="{% static 'boot/css/bootstrap-grid.css' %}">
<link rel="stylesheet" href="{% static 'boot/css/bootstrap-reboot.css' %}">

<!-- After -->
<link rel="stylesheet" href="{% static 'boot/css/bootstrap.min.css' %}">
<!-- grid and reboot are included in bootstrap.min.css -->
```

**Verification:** Confirm `.min.css` files exist in `source_static/boot/css/`.

---

### Fix 5: Create Collapsible Card Component

**Create:** `core/templates/core/includes/collapsible_card.html`

```html
{% comment %}
Reusable collapsible card component.

Usage:
{% include "core/includes/collapsible_card.html" with id="unique-id" title="Section Title" icon="fa-users" collapsed=True %}
  ... card body content ...
{% endinclude %}

Parameters:
- id: Unique ID for collapse target (required)
- title: Card header title (required)
- icon: FontAwesome icon class without 'fa-' prefix (optional)
- title_class: Additional classes for title (optional)
- collapsed: Whether to start collapsed, default True (optional)
{% endcomment %}

<div class="tg-card-header text-center collapsible-header"
     data-toggle="collapse"
     data-target="#{{ id }}">
    <h3 class="tg-card-title {{ title_class|default:'' }}">
        <i class="fas fa-chevron-down"></i>
        {% if icon %}<i class="fas fa-{{ icon }}"></i>{% endif %}
        {{ title }}
    </h3>
</div>
<div id="{{ id }}" class="collapse {% if not collapsed %}show{% endif %}">
    <div class="tg-card-body collapsible-body">
        {{ content }}
    </div>
</div>
```

**Add to `source_static/style.css`:**
```css
/* Collapsible card component */
.collapsible-header {
    cursor: pointer;
}

.collapsible-body {
    padding: 20px;
}
```

**Refactor:** Update 19 files in `accounts/templates/accounts/includes/` to use component.

---

### Fix 6: Standardize Button Classes

**Files:** ~20 templates in `characters/templates/characters/`

**Pattern:**
- `class="btn btn-primary"` → `class="tg-btn btn-primary"`
- `class="btn btn-secondary"` → `class="tg-btn btn-secondary"`
- `class="btn"` → `class="tg-btn"`

**Verification:** Check for existing `tg-btn` usage to avoid double-application.

---

## Tier 3 Fixes (Polish)

### Fix 7: Move base.html Styles to CSS

**Location:** `core/templates/core/base.html:40-158` → `source_static/themes/components.css`

**Steps:**
1. Extract 119-line `<style>` block (notification dropdown styles)
2. Append to `themes/components.css`
3. Consolidate duplicate dark theme logic:
   - Remove `@media (prefers-color-scheme: dark)` block
   - Keep `.theme-dark` selector (explicit preference)
4. Delete `<style>` block from base.html

---

### Fix 8: Consolidate CSS Files

**Current State:**
- `source_static/style.css`: 715 lines
- `source_static/themes/components.css`: 825 lines
- Badge styles defined 36 times across files

**Approach:**
1. Audit for duplicate selectors
2. Move component styles to `components.css`
3. Keep `style.css` for layout/base styles
4. Remove duplicate `.badge-*` definitions
5. Add file purpose comments at top of each

---

## Implementation Priority

| Priority | Fix | Impact | Effort |
|----------|-----|--------|--------|
| 1 | Cache notification_count() | High | Medium |
| 2 | Prefetch active scenes | High | Low |
| 3 | Delete duplicate jQuery | Medium | Trivial |
| 4 | Minified Bootstrap | Low | Trivial |
| 5 | Collapsible card component | Medium | Medium |
| 6 | Standardize button classes | Low | Low |
| 7 | Move base.html styles | Low | Low |
| 8 | Consolidate CSS | Low | Medium |

---

## Files to Modify

### Performance Fixes
- `accounts/context_processors.py`
- `core/templates/core/base.html`

### Visual Consistency Fixes
- `characters/templates/characters/**/*.html` (~20 files)
- `accounts/templates/accounts/includes/*.html` (19 files)
- `core/templates/core/base.html`

### New Files
- `core/templates/core/includes/collapsible_card.html`

### CSS Changes
- `source_static/style.css`
- `source_static/themes/components.css`

---

## Success Metrics

- Page load queries reduced from 20+ to ~5
- No inline `style=` attributes in modified files
- Consistent `tg-btn` usage across character templates
- Single source of truth for collapsible card pattern
