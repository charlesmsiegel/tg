---
name: tg-frontend-specifications
description: Provides comprehensive frontend design specifications for the World of Darkness tabletop RPG application. Use when building or reviewing HTML templates, creating forms, implementing CSS styles, ensuring design consistency, or applying gameline-specific theming. Covers detail views, forms, components, stat displays, and responsive layouts.
allowed-tools: Read, Glob, Grep
---

# TG Frontend Specifications

This skill provides the complete frontend design system for the Tellurium Games World of Darkness web application.

## When to Use This Skill

- Creating or modifying HTML templates (detail views, forms, lists)
- Implementing new components or stat displays
- Reviewing templates for design consistency
- Applying gameline-specific theming (Mage, Vampire, Werewolf, etc.)
- Building responsive layouts
- Styling forms to match detail views

## Core Design Principles

### 1. Use TG Components, Not Bootstrap

Always use custom TG classes instead of Bootstrap defaults:

| Use This | NOT This |
|----------|----------|
| `tg-card` | `card` |
| `tg-card-header` | `card-header` |
| `tg-card-body` | `card-body` |
| `tg-card-title` | `card-title` |
| `tg-table` | `table` |
| `tg-badge` | `badge` |
| `tg-btn` | `btn` |

### 2. Centered, Card-Based Layouts

- Card headers should be centered using `text-center` class
- Large stat displays should be centered and prominent
- Content boxes use subtle backgrounds for visual hierarchy

### 3. Gameline-Specific Theming

Apply gameline classes to headers and titles:

| Gameline | Heading Class | Data Attribute |
|----------|---------------|----------------|
| Mage: The Ascension | `mta_heading` | `data-gameline="mta"` |
| Vampire: The Masquerade | `vtm_heading` | `data-gameline="vtm"` |
| Werewolf: The Apocalypse | `wta_heading` | `data-gameline="wta"` |
| Changeling: The Dreaming | `ctd_heading` | `data-gameline="ctd"` |
| Wraith: The Oblivion | `wto_heading` | `data-gameline="wto"` |
| Demon: The Fallen | `dtf_heading` | `data-gameline="dtf"` |
| Hunter: The Reckoning | `htr_heading` | `data-gameline="htr"` |
| Mummy: The Resurrection | `mtr_heading` | `data-gameline="mtr"` |

Use `{{ object.get_heading }}` in templates for dynamic heading class.

---

## Detail View Patterns

### Page Header Card

```html
<div class="tg-card header-card mb-4" data-gameline="mta">
    <div class="tg-card-header">
        <h1 class="tg-card-title mta_heading">
            {{ object.name }}
            {% if object.rank %}<small><span class="dots colored-dots">{{ object.rank|dots }}</span></small>{% endif %}
        </h1>
        {% if object.parent %}
            <p class="tg-card-subtitle mb-0">
                Located in: <a href="{{ object.parent.get_absolute_url }}">{{ object.parent.name }}</a>
            </p>
        {% endif %}
    </div>
</div>
```

### Section Card with Centered Header

```html
<div class="tg-card">
    <div class="tg-card-header text-center">
        <h5 class="tg-card-title {{ object.get_heading }}">Section Title</h5>
    </div>
    <div class="tg-card-body text-center" style="padding: 20px;">
        <!-- Content here -->
    </div>
</div>
```

### Inline Stat Box (Label Beside Value)

For compact key-value displays:

```html
<div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
    <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Label:</span>
    <span style="font-weight: 700; color: var(--theme-text-primary);">{{ value }}</span>
</div>
```

### Large Stat Display (Label Above Value)

For prominent statistics:

```html
<div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
    <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ value }}</div>
    <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Label</div>
</div>
```

### Three-Column Stat Grid

```html
<div class="row text-center">
    <div class="col-md-4 mb-3 mb-md-0">
        <div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
            <div style="font-size: 1.2rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ object.value1|dots }}</div>
            <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Label 1</div>
        </div>
    </div>
    <div class="col-md-4 mb-3 mb-md-0">
        <!-- Stat 2 -->
    </div>
    <div class="col-md-4 mb-3 mb-md-0">
        <!-- Stat 3 -->
    </div>
</div>
```

### Two-Column Properties Card

```html
<div class="row mb-4">
    <div class="col-md-6 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-header text-center">
                <h5 class="tg-card-title {{ object.get_heading }}">Properties</h5>
            </div>
            <div class="tg-card-body" style="padding: 20px;">
                <div class="row mb-2">
                    <div class="col-6"><strong>Label:</strong></div>
                    <div class="col-6">{{ object.value }}</div>
                </div>
                <!-- More rows -->
            </div>
        </div>
    </div>
    <div class="col-md-6 mb-3">
        <!-- Second card -->
    </div>
</div>
```

### Boolean Feature Grid

For displaying yes/no features:

```html
<div class="row">
    <div class="col-6 mb-2">
        <div style="padding: 8px; border-radius: 4px; background-color: {{ object.feature|yesno:'rgba(0,255,0,0.1),rgba(0,0,0,0.02)' }};">
            <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary); margin-bottom: 2px;">Feature Name</div>
            <div style="font-weight: 700; color: var(--theme-text-primary);">{{ object.feature|yesno:"Yes,No" }}</div>
        </div>
    </div>
</div>
```

### Inline Flowing List (Merits, Tags, etc.)

```html
<div class="tg-card-body text-center" style="padding: 20px;">
    <div class="d-flex justify-content-center align-items-center flex-wrap">
        {% for item, value in object.items %}
            <div class="px-3 py-2">
                <a href="{{ item.get_absolute_url }}" style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">{{ item.name }}:</a>
                <span style="font-weight: 700; {% if value > 0 %}color: #28a745;{% else %}color: #dc3545;{% endif %}">{{ value }}</span>
            </div>
        {% endfor %}
    </div>
</div>
```

### Card Grid for Related Items

```html
<div class="row">
    {% for item in items %}
        <div class="col-sm-6 col-md-4 col-lg-3 mb-3">
            <div class="tg-card h-100">
                <div class="tg-card-body text-center" style="padding: 16px;">
                    <div class="mb-2">
                        <a href="{{ item.get_absolute_url }}" style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-primary);">{{ item.name }}</a>
                    </div>
                    <div style="font-size: 0.75rem; color: var(--theme-text-secondary);">{{ item.subtitle }}</div>
                </div>
            </div>
        </div>
    {% endfor %}
</div>
```

---

## Form Patterns

Forms should visually match detail views. The Haven form is the gold standard example.

### Modern Form Card Structure

```html
{% extends "core/form.html" %}
{% block creation_title %}
    {% if object %}Update{% else %}Create{% endif %} Object Name
{% endblock creation_title %}
{% block contents %}
    <div class="tg-card">
        <div class="tg-card-header">
            <h2 class="tg-card-title {{ object.get_heading|default:'mta_heading' }}">Section Title</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <!-- Form fields here -->
        </div>
    </div>
{% endblock contents %}
```

### Form Field with Label (Text/Select)

```html
<div class="row mb-3">
    <div class="col-md-6">
        <label for="{{ form.name.id_for_label }}" class="form-label">Name</label>
        {{ form.name }}
    </div>
    <div class="col-md-6">
        <label for="{{ form.parent.id_for_label }}" class="form-label">Parent Location</label>
        {{ form.parent }}
    </div>
</div>
```

### Three-Column Form Row

```html
<div class="row mb-3">
    <div class="col-md-4">
        <label for="{{ form.size.id_for_label }}" class="form-label">Size</label>
        {{ form.size }}
    </div>
    <div class="col-md-4">
        <label for="{{ form.security.id_for_label }}" class="form-label">Security (0-5 dots)</label>
        {{ form.security }}
    </div>
    <div class="col-md-4">
        <label for="{{ form.location.id_for_label }}" class="form-label">Location Quality (0-5 dots)</label>
        {{ form.location }}
    </div>
</div>
```

### Checkbox Group with Section Header

```html
<div class="row mb-3">
    <div class="col-md-12">
        <h6 class="{{ object.get_heading|default:'mta_heading' }} mb-2">Features</h6>
    </div>
    <div class="col-md-4">
        <div class="form-check">
            {{ form.has_feature }}
            <label class="form-check-label" for="{{ form.has_feature.id_for_label }}">
                Has Feature
            </label>
        </div>
    </div>
    <div class="col-md-4">
        <div class="form-check">
            {{ form.another_feature }}
            <label class="form-check-label" for="{{ form.another_feature.id_for_label }}">
                Another Feature
            </label>
        </div>
    </div>
</div>
```

### Textarea Field

```html
<div class="row mb-3">
    <div class="col-md-12">
        <label for="{{ form.description.id_for_label }}" class="form-label">Description</label>
        {{ form.description }}
    </div>
</div>
```

### Multi-Section Form

```html
{% block contents %}
    <!-- Section 1: Basic Information -->
    <div class="tg-card mb-4">
        <div class="tg-card-header">
            <h2 class="tg-card-title {{ object.get_heading }}">Basic Information</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <!-- Basic fields -->
        </div>
    </div>

    <!-- Section 2: Properties -->
    <div class="tg-card mb-4">
        <div class="tg-card-header">
            <h2 class="tg-card-title {{ object.get_heading }}">Properties</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <!-- Property fields -->
        </div>
    </div>

    <!-- Section 3: Features -->
    <div class="tg-card">
        <div class="tg-card-header">
            <h2 class="tg-card-title {{ object.get_heading }}">Features</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <!-- Feature checkboxes -->
        </div>
    </div>
{% endblock contents %}
```

---

## Template Tags

Load these at the top of templates:

```html
{% load sanitize_text dots %}
```

### Dots Filter

Displays WoD-style dot ratings:

```html
{{ rating|dots }}      → ●●●○○ (default max 5)
{{ rating|dots:10 }}   → ●●●○○○○○○○ (explicit max 10)
```

Auto-expands to 10 if value exceeds 5.

### Boxes Filter

Displays box-style ratings (for temporary values):

```html
{{ value|boxes }}      → ■■■□□
{{ value|boxes:10 }}   → ■■■□□□□□□□
```

### Sanitize Filter

Safe HTML rendering:

```html
{{ content|sanitize_html }}
{{ content|sanitize_html|linebreaks }}
```

---

## Status Badges

```html
<span class="tg-badge badge-{{ object.status|lower }}">{{ object.get_status_display }}</span>
```

| Status | Class | Appearance |
|--------|-------|------------|
| Unfinished | `badge-un` | Gray |
| Submitted | `badge-sub` | Blue |
| Approved | `badge-app` | Green |
| Retired | `badge-ret` | Orange |
| Deceased | `badge-dec` | Red |

---

## Gameline Badge Colors

Gameline badges are used in index pages to identify object types. Use `{{ object.get_badge_class }}` to get the appropriate class dynamically.

### Badge Classes

| Gameline | Badge Class | Light Theme | Dark Theme |
|----------|-------------|-------------|------------|
| Vampire: The Masquerade | `badge-vtm` | `#8b0000` (Dark Red) | `#dc143c` (Crimson) |
| Werewolf: The Apocalypse | `badge-wta` | `#228b22` (Forest Green) | `#32cd32` (Lime Green) |
| Mage: The Ascension | `badge-mta` | `#4b0082` (Indigo) | `#9370db` (Medium Purple) |
| Changeling: The Dreaming | `badge-ctd` | `#20b2aa` (Light Sea Green) | `#48d1cc` (Medium Turquoise) |
| Wraith: The Oblivion | `badge-wto` | `#2f4f4f` (Dark Slate Gray) | `#708090` (Slate Gray) |
| Hunter: The Reckoning | `badge-htr` | `#d4a017` (Golden Yellow) | `#ffa500` (Orange) |
| Demon: The Fallen | `badge-dtf` | `#e74c3c` (Bright Red) | `#e74c3c` (Bright Red) |
| Mummy: The Resurrection | `badge-mtr` | `#8e44ad` (Purple) | `#bb8fce` (Light Purple) |
| World of Darkness (generic) | `badge-wod` | `#6c757d` (Gray) | `#6c757d` (Gray) |

### Light Variants (for Secondary Types)

For secondary character types (mortals, companions, ghouls), use light variants with reduced opacity:

| Class | Usage |
|-------|-------|
| `badge-vtm-light` | Ghouls, Revenants |
| `badge-wta-light` | Kinfolk, Fera companions |
| `badge-mta-light` | Sorcerers, Consors |
| `badge-ctd-light` | Kinain, Enchanted |
| `badge-wto-light` | Risen, Spectres |

These use the same base color with `opacity: 0.7`.

### CSS Variables

Gameline colors are defined as CSS variables in `static/themes/theme-system.css`:

```css
/* Light Theme */
--gameline-vtm: #8b0000;
--gameline-wta: #228b22;
--gameline-mta: #4b0082;
--gameline-ctd: #ff69b4;  /* Hot Pink - but badges use #20b2aa */
--gameline-wto: #2f4f4f;
--gameline-htr: #d4a017;
--gameline-dtf: #e74c3c;
--gameline-mtr: #8e44ad;

/* Dark Theme (brighter for visibility) */
--gameline-vtm: #dc143c;
--gameline-wta: #32cd32;
--gameline-mta: #9370db;
--gameline-ctd: #ff69b4;  /* Hot Pink - but badges use #48d1cc */
--gameline-wto: #708090;
--gameline-htr: #ffa500;
--gameline-dtf: #e74c3c;
--gameline-mtr: #bb8fce;
```

### Usage in Templates

```html
<!-- Type badge in index tables -->
<span class="tg-badge {{ item.get_badge_class }} badge-pill">{{ item.get_type }}</span>

<!-- Manual badge -->
<span class="tg-badge badge-mta badge-pill">Talisman</span>

<!-- Light variant for secondary types -->
<span class="tg-badge badge-vtm-light badge-pill">Ghoul</span>
```

### Badge Styling in Index Pages

Index pages include additional badge styling in their `{% block styling %}`:

```css
/* Gameline-specific badge colors */
.tg-badge.badge-vtm {
    background-color: var(--gameline-vtm);
    color: var(--color-white);
}

/* Light variants use opacity */
.tg-badge.badge-vtm-light {
    background-color: #8b0000;
    opacity: 0.7;
    color: var(--color-white);
}
```

### Gameline Fonts

Each gameline has a distinctive font for headings:

| Gameline | Font Family | CSS Variable |
|----------|-------------|--------------|
| VTM | Delavan | `--font-family-vtm` |
| WTA | Balthazar | `--font-family-wta` |
| MTA | Abbess | `--font-family-mta` |
| CTD | Kells | `--font-family-ctd` |
| WTO | MatrixTall | `--font-family-wto` |
| HTR | Futura PT | `--font-family-htr` |
| WoD | OPTIProtea | `--font-family-wod` |

---

## Spacing Standards

### Card Body Padding

- Standard: `padding: 20px;`
- Spacious: `padding: 24px;` to `padding: 32px;`

### Margins

- Between major sections: `mb-4` or `mb-5`
- Between related items: `mb-3`
- Between form rows: `mb-3`
- Between closely related items: `mb-2`

### Inline Spacing

- Label-value gap: `margin-right: 8px`

---

## Typography

### Labels

```css
font-weight: 600;
font-size: 0.75rem;
text-transform: uppercase;
letter-spacing: 0.5px;
color: var(--theme-text-secondary);
```

### Values

```css
font-weight: 700;
color: var(--theme-text-primary);
```

### Large Numbers

```css
font-size: 1.5rem;  /* or 1.75rem for very prominent */
font-weight: 700;
color: var(--theme-text-primary);
```

### Section Headers in Cards

Use `<h6>` with gameline class:

```html
<h6 class="mta_heading mb-3" style="font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; font-size: 0.875rem;">Section Title</h6>
```

---

## Color Usage

### Backgrounds

- Primary stat boxes: `rgba(0,0,0,0.05)`
- Content boxes: `rgba(0,0,0,0.02)`
- Active/positive features: `rgba(0,255,0,0.1)`

### Text Colors

- Primary: `var(--theme-text-primary)`
- Secondary (labels): `var(--theme-text-secondary)`
- Muted: `text-muted` class

### Value Colors

- Positive values: `color: #28a745;`
- Negative values: `color: #dc3545;`

---

## Responsive Design

### Column Patterns

- Two-column: `col-md-6`
- Three-column: `col-md-4`
- Four-column card grid: `col-sm-6 col-md-4 col-lg-3`

### Mobile Margins

Add bottom margin on mobile, remove on desktop:

```html
<div class="col-md-4 mb-3 mb-md-0">
```

### Equal Height Cards

Use `h-100` on cards within grid:

```html
<div class="col-md-6 mb-3">
    <div class="tg-card h-100">
```

---

## Template Inheritance

### Base Templates

- All objects: `core/object.html`
- All forms: `core/form.html`
- Locations: `locations/core/location/detail.html`
- Items: `items/core/item/detail.html`
- Characters: `characters/core/character/detail.html`

### Common Blocks

- `{% block objectname %}` - Page header
- `{% block contents %}` - Main content
- `{% block model_specific %}` - Gameline-specific content
- `{% block additional_stats %}` - Extra statistics
- `{% block description %}` - Description section

### Display Includes

Reusable components in `display_includes/` subdirectories:

```html
{% include "locations/mage/node/display_includes/basics.html" %}
{% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
{% include "characters/mage/resonance/display_includes/resonance.html" %}
```

---

## Consistency Checklist

When creating or reviewing templates:

- [ ] All cards use `tg-card` components (not Bootstrap `card`)
- [ ] Headers have gameline class and `data-gameline` attribute
- [ ] Headers are centered where appropriate
- [ ] Spacing follows standards (20-24px padding, proper margins)
- [ ] Labels use uppercase styling with proper font size
- [ ] Values use bold weight
- [ ] Forms use proper `form-label` classes
- [ ] Checkboxes wrapped in `form-check` divs
- [ ] Layout is responsive (mobile-friendly)
- [ ] Equal-height cards use `h-100`
- [ ] Template loads required filters (`{% load dots sanitize_text %}`)

---

## Reference Files

- Style guide: `SOURCES/STYLE.md`
- CSS components: `static/themes/components.css`
- Base styles: `static/style.css`
- Example detail template: `locations/templates/locations/vampire/haven/detail.html`
- Example form template: `locations/templates/locations/vampire/haven/form.html`
- Example display include: `locations/templates/locations/mage/node/display_includes/basics.html`
