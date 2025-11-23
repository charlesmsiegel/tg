# Items App - Template Style Guide

## Overview

Item templates follow similar patterns to character templates, with gameline-specific styling and polymorphic inheritance. This guide covers item display layouts and gameline-specific patterns.

## Template Inheritance Pattern

```html
<!-- templates/items/werewolf/fetish/detail.html -->
{% extends "items/core/item/detail.html" %}
{% load dots sanitize_text %}

{% block item_header %}
    <!-- Gameline-specific header -->
{% endblock %}

{% block item_stats %}
    <!-- Item statistics (level, gnosis, etc.) -->
{% endblock %}

{% block gameline_specific %}
    <!-- Powers, effects, etc. -->
{% endblock %}
```

## Item Header Card

```html
{% block item_header %}
<div class="tg-card header-card mb-4" data-gameline="wta">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h1 class="tg-card-title wta_heading">{{ item.name }}</h1>
                <p class="tg-card-subtitle">
                    {{ item.item_type }}
                    {% if item.level %}
                        (Level {{ item.level }})
                    {% endif %}
                </p>
            </div>
            <div>
                <span class="tg-badge badge-{{ item.status|lower }}">
                    {{ item.get_status_display }}
                </span>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Item Stats Section

### Two-Column Stats Layout

```html
{% block item_stats %}
<div class="row mb-4">
    <div class="col-md-6 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="wta_heading">Gnosis Requirement</h6>
                <div class="stat-display">
                    {{ item.gnosis|dots }}
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-6 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="wta_heading">Background Cost</h6>
                <div class="stat-value">
                    {{ item.background_cost }}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Stat Box Pattern

```html
<div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
    <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">
        Level:
    </span>
    <span style="font-weight: 700; color: var(--theme-text-primary);">
        {{ item.level }}
    </span>
</div>
```

## Gameline-Specific Sections

### Werewolf: Fetish Power

```html
{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-body">
        <h6 class="wta_heading">Power</h6>
        <p>{{ item.power }}</p>

        <h6 class="wta_heading mt-3">Spirit Type</h6>
        <p>{{ item.spirit_type }}</p>

        {% if item.activation %}
            <h6 class="wta_heading mt-3">Activation</h6>
            <p>{{ item.activation }}</p>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### Mage: Wonder Effects

```html
{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title mta_heading">Wonder Properties</h5>
    </div>
    <div class="tg-card-body">
        <div class="row mb-3">
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Arete</div>
                    <div class="stat-value">{{ item.arete|dots }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Quintessence</div>
                    <div class="stat-value">{{ item.quintessence }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Paradox</div>
                    <div class="stat-value">{{ item.paradox }}</div>
                </div>
            </div>
        </div>

        <h6 class="mta_heading">Sphere Requirements</h6>
        <div class="row">
            {% for sphere, level in item.sphere_requirements.items %}
                <div class="col-md-6 mb-2">
                    <div class="trait-row">
                        <span class="trait-name">{{ sphere }}:</span>
                        <span class="trait-dots">{{ level|dots }}</span>
                    </div>
                </div>
            {% endfor %}
        </div>

        <h6 class="mta_heading mt-3">Effects</h6>
        <p>{{ item.effects|sanitize_html }}</p>
    </div>
</div>
{% endblock %}
```

## Item Properties Card

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ item.get_heading }}">Properties</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% if item.weight %}
                <div class="col-md-6 mb-2">
                    <strong>Weight:</strong> {{ item.weight }} lbs
                </div>
            {% endif %}
            {% if item.value %}
                <div class="col-md-6 mb-2">
                    <strong>Value:</strong> {{ item.value }} (Resources dots)
                </div>
            {% endif %}
            {% if item.owner %}
                <div class="col-md-6 mb-2">
                    <strong>Owner:</strong>
                    <a href="{% url 'accounts:profile' item.owner.pk %}">
                        {{ item.owner.username }}
                    </a>
                </div>
            {% endif %}
            {% if item.chronicle %}
                <div class="col-md-6 mb-2">
                    <strong>Chronicle:</strong>
                    <a href="{{ item.chronicle.get_absolute_url }}">
                        {{ item.chronicle.name }}
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
```

## Description Section

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ item.get_heading }}">Description</h5>
    </div>
    <div class="tg-card-body">
        {{ item.description|sanitize_html }}
    </div>
</div>
```

## Item List View

```html
<div class="tg-card">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Items</h5>
    </div>
    <div class="tg-card-body">
        <table class="tg-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Level</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for item in items %}
                    <tr>
                        <td>
                            <a href="{{ item.get_absolute_url }}">
                                {{ item.name }}
                            </a>
                        </td>
                        <td>{{ item.item_type }}</td>
                        <td>{{ item.level|default:"—" }}</td>
                        <td>
                            <span class="tg-badge badge-{{ item.status|lower }}">
                                {{ item.get_status_display }}
                            </span>
                        </td>
                        <td>
                            {% if can_edit %}
                                <a href="{{ item.get_update_url }}" class="btn btn-sm btn-primary">
                                    Edit
                                </a>
                            {% endif %}
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="5" class="text-center text-muted">
                            No items found
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

## Responsive Design

```html
<!-- Desktop: 2 columns, Mobile: 1 column -->
<div class="row">
    <div class="col-md-6 col-12 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="{{ item.get_heading }}">Stat 1</h6>
                <!-- Content -->
            </div>
        </div>
    </div>
    <div class="col-md-6 col-12 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="{{ item.get_heading }}">Stat 2</h6>
                <!-- Content -->
            </div>
        </div>
    </div>
</div>
```

## Template Checklist

- [ ] Extends `items/core/item/detail.html`
- [ ] Loads template tags (`{% load dots sanitize_text %}`)
- [ ] Uses gameline-specific heading class
- [ ] Displays status badge
- [ ] Shows item stats in organized layout
- [ ] Includes gameline-specific properties
- [ ] Sanitizes description HTML
- [ ] Implements responsive design
- [ ] Uses `tg-card` components
- [ ] Uses `h-100` for equal-height cards

## See Also

- `characters/docs/STYLE.md` - Character template patterns (similar structure)
- `core/docs/STYLE.md` - Base template styling
- `/SOURCES/STYLE.md` - Project-wide style guide
