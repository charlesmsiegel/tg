# Game App - Code Style Guide

## Overview

The game app manages chronicles, scenes, and XP tracking. Unlike characters/items/locations, it does not use polymorphic models but has simpler, more direct relationships.

## General Principles

1. **Simple Models** - No polymorphism needed, straightforward Django models
2. **Clear Relationships** - Chronicle → Story → Scene hierarchy
3. **Signal-Driven** - Use signals for automatic XP processing
4. **Permission-Aware** - Strict ST/player permission separation

## Model Patterns

### Chronicle Model

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Chronicle(models.Model):
    """Represents a campaign or ongoing game."""

    # Basic info
    name = models.CharField(max_length=100)
    description = models.TextField()
    gameline = models.CharField(max_length=20, choices=GAMELINE_CHOICES)

    # Participants
    storytellers = models.ManyToManyField(
        User,
        related_name='st_chronicles'
    )
    players = models.ManyToManyField(
        User,
        related_name='player_chronicles'
    )

    # Settings
    allowed_books = models.ManyToManyField('core.Book', blank=True)
    house_rules = models.ManyToManyField('core.HouseRule', blank=True)

    # Status
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='Un'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def is_st(self, user):
        """Check if user is storyteller of this chronicle."""
        return self.storytellers.filter(id=user.id).exists()

    def is_player(self, user):
        """Check if user is player in this chronicle."""
        return self.players.filter(id=user.id).exists()
```

**Best Practices:**
- Use descriptive related_names to avoid conflicts
- Provide helper methods for permission checking
- Keep business logic in model methods

### Scene Model

```python
class Scene(models.Model):
    """Represents a single game session."""

    # Identity
    name = models.CharField(max_length=100)
    chronicle = models.ForeignKey(
        Chronicle,
        on_delete=models.CASCADE,
        related_name='scenes'
    )
    story = models.ForeignKey(
        'Story',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scenes'
    )

    # Session details
    date = models.DateField()
    description = models.TextField()
    notes = models.TextField(blank=True)

    # Participants
    characters = models.ManyToManyField('characters.Character')

    # XP
    base_xp = models.IntegerField(default=1)
    bonus_xp = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def total_xp(self):
        """Calculate total XP awarded."""
        return self.base_xp + self.bonus_xp

    def award_xp(self):
        """Award XP to all participating characters."""
        total = self.total_xp()
        for character in self.characters.all():
            character.add_xp(total)
```

## Form Patterns

```python
# forms.py
from django import forms
from .models import Chronicle, Scene

class ChronicleForm(forms.ModelForm):
    """Form for creating/editing Chronicles."""

    class Meta:
        model = Chronicle
        fields = [
            'name', 'description', 'gameline',
            'allowed_books', 'house_rules'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'allowed_books': forms.CheckboxSelectMultiple(),
        }

class SceneForm(forms.ModelForm):
    """Form for creating/editing Scenes."""

    class Meta:
        model = Scene
        fields = [
            'name', 'date', 'description', 'story',
            'characters', 'base_xp', 'bonus_xp'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'characters': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, chronicle=None, **kwargs):
        """Filter characters to chronicle members."""
        super().__init__(*args, **kwargs)
        if chronicle:
            self.fields['characters'].queryset = \
                Character.objects.filter(chronicle=chronicle)
```

## View Patterns

```python
# views.py
from django.views.generic import DetailView, CreateView, UpdateView
from core.mixins import StorytellerRequiredMixin
from .models import Chronicle, Scene
from .forms import ChronicleForm, SceneForm

class ChronicleDetailView(DetailView):
    """Display chronicle details."""
    model = Chronicle
    template_name = 'game/chronicle/detail.html'
    context_object_name = 'chronicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_scenes'] = self.object.scenes.all()[:5]
        context['is_st'] = self.object.is_st(self.request.user)
        context['is_player'] = self.object.is_player(self.request.user)
        return context

class SceneCreateView(StorytellerRequiredMixin, CreateView):
    """Create new scene (ST only)."""
    model = Scene
    form_class = SceneForm
    template_name = 'game/scene/create.html'

    def get_form_kwargs(self):
        """Pass chronicle to form."""
        kwargs = super().get_form_kwargs()
        kwargs['chronicle'] = self.get_chronicle()
        return kwargs

    def form_valid(self, form):
        """Set chronicle on scene."""
        form.instance.chronicle = self.get_chronicle()
        return super().form_valid(form)

    def get_chronicle(self):
        """Get chronicle from URL."""
        return Chronicle.objects.get(pk=self.kwargs['chronicle_pk'])
```

## Signal Patterns

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Scene, WeeklyXPRequest

@receiver(post_save, sender=Scene)
def award_scene_xp(sender, instance, created, **kwargs):
    """Award XP when scene is created."""
    if created:
        instance.award_xp()

@receiver(post_save, sender=WeeklyXPRequest)
def process_xp_request(sender, instance, created, **kwargs):
    """Deduct XP when request is approved."""
    if not created and instance.approved:
        # Check if previously unapproved
        old_instance = WeeklyXPRequest.objects.get(pk=instance.pk)
        if not old_instance.approved:
            instance.character.xp -= instance.cost
            instance.character.save()
```

**Best Practices:**
- Use signals for automatic processing
- Check for state changes in post_save
- Document signal behavior clearly

## URL Patterns

```python
# urls.py
from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    # Chronicles
    path('chronicles/', views.ChronicleListView.as_view(), name='chronicle_list'),
    path('chronicles/<int:pk>/', views.ChronicleDetailView.as_view(), name='chronicle_detail'),
    path('chronicles/create/', views.ChronicleCreateView.as_view(), name='chronicle_create'),

    # Scenes
    path('chronicles/<int:chronicle_pk>/scenes/create/', views.SceneCreateView.as_view(), name='scene_create'),
    path('scenes/<int:pk>/', views.SceneDetailView.as_view(), name='scene_detail'),

    # XP
    path('xp/requests/', views.XPRequestListView.as_view(), name='xp_request_list'),
    path('xp/requests/<int:pk>/approve/', views.approve_xp_request, name='xp_request_approve'),
]
```

## Template Patterns

```html
<!-- templates/game/chronicle/detail.html -->
{% extends "core/base.html" %}
{% load sanitize_text %}

{% block content %}
<div class="tg-card mb-4" data-gameline="{{ chronicle.gameline }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ chronicle.gameline }}_heading">
            {{ chronicle.name }}
        </h1>
    </div>
    <div class="tg-card-body">
        {{ chronicle.description|sanitize_html }}
    </div>
</div>

{% if is_st %}
    <div class="st-controls mb-4">
        <a href="{% url 'game:scene_create' chronicle.pk %}" class="btn btn-primary">
            Create Scene
        </a>
    </div>
{% endif %}

<div class="tg-card">
    <div class="tg-card-header">
        <h5>Recent Scenes</h5>
    </div>
    <div class="tg-card-body">
        {% for scene in recent_scenes %}
            <div class="scene-item">
                <a href="{{ scene.get_absolute_url }}">{{ scene.name }}</a>
                <span class="date">{{ scene.date }}</span>
            </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

## Testing Patterns

```python
# tests.py
from django.test import TestCase
from game.models import Chronicle, Scene
from characters.models.vampire import Vampire

class ChronicleTestCase(TestCase):
    """Tests for Chronicle model."""

    def setUp(self):
        self.st = User.objects.create_user('st', password='test')
        self.player = User.objects.create_user('player', password='test')
        self.chronicle = Chronicle.objects.create(
            name="Test Chronicle",
            gameline='vtm'
        )
        self.chronicle.storytellers.add(self.st)
        self.chronicle.players.add(self.player)

    def test_is_st(self):
        """Test ST check."""
        self.assertTrue(self.chronicle.is_st(self.st))
        self.assertFalse(self.chronicle.is_st(self.player))

    def test_is_player(self):
        """Test player check."""
        self.assertTrue(self.chronicle.is_player(self.player))
        self.assertTrue(self.chronicle.is_player(self.st))  # ST is also player
```

## Best Practices

- Use descriptive names for chronicles and scenes
- Always check permissions in views
- Use signals for XP automation
- Provide clear feedback on XP approval/rejection
- Keep XP costs consistent with game rules

## Anti-Patterns to Avoid

- ❌ Manually awarding XP instead of using signals
- ❌ Allowing players to approve their own XP requests
- ❌ Mixing gamelines in a single chronicle
- ❌ Skipping permission checks in views

## See Also

- `/CLAUDE.md` - Project-wide conventions
- `accounts/docs/CODE_STYLE.md` - User and ST management
