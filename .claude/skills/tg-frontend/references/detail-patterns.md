# Detail View Patterns

Reusable component patterns for detail templates.

## Table of Contents
- [Page Headers](#page-headers)
- [Section Cards](#section-cards)
- [Stat Displays](#stat-displays)
- [Boolean Features](#boolean-features)
- [Lists and Grids](#lists-and-grids)
- [Properties Tables](#properties-tables)

## Page Headers

### Standard Header
```html
<div class="tg-card header-card mb-4" data-gameline="{{ object.gameline|lower }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">
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

### Header with Multiple Subtitles
```html
<div class="tg-card header-card mb-4" data-gameline="ctd">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">{{ object.name }}</h1>
        <p class="tg-card-subtitle mb-0">
            <strong>{{ object.get_type_display }}</strong>
            {% if object.subtype %} - {{ object.subtype }}{% endif %}
        </p>
    </div>
</div>
```

## Section Cards

### Centered Header Card
```html
<div class="tg-card">
    <div class="tg-card-header text-center">
        <h5 class="tg-card-title {{ object.get_heading }}">Section Title</h5>
    </div>
    <div class="tg-card-body text-center" style="padding: 20px;">
        <!-- Content -->
    </div>
</div>
```

### Left-Aligned Card (for tables/properties)
```html
<div class="tg-card">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ object.get_heading }}">Properties</h5>
    </div>
    <div class="tg-card-body" style="padding: 20px;">
        <!-- Content -->
    </div>
</div>
```

## Stat Displays

### Inline Stat Box (Label Beside Value)
For compact key-value displays:
```html
<div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
    <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Label:</span>
    <span style="font-weight: 700; color: var(--theme-text-primary);">{{ value }}</span>
</div>
```

### Large Stat Display (Label Below Value)
For prominent statistics:
```html
<div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
    <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ value }}</div>
    <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Label</div>
</div>
```

### Large Stat with Subtext
```html
<div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
    <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ object.value }}</div>
    <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary); margin-bottom: 4px;">Label</div>
    <small class="text-muted" style="font-size: 0.7rem;">{{ object.subtext }}</small>
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

### Dots/Boxes Row (for Advantages)
```html
<div class="row mb-2 text-center">
    <div class="col-3" style="font-weight: 600; color: var(--theme-text-secondary);">Willpower:</div>
    <div class="col-3 dots">{{ object.willpower|dots:10 }}</div>
    <div class="col-3" style="font-weight: 600; color: var(--theme-text-secondary);">Temp Willpower:</div>
    <div class="col-3 dots">{{ object.temporary_willpower|boxes:10 }}</div>
</div>
```

## Boolean Features

### Feature Grid (Yes/No with Background)
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

## Lists and Grids

### Inline Flowing List (Merits, Tags)
```html
<div class="d-flex justify-content-center align-items-center flex-wrap">
    {% for item, value in object.items %}
        <div class="px-3 py-2">
            <a href="{{ item.get_absolute_url }}" style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">{{ item.name }}:</a>
            <span style="font-weight: 700; {% if value > 0 %}color: #28a745;{% else %}color: #dc3545;{% endif %}">{{ value }}</span>
        </div>
    {% endfor %}
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

### Card Grid with Dots Rating
```html
<div class="row">
    {% for item in items %}
        <div class="col-sm-6 col-md-4 col-lg-3 mb-3">
            <div class="tg-card h-100">
                <div class="tg-card-body text-center" style="padding: 16px;">
                    <div class="mb-2">
                        <a href="{{ item.get_absolute_url }}" style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-primary);">{{ item.name }}</a>
                    </div>
                    <div class="dots" style="font-size: 0.875rem;">{{ item.rating|dots }}</div>
                </div>
            </div>
        </div>
    {% endfor %}
</div>
```

## Properties Tables

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

### Appearance Section (Stats + Description)
```html
<div class="tg-card-body text-center" style="padding: 20px;">
    <div class="d-flex justify-content-center align-items-center flex-wrap">
        <div class="px-3 py-2">
            <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">Date of Birth:</span>
            {{ object.date_of_birth }}
        </div>
        <div class="px-3 py-2">
            <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">Age:</span>
            {{ object.age }}
        </div>
    </div>
    <div class="mt-3 text-center">
        <div class="mb-2">
            <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary);">Description:</span>
        </div>
        <p class="mb-0 text-center" style="line-height: 1.6;">{{ object.description|sanitize_html|linebreaks }}</p>
    </div>
</div>
```

## Section Headers Within Cards

```html
<h6 class="{{ object.get_heading }} mb-3" style="font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; font-size: 0.875rem;">Subsection Title</h6>
```

## Display Includes Pattern

For reusable components, create files in `display_includes/` subdirectory:
```html
{% include "locations/mage/node/display_includes/basics.html" %}
{% include "characters/core/meritflaw/display_includes/meritflaw_block.html" %}
```

Common blocks: `{% if object.items %}...{% endif %}` wrapper for conditional display.
