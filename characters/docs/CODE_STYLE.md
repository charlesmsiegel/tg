# Characters App - Code Style Guide

## Overview

This document outlines coding standards for the `characters` app, which manages all character types across World of Darkness gamelines using polymorphic inheritance.

## General Principles

1. **Gameline Separation** - Each gameline has its own subdirectory in models/, forms/, views/, etc.
2. **Shared Core** - Common functionality goes in core/ subdirectories
3. **Polymorphic Pattern** - All characters extend the base Character model
4. **Consistent Structure** - Mirror the structure across gamelines for maintainability

## Directory Organization

### Models Structure

```
models/
├── __init__.py                 # Import all models for registration
├── core/
│   ├── __init__.py
│   ├── character.py            # Base Character model
│   ├── ability_block.py        # Talents, Skills, Knowledges
│   ├── attribute_block.py      # Physical, Social, Mental
│   ├── meritflaw.py           # MeritFlaw assignments
│   └── specialty.py           # Specialty assignments
└── {gameline}/
    ├── __init__.py
    ├── {type}.py              # Main character type
    ├── background.py          # Gameline backgrounds
    ├── power.py               # Disciplines/Gifts/Spheres/etc
    └── faction.py             # Clans/Tribes/Traditions/etc
```

**Best Practices:**
- One model per file (except closely related models)
- Import all models in `__init__.py` for polymorphic registration
- Use descriptive filenames matching model names (lowercase)

### Forms Structure

```
forms/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── character.py           # Base character form components
│   └── mixins.py              # Reusable form mixins
└── {gameline}/
    ├── __init__.py
    ├── {type}.py              # Character creation/edit forms
    └── partials.py            # Reusable form components
```

### Views Structure

```
views/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── character.py           # Base character views
│   └── mixins.py              # Reusable view mixins
└── {gameline}/
    ├── __init__.py
    ├── {type}.py              # CRUD views for character type
    ├── advancement.py         # XP spending views
    └── utils.py               # Helper functions
```

### Templates Structure

```
templates/characters/
├── core/
│   ├── character/
│   │   ├── detail.html        # Base character detail template
│   │   ├── list.html          # Character list template
│   │   └── display_includes/  # Reusable template fragments
│   └── ...
└── {gameline}/
    ├── {type}/
    │   ├── detail.html        # Extends core/character/detail.html
    │   ├── create.html        # Character creation
    │   ├── update.html        # Character editing
    │   └── display_includes/  # Gameline-specific fragments
    └── ...
```

## Model Patterns

### Base Character Model

The base Character model should be minimal and generic:

```python
# models/core/character.py
from core.models import Model
from django.db import models

class Character(Model):
    """Base model for all character types across gamelines."""

    # Ownership
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='characters'
    )

    # Campaign
    chronicle = models.ForeignKey(
        'game.Chronicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='characters'
    )

    # Status
    status = models.CharField(
        max_length=3,
        choices=core.constants.STATUS_CHOICES,
        default='Un'
    )

    # Core character info
    concept = models.CharField(max_length=100, blank=True)
    nature = models.ForeignKey('core.Nature', on_delete=models.SET_NULL, null=True)
    demeanor = models.ForeignKey('core.Demeanor', on_delete=models.SET_NULL, null=True)

    # XP tracking
    xp = models.IntegerField(default=0)
    spent_xp = models.JSONField(default=dict)
    freebies = models.IntegerField(default=15)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Return URL using polymorphic type."""
        return reverse(
            f'{self.get_gameline()}:{self.get_type()}_detail',
            kwargs={'pk': self.pk}
        )

    def get_gameline(self):
        """Return gameline code ('vtm', 'wta', etc)."""
        raise NotImplementedError("Subclasses must implement get_gameline()")

    def get_type(self):
        """Return character type ('vampire', 'werewolf', etc)."""
        return self.__class__.__name__.lower()
```

**Best Practices:**
- Keep base model generic - no gameline-specific fields
- Use JSONField for flexible data structures
- Implement helper methods for common operations
- Raise NotImplementedError for methods subclasses must override

### Gameline-Specific Models

Each gameline extends Character with specific traits:

```python
# models/vampire/vtm.py
from characters.models.core import Character

class VtMHuman(Character):
    """Base for all Vampire: The Masquerade characters."""

    # Generation and lineage
    generation = models.IntegerField(default=13)
    sire = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='childer'
    )

    # Clan
    clan = models.ForeignKey(
        'Clan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Blood
    blood_pool = models.IntegerField(default=10)
    blood_max = models.IntegerField(default=10)

    # Virtues (VtM-specific)
    conscience = models.IntegerField(default=1)
    self_control = models.IntegerField(default=1)
    courage = models.IntegerField(default=1)

    # Paths (for alternate morality)
    path = models.CharField(max_length=100, blank=True)
    path_rating = models.IntegerField(default=0)

    # Disciplines (stored as JSON)
    disciplines = models.JSONField(default=dict)
    # Example: {"Celerity": 2, "Potence": 1}

    class Meta:
        verbose_name = "VtM Character"
        verbose_name_plural = "VtM Characters"

    def get_gameline(self):
        return 'vtm'

    def calculate_blood_max(self):
        """Calculate max blood pool based on generation."""
        blood_by_generation = {
            3: 30, 4: 25, 5: 20, 6: 15, 7: 13,
            8: 12, 9: 11, 10: 10, 11: 9, 12: 8, 13: 7
        }
        return blood_by_generation.get(self.generation, 10)
```

**Best Practices:**
- Group related fields together with comments
- Use JSONField for variable-length lists (Disciplines, Gifts, Spheres)
- Provide calculation methods for derived values
- Use descriptive ForeignKey related_names
- Override get_gameline() to return gameline code

### Model Method Conventions

```python
class Character(Model):
    # Display methods (for templates)
    def get_absolute_url(self):
        """Canonical URL for this character."""
        pass

    def get_update_url(self):
        """URL for editing this character."""
        pass

    def get_heading(self):
        """CSS class for gameline-specific styling."""
        return f"{self.get_gameline()}_heading"

    # Status checks
    def is_approved(self):
        """Check if character is approved."""
        return self.status == 'App'

    def is_submitted(self):
        """Check if character is submitted for review."""
        return self.status == 'Sub'

    # Permission checks
    def can_be_edited_by(self, user):
        """Check if user can edit this character."""
        if user.is_superuser:
            return True
        if self.owner == user:
            return True
        if hasattr(user, 'profile') and user.profile.is_st():
            if self.chronicle and self.chronicle.storytellers.filter(id=user.id).exists():
                return True
        return False

    # Business logic
    def add_xp(self, amount, reason=""):
        """Add XP to character."""
        self.xp += amount
        self.save()

    def spend_xp(self, trait, cost):
        """Record XP spending (requires ST approval)."""
        if self.xp < cost:
            raise ValueError("Insufficient XP")
        self.spent_xp[trait] = {
            'cost': cost,
            'approved': False
        }
        self.save()

    # Calculation methods
    def calculate_total_freebies(self):
        """Calculate total freebie points."""
        base = 15
        # Add bonus points from merits/flaws
        return base + self.get_freebie_bonus()
```

**Naming Conventions:**
- `get_*` - Returns a value
- `is_*` - Boolean check
- `can_*` - Permission check
- `calculate_*` - Performs calculation
- `add_*` / `remove_*` - Modifies data

## Form Patterns

### Character Creation Forms

```python
# forms/vampire/vampire.py
from django import forms
from characters.models.vampire import Vampire

class VampireForm(forms.ModelForm):
    """Form for creating/editing Vampire characters."""

    class Meta:
        model = Vampire
        fields = [
            'name', 'concept', 'nature', 'demeanor',
            'clan', 'generation', 'sire',
            'strength', 'dexterity', 'stamina',
            # ... all character fields
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'sire': forms.Select(attrs={'class': 'select2'}),
        }

    def __init__(self, *args, **kwargs):
        """Customize form initialization."""
        super().__init__(*args, **kwargs)

        # Filter sire choices to same clan
        if 'clan' in self.data:
            clan_id = self.data.get('clan')
            self.fields['sire'].queryset = Vampire.objects.filter(clan_id=clan_id)

        # Add CSS classes
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        """Validate form data."""
        cleaned_data = super().clean()

        # Custom validation logic
        generation = cleaned_data.get('generation')
        if generation and generation < 3:
            raise forms.ValidationError("Generation cannot be less than 3")

        return cleaned_data
```

**Best Practices:**
- Specify fields explicitly (don't use `__all__`)
- Customize widgets for better UX
- Override `__init__` for dynamic field configuration
- Implement `clean()` for cross-field validation
- Add helpful help_text to fields

### Form Mixins

Create reusable form components:

```python
# forms/core/mixins.py
class AttributeFormMixin:
    """Mixin for forms with Physical/Social/Mental attributes."""

    def validate_attribute_priorities(self):
        """Ensure attributes follow 7/5/3 priority distribution."""
        physical = self.cleaned_data.get('strength', 0) + \
                  self.cleaned_data.get('dexterity', 0) + \
                  self.cleaned_data.get('stamina', 0)
        # ... validation logic

class XPSpendingFormMixin:
    """Mixin for forms that spend XP."""

    def clean_xp_cost(self):
        """Verify character has enough XP."""
        cost = self.cleaned_data.get('xp_cost')
        if self.instance.xp < cost:
            raise forms.ValidationError("Insufficient XP")
        return cost
```

## View Patterns

### Character CRUD Views

```python
# views/vampire/vampire.py
from django.views.generic import DetailView, CreateView, UpdateView
from core.mixins import CharacterOwnerMixin
from characters.models.vampire import Vampire
from characters.forms.vampire import VampireForm

class VampireDetailView(DetailView):
    """Display vampire character sheet."""
    model = Vampire
    template_name = 'characters/vampire/vampire/detail.html'
    context_object_name = 'character'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context
        context['disciplines'] = self.object.get_disciplines()
        context['can_edit'] = self.object.can_be_edited_by(self.request.user)
        return context

class VampireCreateView(CharacterOwnerMixin, CreateView):
    """Create new vampire character."""
    model = Vampire
    form_class = VampireForm
    template_name = 'characters/vampire/vampire/create.html'

    def form_valid(self, form):
        """Set owner on character creation."""
        form.instance.owner = self.request.user
        form.instance.status = 'Un'
        return super().form_valid(form)

class VampireUpdateView(CharacterOwnerMixin, UpdateView):
    """Edit existing vampire character."""
    model = Vampire
    form_class = VampireForm
    template_name = 'characters/vampire/vampire/update.html'

    def get_queryset(self):
        """Limit to characters user can edit."""
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(owner=self.request.user)
        return qs
```

**Best Practices:**
- Use class-based views for consistency
- Inherit from appropriate mixins for permission checking
- Override `get_context_data()` for additional context
- Override `form_valid()` for pre-save logic
- Use `get_queryset()` to filter accessible objects

### View Mixins

```python
# views/core/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class CharacterOwnerMixin(LoginRequiredMixin):
    """Ensure user owns the character or is ST."""

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not obj.can_be_edited_by(self.request.user):
            raise PermissionDenied("You don't have permission to edit this character")

        return obj
```

## Template Patterns

### Character Detail Template

```html
<!-- templates/characters/vampire/vampire/detail.html -->
{% extends "characters/core/character/detail.html" %}
{% load dots sanitize_text %}

{% block character_header %}
<div class="tg-card header-card mb-4" data-gameline="vtm">
    <div class="tg-card-header">
        <h1 class="tg-card-title vtm_heading">{{ character.name }}</h1>
        <p class="tg-card-subtitle">
            {{ character.concept }}
            {% if character.clan %}
                - {{ character.clan.name }}
            {% endif %}
        </p>
    </div>
</div>
{% endblock %}

{% block character_vitals %}
<div class="row mb-4">
    <div class="col-md-4">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="vtm_heading">Blood Pool</h6>
                <div class="stat-display">
                    {{ character.blood_pool|dots:character.blood_max }}
                    <span>({{ character.blood_pool }}/{{ character.blood_max }})</span>
                </div>
            </div>
        </div>
    </div>
    <!-- More vitals -->
</div>
{% endblock %}

{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-body">
        <h6 class="vtm_heading">Disciplines</h6>
        {% include "characters/vampire/vampire/display_includes/disciplines.html" %}
    </div>
</div>
{% endblock %}
```

**Best Practices:**
- Extend gameline-specific base templates
- Use `{% load %}` at top for custom tags
- Use gameline heading classes for styling
- Break complex sections into includes
- Use consistent block names across gamelines

### Display Includes

Create reusable template fragments:

```html
<!-- templates/characters/vampire/vampire/display_includes/disciplines.html -->
{% load dots %}

<div class="disciplines-list">
    {% for discipline, rating in character.disciplines.items %}
        <div class="discipline-row">
            <span class="discipline-name">{{ discipline }}:</span>
            <span class="discipline-dots">{{ rating|dots }}</span>
        </div>
    {% empty %}
        <p class="text-muted">No disciplines</p>
    {% endfor %}
</div>
```

## Testing Patterns

### Model Tests

```python
# tests/vampire/test_vampire.py
import pytest
from django.test import TestCase
from characters.models.vampire import Vampire
from accounts.models import Profile

class VampireModelTest(TestCase):
    """Tests for Vampire model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user('testuser', password='testpass')
        self.vampire = Vampire.objects.create(
            owner=self.user,
            name="Test Vampire",
            clan=Clan.objects.create(name="Brujah"),
            generation=10
        )

    def test_vampire_creation(self):
        """Test vampire is created with correct attributes."""
        self.assertIsNotNone(self.vampire.pk)
        self.assertEqual(self.vampire.name, "Test Vampire")
        self.assertEqual(self.vampire.generation, 10)

    def test_blood_pool_calculation(self):
        """Test blood pool max is calculated correctly."""
        expected = 10  # Generation 10 = 10 blood
        self.assertEqual(self.vampire.calculate_blood_max(), expected)

    def test_get_gameline(self):
        """Test get_gameline returns 'vtm'."""
        self.assertEqual(self.vampire.get_gameline(), 'vtm')
```

### View Tests

```python
# tests/vampire/test_vampire_views.py
import pytest
from django.test import TestCase, Client
from django.urls import reverse

class VampireViewTest(TestCase):
    """Tests for Vampire views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='testpass')
        self.vampire = Vampire.objects.create(
            owner=self.user,
            name="Test Vampire"
        )

    def test_detail_view(self):
        """Test vampire detail view."""
        url = reverse('characters:vampire_detail', kwargs={'pk': self.vampire.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Vampire")

    def test_create_view_requires_login(self):
        """Test create view requires authentication."""
        url = reverse('characters:vampire_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
```

## Naming Conventions

- **Models**: PascalCase (e.g., `Vampire`, `VtMHuman`)
- **Forms**: ModelNameForm (e.g., `VampireForm`)
- **Views**: ModelNameActionView (e.g., `VampireCreateView`)
- **URLs**: `{model}_{action}` (e.g., `vampire_detail`, `vampire_create`)
- **Templates**: `{model}/{action}.html`

## Import Order

```python
# 1. Standard library
import json
from datetime import datetime

# 2. Django imports
from django.db import models
from django.views.generic import DetailView

# 3. Third-party
from polymorphic.models import PolymorphicModel

# 4. Other TG apps
from core.models import Model
from game.models import Chronicle

# 5. Current app, other gamelines
from characters.models.core import Character

# 6. Current gameline
from .clan import Clan
```

## Anti-Patterns to Avoid

- ❌ Putting gameline-specific logic in core Character model
- ❌ Hardcoding attribute/ability lists (use constants)
- ❌ Inconsistent structure across gamelines
- ❌ Direct database queries in templates
- ❌ Skipping permission checks in views
- ❌ Duplicate code instead of using mixins

## Code Review Checklist

- [ ] Model extends appropriate base (Character or subclass)
- [ ] Forms specify fields explicitly
- [ ] Views implement permission checking
- [ ] Templates extend gameline-specific bases
- [ ] Tests cover model methods and view logic
- [ ] Consistent naming across gamelines
- [ ] Documentation updated
- [ ] Migrations created and tested
