# Character Template System

A comprehensive templating system for World of Darkness character creation, allowing users to start with pre-configured character concepts from sourcebooks.

## Overview

**Status**: ✅ **Fully Implemented for Mage**, 📋 Templates Ready for All Gamelines

The template system provides:
- **30 pre-configured character templates** (5 per gameline)
- Optional template selection during character creation
- Full customization after template application
- Usage tracking and admin management

## Available Templates

### Mage: The Ascension (✅ Fully Integrated)
1. Virtual Adept Hacker
2. Order of Hermes Scholar
3. Verbena Healer
4. Akashic Brother
5. Cult of Ecstasy DJ

### Vampire: The Masquerade (📋 Templates Ready)
1. Detective
2. Socialite
3. Street Preacher
4. Criminal
5. Scholar

### Werewolf: The Apocalypse (📋 Templates Ready)
1. Ahroun Warrior
2. Theurge Mystic
3. Ragabash Trickster
4. Philodox Judge
5. Galliard Bard

### Changeling: The Dreaming (📋 Templates Ready)
1. Childling Dreamer
2. Wilder Artist
3. Grump Crafter
4. Knight Errant
5. Street Urchin

### Wraith: The Oblivion (📋 Templates Ready)
1. Detective Ghost
2. Vengeful Spirit
3. Guardian Spirit
4. Lost Soul
5. Scholar of Death

### Demon: The Fallen (📋 Templates Ready)
1. Fallen Detective
2. Corrupted Artist
3. Angelic Warrior
4. Tempter
5. Angelic Healer

## Loading Templates

### Load All Templates
```bash
source venv/bin/activate
python populate_db/character_templates/__init__.py
```

### Load Individual Gamelines
```bash
python populate_db/character_templates/mage_templates.py
python populate_db/character_templates/vampire_templates.py
python populate_db/character_templates/werewolf_templates.py
python populate_db/character_templates/changeling_templates.py
python populate_db/character_templates/wraith_templates.py
python populate_db/character_templates/demon_templates.py
```

## Integration Guide

### Reference Implementation: Mage (MtAHuman)

The Mage character creation fully integrates template selection. Use this as the reference for other gamelines.

**Files Modified:**
- `characters/views/mage/mtahuman.py` - Added template selection view and form
- `characters/urls/mage/detail.py` - Added template and creation URLs
- `characters/templates/characters/mage/mtahuman/template_select.html` - Template selection UI

### Adding Template Selection to Other Character Types

Follow this pattern for any character type (Vampire, Werewolf, etc.):

#### Step 1: Add Template Selection Form (in character views file)

```python
# Example: characters/views/vampire/vampire.py

from core.models import CharacterTemplate
from django import forms
from django.contrib import messages
from django.shortcuts import redirect

class CharacterTemplateSelectionForm(forms.Form):
    """Form for selecting optional character template"""

    template = forms.ModelChoiceField(
        queryset=CharacterTemplate.objects.none(),
        required=False,
        empty_label="No template - build from scratch",
        widget=forms.RadioSelect,
        help_text="Select a pre-made character concept to speed up creation",
    )

    def __init__(self, *args, gameline="vtm", character_type="vampire", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["template"].queryset = CharacterTemplate.objects.filter(
            gameline=gameline,
            character_type=character_type,
            is_public=True
        ).order_by("name")
```

#### Step 2: Add Template Selection View

```python
# Example: characters/views/vampire/vampire.py

class VampireTemplateSelectView(LoginRequiredMixin, FormView):
    """Step 0.5: Optional template selection after basics"""

    form_class = CharacterTemplateSelectionForm
    template_name = "characters/vampire/vampire/template_select.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            Vampire, pk=kwargs["pk"], owner=request.user
        )
        # Only allow if creation hasn't started
        if self.object.creation_status > 0:
            return redirect("characters:vampire:vampire_creation", pk=self.object.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["gameline"] = "vtm"
        kwargs["character_type"] = "vampire"
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["character"] = self.object
        context["available_templates"] = CharacterTemplate.objects.filter(
            gameline="vtm", character_type="vampire", is_public=True
        ).order_by("name")
        return context

    def form_valid(self, form):
        template = form.cleaned_data.get("template")
        if template:
            template.apply_to_character(self.object)
            messages.success(
                self.request,
                f"Applied template '{template.name}'. Customize as needed."
            )

        # Proceed to character creation
        self.object.creation_status = 1
        self.object.save()
        return redirect("characters:vampire:vampire_creation", pk=self.object.pk)
```

#### Step 3: Update Basics View

Modify the `get_success_url()` in the Basics view to redirect to template selection:

```python
# Example: characters/views/vampire/vampire.py

class VampireBasicsView(LoginRequiredMixin, FormView):
    # ... existing code ...

    def get_success_url(self):
        # Redirect to template selection instead of detail/creation
        return reverse("characters:vampire:vampire_template", kwargs={"pk": self.object.pk})
```

#### Step 4: Add URLs

```python
# Example: characters/urls/vampire/detail.py

from characters.views.vampire import VampireCharacterCreationView, VampireTemplateSelectView

urls = [
    path(
        "vampire/<int:pk>/template/",
        VampireTemplateSelectView.as_view(),
        name="vampire_template",
    ),
    path(
        "vampire/<int:pk>/creation/",
        VampireCharacterCreationView.as_view(),
        name="vampire_creation",
    ),
    # ... other URLs ...
]
```

#### Step 5: Export View in __init__.py

```python
# Example: characters/views/vampire/__init__.py

from .vampire import (
    VampireBasicsView,
    VampireTemplateSelectView,  # Add this
    VampireCharacterCreationView,
    # ... other exports ...
)
```

#### Step 6: Create Template Selection HTML

Copy and modify `characters/templates/characters/mage/mtahuman/template_select.html`:

```html
<!-- Example: characters/templates/characters/vampire/vampire/template_select.html -->
{% extends "core/base.html" %}
{% load sanitize_text %}

{% block heading %}Character Template Selection{% endblock %}

{% block content %}
<div class="tg-card mb-4" data-gameline="vtm">  <!-- Change gameline here -->
    <div class="tg-card-header">
        <h4 class="tg-card-title vtm_heading">Choose a Starting Template</h4>  <!-- Change heading class -->
        <!-- ... rest same as Mage template ... -->
    </div>
    <!-- ... rest same as Mage template ... -->
</div>
{% endblock %}
```

**Key Changes:**
- `data-gameline="vtm"` (or wta, ctd, wto, dtf)
- Heading class: `vtm_heading`, `wta_heading`, `ctd_heading`, `wto_heading`, `dtf_heading`
- Border color in JavaScript: `var(--vtm-primary)` (or wta, ctd, wto, dtf)

## Template Data Structure

Templates are stored in the `CharacterTemplate` model (inherits from `Model` class) with:

```python
{
    # Inherited from Model class
    "name": "Template Name",
    "description": "Description text",
    "owner": User,  # Who created this template
    "chronicle": Chronicle,  # Optional: chronicle-specific template
    "status": "App",  # Approval status
    "visibility": "PUB",  # Public/Private/Chronicle/Custom
    # Use add_source("Book Name", page_number) method for sources

    # Template-specific fields
    "gameline": "mta",  # vtm, wta, mta, wto, ctd, dtf
    "character_type": "mage",  # vampire, werewolf, etc.
    "concept": "Concept Name",

    # Character Data (JSONFields)
    "basic_info": {
        "nature": "FK:Archetype:Name",  # FK: prefix for foreign keys
        "demeanor": "FK:Archetype:Name",
        "concept": "Concept",
    },
    "attributes": {"strength": 2, "perception": 4, ...},
    "abilities": {"alertness": 2, "investigation": 3, ...},
    "backgrounds": [{"name": "Contacts", "rating": 3}],
    "powers": {"auspex": 2, "celerity": 1},  # Disciplines, spheres, gifts, etc.
    "merits_flaws": [{"name": "Merit Name", "rating": 2}],
    "specialties": ["Ability (Specialty)"],
    "languages": ["English", "Latin"],
    "equipment": "Starting gear description",
    "suggested_freebie_spending": {"disciplines": 5, "willpower": 3},

    # Metadata
    "is_official": True,  # Official WW template vs user-created
    "is_public": True,  # Available to all users
    "times_used": 0,  # Auto-incremented when applied
}
```

## Admin Management

Access at `/admin/core/charactertemplate/`

Features:
- Create/edit templates
- Filter by gameline, character type
- Track usage statistics
- Manage public/private status
- Mark official vs user-created

## Creating Custom Templates

### Via Admin Interface
1. Go to `/admin/core/charactertemplate/`
2. Click "Add Character Template"
3. Fill in basic info and character data (JSON format)
4. Save

### Via Code (for bulk creation)
```python
# populate_db/character_templates/custom_templates.py

from core.models import CharacterTemplate

template = CharacterTemplate.objects.create(
    name="My Custom Template",
    gameline="vtm",
    character_type="vampire",
    description="Custom description",
    # ... character data ...
    is_official=False,  # Mark as user-created
    is_public=True,  # Make available to all
)

# Add sources using the inherited add_source() method
template.add_source("Vampire: The Masquerade", 42)
template.add_source("Guide to the Camarilla", 156)
```

## Template Application Logic

The `CharacterTemplate.apply_to_character()` method:

1. **Resolves Foreign Keys**: `"FK:Model:Name"` → actual object
2. **Sets Attributes**: Directly assigns attribute values
3. **Sets Abilities**: Directly assigns ability ratings
4. **Creates Backgrounds**: Creates BackgroundRating entries
5. **Sets Powers**: Assigns discipline/sphere/gift ratings
6. **Adds Merits/Flaws**: Creates MeritFlawRating entries
7. **Adds Languages**: Links Language objects
8. **Adds Specialties**: Creates Specialty entries
9. **Tracks Application**: Creates TemplateApplication record
10. **Increments Usage**: Updates times_used counter

## Character Creation Flow

**With Templates:**
1. User creates character basics (name, nature, etc.)
2. **→ Template selection page** (optional - can skip)
3. → Character creation wizard (attributes, abilities, etc.)
4. User can still customize all pre-filled values

**Without Templates:**
1. User creates character basics
2. → Directly to creation wizard
3. User fills in everything manually

## File Structure

```
tg/
├── core/
│   ├── models.py                    # CharacterTemplate, TemplateApplication models
│   └── admin.py                     # Admin interface
├── populate_db/
│   └── character_templates/
│       ├── __init__.py              # Load all templates
│       ├── mage_templates.py        # 5 Mage templates
│       ├── vampire_templates.py     # 5 Vampire templates
│       ├── werewolf_templates.py    # 5 Werewolf templates
│       ├── changeling_templates.py  # 5 Changeling templates
│       ├── wraith_templates.py      # 5 Wraith templates
│       └── demon_templates.py       # 5 Demon templates
└── characters/
    ├── views/
    │   └── mage/
    │       └── mtahuman.py          # ✅ Template selection implemented
    ├── urls/
    │   └── mage/
    │       └── detail.py            # ✅ Template/creation URLs added
    └── templates/
        └── characters/
            └── mage/
                └── mtahuman/
                    └── template_select.html  # ✅ Template selection UI
```

## Usage Statistics

Templates track:
- **times_used**: How many times the template has been applied
- **created_at**: When template was created
- **updated_at**: Last modification

View statistics in admin interface.

## Future Enhancements

- [ ] User-created templates (Storyteller-only)
- [ ] Template variations by clan/tribe/tradition
- [ ] Template import/export (JSON)
- [ ] Template voting/ratings
- [ ] NPC quick-creation from templates

## Troubleshooting

### Templates not appearing?
- Run `python populate_db/character_templates/__init__.py`
- Check `is_public=True` in admin
- Verify correct gameline and character_type

### Foreign key errors?
- Ensure Archetypes exist in database
- Check FK format: `"FK:Model:Name"`
- Verify exact name matches

### Template not applying?
- Check character creation_status
- Verify character type matches template
- Check template.apply_to_character() logs

## Support

For issues or questions:
- Check Mage implementation as reference
- Review CLAUDE.md for project conventions
- Test with existing Mage templates first
