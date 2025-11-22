# Items App - Code Style Guide

## Overview

The items app follows the same architectural patterns as the characters app. Items use polymorphic inheritance with gameline-specific implementations.

## Key Principles

1. **Mirror Characters Structure** - Items app structure mirrors characters app for consistency
2. **Polymorphic Pattern** - All items extend the base ItemModel
3. **Gameline Separation** - Each gameline has its own subdirectory
4. **Shared Components** - Common functionality in core/ subdirectories

## Model Patterns

### Base ItemModel

```python
# models/core/item.py
from core.models import Model

class ItemModel(Model):
    """Base model for all item types across gamelines."""

    # Ownership
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    chronicle = models.ForeignKey('game.Chronicle', on_delete=models.SET_NULL, null=True, blank=True)

    # Status
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='Un')

    # Item properties
    item_type = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    value = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def get_gameline(self):
        """Return gameline code."""
        raise NotImplementedError("Subclasses must implement get_gameline()")
```

### Gameline-Specific Items

```python
# models/werewolf/fetish.py
from items.models.core import ItemModel

class Fetish(ItemModel):
    """Werewolf fetish (spirit-bound item)."""

    # Fetish-specific fields
    gnosis = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    spirit_type = models.CharField(max_length=100)
    power = models.TextField()

    # Background requirement
    background_cost = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Fetish"
        verbose_name_plural = "Fetishes"

    def get_gameline(self):
        return 'wta'

    def can_be_activated_by(self, character):
        """Check if character can activate this fetish."""
        return character.gnosis >= self.gnosis
```

## Form Patterns

```python
# forms/werewolf/fetish.py
from django import forms
from items.models.werewolf import Fetish

class FetishForm(forms.ModelForm):
    """Form for creating/editing Fetish items."""

    class Meta:
        model = Fetish
        fields = [
            'name', 'description', 'gnosis', 'level',
            'spirit_type', 'power', 'background_cost'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'power': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_gnosis(self):
        """Validate gnosis rating."""
        gnosis = self.cleaned_data.get('gnosis')
        if gnosis < 1 or gnosis > 10:
            raise forms.ValidationError("Gnosis must be between 1 and 10")
        return gnosis
```

## View Patterns

```python
# views/werewolf/fetish.py
from django.views.generic import DetailView, CreateView, UpdateView
from items.models.werewolf import Fetish
from items.forms.werewolf import FetishForm

class FetishDetailView(DetailView):
    """Display fetish details."""
    model = Fetish
    template_name = 'items/werewolf/fetish/detail.html'
    context_object_name = 'item'

class FetishCreateView(CreateView):
    """Create new fetish."""
    model = Fetish
    form_class = FetishForm
    template_name = 'items/werewolf/fetish/create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.item_type = 'Fetish'
        return super().form_valid(form)
```

## Template Patterns

```html
<!-- templates/items/werewolf/fetish/detail.html -->
{% extends "items/core/item/detail.html" %}
{% load dots %}

{% block item_header %}
<div class="tg-card header-card mb-4" data-gameline="wta">
    <div class="tg-card-header">
        <h1 class="tg-card-title wta_heading">{{ item.name }}</h1>
        <p class="tg-card-subtitle">Fetish (Level {{ item.level }})</p>
    </div>
</div>
{% endblock %}

{% block item_stats %}
<div class="row mb-4">
    <div class="col-md-6">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="wta_heading">Gnosis Requirement</h6>
                <div class="stat-value">{{ item.gnosis|dots }}</div>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="tg-card h-100">
            <div class="tg-card-body">
                <h6 class="wta_heading">Background Cost</h6>
                <div class="stat-value">{{ item.background_cost }}</div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block gameline_specific %}
<div class="tg-card mb-4">
    <div class="tg-card-body">
        <h6 class="wta_heading">Power</h6>
        <p>{{ item.power }}</p>

        <h6 class="wta_heading mt-3">Spirit Type</h6>
        <p>{{ item.spirit_type }}</p>
    </div>
</div>
{% endblock %}
```

## Testing Patterns

```python
# tests/werewolf/test_fetish.py
from django.test import TestCase
from items.models.werewolf import Fetish

class FetishModelTest(TestCase):
    """Tests for Fetish model."""

    def setUp(self):
        self.user = User.objects.create_user('testuser', password='testpass')
        self.fetish = Fetish.objects.create(
            owner=self.user,
            name="Spirit Whistle",
            gnosis=5,
            level=2,
            spirit_type="Wind Spirit"
        )

    def test_fetish_creation(self):
        """Test fetish is created correctly."""
        self.assertIsNotNone(self.fetish.pk)
        self.assertEqual(self.fetish.name, "Spirit Whistle")
        self.assertEqual(self.fetish.gnosis, 5)

    def test_get_gameline(self):
        """Test get_gameline returns 'wta'."""
        self.assertEqual(self.fetish.get_gameline(), 'wta')
```

## Naming Conventions

Follow the same conventions as characters app:

- **Models**: PascalCase (e.g., `Fetish`, `Wonder`)
- **Forms**: ModelNameForm (e.g., `FetishForm`)
- **Views**: ModelNameActionView (e.g., `FetishDetailView`)
- **URLs**: `{model}_{action}` (e.g., `fetish_detail`, `fetish_create`)
- **Templates**: `{model}/{action}.html`

## Best Practices

- Use JSONField for variable properties (e.g., sphere requirements for Wonders)
- Provide validation methods for item properties
- Include requirements checking (e.g., can_be_activated_by)
- Follow consistent structure across gamelines
- Mirror characters app patterns for familiarity

## Anti-Patterns to Avoid

- ❌ Putting gameline-specific logic in base ItemModel
- ❌ Inconsistent structure across gamelines
- ❌ Skipping permission checks in views
- ❌ Duplicate code instead of using mixins

## See Also

- `characters/docs/CODE_STYLE.md` - Parallel structure for reference
- `/CLAUDE.md` - Project-wide conventions
