# Accounts App - Template Style Guide

## Overview

Accounts templates handle user profiles, authentication, and dashboard displays. This guide covers user-facing templates and profile layouts.

## User Dashboard

### Dashboard Header

```html
<div class="tg-card header-card mb-4">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h1 class="tg-card-title">
                    {% if user_profile.display_name %}
                        {{ user_profile.display_name }}
                    {% else %}
                        {{ user.username }}
                    {% endif %}
                </h1>
                <p class="tg-card-subtitle">
                    {% if is_st %}
                        Storyteller
                    {% else %}
                        Player
                    {% endif %}
                </p>
            </div>
            <div>
                <a href="{% url 'accounts:profile_edit' %}" class="btn btn-sm btn-primary">
                    Edit Profile
                </a>
            </div>
        </div>
    </div>
</div>
```

### My Characters Section

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-center">
            <h5 class="tg-card-title">My Characters</h5>
            <a href="{% url 'characters:create' %}" class="btn btn-sm btn-primary">
                Create Character
            </a>
        </div>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% for character in my_characters %}
                <div class="col-md-6 col-lg-4 mb-3">
                    <div class="tg-card h-100" data-gameline="{{ character.gameline }}">
                        <div class="tg-card-body">
                            <h6 class="{{ character.get_heading }}">
                                <a href="{{ character.get_absolute_url }}">
                                    {{ character.name }}
                                </a>
                            </h6>
                            <p class="mb-1">{{ character.concept }}</p>
                            <span class="tg-badge badge-{{ character.status|lower }}">
                                {{ character.get_status_display }}
                            </span>
                        </div>
                    </div>
                </div>
            {% empty %}
                <div class="col-12">
                    <p class="text-center text-muted">No characters yet</p>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
```

### My Chronicles Section

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title">My Chronicles</h5>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% for chronicle in my_chronicles %}
                <div class="col-md-6 mb-3">
                    <div class="tg-card h-100" data-gameline="{{ chronicle.gameline }}">
                        <div class="tg-card-body">
                            <h6 class="{{ chronicle.gameline }}_heading">
                                <a href="{{ chronicle.get_absolute_url }}">
                                    {{ chronicle.name }}
                                </a>
                            </h6>
                            <p class="text-muted mb-0">
                                {{ chronicle.get_gameline_display }}
                            </p>
                        </div>
                    </div>
                </div>
            {% empty %}
                <div class="col-12">
                    <p class="text-center text-muted">Not in any chronicles yet</p>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
```

## Storyteller Dashboard

### ST Chronicles Section

```html
{% if is_st %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-center">
            <h5 class="tg-card-title">Chronicles I Run</h5>
            <a href="{% url 'game:chronicle_create' %}" class="btn btn-sm btn-primary">
                Create Chronicle
            </a>
        </div>
    </div>
    <div class="tg-card-body">
        <div class="row">
            {% for chronicle in st_chronicles %}
                <div class="col-md-6 mb-3">
                    <div class="tg-card h-100" data-gameline="{{ chronicle.gameline }}">
                        <div class="tg-card-body">
                            <h6 class="{{ chronicle.gameline }}_heading">
                                <a href="{{ chronicle.get_absolute_url }}">
                                    {{ chronicle.name }}
                                </a>
                            </h6>
                            <p class="mb-2">{{ chronicle.get_gameline_display }}</p>
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
                    <p class="text-center text-muted">Not running any chronicles yet</p>
                </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}
```

### Approval Queue

```html
{% if is_st and pending_approvals %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-center">
            <h5 class="tg-card-title">Approval Queue</h5>
            <span class="tg-badge badge-pill badge-sub">
                {{ pending_approvals|length }}
            </span>
        </div>
    </div>
    <div class="tg-card-body">
        <table class="tg-table">
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Name</th>
                    <th>Chronicle</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for item in pending_approvals %}
                    <tr>
                        <td>{{ item.type }}</td>
                        <td>
                            <a href="{{ item.get_absolute_url }}">
                                {{ item.name }}
                            </a>
                        </td>
                        <td>{{ item.chronicle.name }}</td>
                        <td>
                            <a href="{{ item.get_absolute_url }}" class="btn btn-sm btn-primary">
                                Review
                            </a>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endif %}
```

## Profile Display

### Profile Header

```html
<div class="tg-card header-card mb-4">
    <div class="tg-card-header">
        <div class="d-flex justify-content-between align-items-start">
            <div class="d-flex align-items-start">
                {% if profile.avatar %}
                    <img src="{{ profile.avatar.url }}"
                         alt="{{ user.username }}"
                         class="profile-avatar mr-3"
                         style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover;">
                {% endif %}
                <div>
                    <h1 class="tg-card-title">
                        {% if profile.display_name %}
                            {{ profile.display_name }}
                        {% else %}
                            {{ user.username }}
                        {% endif %}
                    </h1>
                    <p class="tg-card-subtitle">@{{ user.username }}</p>
                    {% if profile.is_st %}
                        <span class="tg-badge badge-pill badge-app">Storyteller</span>
                    {% endif %}
                </div>
            </div>
            {% if user == request.user %}
                <a href="{% url 'accounts:profile_edit' %}" class="btn btn-sm btn-primary">
                    Edit Profile
                </a>
            {% endif %}
        </div>
    </div>
</div>
```

### Profile Bio

```html
{% load sanitize_text %}

{% if profile.bio %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Bio</h5>
    </div>
    <div class="tg-card-body">
        {{ profile.bio|sanitize_html }}
    </div>
</div>
{% endif %}
```

## Authentication Forms

### Login Form

```html
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="tg-card">
                <div class="tg-card-header">
                    <h3 class="tg-card-title">Login</h3>
                </div>
                <div class="tg-card-body">
                    <form method="post">
                        {% csrf_token %}

                        <div class="mb-3">
                            <label for="id_username" class="form-label">Username</label>
                            <input type="text"
                                   name="username"
                                   id="id_username"
                                   class="form-control"
                                   required>
                        </div>

                        <div class="mb-3">
                            <label for="id_password" class="form-label">Password</label>
                            <input type="password"
                                   name="password"
                                   id="id_password"
                                   class="form-control"
                                   required>
                        </div>

                        {% if form.errors %}
                            <div class="alert alert-danger">
                                Invalid username or password
                            </div>
                        {% endif %}

                        <button type="submit" class="btn btn-primary w-100">
                            Login
                        </button>
                    </form>

                    <div class="mt-3 text-center">
                        <p class="mb-0">
                            Don't have an account?
                            <a href="{% url 'accounts:register' %}">Register</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Registration Form

```html
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="tg-card">
                <div class="tg-card-header">
                    <h3 class="tg-card-title">Register</h3>
                </div>
                <div class="tg-card-body">
                    <form method="post">
                        {% csrf_token %}

                        {{ form.as_p }}

                        <button type="submit" class="btn btn-primary w-100">
                            Register
                        </button>
                    </form>

                    <div class="mt-3 text-center">
                        <p class="mb-0">
                            Already have an account?
                            <a href="{% url 'accounts:login' %}">Login</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

## Profile Edit Form

```html
<div class="tg-card">
    <div class="tg-card-header">
        <h3 class="tg-card-title">Edit Profile</h3>
    </div>
    <div class="tg-card-body">
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}

            <div class="mb-3">
                <label for="{{ form.display_name.id_for_label }}" class="form-label">
                    {{ form.display_name.label }}
                </label>
                {{ form.display_name }}
                {% if form.display_name.help_text %}
                    <small class="form-text text-muted">
                        {{ form.display_name.help_text }}
                    </small>
                {% endif %}
            </div>

            <div class="mb-3">
                <label for="{{ form.bio.id_for_label }}" class="form-label">
                    {{ form.bio.label }}
                </label>
                {{ form.bio }}
            </div>

            <div class="mb-3">
                <label for="{{ form.avatar.id_for_label }}" class="form-label">
                    {{ form.avatar.label }}
                </label>
                {{ form.avatar }}
                {% if profile.avatar %}
                    <div class="mt-2">
                        <img src="{{ profile.avatar.url }}"
                             alt="Current avatar"
                             style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover;">
                    </div>
                {% endif %}
            </div>

            <div class="mb-3">
                <label for="{{ form.theme.id_for_label }}" class="form-label">
                    {{ form.theme.label }}
                </label>
                {{ form.theme }}
            </div>

            <button type="submit" class="btn btn-primary">Save Changes</button>
            <a href="{% url 'accounts:profile' %}" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</div>
```

## Theme Selector

```html
<div class="mb-3">
    <label class="form-label">Theme</label>
    <div class="theme-selector">
        {% for theme_code, theme_name in theme_choices %}
            <div class="form-check">
                <input class="form-check-input"
                       type="radio"
                       name="theme"
                       id="theme_{{ theme_code }}"
                       value="{{ theme_code }}"
                       {% if profile.theme == theme_code %}checked{% endif %}>
                <label class="form-check-label" for="theme_{{ theme_code }}">
                    {{ theme_name }}
                </label>
            </div>
        {% endfor %}
    </div>
</div>
```

## Activity Feed

```html
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title">Recent Activity</h5>
    </div>
    <div class="tg-card-body">
        {% for activity in recent_activity %}
            <div class="activity-item mb-3 pb-3 border-bottom">
                <div class="d-flex align-items-start">
                    <div class="activity-icon mr-3">
                        {% if activity.type == 'character' %}
                            <i class="fas fa-user"></i>
                        {% elif activity.type == 'scene' %}
                            <i class="fas fa-scroll"></i>
                        {% elif activity.type == 'xp' %}
                            <i class="fas fa-star"></i>
                        {% endif %}
                    </div>
                    <div class="flex-grow-1">
                        <p class="mb-1">{{ activity.description }}</p>
                        <small class="text-muted">{{ activity.timestamp|timesince }} ago</small>
                    </div>
                </div>
            </div>
        {% empty %}
            <p class="text-muted">No recent activity</p>
        {% endfor %}
    </div>
</div>
```

## Responsive Considerations

```html
<!-- Desktop: 3 columns, Tablet: 2 columns, Mobile: 1 column -->
<div class="row">
    <div class="col-lg-4 col-md-6 col-12 mb-3">
        <!-- Content -->
    </div>
</div>
```

## Template Checklist

- [ ] Uses `tg-card` components
- [ ] Implements responsive layout
- [ ] Sanitizes user-provided content with `|sanitize_html`
- [ ] Shows appropriate content based on user permissions
- [ ] Uses proper form handling with CSRF tokens
- [ ] Displays avatar images responsively
- [ ] Includes helpful error messages
- [ ] Uses consistent spacing (mb-3, mb-4)

## See Also

- `core/docs/STYLE.md` - Base template styling
- `game/docs/STYLE.md` - Chronicle and scene templates
- `/SOURCES/STYLE.md` - Project-wide style guide
