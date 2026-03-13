# UX Quick Wins Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve application performance and visual consistency through targeted fixes.

**Architecture:** Performance fixes focus on reducing database queries in the notification context processor and base template navigation. Visual fixes standardize component usage and extract inline styles to CSS.

**Tech Stack:** Django 5.1.7, Bootstrap 4, Django cache framework

---

## Task 1: Delete Duplicate jQuery

**Files:**

- Modify: `core/templates/core/base.html:338`

**Step 1: Remove the duplicate jQuery line**

In `core/templates/core/base.html`, delete line 338:

```html
<!-- DELETE THIS LINE -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.js"></script>
```

The file currently loads jQuery twice:
- Line 19: `jquery-3.5.1.min.js` (keep this)
- Line 338: `jquery-1.7.1.js` (delete this - ancient, non-minified, redundant)

**Step 2: Verify the change**

```bash
grep -n "jquery" core/templates/core/base.html
```

Expected: Only line 19 should show jQuery, and possibly jquery-ui on line 339.

**Step 3: Commit**

```bash
git add core/templates/core/base.html
git commit -m "perf: remove duplicate jQuery 1.7.1 load

Keep only the modern jQuery 3.5.1 from CDN. The old jQuery 1.7.1 was
redundant and non-minified."
```

---

## Task 2: Switch to Minified Bootstrap CSS

**Files:**

- Modify: `core/templates/core/base.html:8-16`

**Step 1: Update Bootstrap CSS references**

In `core/templates/core/base.html`, change lines 8-16 from:

```html
<link rel="stylesheet"
      type="text/css"
      href="{% static 'boot/css/bootstrap.css' %}" />
<link rel="stylesheet"
      type="text/css"
      href="{% static 'boot/css/bootstrap-reboot.css' %}" />
<link rel="stylesheet"
      type="text/css"
      href="{% static 'boot/css/bootstrap-grid.css' %}" />
```

To:

```html
<link rel="stylesheet"
      type="text/css"
      href="{% static 'boot/css/bootstrap.min.css' %}" />
```

Note: `bootstrap.min.css` already includes reboot and grid, so we remove the redundant files.

**Step 2: Verify the change**

```bash
grep -n "bootstrap" core/templates/core/base.html
```

Expected: Only one bootstrap.min.css reference.

**Step 3: Commit**

```bash
git add core/templates/core/base.html
git commit -m "perf: use minified Bootstrap CSS

Switch from 3 separate unminified Bootstrap files to single minified
bundle. Reduces CSS payload size."
```

---

## Task 3: Fix len() to .count() in Context Processor

**Files:**

- Modify: `accounts/context_processors.py:67,73,79`
- Test: `accounts/tests/test_context_processors.py` (spot check)

**Step 1: Examine which methods return QuerySets vs lists**

The following methods return QuerySets (can use `.count()`):
- `rotes_to_approve()` - returns QuerySet
- `freebies_to_approve()` - returns QuerySet
- `xp_spend_requests()` - returns QuerySet

The following return lists (must use `len()`):
- `get_unfulfilled_weekly_xp_requests()` - returns list of tuples
- `get_unfulfilled_weekly_xp_requests_to_approve()` - returns list of tuples

**Step 2: Update context_processors.py**

Change lines 67, 73, 79 from `len()` to `.count()`:

```python
# Line 67: Change from
rotes_to_approve = len(profile.rotes_to_approve())
# To
rotes_to_approve = profile.rotes_to_approve().count()

# Line 73: Change from
freebies = len(profile.freebies_to_approve())
# To
freebies = profile.freebies_to_approve().count()

# Line 79: Change from
xp_spend = len(profile.xp_spend_requests())
# To
xp_spend = profile.xp_spend_requests().count()
```

**Step 3: Spot check tests**

```bash
python manage.py test accounts.tests.test_context_processors -v 2
```

If no test file exists, that's okay - the change is straightforward.

**Step 4: Commit**

```bash
git add accounts/context_processors.py
git commit -m "perf: use .count() instead of len() for QuerySets

Avoids materializing full QuerySets into memory when only the count
is needed. Reduces memory usage and improves query efficiency."
```

---

## Task 4: Add Caching to notification_count Context Processor

**Files:**

- Modify: `accounts/context_processors.py:19-131`
- Test: `accounts/tests/test_context_processors.py` (spot check)

**Step 1: Add cache import**

At top of `accounts/context_processors.py`, add:

```python
from django.core.cache import cache
```

**Step 2: Wrap notification_count with caching**

Modify the `notification_count` function to check cache first:

```python
def notification_count(request):
    """
    Add notification count and breakdown to all templates for authenticated users.
    Results are cached for 60 seconds to reduce database queries.
    """
    context = {"notification_count": 0, "notification_breakdown": {}}

    if request.user.is_authenticated:
        cache_key = f'notification_count_{request.user.id}'
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            profile = request.user.profile
            breakdown = {}
            count = 0

            # ... existing counting logic (unchanged) ...

            context["notification_count"] = count
            context["notification_breakdown"] = breakdown

            # Cache for 60 seconds
            cache.set(cache_key, context, 60)

        except Exception as e:
            logger.warning(
                f"Error calculating notification count for user {request.user.id}: {e}",
                exc_info=True,
            )
            context["notification_count"] = 0
            context["notification_breakdown"] = {}

    return context
```

**Step 3: Spot check tests**

```bash
python manage.py test accounts.tests.test_context_processors -v 2
```

**Step 4: Commit**

```bash
git add accounts/context_processors.py
git commit -m "perf: cache notification counts for 60 seconds

Reduces database queries from 15-20 per page to 0 for cached requests.
Cache invalidates after 60 seconds ensuring reasonable freshness."
```

---

## Task 5: Prefetch Active Scenes for Navigation

**Files:**

- Modify: `accounts/context_processors.py` (add chronicles with prefetch)
- Modify: `core/templates/core/base.html:195` (use prefetched attribute)

**Step 1: Find where chronicles context is set**

Search for where `chronicles` is added to template context:

```bash
grep -rn "chronicles" accounts/context_processors.py core/context_processors.py tg/context_processors.py
```

If not found in context processors, check `core/views.py` or base view mixins.

**Step 2: Add prefetch for active scenes**

Wherever chronicles are queried, add prefetch:

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

**Step 3: Update base.html template**

Change line 195 from:

```html
{% with active_scenes=chronicle.get_active_scenes %}
```

To:

```html
{% with active_scenes=chronicle.active_scenes %}
```

This uses the prefetched attribute instead of calling a method.

**Step 4: Spot check**

Run the development server and verify the Chronicles dropdown still works:

```bash
python manage.py runserver 7000
```

Navigate to site and check Chronicles dropdown shows active scenes.

**Step 5: Commit**

```bash
git add accounts/context_processors.py core/templates/core/base.html
git commit -m "perf: prefetch active scenes for navigation

Eliminates N+1 query pattern where get_active_scenes() was called
per chronicle in the navigation template loop."
```

---

## Task 6: Move Notification Dropdown Styles to CSS

**Files:**

- Modify: `core/templates/core/base.html:40-158` (remove style block)
- Modify: `source_static/themes/components.css` (add styles)

**Step 1: Copy styles to components.css**

Add the following to the end of `source_static/themes/components.css`:

```css
/* Notification dropdown styles */
.nav-link .badge {
    border-radius: 50%;
    min-width: 1.5em;
    height: 1.5em;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
}

.nav-link:hover .badge {
    animation: none;
}

.notification-dropdown {
    min-width: 320px;
    max-width: 400px;
    max-height: 500px;
    overflow-y: auto;
}

.notification-dropdown .dropdown-header {
    font-size: 1rem;
    font-weight: 600;
    padding: 0.75rem 1rem;
}

.notification-dropdown .dropdown-item-text {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    white-space: normal;
    cursor: default;
}

.notification-dropdown .dropdown-item-text:hover {
    background-color: var(--tg-dropdown-hover-bg, #f8f9fa);
}

.notification-dropdown .badge-pill {
    font-size: 0.75rem;
    padding: 0.35em 0.65em;
}

.notification-dropdown .dropdown-item {
    font-weight: 500;
}

.notification-dropdown .dropdown-item:hover {
    background-color: var(--tg-dropdown-hover-bg, #e9ecef);
}
```

**Step 2: Add dark theme overrides**

Add to `source_static/themes/dark.css`:

```css
/* Notification dropdown dark theme */
.notification-dropdown {
    background-color: #343a40;
    border-color: #495057;
}

.notification-dropdown .dropdown-header {
    color: #f8f9fa;
}

.notification-dropdown .dropdown-item-text {
    color: #dee2e6;
}

.notification-dropdown .dropdown-item-text:hover,
.notification-dropdown .dropdown-item:hover {
    background-color: #495057;
}

.notification-dropdown .dropdown-divider {
    border-color: #495057;
}
```

**Step 3: Remove style block from base.html**

Delete lines 40-158 (the entire `<style>` block) from `core/templates/core/base.html`.

**Step 4: Verify styles still work**

```bash
python manage.py collectstatic --noinput
python manage.py runserver 7000
```

Check notification dropdown appears correctly in both light and dark themes.

**Step 5: Commit**

```bash
git add core/templates/core/base.html source_static/themes/components.css source_static/themes/dark.css
git commit -m "refactor: move notification dropdown styles to CSS files

Extracts 119 lines of inline CSS from base.html to proper theme files.
Improves maintainability and separates concerns."
```

---

## Task 7: Standardize Button Classes

**Files:**

- Modify: Multiple templates in `characters/templates/characters/`

**Step 1: Find buttons using raw Bootstrap classes**

```bash
grep -rn 'class="btn btn-' characters/templates/ --include="*.html" | head -20
```

**Step 2: Update to tg-btn**

For each file found, change:
- `class="btn btn-primary"` to `class="tg-btn btn-primary"`
- `class="btn btn-secondary"` to `class="tg-btn btn-secondary"`
- etc.

**Step 3: Verify no double-application**

```bash
grep -rn 'tg-btn tg-btn' characters/templates/
```

Should return nothing.

**Step 4: Commit**

```bash
git add characters/templates/
git commit -m "style: standardize button classes to tg-btn

Ensures consistent button styling across character templates by using
the project's custom tg-btn class instead of raw Bootstrap btn."
```

---

## Summary

| Task | Type | Impact |
|------|------|--------|
| 1. Delete duplicate jQuery | Performance | Medium |
| 2. Use minified Bootstrap | Performance | Low |
| 3. Fix len() to .count() | Performance | Medium |
| 4. Cache notification counts | Performance | High |
| 5. Prefetch active scenes | Performance | High |
| 6. Move styles to CSS | Maintainability | Low |
| 7. Standardize buttons | Consistency | Low |

**Estimated total: 7 commits, ~30 minutes of implementation**
