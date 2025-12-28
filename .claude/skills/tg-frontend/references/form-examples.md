# Form Examples

Real working examples from the TG codebase.

## Gold Standard: Haven Form

The Haven form is the reference implementation for modern form styling.

From `locations/templates/locations/vampire/haven/form.html`:

```html
{% extends "core/form.html" %}
{% block creation_title %}
    {% if object %}Update{% else %}Create{% endif %} Haven
{% endblock creation_title %}
{% block contents %}
    <div class="tg-card">
        <div class="tg-card-header">
            <h2 class="tg-card-title vtm_heading">Haven Information</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
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

            <div class="row mb-3">
                <div class="col-md-12">
                    <h6 class="vtm_heading mb-2">Features</h6>
                </div>
                <div class="col-md-4">
                    <div class="form-check">
                        {{ form.has_guardian }}
                        <label class="form-check-label" for="{{ form.has_guardian.id_for_label }}">
                            Has Guardian
                        </label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-check">
                        {{ form.has_luxury }}
                        <label class="form-check-label" for="{{ form.has_luxury.id_for_label }}">
                            Luxurious
                        </label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-check">
                        {{ form.is_hidden }}
                        <label class="form-check-label" for="{{ form.is_hidden.id_for_label }}">
                            Hidden Location
                        </label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-check">
                        {{ form.has_library }}
                        <label class="form-check-label" for="{{ form.has_library.id_for_label }}">
                            Contains Library
                        </label>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-check">
                        {{ form.has_workshop }}
                        <label class="form-check-label" for="{{ form.has_workshop.id_for_label }}">
                            Contains Workshop
                        </label>
                    </div>
                </div>
            </div>

            <div class="row mb-3">
                <div class="col-md-12">
                    <label for="{{ form.description.id_for_label }}" class="form-label">Description</label>
                    {{ form.description }}
                </div>
            </div>
        </div>
    </div>
{% endblock contents %}
```

## Multi-Section Form Example: Node

Example of a complex form split into logical sections:

```html
{% extends "core/form.html" %}
{% block creation_title %}
    {% if object %}Update{% else %}Create{% endif %} Node
{% endblock creation_title %}
{% block contents %}
    <!-- Section 1: Basic Information -->
    <div class="tg-card mb-4">
        <div class="tg-card-header">
            <h2 class="tg-card-title mta_heading">Basic Information</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
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
            <div class="row mb-3">
                <div class="col-md-4">
                    <label for="{{ form.rank.id_for_label }}" class="form-label">Rank</label>
                    {{ form.rank }}
                </div>
                <div class="col-md-4">
                    <label for="{{ form.size.id_for_label }}" class="form-label">Size</label>
                    {{ form.size }}
                </div>
                <div class="col-md-4">
                    <label for="{{ form.ratio.id_for_label }}" class="form-label">Ratio</label>
                    {{ form.ratio }}
                </div>
            </div>
        </div>
    </div>

    <!-- Section 2: Dimensional Barriers -->
    <div class="tg-card mb-4">
        <div class="tg-card-header">
            <h2 class="tg-card-title mta_heading">Dimensional Barriers</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <div class="row mb-3">
                <div class="col-md-4">
                    <label for="{{ form.gauntlet.id_for_label }}" class="form-label">Gauntlet</label>
                    {{ form.gauntlet }}
                </div>
                <div class="col-md-4">
                    <label for="{{ form.shroud.id_for_label }}" class="form-label">Shroud</label>
                    {{ form.shroud }}
                </div>
                <div class="col-md-4">
                    <label for="{{ form.dimension_barrier.id_for_label }}" class="form-label">Dimension Barrier</label>
                    {{ form.dimension_barrier }}
                </div>
            </div>
        </div>
    </div>

    <!-- Section 3: Energy Output -->
    <div class="tg-card mb-4">
        <div class="tg-card-header">
            <h2 class="tg-card-title mta_heading">Energy Output</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <div class="row mb-3">
                <div class="col-md-6">
                    <label for="{{ form.quintessence_form.id_for_label }}" class="form-label">Quintessence Form</label>
                    {{ form.quintessence_form }}
                    <small class="text-muted">The thematic form quintessence takes at this node.</small>
                </div>
                <div class="col-md-6">
                    <label for="{{ form.tass_form.id_for_label }}" class="form-label">Tass Form</label>
                    {{ form.tass_form }}
                    <small class="text-muted">The physical form tass takes at this node.</small>
                </div>
            </div>
        </div>
    </div>

    <!-- Section 4: Description -->
    <div class="tg-card">
        <div class="tg-card-header">
            <h2 class="tg-card-title mta_heading">Description</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <div class="row mb-3">
                <div class="col-md-12">
                    <label for="{{ form.description.id_for_label }}" class="form-label">Description</label>
                    {{ form.description }}
                </div>
            </div>
        </div>
    </div>
{% endblock contents %}
```

## Key Patterns in Haven Form

1. **Single `tg-card` wrapper** for simple forms
2. **Two-column layout** for name/parent fields
3. **Three-column layout** for numeric dot ratings
4. **Section header `<h6>`** before checkbox groups
5. **`form-check` wrapper** for each checkbox
6. **Full-width textarea** at the bottom for description
7. **`padding: 24px`** on card body for spacious feel
8. **`mb-3` on every row** for consistent spacing
