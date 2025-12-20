# Form Examples

Real working examples and patterns for forms that match the detail view styling.

## Gold Standard: Haven Form

The Haven form is the best example of modern form styling. Use this as a reference when creating new forms.

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

---

## Base Form Template

The `core/form.html` template provides structure. All forms extend it:

```html
{% extends "core/form.html" %}
{% block creation_title %}
    {% if object %}Update{% else %}Create{% endif %} Object Type
{% endblock creation_title %}
{% block contents %}
    <!-- Form content goes here -->
{% endblock contents %}
```

Key features of base form:
- Page header card with gameline styling
- Error display for non-field errors
- Wraps `{% block contents %}` in a `tg-card`
- Save/Cancel buttons at bottom

---

## Form Field Patterns

### Two-Column Text/Select Fields

```html
<div class="row mb-3">
    <div class="col-md-6">
        <label for="{{ form.name.id_for_label }}" class="form-label">Name</label>
        {{ form.name }}
    </div>
    <div class="col-md-6">
        <label for="{{ form.type.id_for_label }}" class="form-label">Type</label>
        {{ form.type }}
    </div>
</div>
```

### Three-Column Numeric Fields

```html
<div class="row mb-3">
    <div class="col-md-4">
        <label for="{{ form.rank.id_for_label }}" class="form-label">Rank (0-5)</label>
        {{ form.rank }}
    </div>
    <div class="col-md-4">
        <label for="{{ form.size.id_for_label }}" class="form-label">Size</label>
        {{ form.size }}
    </div>
    <div class="col-md-4">
        <label for="{{ form.rating.id_for_label }}" class="form-label">Rating</label>
        {{ form.rating }}
    </div>
</div>
```

### Single Full-Width Field

```html
<div class="row mb-3">
    <div class="col-md-12">
        <label for="{{ form.description.id_for_label }}" class="form-label">Description</label>
        {{ form.description }}
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
            {{ form.feature_one }}
            <label class="form-check-label" for="{{ form.feature_one.id_for_label }}">
                Feature One
            </label>
        </div>
    </div>
    <div class="col-md-4">
        <div class="form-check">
            {{ form.feature_two }}
            <label class="form-check-label" for="{{ form.feature_two.id_for_label }}">
                Feature Two
            </label>
        </div>
    </div>
    <div class="col-md-4">
        <div class="form-check">
            {{ form.feature_three }}
            <label class="form-check-label" for="{{ form.feature_three.id_for_label }}">
                Feature Three
            </label>
        </div>
    </div>
</div>
```

### Required Field Label

Add visual indicator for required fields:

```html
<label for="{{ form.name.id_for_label }}" class="form-label">
    Name <span style="color: #dc3545;">*</span>
</label>
```

Or use the TG class:

```html
<label for="{{ form.name.id_for_label }}" class="tg-form-label required">Name</label>
```

### Help Text Under Field

```html
<div class="col-md-6">
    <label for="{{ form.rating.id_for_label }}" class="form-label">Rating (0-5 dots)</label>
    {{ form.rating }}
    <small class="text-muted">Each dot increases the background cost by 1.</small>
</div>
```

---

## Multi-Section Forms

For complex objects, split into logical sections:

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

    <!-- Section 2: Barriers -->
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

---

## Formset Patterns

For dynamic lists of related items:

### Formset with Add Button

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h2 class="tg-card-title mta_heading">Resonance</h2>
    </div>
    <div class="tg-card-body" style="padding: 24px;">
        {{ form.resonance_formset.management_form }}
        <div id="resonance_formset">
            {% for subform in form.resonance_formset.forms %}
                <div class="row mb-3 resonance-row">
                    <div class="col-md-6">
                        <label class="form-label">Resonance Type</label>
                        {{ subform.resonance }}
                    </div>
                    <div class="col-md-4">
                        <label class="form-label">Rating</label>
                        {{ subform.rating }}
                    </div>
                    <div class="col-md-2 d-flex align-items-end">
                        <button type="button" class="tg-btn btn-danger btn-sm remove-row">Remove</button>
                    </div>
                </div>
            {% endfor %}
        </div>

        <!-- Empty form template for JS cloning -->
        <div id="empty_resonance_form" class="d-none">
            <div class="row mb-3 resonance-row">
                <div class="col-md-6">
                    <label class="form-label">Resonance Type</label>
                    {{ form.resonance_formset.empty_form.resonance }}
                </div>
                <div class="col-md-4">
                    <label class="form-label">Rating</label>
                    {{ form.resonance_formset.empty_form.rating }}
                </div>
                <div class="col-md-2 d-flex align-items-end">
                    <button type="button" class="tg-btn btn-danger btn-sm remove-row">Remove</button>
                </div>
            </div>
        </div>

        <button type="button" id="add-resonance" class="tg-btn btn-primary">Add Resonance</button>
    </div>
</div>

<script>
document.getElementById('add-resonance').addEventListener('click', function() {
    const totalForms = document.getElementById('id_resonance-TOTAL_FORMS');
    const currentFormCount = parseInt(totalForms.value);
    const formHtml = document.getElementById('empty_resonance_form').innerHTML
        .replace(/__prefix__/g, currentFormCount);
    totalForms.value = currentFormCount + 1;
    document.getElementById('resonance_formset').insertAdjacentHTML('beforeend', formHtml);
});
</script>
```

---

## Comparison: Old vs New Form Styles

### Old Style (Avoid)

```html
<!-- Don't do this -->
<div class="row">
    <div class="col-sm">Name</div>
    <div class="col-sm">{{ form.name }}</div>
</div>
<div class="row">
    <div class="col-sm">Description</div>
    <div class="col-sm">{{ form.description }}</div>
</div>
```

Problems:
- No `tg-card` wrapper
- No proper labels with `form-label` class
- No proper spacing (`mb-3`)
- Raw row layout doesn't match detail view aesthetics

### New Style (Use This)

```html
<!-- Do this instead -->
<div class="tg-card">
    <div class="tg-card-header">
        <h2 class="tg-card-title mta_heading">Basic Information</h2>
    </div>
    <div class="tg-card-body" style="padding: 24px;">
        <div class="row mb-3">
            <div class="col-md-12">
                <label for="{{ form.name.id_for_label }}" class="form-label">Name</label>
                {{ form.name }}
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
```

Benefits:
- Uses `tg-card` components
- Proper `form-label` class
- Consistent spacing with `mb-3`
- Matches detail view aesthetics
- Better accessibility with proper label associations

---

## Form Styling Checklist

When creating or reviewing forms:

- [ ] Extends `core/form.html`
- [ ] Uses `{% block creation_title %}` for dynamic title
- [ ] Uses `tg-card` wrapper with gameline heading
- [ ] Card body has `padding: 24px;`
- [ ] Each field row has `mb-3` class
- [ ] Labels use `form-label` class
- [ ] Labels reference field with `for="{{ form.field.id_for_label }}"`
- [ ] Checkboxes wrapped in `form-check` divs
- [ ] Checkbox groups have section header with gameline class
- [ ] Help text uses `<small class="text-muted">`
- [ ] Multi-section forms use separate `tg-card mb-4` for each section
- [ ] Responsive columns (e.g., `col-md-6`, `col-md-4`)
