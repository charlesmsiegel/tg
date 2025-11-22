# Core App - Template Tags & Filters

## Overview

The core app provides custom template tags and filters for common operations throughout the TG project. These tags enable World of Darkness-specific display formatting and safe content rendering.

## Loading Template Tags

At the top of your template:

```html
{% load dots sanitize_text %}
```

## Available Filters

### `dots` - WoD Rating Display

Converts numeric ratings to World of Darkness-style dot notation.

**Syntax:**
```html
{{ value|dots }}
{{ value|dots:max_value }}
```

**Examples:**

```html
<!-- Basic usage (auto-detects max of 5 or 10) -->
{{ character.strength|dots }}
<!-- If strength=3, outputs: ●●●○○ -->

<!-- Specify maximum dots -->
{{ trait.rating|dots:10 }}
<!-- If rating=7, outputs: ●●●●●●●○○○ -->

{{ willpower.current|dots:willpower.maximum }}
<!-- If current=5, maximum=7, outputs: ●●●●●○○ -->
```

**Parameters:**
- `value` (required): Numeric rating to display
- `max_dots` (optional): Maximum dots to show (default: auto-detects 5 or 10)

**Behavior:**
- Returns empty string for non-numeric values
- Filled dots (●) for current rating
- Empty dots (○) for remaining
- Auto-expands to 10 if value > 5

**Use Cases:**
- Character attributes (Strength, Dexterity, etc.)
- Abilities (Talents, Skills, Knowledges)
- Willpower tracking
- Blood pool / Essence / Gnosis
- Any 1-10 rating system

### `boxes` - Box Display

Similar to `dots` but uses boxes instead.

**Syntax:**
```html
{{ value|boxes }}
{{ value|boxes:max_value }}
```

**Examples:**

```html
{{ character.health|boxes }}
<!-- Outputs: ■■■■■□□ -->

{{ bruised_levels|boxes:7 }}
<!-- If bruised_levels=3, outputs: ■■■□□□□ -->
```

**Use Cases:**
- Health levels
- Temporary traits
- Damage tracking

### `sanitize_html` - Safe HTML Rendering

Sanitizes user-provided HTML to prevent XSS attacks while preserving safe formatting.

**Syntax:**
```html
{{ content|sanitize_html }}
```

**Examples:**

```html
<!-- User-provided description -->
{{ character.description|sanitize_html }}

<!-- Background/history fields -->
{{ chronicle.description|sanitize_html }}

<!-- In-game journal entries -->
{{ journal_entry.content|sanitize_html }}
```

**Allowed Tags:**
- Text formatting: `<b>`, `<i>`, `<u>`, `<em>`, `<strong>`
- Structure: `<p>`, `<br>`, `<hr>`
- Lists: `<ul>`, `<ol>`, `<li>`
- Links: `<a href="...">`
- Headers: `<h1>` through `<h6>`

**Stripped Elements:**
- `<script>` tags
- `onclick` and other event handlers
- `<iframe>` tags
- Potentially dangerous attributes

**When to Use:**
- Any user-provided content displayed in templates
- Rich text editor outputs
- Chronicle descriptions
- Character backgrounds
- House rules

**Security Note:** Always use this filter for user-generated HTML content. Never use `|safe` directly on user input.

## Common Patterns

### Displaying Character Traits

```html
<div class="trait-block">
    <h6>Physical Attributes</h6>
    <div class="trait-row">
        <span class="trait-name">Strength:</span>
        <span class="trait-dots">{{ character.strength|dots }}</span>
    </div>
    <div class="trait-row">
        <span class="trait-name">Dexterity:</span>
        <span class="trait-dots">{{ character.dexterity|dots }}</span>
    </div>
    <div class="trait-row">
        <span class="trait-name">Stamina:</span>
        <span class="trait-dots">{{ character.stamina|dots }}</span>
    </div>
</div>
```

### Willpower Display with Current/Max

```html
<div class="stat-box">
    <div class="stat-label">Willpower</div>
    <div class="stat-value">
        {{ character.current_willpower|dots:character.willpower }}
        <span class="numeric">({{ character.current_willpower }}/{{ character.willpower }})</span>
    </div>
</div>
```

### Abilities with Specialties

```html
{% for ability, rating in character.get_abilities.items %}
    <div class="ability-row">
        <span class="ability-name">{{ ability }}:</span>
        <span class="ability-dots">{{ rating|dots }}</span>
        {% if ability in character.specialties %}
            <span class="specialty">({{ character.specialties[ability] }})</span>
        {% endif %}
    </div>
{% endfor %}
```

### Safe Description Rendering

```html
<div class="tg-card">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Description</h5>
    </div>
    <div class="tg-card-body">
        {{ character.description|sanitize_html }}
    </div>
</div>
```

### Health Tracking

```html
<div class="health-tracker">
    <h6>Health Levels</h6>
    {% for level in health_levels %}
        <div class="health-level">
            <span>{{ level.name }}:</span>
            {{ level.damage|boxes:level.max }}
        </div>
    {% endfor %}
</div>
```

## Implementation Details

### `dots` Filter Implementation

```python
from django import template

register = template.Library()

@register.filter(name='dots')
def dots(value, max_dots=None):
    """Convert numeric rating to WoD-style dots."""
    if not isinstance(value, (int, float)):
        return ''

    value = int(value)
    if max_dots is None:
        max_dots = 10 if value > 5 else 5

    filled = '●' * value
    empty = '○' * (max_dots - value)
    return filled + empty
```

### `sanitize_html` Filter Implementation

Uses a whitelist approach with the `bleach` library:

```python
import bleach
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'b', 'i',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'hr'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
}

@register.filter(name='sanitize_html')
def sanitize_html(value):
    """Sanitize HTML content."""
    if not value:
        return ''

    cleaned = bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    return mark_safe(cleaned)
```

## Best Practices

### 1. Always Load Tags

Load template tags at the top of every template that uses them:

```html
{% extends "core/base.html" %}
{% load dots sanitize_text %}

{% block content %}
    {{ character.strength|dots }}
{% endblock %}
```

### 2. Combine with Styling

Use consistent CSS classes for formatted output:

```html
<style>
.trait-dots {
    font-size: 1.2rem;
    letter-spacing: 2px;
    color: var(--theme-primary);
}
</style>

<span class="trait-dots">{{ character.strength|dots }}</span>
```

### 3. Provide Fallbacks

Handle missing or zero values gracefully:

```html
{% if character.strength %}
    {{ character.strength|dots }}
{% else %}
    <span class="no-value">—</span>
{% endif %}
```

### 4. Use with Template Variables

Store repeated max values in variables:

```html
{% with max_gnosis=10 %}
    <div>Current: {{ character.gnosis|dots:max_gnosis }}</div>
    <div>Permanent: {{ character.permanent_gnosis|dots:max_gnosis }}</div>
{% endwith %}
```

## Testing Template Tags

### Testing Dots Filter

```python
from django.test import TestCase
from core.templatetags.dots import dots

class DotsFilterTest(TestCase):
    def test_basic_dots(self):
        """Test basic dot rendering."""
        result = dots(3)
        self.assertEqual(result, '●●●○○')

    def test_ten_dots(self):
        """Test 10-dot scale."""
        result = dots(7)
        self.assertEqual(result, '●●●●●●●○○○')

    def test_custom_max(self):
        """Test custom maximum."""
        result = dots(5, 7)
        self.assertEqual(result, '●●●●●○○')

    def test_invalid_input(self):
        """Test non-numeric input."""
        result = dots("invalid")
        self.assertEqual(result, '')

    def test_zero_value(self):
        """Test zero rating."""
        result = dots(0)
        self.assertEqual(result, '○○○○○')
```

### Testing Sanitize Filter

```python
from core.templatetags.sanitize_text import sanitize_html

class SanitizeFilterTest(TestCase):
    def test_safe_html(self):
        """Test safe HTML is preserved."""
        html = '<p>Safe <strong>content</strong></p>'
        result = sanitize_html(html)
        self.assertIn('<strong>content</strong>', result)

    def test_script_removal(self):
        """Test script tags are removed."""
        html = '<p>Text</p><script>alert("xss")</script>'
        result = sanitize_html(html)
        self.assertNotIn('<script>', result)
        self.assertIn('<p>Text</p>', result)

    def test_event_handler_removal(self):
        """Test event handlers are removed."""
        html = '<a onclick="malicious()">Link</a>'
        result = sanitize_html(html)
        self.assertNotIn('onclick', result)
```

## Extending Template Tags

### Creating Custom Filters

Add new filters to existing tag libraries:

```python
# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='my_custom_filter')
def my_custom_filter(value, arg):
    """
    Custom filter description.

    Usage: {{ value|my_custom_filter:arg }}
    """
    # Implementation
    return processed_value
```

### Creating Template Tags (Not Just Filters)

For more complex logic:

```python
@register.simple_tag
def display_trait_block(character, trait_name):
    """
    Render a complete trait block.

    Usage: {% display_trait_block character "Strength" %}
    """
    rating = getattr(character, trait_name.lower())
    return f'<div class="trait">{trait_name}: {dots(rating)}</div>'
```

## Performance Notes

- Template filters are called for each instance in loops - optimize implementations
- Cache complex calculations in the model rather than in filters
- Use `select_related` and `prefetch_related` to avoid N+1 queries in templates

## See Also

- `/CLAUDE.md` - Project-wide template styling conventions
- `SOURCES/STYLE.md` - Complete style guide
- `core/docs/CODE_STYLE.md` - Core app coding standards
