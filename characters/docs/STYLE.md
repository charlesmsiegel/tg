# Characters App - Template Style Guide

## Overview

Character templates use gameline-specific styling and polymorphic template inheritance. This guide covers character sheet layouts, stat displays, and gameline-specific patterns.

## Template Inheritance Pattern

### Base Character Template

All character detail templates extend the base character template:

```html
<!-- templates/characters/vampire/vampire/detail.html -->
{% extends "characters/core/character/detail.html" %}
{% load dots sanitize_text %}

{% block character_header %}
    <!-- Gameline-specific header -->
{% endblock %}

{% block character_vitals %}
    <!-- Gameline-specific vitals (Blood Pool, Rage, etc.) -->
{% endblock %}

{% block gameline_specific %}
    <!-- Powers, abilities, etc. -->
{% endblock %}
```

### Block Structure

Standard blocks in character templates:

- `{% block title %}` - Page title
- `{% block character_header %}` - Character name, concept, status
- `{% block character_vitals %}` - Health, resources, power pools
- `{% block attributes %}` - Physical/Social/Mental attributes
- `{% block abilities %}` - Talents, Skills, Knowledges
- `{% block backgrounds %}` - Backgrounds and advantages
- `{% block gameline_specific %}` - Disciplines, Gifts, Spheres, etc.
- `{% block merits_flaws %}` - Merits and Flaws
- `{% block xp_section %}` - XP display and spending

## Character Header Card

### Standard Header

```html
{% block character_header %}
<div class="tg-card header-card mb-4" data-gameline="vtm">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h1 class="tg-card-title vtm_heading">{{ character.name }}</h1>
                <p class="tg-card-subtitle">
                    {{ character.concept }}
                    {% if character.clan %}
                        - {{ character.clan.name }}
                    {% endif %}
                </p>
            </div>
            <div>
                <span class="tg-badge badge-{{ character.status|lower }}">
                    {{ character.get_status_display }}
                </span>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Header with Edit Button

```html
<div class="tg-card header-card mb-4" data-gameline="vtm">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h1 class="tg-card-title vtm_heading">{{ character.name }}</h1>
                <p class="tg-card-subtitle">{{ character.concept }}</p>
            </div>
            <div>
                {% if can_edit %}
                    <a href="{{ character.get_update_url }}" class="btn btn-sm btn-primary">
                        Edit
                    </a>
                {% endif %}
                <span class="tg-badge badge-pill badge-{{ character.status|lower }}">
                    {{ character.get_status_display }}
                </span>
            </div>
        </div>
    </div>
</div>
```

## Character Vitals Section

### Three-Column Vitals Layout

```html
{% block character_vitals %}
<div class="row mb-4">
    <!-- Health/Corpus -->
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="vtm_heading">Health</h6>
                <div class="stat-display">
                    {{ character.health|boxes:7 }}
                </div>
            </div>
        </div>
    </div>

    <!-- Willpower -->
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="vtm_heading">Willpower</h6>
                <div class="stat-display">
                    {{ character.current_willpower|dots:character.willpower }}
                    <span class="numeric">({{ character.current_willpower }}/{{ character.willpower }})</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Resource Pool (Blood Pool, Rage, Quintessence, etc.) -->
    <div class="col-md-4 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="vtm_heading">Blood Pool</h6>
                <div class="stat-display">
                    {{ character.blood_pool|dots:character.blood_max }}
                    <span class="numeric">({{ character.blood_pool }}/{{ character.blood_max }})</span>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Attributes Display

### Standard Three-Category Layout

```html
{% block attributes %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title vtm_heading">Attributes</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            <!-- Physical -->
            <div class="col-md-4">
                <h6 class="vtm_heading">Physical</h6>
                <div class="trait-list">
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
            </div>

            <!-- Social -->
            <div class="col-md-4">
                <h6 class="vtm_heading">Social</h6>
                <div class="trait-list">
                    <div class="trait-row">
                        <span class="trait-name">Charisma:</span>
                        <span class="trait-dots">{{ character.charisma|dots }}</span>
                    </div>
                    <div class="trait-row">
                        <span class="trait-name">Manipulation:</span>
                        <span class="trait-dots">{{ character.manipulation|dots }}</span>
                    </div>
                    <div class="trait-row">
                        <span class="trait-name">Appearance:</span>
                        <span class="trait-dots">{{ character.appearance|dots }}</span>
                    </div>
                </div>
            </div>

            <!-- Mental -->
            <div class="col-md-4">
                <h6 class="vtm_heading">Mental</h6>
                <div class="trait-list">
                    <div class="trait-row">
                        <span class="trait-name">Perception:</span>
                        <span class="trait-dots">{{ character.perception|dots }}</span>
                    </div>
                    <div class="trait-row">
                        <span class="trait-name">Intelligence:</span>
                        <span class="trait-dots">{{ character.intelligence|dots }}</span>
                    </div>
                    <div class="trait-row">
                        <span class="trait-name">Wits:</span>
                        <span class="trait-dots">{{ character.wits|dots }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Custom CSS for Trait Rows

```css
.trait-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}

.trait-row:last-child {
    border-bottom: none;
}

.trait-name {
    font-weight: 500;
    color: var(--theme-text-primary);
}

.trait-dots {
    font-size: 1.1rem;
    letter-spacing: 2px;
    color: var(--theme-accent);
}
```

## Abilities Display

### Three-Column Layout with Specialties

```html
{% block abilities %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title vtm_heading">Abilities</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            <!-- Talents -->
            <div class="col-md-4">
                <h6 class="vtm_heading">Talents</h6>
                {% for talent, rating in character.get_talents.items %}
                    <div class="trait-row">
                        <span class="trait-name">
                            {{ talent }}
                            {% if talent in character.specialties %}
                                <span class="specialty">({{ character.specialties[talent] }})</span>
                            {% endif %}
                        </span>
                        <span class="trait-dots">{{ rating|dots }}</span>
                    </div>
                {% endfor %}
            </div>

            <!-- Skills -->
            <div class="col-md-4">
                <h6 class="vtm_heading">Skills</h6>
                {% for skill, rating in character.get_skills.items %}
                    <div class="trait-row">
                        <span class="trait-name">
                            {{ skill }}
                            {% if skill in character.specialties %}
                                <span class="specialty">({{ character.specialties[skill] }})</span>
                            {% endif %}
                        </span>
                        <span class="trait-dots">{{ rating|dots }}</span>
                    </div>
                {% endfor %}
            </div>

            <!-- Knowledges -->
            <div class="col-md-4">
                <h6 class="vtm_heading">Knowledges</h6>
                {% for knowledge, rating in character.get_knowledges.items %}
                    <div class="trait-row">
                        <span class="trait-name">
                            {{ knowledge }}
                            {% if knowledge in character.specialties %}
                                <span class="specialty">({{ knowledge.specialties[knowledge] }})</span>
                            {% endif %}
                        </span>
                        <span class="trait-dots">{{ rating|dots }}</span>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Specialty Styling

```css
.specialty {
    font-size: 0.85rem;
    font-style: italic;
    color: var(--theme-text-secondary);
    margin-left: 4px;
}
```

## Gameline-Specific Powers

### Vampire: Disciplines

```html
{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title vtm_heading">Disciplines</h5>
    </div>
    <div class="tg-card-body">
        {% if character.disciplines %}
            <div class="row">
                {% for discipline, rating in character.disciplines.items %}
                    <div class="col-md-4 mb-2">
                        <div class="trait-row">
                            <span class="trait-name">{{ discipline }}:</span>
                            <span class="trait-dots">{{ rating|dots }}</span>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <p class="text-muted">No disciplines yet</p>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### Werewolf: Gifts

```html
{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title wta_heading">Gifts</h5>
    </div>
    <div class="tg-card-body">
        {% if character.gifts %}
            {% for gift_type, gifts in character.gifts_by_type.items %}
                <h6 class="wta_heading">{{ gift_type }}</h6>
                <ul class="gift-list">
                    {% for gift in gifts %}
                        <li>
                            <strong>{{ gift.name }}</strong> (Level {{ gift.level }})
                            <p class="text-muted">{{ gift.description|truncatewords:20 }}</p>
                        </li>
                    {% endfor %}
                </ul>
            {% endfor %}
        {% else %}
            <p class="text-muted">No gifts yet</p>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### Mage: Spheres

```html
{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title mta_heading">Spheres</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% for sphere, rating in character.spheres.items %}
                <div class="col-md-4 mb-3">
                    <div class="sphere-display">
                        <div class="sphere-name">{{ sphere }}</div>
                        <div class="sphere-dots">{{ rating|dots }}</div>
                    </div>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

## Display Includes Pattern

### Creating Reusable Components

**File: `templates/characters/vampire/vampire/display_includes/disciplines.html`**

```html
{% load dots %}

<div class="disciplines-section">
    {% if disciplines %}
        <div class="row">
            {% for discipline, rating in disciplines.items %}
                <div class="col-md-6 mb-2">
                    <div class="discipline-item">
                        <span class="discipline-name">{{ discipline }}</span>
                        <span class="discipline-dots">{{ rating|dots }}</span>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p class="text-muted">No disciplines</p>
    {% endif %}
</div>
```

### Using Display Includes

```html
{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title vtm_heading">Disciplines</h5>
    </div>
    <div class="tg-card-body">
        {% include "characters/vampire/vampire/display_includes/disciplines.html" with disciplines=character.disciplines %}
    </div>
</div>
{% endblock %}
```

## Backgrounds Display

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title vtm_heading">Backgrounds</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% for background, rating in character.backgrounds.items %}
                <div class="col-md-6 mb-2">
                    <div class="trait-row">
                        <span class="trait-name">{{ background }}:</span>
                        <span class="trait-dots">{{ rating|dots }}</span>
                    </div>
                </div>
            {% empty %}
                <div class="col-12">
                    <p class="text-muted">No backgrounds</p>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
```

## Merits and Flaws Display

```html
{% block merits_flaws %}
<div class="row mb-4">
    <!-- Merits -->
    <div class="col-md-6">
        <div class="tg-card h-100">
            <div class="tg-card-header">
                <h5 class="tg-card-title vtm_heading">Merits</h5>
            </div>
            <div class="tg-card-body">
                {% if character.merits %}
                    <ul class="merit-list">
                        {% for merit, rating in character.merits.items %}
                            <li>
                                <strong>{{ merit }}</strong>
                                <span class="badge badge-success">{{ rating }} pts</span>
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p class="text-muted">No merits</p>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Flaws -->
    <div class="col-md-6">
        <div class="tg-card h-100">
            <div class="tg-card-header">
                <h5 class="tg-card-title vtm_heading">Flaws</h5>
            </div>
            <div class="tg-card-body">
                {% if character.flaws %}
                    <ul class="flaw-list">
                        {% for flaw, rating in character.flaws.items %}
                            <li>
                                <strong>{{ flaw }}</strong>
                                <span class="badge badge-danger">{{ rating }} pts</span>
                            </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p class="text-muted">No flaws</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## XP Section

```html
{% block xp_section %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title vtm_heading">Experience</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            <div class="col-md-4">
                <div class="xp-stat">
                    <div class="xp-value">{{ character.xp }}</div>
                    <div class="xp-label">Available XP</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="xp-stat">
                    <div class="xp-value">{{ character.total_xp }}</div>
                    <div class="xp-label">Total Earned</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="xp-stat">
                    <div class="xp-value">{{ character.spent_total }}</div>
                    <div class="xp-label">Total Spent</div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### XP Stat Styling

```css
.xp-stat {
    text-align: center;
    padding: 16px;
    background-color: rgba(0,0,0,0.02);
    border-radius: 6px;
}

.xp-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--theme-text-primary);
    margin-bottom: 8px;
}

.xp-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--theme-text-secondary);
}
```

## Character List Views

```html
<div class="tg-card">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Characters</h5>
    </div>
    <div class="tg-card-body">
        <table class="tg-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for character in characters %}
                    <tr>
                        <td>
                            <a href="{{ character.get_absolute_url }}">
                                {{ character.name }}
                            </a>
                        </td>
                        <td>{{ character.get_type_display }}</td>
                        <td>
                            <span class="tg-badge badge-{{ character.status|lower }}">
                                {{ character.get_status_display }}
                            </span>
                        </td>
                        <td>
                            <a href="{{ character.get_update_url }}" class="btn btn-sm btn-primary">
                                Edit
                            </a>
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="4" class="text-center text-muted">
                            No characters found
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

## Responsive Considerations

### Mobile-Friendly Attributes

```html
<!-- Desktop: 3 columns, Mobile: 1 column -->
<div class="row">
    <div class="col-md-4 col-12 mb-3">
        <h6 class="vtm_heading">Physical</h6>
        <!-- Attributes -->
    </div>
    <div class="col-md-4 col-12 mb-3">
        <h6 class="vtm_heading">Social</h6>
        <!-- Attributes -->
    </div>
    <div class="col-md-4 col-12 mb-3">
        <h6 class="vtm_heading">Mental</h6>
        <!-- Attributes -->
    </div>
</div>
```

## Common Anti-Patterns

❌ **Don't hardcode gameline classes:**
```html
<!-- Wrong -->
<h5 class="vtm_heading">{{ character.name }}</h5>

<!-- Correct -->
<h5 class="{{ character.get_heading }}">{{ character.name }}</h5>
```

❌ **Don't display raw JSONField data:**
```html
<!-- Wrong -->
{{ character.disciplines }}

<!-- Correct -->
{% for discipline, rating in character.disciplines.items %}
    {{ discipline }}: {{ rating|dots }}
{% endfor %}
```

❌ **Don't skip responsive classes:**
```html
<!-- Wrong -->
<div class="col-4">...</div>

<!-- Correct -->
<div class="col-md-4 col-12">...</div>
```

## Template Checklist

- [ ] Extends `characters/core/character/detail.html`
- [ ] Loads template tags (`{% load dots sanitize_text %}`)
- [ ] Uses gameline-specific heading class
- [ ] Displays status badge
- [ ] Shows attributes in three columns
- [ ] Displays abilities with specialties
- [ ] Includes gameline-specific powers
- [ ] Shows XP information
- [ ] Uses display includes for complex sections
- [ ] Implements responsive design
- [ ] Uses `tg-card` components

## See Also

- `core/docs/STYLE.md` - Base template styling
- `/SOURCES/STYLE.md` - Project-wide style guide
- `/CLAUDE.md` - Template conventions
