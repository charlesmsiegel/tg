# Core App - Template Style Guide

## Overview

The core app provides the base template (`base.html`) and shared template components used throughout the TG project. This guide covers styling conventions and patterns for core templates.

## Base Template Structure

### `core/templates/core/base.html`

The base template provides the fundamental HTML structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TG - World of Darkness{% endblock %}</title>

    <!-- CSS -->
    <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static 'css/tg-styles.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body data-theme="{{ user_theme|default:'dark' }}">
    {% include "core/includes/navbar.html" %}

    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>

    {% include "core/includes/footer.html" %}

    <!-- JS -->
    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## TG Component Classes

### Cards (Use `tg-card`, NOT Bootstrap `card`)

**Basic Card:**
```html
<div class="tg-card">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Card Title</h5>
    </div>
    <div class="tg-card-body">
        Card content goes here
    </div>
</div>
```

**Card with Subtitle:**
```html
<div class="tg-card">
    <div class="tg-card-header">
        <h1 class="tg-card-title">Main Title</h1>
        <p class="tg-card-subtitle">Subtitle or description</p>
    </div>
    <div class="tg-card-body">
        Content
    </div>
</div>
```

**Header Card (for page headers):**
```html
<div class="tg-card header-card mb-4" data-gameline="vtm">
    <div class="tg-card-header">
        <h1 class="tg-card-title vtm_heading">Character Name</h1>
        <p class="tg-card-subtitle">Concept - Clan</p>
    </div>
</div>
```

### Tables (Use `tg-table`, NOT Bootstrap `table`)

```html
<table class="tg-table">
    <thead>
        <tr>
            <th>Name</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Attribute</td>
            <td>3</td>
        </tr>
    </tbody>
</table>
```

### Badges (Use `tg-badge`)

**Status Badges:**
```html
<span class="tg-badge badge-{{ object.status|lower }}">
    {{ object.get_status_display }}
</span>
```

**Badge Classes:**
- `badge-un` - Gray (Unfinished)
- `badge-sub` - Blue (Submitted)
- `badge-app` - Green (Approved)
- `badge-ret` - Orange (Retired)
- `badge-dec` - Red (Deceased)

**Pill Badges:**
```html
<span class="tg-badge badge-pill badge-app">Approved</span>
```

## Gameline-Specific Styling

### Gameline Heading Classes

Apply to headers for consistent theming:

```html
<h1 class="vtm_heading">Vampire Title</h1>
<h2 class="wta_heading">Werewolf Subtitle</h2>
<h3 class="mta_heading">Mage Section</h3>
<h4 class="wto_heading">Wraith Detail</h4>
<h5 class="ctd_heading">Changeling Info</h5>
<h6 class="dtf_heading">Demon Note</h6>
```

**Available Classes:**
- `vtm_heading` - Vampire: The Masquerade
- `wta_heading` - Werewolf: The Apocalypse
- `mta_heading` - Mage: The Ascension
- `wto_heading` - Wraith: The Oblivion
- `ctd_heading` - Changeling: The Dreaming
- `dtf_heading` - Demon: The Fallen

### Dynamic Gameline Styling

Use `data-gameline` attribute for context-aware styling:

```html
<div class="tg-card" data-gameline="{{ object.gameline }}">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ object.get_heading }}">
            {{ object.name }}
        </h5>
    </div>
</div>
```

## Stat Display Patterns

### Inline Stat Box (Label beside value)

```html
<div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
    <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">
        Willpower:
    </span>
    <span style="font-weight: 700; color: var(--theme-text-primary);">
        {{ character.willpower }}
    </span>
</div>
```

### Large Stat Display (Label above value)

```html
<div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
    <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">
        {{ character.xp }}
    </div>
    <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">
        Experience Points
    </div>
</div>
```

### Dots Display

```html
{% load dots %}

<div class="trait-row">
    <span class="trait-name">Strength:</span>
    <span class="trait-dots">{{ character.strength|dots }}</span>
</div>
```

## Layout Patterns

### Two-Column Stat Grid

```html
<div class="row">
    <div class="col-md-6 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="{{ gameline }}_heading">Left Section</h6>
                <!-- Content -->
            </div>
        </div>
    </div>
    <div class="col-md-6 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="{{ gameline }}_heading">Right Section</h6>
                <!-- Content -->
            </div>
        </div>
    </div>
</div>
```

### Three-Column Layout

```html
<div class="row">
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <!-- Content -->
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <!-- Content -->
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <!-- Content -->
            </div>
        </div>
    </div>
</div>
```

## CSS Variables

### Theme-Aware Colors

Use CSS variables for consistent theming:

```html
<div style="color: var(--theme-text-primary);">Primary text</div>
<div style="color: var(--theme-text-secondary);">Secondary text</div>
<div style="background-color: var(--theme-bg-primary);">Background</div>
<div style="border-color: var(--theme-border);">Border</div>
```

### Common Variables:
- `--theme-text-primary` - Main text color
- `--theme-text-secondary` - Muted/label text
- `--theme-bg-primary` - Main background
- `--theme-bg-secondary` - Card/section background
- `--theme-border` - Border color
- `--theme-accent` - Accent color (buttons, links)

## Spacing Standards

### Margins and Padding

**Between Major Sections:**
```html
<div class="mb-4"><!-- 1.5rem / 24px --></div>
<div class="mb-5"><!-- 3rem / 48px --></div>
```

**Between Related Items:**
```html
<div class="mb-3"><!-- 1rem / 16px --></div>
```

**Within Cards:**
```html
<div class="tg-card-body" style="padding: 20px;">
    <!-- Standard padding -->
</div>

<div class="tg-card-body" style="padding: 24px 32px;">
    <!-- Spacious padding -->
</div>
```

## Typography Standards

### Heading Hierarchy

```html
<h1 class="tg-card-title {{ gameline }}_heading">Page Title (1.5-2rem)</h1>
<h2 class="{{ gameline }}_heading">Major Section (1.3rem)</h2>
<h3 class="{{ gameline }}_heading">Subsection (1.1rem)</h3>
<h4 class="{{ gameline }}_heading">Minor Section (1rem)</h4>
<h5 class="{{ gameline }}_heading">Detail Section (0.9rem)</h5>
<h6 class="{{ gameline }}_heading">Small Section (0.85rem)</h6>
```

### Text Styles

**Label Text:**
```html
<span style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary);">
    Label
</span>
```

**Large Numbers:**
```html
<span style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary);">
    {{ value }}
</span>
```

**Body Text:**
```html
<p style="line-height: 1.6; color: var(--theme-text-primary);">
    Standard paragraph text
</p>
```

## Form Styling

### Standard Form Layout

```html
<form method="post">
    {% csrf_token %}

    <div class="mb-3">
        <label for="{{ form.name.id_for_label }}" class="form-label">
            {{ form.name.label }}
        </label>
        {{ form.name }}
        {% if form.name.errors %}
            <div class="text-danger">{{ form.name.errors }}</div>
        {% endif %}
    </div>

    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

## Template Blocks

### Standard Block Structure

```html
{% extends "core/base.html" %}
{% load dots sanitize_text %}

{% block title %}{{ object.name }} - TG{% endblock %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/custom.css' %}">
{% endblock %}

{% block content %}
    <div class="container">
        <!-- Page content -->
    </div>
{% endblock %}

{% block extra_js %}
    <script src="{% static 'js/custom.js' %}"></script>
{% endblock %}
```

## Responsive Design

### Mobile Breakpoints

```html
<!-- Stack on mobile, side-by-side on tablet+ -->
<div class="row">
    <div class="col-md-6 col-12">Left</div>
    <div class="col-md-6 col-12">Right</div>
</div>

<!-- Hide on mobile -->
<div class="d-none d-md-block">Desktop only</div>

<!-- Show on mobile only -->
<div class="d-block d-md-none">Mobile only</div>
```

## Accessibility

### ARIA Labels

```html
<button aria-label="Close modal">×</button>
<nav aria-label="Main navigation">...</nav>
<div role="status" aria-live="polite">Status message</div>
```

### Semantic HTML

```html
<!-- Use semantic elements -->
<header>...</header>
<nav>...</nav>
<main>...</main>
<article>...</article>
<aside>...</aside>
<footer>...</footer>
```

## Common Anti-Patterns

❌ **Don't use Bootstrap card classes:**
```html
<!-- Wrong -->
<div class="card">
    <div class="card-header">...</div>
</div>

<!-- Correct -->
<div class="tg-card">
    <div class="tg-card-header">...</div>
</div>
```

❌ **Don't use inline styles for theme colors:**
```html
<!-- Wrong -->
<div style="color: #333;">Text</div>

<!-- Correct -->
<div style="color: var(--theme-text-primary);">Text</div>
```

❌ **Don't skip gameline styling:**
```html
<!-- Wrong -->
<h1>Character Name</h1>

<!-- Correct -->
<h1 class="vtm_heading">Character Name</h1>
```

## Template Checklist

- [ ] Extends appropriate base template
- [ ] Loads required template tags (`{% load dots sanitize_text %}`)
- [ ] Uses `tg-card`, not Bootstrap `card`
- [ ] Uses `tg-table`, not Bootstrap `table`
- [ ] Uses `tg-badge` for status indicators
- [ ] Applies gameline heading classes
- [ ] Uses CSS variables for colors
- [ ] Follows spacing standards (mb-3, mb-4, mb-5)
- [ ] Implements responsive design
- [ ] Includes ARIA labels for accessibility
- [ ] Uses `h-100` for equal-height cards in grids

## See Also

- `/SOURCES/STYLE.md` - Project-wide style guide with more examples
- `/CLAUDE.md` - Template styling conventions section
- `core/docs/TEMPLATE_TAGS.md` - Custom template tag documentation
