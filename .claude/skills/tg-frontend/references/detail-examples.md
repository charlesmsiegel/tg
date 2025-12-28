# Detail View Examples

Real working examples extracted from the TG codebase.

## Page Headers

### Location Header (Node)
From `locations/templates/locations/mage/node/detail.html`:
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

### Character Header
From `characters/templates/characters/core/character/detail.html`:
```html
<div class="tg-card header-card mb-2" data-gameline="{{ object.gameline|lower }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">{{ object.name }}</h1>
        <p class="tg-card-subtitle mb-0 text-center">
            {{ object.concept }}{% if object.chronicle %} | <a href="{{ object.chronicle.get_absolute_url }}">{{ object.chronicle }}</a>{% endif %}
        </p>
    </div>
</div>
```

## Stat Display Blocks

### Node Properties (Inline + Large Stats)
From `locations/templates/locations/mage/node/display_includes/basics.html`:
```html
<div class="col-md-6 mb-3">
    <div class="tg-card h-100">
        <div class="tg-card-header text-center">
            <h5 class="tg-card-title mta_heading">Node Properties</h5>
        </div>
        <div class="tg-card-body text-center" style="padding: 20px;">
            <!-- Size (inline stat box) -->
            <div class="mb-3">
                <div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
                    <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Size:</span>
                    <span style="font-weight: 700; color: var(--theme-text-primary);">{{ object.get_size_display }}</span>
                </div>
            </div>

            <!-- Energy Output (section header) -->
            <h6 class="mta_heading mb-3" style="font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; font-size: 0.875rem;">Energy Output</h6>

            <!-- Two-column large stats -->
            <div class="row">
                <div class="col-6">
                    <div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
                        <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ object.quintessence_per_week }}</div>
                        <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary); margin-bottom: 4px;">Quintessence/week</div>
                        <small class="text-muted" style="font-size: 0.7rem;">{{ object.quintessence_form }}</small>
                    </div>
                </div>
                <div class="col-6">
                    <div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
                        <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ object.tass_per_week }}</div>
                        <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary); margin-bottom: 4px;">Tass/week</div>
                        <small class="text-muted" style="font-size: 0.7rem;">{{ object.tass_form }}</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Haven Statistics (Total + Components)
From `locations/templates/locations/vampire/haven/display_includes/basics.html`:
```html
<div class="col-md-6 mb-3">
    <div class="tg-card h-100">
        <div class="tg-card-header text-center">
            <h5 class="tg-card-title vtm_heading">Haven Statistics</h5>
        </div>
        <div class="tg-card-body text-center" style="padding: 20px;">
            <!-- Total Rating (prominent) -->
            <div class="mb-4">
                <div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
                    <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ object.total_rating|dots:10 }}</div>
                    <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Total Rating</div>
                </div>
            </div>

            <!-- Component Ratings (three columns) -->
            <div class="row">
                <div class="col-4">
                    <div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
                        <div style="font-size: 1.2rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ object.get_size_display }}</div>
                        <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Size</div>
                    </div>
                </div>
                <div class="col-4">
                    <div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
                        <div style="font-size: 1.2rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ object.security|dots }}</div>
                        <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Security</div>
                    </div>
                </div>
                <div class="col-4">
                    <div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
                        <div style="font-size: 1.2rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ object.location|dots }}</div>
                        <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Location</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Boolean Features Grid
From `locations/templates/locations/vampire/haven/display_includes/basics.html`:
```html
<div class="col-md-6 mb-3">
    <div class="tg-card h-100">
        <div class="tg-card-header text-center">
            <h5 class="tg-card-title vtm_heading">Haven Features</h5>
        </div>
        <div class="tg-card-body" style="padding: 20px;">
            <div class="row">
                <div class="col-6 mb-2">
                    <div style="padding: 8px; border-radius: 4px; background-color: {{ object.has_guardian|yesno:'rgba(0,255,0,0.1),rgba(0,0,0,0.02)' }};">
                        <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary); margin-bottom: 2px;">Guardian</div>
                        <div style="font-weight: 700; color: var(--theme-text-primary);">{{ object.has_guardian|yesno:"Yes,No" }}</div>
                    </div>
                </div>
                <div class="col-6 mb-2">
                    <div style="padding: 8px; border-radius: 4px; background-color: {{ object.has_luxury|yesno:'rgba(0,255,0,0.1),rgba(0,0,0,0.02)' }};">
                        <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary); margin-bottom: 2px;">Luxury</div>
                        <div style="font-weight: 700; color: var(--theme-text-primary);">{{ object.has_luxury|yesno:"Yes,No" }}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

## Reusable Display Includes

### Merits & Flaws Block
From `characters/templates/characters/core/meritflaw/display_includes/meritflaw_block.html`:
```html
{% if object.get_mf_and_rating_list %}
<div class="row mb-3">
    <div class="col-12">
        <div class="tg-card">
            <div class="tg-card-header text-center">
                <h5 class="tg-card-title {{ object.get_heading }}">Merits & Flaws</h5>
            </div>
            <div class="tg-card-body text-center" style="padding: 20px;">
                <div class="d-flex justify-content-center align-items-center flex-wrap">
                    {% for mf, rating in object.get_mf_and_rating_list %}
                        <div class="px-3 py-2">
                            <a href="{{ mf.get_absolute_url }}" style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">{{ mf.name }}:</a>
                            <span style="font-weight: 700; {% if rating > 0 %}color: #28a745;{% else %}color: #dc3545;{% endif %}">{{ rating }}</span>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}
```

### Resonance Display
From `characters/templates/characters/mage/resonance/display_includes/resonance.html`:
```html
{% load dots %}
{% if resonance %}
<div class="row mb-3">
    <div class="col-12">
        <div class="tg-card">
            <div class="tg-card-header text-center">
                <h5 class="tg-card-title {{ object.get_heading }}">Resonance</h5>
            </div>
            <div class="tg-card-body" style="padding: 20px;">
                <div class="row">
                    {% for res in resonance %}
                        <div class="col-sm-6 col-md-4 col-lg-3 mb-3">
                            <div class="tg-card h-100">
                                <div class="tg-card-body text-center" style="padding: 16px;">
                                    <div class="mb-2">
                                        <a href="{{ res.resonance.get_absolute_url }}" style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-primary);">{{ res.resonance }}</a>
                                    </div>
                                    <div class="dots" style="font-size: 0.875rem;">{{ res.rating|dots }}</div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}
```

### Status Display
From `core/templates/core/includes/status.html`:
```html
<div class="col-md mb-1">
    <div class="tg-card h-100">
        <div class="tg-card-body text-center" style="padding: 20px;">
            <div class="mb-2">
                <span class="tg-badge badge-{{ object.status|lower }}">{{ object.get_status_display }}</span>
            </div>
            {% if object.owner %}
                <div class="mb-0">
                    <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary);">Owner:</span>
                    <a href="{% url 'profile' object.owner.id %}">{{ object.owner.username }}</a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
```

## Character-Specific Patterns

### Garou Advantages (Dots with Labels)
From `characters/templates/characters/werewolf/garou/detail.html`:
```html
<div class="row mb-3">
    <div class="col-12">
        <div class="tg-card">
            <div class="tg-card-header text-center">
                <h5 class="tg-card-title {{ object.get_heading }}">Advantages</h5>
            </div>
            <div class="tg-card-body" style="padding: 20px;">
                <div class="row mb-2 text-center">
                    <div class="col-3" style="font-weight: 600; color: var(--theme-text-secondary);">Willpower:</div>
                    <div class="col-3 dots">{{ object.willpower|dots:10 }}</div>
                    <div class="col-3" style="font-weight: 600; color: var(--theme-text-secondary);">Temporary Willpower:</div>
                    <div class="col-3 dots">{{ object.temporary_willpower|boxes:10 }}</div>
                </div>
                <div class="row mb-2 text-center">
                    <div class="col-3" style="font-weight: 600; color: var(--theme-text-secondary);">Gnosis:</div>
                    <div class="col-3 dots">{{ object.gnosis|dots:10 }}</div>
                    <div class="col-3" style="font-weight: 600; color: var(--theme-text-secondary);">Temporary Gnosis:</div>
                    <div class="col-3 dots">{{ object.temporary_gnosis|default:0|boxes:10 }}</div>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Gifts Grid
From `characters/templates/characters/werewolf/garou/detail.html`:
```html
{% if object.gifts.all %}
<div class="row mb-3">
    <div class="col-12">
        <div class="tg-card">
            <div class="tg-card-header text-center">
                <h5 class="tg-card-title {{ object.get_heading }}">Gifts</h5>
            </div>
            <div class="tg-card-body" style="padding: 20px;">
                <div class="row">
                    {% for gift in object.gifts.all %}
                        <div class="col-sm-6 col-md-4 col-lg-3 mb-3">
                            <div class="tg-card h-100">
                                <div class="tg-card-body text-center" style="padding: 16px;">
                                    <div class="mb-2">
                                        <a href="{{ gift.get_absolute_url }}" style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-primary);">{{ gift }}</a>
                                    </div>
                                    <div style="font-size: 0.75rem; color: var(--theme-text-secondary);">Rank {{ gift.rank }}</div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}
```
