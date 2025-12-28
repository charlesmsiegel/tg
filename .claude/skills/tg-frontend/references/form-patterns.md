# Form Patterns

Reusable patterns for forms that match detail view styling. All forms extend `core/form.html`.

## Table of Contents
- [Base Structure](#base-structure)
- [Field Patterns](#field-patterns)
- [Checkbox Groups](#checkbox-groups)
- [Multi-Section Forms](#multi-section-forms)
- [Formsets](#formsets)

## Base Structure

### Standard Form Template
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

## Field Patterns

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

### Full-Width Field
```html
<div class="row mb-3">
    <div class="col-md-12">
        <label for="{{ form.description.id_for_label }}" class="form-label">Description</label>
        {{ form.description }}
    </div>
</div>
```

### Required Field Indicator
```html
<label for="{{ form.name.id_for_label }}" class="form-label">
    Name <span style="color: #dc3545;">*</span>
</label>
```

### Help Text Under Field
```html
<div class="col-md-6">
    <label for="{{ form.rating.id_for_label }}" class="form-label">Rating (0-5 dots)</label>
    {{ form.rating }}
    <small class="text-muted">Each dot increases the background cost by 1.</small>
</div>
```

## Checkbox Groups

### Section Header with Checkboxes
```html
<div class="row mb-3">
    <div class="col-md-12">
        <h6 class="{{ object.get_heading|default:'mta_heading' }} mb-2">Features</h6>
    </div>
    <div class="col-md-4">
        <div class="form-check">
            {{ form.feature_one }}
            <label class="form-check-label" for="{{ form.feature_one.id_for_label }}">Feature One</label>
        </div>
    </div>
    <div class="col-md-4">
        <div class="form-check">
            {{ form.feature_two }}
            <label class="form-check-label" for="{{ form.feature_two.id_for_label }}">Feature Two</label>
        </div>
    </div>
    <div class="col-md-4">
        <div class="form-check">
            {{ form.feature_three }}
            <label class="form-check-label" for="{{ form.feature_three.id_for_label }}">Feature Three</label>
        </div>
    </div>
</div>
```

## Multi-Section Forms

For complex objects, split into logical sections with separate cards:

```html
{% block contents %}
    <!-- Section 1: Basic Information -->
    <div class="tg-card mb-4">
        <div class="tg-card-header">
            <h2 class="tg-card-title {{ object.get_heading }}">Basic Information</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <div class="row mb-3">
                <div class="col-md-6">
                    <label for="{{ form.name.id_for_label }}" class="form-label">Name</label>
                    {{ form.name }}
                </div>
                <div class="col-md-6">
                    <label for="{{ form.parent.id_for_label }}" class="form-label">Parent</label>
                    {{ form.parent }}
                </div>
            </div>
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

    <!-- Section 3: Description (last section, no mb-4) -->
    <div class="tg-card">
        <div class="tg-card-header">
            <h2 class="tg-card-title {{ object.get_heading }}">Description</h2>
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

## Formsets

For dynamic lists of related items:

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

        <!-- Empty form template -->
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

## Anti-Patterns

### Old Style (Avoid)
```html
<!-- Don't do this -->
<div class="row">
    <div class="col-sm">Name</div>
    <div class="col-sm">{{ form.name }}</div>
</div>
```

Problems: No `tg-card`, no `form-label`, no `mb-3` spacing, doesn't match detail views.

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
    </div>
</div>
```

## Form Checklist

- [ ] Extends `core/form.html`
- [ ] Uses `{% block creation_title %}` for dynamic title
- [ ] Uses `tg-card` wrapper with gameline heading
- [ ] Card body has `padding: 24px;`
- [ ] Each field row has `mb-3` class
- [ ] Labels use `form-label` class
- [ ] Labels reference field with `for="{{ form.field.id_for_label }}"`
- [ ] Checkboxes wrapped in `form-check` divs
- [ ] Multi-section forms use `mb-4` between sections
- [ ] Responsive columns (`col-md-6`, `col-md-4`)
