# Template Patterns

## Directory Structure

```
app/templates/app/gameline/
├── my_character/
│   ├── detail.html
│   ├── list.html
│   ├── form.html
│   ├── chargen.html          # If applicable
│   └── display_includes/
│       ├── basics.html
│       ├── powers.html
│       └── buttons.html
└── my_reference/
    ├── detail.html
    └── list.html
```

## Character Detail Template

```html
{% extends "characters/core/human/detail.html" %}
{% load dots sanitize_text %}

{% block objectname %}
<div class="tg-card header-card mb-4" data-gameline="{{ object.gameline|lower }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">{{ object.name }}</h1>
        <p class="tg-card-subtitle">{{ object.concept }}</p>
    </div>
</div>
{% endblock %}

{% block basics %}
{% include "app/gameline/my_character/display_includes/basics.html" %}
{% endblock %}

{% block powers %}
{% include "app/gameline/my_character/display_includes/powers.html" %}
{% endblock %}
```

## Item Detail Template

```html
{% extends "items/core/item/detail.html" %}

{% block objectname %}
<div class="tg-card header-card mb-4" data-gameline="{{ object.gameline|lower }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">{{ object.name }}</h1>
    </div>
</div>
{% endblock %}

{% block contents %}
{% include "app/gameline/my_item/display_includes/basics.html" %}
{% endblock %}
```

## Location Detail Template

```html
{% extends "locations/core/location/detail.html" %}

{% block objectname %}
<div class="tg-card header-card mb-4" data-gameline="{{ object.gameline|lower }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">{{ object.name }}</h1>
    </div>
</div>
{% endblock %}

{% block model_specific %}
{% include "app/gameline/my_location/display_includes/basics.html" %}
{% endblock %}
```

## Display Include (Basics)

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ object.get_heading }}">Basic Information</h5>
    </div>
    <div class="tg-card-body">
        <div style="display: flex; flex-wrap: wrap; gap: 16px; justify-content: flex-start;">
            {% if object.faction %}
            <div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
                <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Faction:</span>
                <span style="font-weight: 700; color: var(--theme-text-primary);">
                    <a href="{{ object.faction.get_absolute_url }}">{{ object.faction.name }}</a>
                </span>
            </div>
            {% endif %}
        </div>
    </div>
</div>
```

## List Template

```html
{% extends "core/base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="tg-card">
        <div class="tg-card-header d-flex justify-content-between align-items-center">
            <h4 class="tg-card-title mb-0">{{ model_name_plural }}</h4>
            {% if user.profile.is_st %}
            <a href="{% url 'app:gameline:create:model_name' %}" class="btn btn-primary btn-sm">Create New</a>
            {% endif %}
        </div>
        <div class="tg-card-body">
            <table class="tg-table">
                <thead>
                    <tr><th>Name</th><th>Owner</th><th>Status</th></tr>
                </thead>
                <tbody>
                    {% for obj in objects %}
                    <tr>
                        <td><a href="{{ obj.get_absolute_url }}">{{ obj.name }}</a></td>
                        <td>{{ obj.owner.username }}</td>
                        <td><span class="tg-badge badge-{{ obj.status|lower }}">{{ obj.get_status_display }}</span></td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="3" class="text-center">No items found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    {% if page_obj.has_other_pages %}
    <nav aria-label="Page navigation" class="mt-4">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a></li>
            {% endif %}
            <li class="page-item disabled"><span class="page-link">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span></li>
            {% if page_obj.has_next %}
            <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a></li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% endblock %}
```

## Form Template

```html
{% extends "core/form.html" %}

{% block creation_title %}
{% if object %}Edit {{ object.name }}{% else %}Create New {{ model_name }}{% endif %}
{% endblock %}

{% block formdetails %}
<form method="post" enctype="multipart/form-data">
{% endblock %}

{% block contents %}
{% csrf_token %}

<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Basic Information</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="id_name" class="form-label">Name</label>
                {{ form.name }}
                {% if form.name.errors %}<div class="text-danger">{{ form.name.errors }}</div>{% endif %}
            </div>
            <div class="col-md-6 mb-3">
                <label for="id_concept" class="form-label">Concept</label>
                {{ form.concept }}
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block buttons %}
<div class="d-flex justify-content-between">
    <a href="{% if object %}{{ object.get_absolute_url }}{% else %}{% url 'app:index' %}{% endif %}" class="btn btn-secondary">Cancel</a>
    <button type="submit" class="btn btn-primary">{% if object %}Update{% else %}Create{% endif %}</button>
</div>
</form>
{% endblock %}
```

## Key CSS Classes

Use `tg-*` classes (project-specific), not Bootstrap defaults:
- `tg-card`, `tg-card-header`, `tg-card-body`, `tg-card-title`
- `tg-table`
- `tg-badge`
