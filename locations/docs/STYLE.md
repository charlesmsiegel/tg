# Locations App - Template Style Guide

## Overview

Location templates follow similar patterns to character and item templates, with gameline-specific styling. This guide covers location display layouts and gameline-specific patterns.

## Template Inheritance Pattern

```html
<!-- templates/locations/werewolf/caern/detail.html -->
{% extends "locations/core/location/detail.html" %}
{% load dots sanitize_text %}

{% block location_header %}
    <!-- Gameline-specific header -->
{% endblock %}

{% block location_stats %}
    <!-- Location statistics -->
{% endblock %}

{% block gameline_specific %}
    <!-- Special properties -->
{% endblock %}
```

## Location Header Card

```html
{% block location_header %}
<div class="tg-card header-card mb-4" data-gameline="wta">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h1 class="tg-card-title wta_heading">{{ location.name }}</h1>
                <p class="tg-card-subtitle">
                    {{ location.location_type }}
                    {% if location.level %}
                        (Level {{ location.level }})
                    {% endif %}
                </p>
                {% if location.city %}
                    <p class="text-muted">{{ location.city }}</p>
                {% endif %}
            </div>
            <div>
                <span class="tg-badge badge-{{ location.status|lower }}">
                    {{ location.get_status_display }}
                </span>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Geographic Information

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ location.get_heading }}">Location</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% if location.address %}
                <div class="col-md-12 mb-2">
                    <strong>Address:</strong><br>
                    {{ location.address }}
                </div>
            {% endif %}
            {% if location.city %}
                <div class="col-md-6 mb-2">
                    <strong>City:</strong> {{ location.city }}
                </div>
            {% endif %}
            {% if location.country %}
                <div class="col-md-6 mb-2">
                    <strong>Country:</strong> {{ location.country }}
                </div>
            {% endif %}
            {% if location.size %}
                <div class="col-md-6 mb-2">
                    <strong>Size:</strong> {{ location.size }}
                </div>
            {% endif %}
        </div>
    </div>
</div>
```

## Location Stats Section

### Three-Column Stats Layout

```html
{% block location_stats %}
<div class="row mb-4">
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body text-center">
                <h6 class="wta_heading">Caern Level</h6>
                <div class="stat-large">{{ location.level }}</div>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body text-center">
                <h6 class="wta_heading">Gauntlet Rating</h6>
                <div class="stat-large">{{ location.gauntlet_rating }}</div>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body text-center">
                <h6 class="wta_heading">Gnosis/Day</h6>
                <div class="stat-large">{{ location.gnosis_per_day }}</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Large Stat Display

```css
.stat-large {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--theme-text-primary);
    margin-top: 8px;
}
```

## Gameline-Specific Sections

### Werewolf: Caern Properties

```html
{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title wta_heading">Caern Properties</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            <div class="col-md-6 mb-3">
                <h6 class="wta_heading">Totem</h6>
                <p>{{ location.totem }}</p>
            </div>
            {% if location.tribe %}
                <div class="col-md-6 mb-3">
                    <h6 class="wta_heading">Tribe</h6>
                    <p>{{ location.tribe.name }}</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### Mage: Node Properties

```html
{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title mta_heading">Node Properties</h5>
    </div>
    <div class="tg-card-body">
        <div class="row mb-3">
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Quintessence/Day</div>
                    <div class="stat-value">{{ location.quintessence_per_day }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Aura</div>
                    <div class="stat-value">{{ location.aura }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Resonance</div>
                    <div class="stat-value">{{ location.resonance }}</div>
                </div>
            </div>
        </div>

        {% if location.sphere_affinities %}
            <h6 class="mta_heading">Sphere Affinities</h6>
            <div class="sphere-list">
                {% for sphere in location.sphere_affinities %}
                    <span class="tg-badge badge-pill badge-app">{{ sphere }}</span>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

## Reality Zone Display (Mage)

```html
{% block reality_zone %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title mta_heading">Reality Zone</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% for sphere, max_level in location.reality_zone.items %}
                <div class="col-md-6 mb-2">
                    <div class="trait-row">
                        <span class="trait-name">{{ sphere }}:</span>
                        <span class="trait-dots">{{ max_level|dots }}</span>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

## Description Section

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ location.get_heading }}">Description</h5>
    </div>
    <div class="tg-card-body">
        {{ location.description|sanitize_html }}
    </div>
</div>
```

## Associated Characters/Items

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ location.get_heading }}">Associated Characters</h5>
    </div>
    <div class="tg-card-body">
        {% if location.characters.all %}
            <ul class="character-list">
                {% for character in location.characters.all %}
                    <li>
                        <a href="{{ character.get_absolute_url }}">
                            {{ character.name }}
                        </a>
                        ({{ character.get_type_display }})
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <p class="text-muted">No associated characters</p>
        {% endif %}
    </div>
</div>
```

## Location List View

```html
<div class="tg-card">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Locations</h5>
    </div>
    <div class="tg-card-body">
        <table class="tg-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>City</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for location in locations %}
                    <tr>
                        <td>
                            <a href="{{ location.get_absolute_url }}">
                                {{ location.name }}
                            </a>
                        </td>
                        <td>{{ location.location_type }}</td>
                        <td>{{ location.city|default:"—" }}</td>
                        <td>
                            <span class="tg-badge badge-{{ location.status|lower }}">
                                {{ location.get_status_display }}
                            </span>
                        </td>
                        <td>
                            {% if can_edit %}
                                <a href="{{ location.get_update_url }}" class="btn btn-sm btn-primary">
                                    Edit
                                </a>
                            {% endif %}
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="5" class="text-center text-muted">
                            No locations found
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

## Template Checklist

- [ ] Extends `locations/core/location/detail.html`
- [ ] Loads template tags (`{% load dots sanitize_text %}`)
- [ ] Uses gameline-specific heading class
- [ ] Displays status badge
- [ ] Shows geographic information
- [ ] Includes gameline-specific properties
- [ ] Sanitizes description HTML
- [ ] Implements responsive design
- [ ] Uses `tg-card` components
- [ ] Uses `h-100` for equal-height cards

## See Also

- `characters/docs/STYLE.md` - Character template patterns
- `items/docs/STYLE.md` - Item template patterns
- `core/docs/STYLE.md` - Base template styling
- `/SOURCES/STYLE.md` - Project-wide style guide
