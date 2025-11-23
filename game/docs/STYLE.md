# Game App - Template Style Guide

## Overview

Game templates handle chronicles, scenes, stories, and XP management. This guide covers layouts for campaign management and session tracking.

## Chronicle Detail Template

### Chronicle Header

```html
<div class="tg-card header-card mb-4" data-gameline="{{ chronicle.gameline }}">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h1 class="tg-card-title {{ chronicle.gameline }}_heading">
                    {{ chronicle.name }}
                </h1>
                <p class="tg-card-subtitle">
                    {{ chronicle.get_gameline_display }}
                </p>
            </div>
            <div>
                {% if is_st %}
                    <a href="{% url 'game:chronicle_edit' chronicle.pk %}" class="btn btn-sm btn-primary">
                        Edit
                    </a>
                {% endif %}
                <span class="tg-badge badge-{{ chronicle.status|lower }}">
                    {{ chronicle.get_status_display }}
                </span>
            </div>
        </div>
    </div>
</div>
```

### Chronicle Description

```html
{% load sanitize_text %}

<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ chronicle.gameline }}_heading">Description</h5>
    </div>
    <div class="tg-card-body">
        {{ chronicle.description|sanitize_html }}
    </div>
</div>
```

### Storytellers and Players

```html
<div class="row mb-4">
    <!-- Storytellers -->
    <div class="col-md-6 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-header">
                <h5 class="tg-card-title {{ chronicle.gameline }}_heading">Storytellers</h5>
            </div>
            <div class="tg-card-body">
                <ul class="user-list">
                    {% for st in chronicle.storytellers.all %}
                        <li>
                            <a href="{% url 'accounts:profile' st.pk %}">
                                {{ st.username }}
                            </a>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>

    <!-- Players -->
    <div class="col-md-6 mb-3">
        <div class="tg-card h-100">
            <div class="tg-card-header">
                <h5 class="tg-card-title {{ chronicle.gameline }}_heading">Players</h5>
            </div>
            <div class="tg-card-body">
                <ul class="user-list">
                    {% for player in chronicle.players.all %}
                        <li>
                            <a href="{% url 'accounts:profile' player.pk %}">
                                {{ player.username }}
                            </a>
                        </li>
                    {% empty %}
                        <li class="text-muted">No players yet</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
    </div>
</div>
```

### Chronicle Characters

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ chronicle.gameline }}_heading">Characters</h5>
    </div>
    <div class="tg-card-body">
        <table class="tg-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Player</th>
                    <th>Type</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for character in chronicle.characters.all %}
                    <tr>
                        <td>
                            <a href="{{ character.get_absolute_url }}">
                                {{ character.name }}
                            </a>
                        </td>
                        <td>{{ character.owner.username }}</td>
                        <td>{{ character.get_type_display }}</td>
                        <td>
                            <span class="tg-badge badge-{{ character.status|lower }}">
                                {{ character.get_status_display }}
                            </span>
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="4" class="text-center text-muted">
                            No characters yet
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

## Scene Display

### Scene Header

```html
<div class="tg-card header-card mb-4" data-gameline="{{ scene.chronicle.gameline }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ scene.chronicle.gameline }}_heading">
            {{ scene.name }}
        </h1>
        <p class="tg-card-subtitle">
            {{ scene.date|date:"F j, Y" }}
            {% if scene.story %}
                - {{ scene.story.name }}
            {% endif %}
        </p>
    </div>
</div>
```

### Scene Details

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ scene.chronicle.gameline }}_heading">Details</h5>
    </div>
    <div class="tg-card-body">
        <div class="row mb-3">
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Base XP</div>
                    <div class="stat-value">{{ scene.base_xp }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Bonus XP</div>
                    <div class="stat-value">{{ scene.bonus_xp }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-box">
                    <div class="stat-label">Total XP</div>
                    <div class="stat-value">{{ scene.total_xp }}</div>
                </div>
            </div>
        </div>

        <h6 class="{{ scene.chronicle.gameline }}_heading">Description</h6>
        {{ scene.description|sanitize_html }}
    </div>
</div>
```

### Scene Participants

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ scene.chronicle.gameline }}_heading">Participants</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% for character in scene.characters.all %}
                <div class="col-md-6 mb-2">
                    <a href="{{ character.get_absolute_url }}">
                        {{ character.name }}
                    </a>
                    ({{ character.owner.username }})
                </div>
            {% empty %}
                <div class="col-12">
                    <p class="text-muted">No participants recorded</p>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
```

## Recent Scenes List

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ chronicle.gameline }}_heading">Recent Scenes</h5>
        {% if is_st %}
            <a href="{% url 'game:scene_create' chronicle.pk %}" class="btn btn-sm btn-primary">
                Create Scene
            </a>
        {% endif %}
    </div>
    <div class="tg-card-body">
        {% for scene in recent_scenes %}
            <div class="scene-item mb-3 pb-3 border-bottom">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6>
                            <a href="{{ scene.get_absolute_url }}">
                                {{ scene.name }}
                            </a>
                        </h6>
                        <p class="text-muted mb-1">{{ scene.date|date:"F j, Y" }}</p>
                        <p class="mb-0">{{ scene.description|truncatewords:30 }}</p>
                    </div>
                    <div class="text-right">
                        <span class="badge badge-success">{{ scene.total_xp }} XP</span>
                    </div>
                </div>
            </div>
        {% empty %}
            <p class="text-muted">No scenes yet</p>
        {% endfor %}
    </div>
</div>
```

## XP Approval Queue

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title">XP Approval Queue</h5>
    </div>
    <div class="tg-card-body">
        <table class="tg-table">
            <thead>
                <tr>
                    <th>Character</th>
                    <th>Trait</th>
                    <th>Cost</th>
                    <th>Notes</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for request in xp_requests %}
                    <tr>
                        <td>
                            <a href="{{ request.character.get_absolute_url }}">
                                {{ request.character.name }}
                            </a>
                        </td>
                        <td>{{ request.trait }}</td>
                        <td>{{ request.cost }} XP</td>
                        <td>{{ request.notes|truncatewords:10 }}</td>
                        <td>
                            <form method="post" action="{% url 'game:xp_approve' request.pk %}" class="d-inline">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-sm btn-success">
                                    Approve
                                </button>
                            </form>
                            <form method="post" action="{% url 'game:xp_reject' request.pk %}" class="d-inline">
                                {% csrf_token %}
                                <button type="submit" class="btn btn-sm btn-danger">
                                    Reject
                                </button>
                            </form>
                        </td>
                    </tr>
                {% empty %}
                    <tr>
                        <td colspan="5" class="text-center text-muted">
                            No pending requests
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

## Story Arc Display

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title {{ chronicle.gameline }}_heading">Current Story</h5>
    </div>
    <div class="tg-card-body">
        {% if current_story %}
            <h6>{{ current_story.name }}</h6>
            <p>{{ current_story.description }}</p>
            <p class="text-muted">
                Started: {{ current_story.start_date|date:"F j, Y" }}
            </p>
        {% else %}
            <p class="text-muted">No active story</p>
        {% endif %}
    </div>
</div>
```

## Chronicle List View

```html
<div class="tg-card">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Chronicles</h5>
        <a href="{% url 'game:chronicle_create' %}" class="btn btn-sm btn-primary">
            Create Chronicle
        </a>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% for chronicle in chronicles %}
                <div class="col-md-6 mb-3">
                    <div class="tg-card h-100" data-gameline="{{ chronicle.gameline }}">
                        <div class="tg-card-body">
                            <h5 class="{{ chronicle.gameline }}_heading">
                                <a href="{{ chronicle.get_absolute_url }}">
                                    {{ chronicle.name }}
                                </a>
                            </h5>
                            <p class="mb-2">{{ chronicle.get_gameline_display }}</p>
                            <p class="text-muted mb-2">
                                {{ chronicle.description|truncatewords:20 }}
                            </p>
                            <div class="mt-2">
                                <small class="text-muted">
                                    {{ chronicle.players.count }} players,
                                    {{ chronicle.characters.count }} characters
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            {% empty %}
                <div class="col-12">
                    <p class="text-center text-muted">No chronicles found</p>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
```

## Stat Box Styling

```css
.stat-box {
    text-align: center;
    padding: 16px;
    background-color: rgba(0,0,0,0.02);
    border-radius: 6px;
}

.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--theme-text-primary);
}

.stat-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--theme-text-secondary);
    margin-top: 8px;
}
```

## Template Checklist

- [ ] Uses gameline-specific heading classes
- [ ] Displays status badges
- [ ] Sanitizes descriptions with `|sanitize_html`
- [ ] Uses `tg-card` components
- [ ] Uses `tg-table` for data tables
- [ ] Implements responsive design
- [ ] Shows ST-specific controls when appropriate
- [ ] Uses `h-100` for equal-height cards
- [ ] Formats dates consistently

## See Also

- `core/docs/STYLE.md` - Base template styling
- `/SOURCES/STYLE.md` - Project-wide style guide
