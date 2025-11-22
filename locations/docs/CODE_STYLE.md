# Locations App - Code Style Guide

## Overview

The locations app follows the same architectural patterns as the characters and items apps. All locations use polymorphic inheritance with gameline-specific implementations.

## Key Principles

1. **Mirror Characters/Items Structure** - Locations follow established patterns
2. **Polymorphic Pattern** - All locations extend base LocationModel
3. **Gameline Separation** - Each gameline has its own subdirectory
4. **Shared Components** - Common functionality in core/ subdirectories

## Model Patterns

### Base LocationModel

```python
# models/core/location.py
from core.models import Model

class LocationModel(Model):
    """Base model for all location types across gamelines."""

    # Ownership
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    chronicle = models.ForeignKey('game.Chronicle', on_delete=models.SET_NULL, null=True, blank=True)

    # Status
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='Un')

    # Location properties
    location_type = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def get_gameline(self):
        """Return gameline code."""
        raise NotImplementedError("Subclasses must implement get_gameline()")
```

### Gameline-Specific Locations

```python
# models/werewolf/caern.py
from locations.models.core import LocationModel

class Caern(LocationModel):
    """Werewolf caern (sacred site)."""

    # Caern-specific fields
    level = models.IntegerField(default=1)
    totem = models.CharField(max_length=100)
    tribe = models.ForeignKey('Tribe', on_delete=models.SET_NULL, null=True)
    gauntlet_rating = models.IntegerField(default=7)

    # Power and resources
    gnosis_per_day = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Caern"
        verbose_name_plural = "Caerns"

    def get_gameline(self):
        return 'wta'

    def is_accessible_to(self, character):
        """Check if character can access this caern."""
        # Logic for tribe restrictions, etc.
        return True
```

## Form Patterns

```python
# forms/werewolf/caern.py
from django import forms
from locations.models.werewolf import Caern

class CaernForm(forms.ModelForm):
    """Form for creating/editing Caern locations."""

    class Meta:
        model = Caern
        fields = [
            'name', 'description', 'level', 'totem',
            'tribe', 'gauntlet_rating', 'gnosis_per_day'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_level(self):
        """Validate caern level."""
        level = self.cleaned_data.get('level')
        if level < 1 or level > 5:
            raise forms.ValidationError("Caern level must be between 1 and 5")
        return level
```

## View Patterns

Follow the same patterns as characters and items apps.

## Template Patterns

```html
<!-- templates/locations/werewolf/caern/detail.html -->
{% extends "locations/core/location/detail.html" %}
{% load dots %}

{% block location_header %}
<div class="tg-card header-card mb-4" data-gameline="wta">
    <div class="tg-card-header">
        <h1 class="tg-card-title wta_heading">{{ location.name }}</h1>
        <p class="tg-card-subtitle">Caern (Level {{ location.level }})</p>
    </div>
</div>
{% endblock %}
```

## Best Practices

- Use descriptive location names
- Include geographic information when relevant
- Provide access control methods
- Follow consistent structure across gamelines
- Mirror characters/items app patterns

## See Also

- `characters/docs/CODE_STYLE.md` - Parallel structure
- `items/docs/CODE_STYLE.md` - Parallel structure
- `/CLAUDE.md` - Project-wide conventions
