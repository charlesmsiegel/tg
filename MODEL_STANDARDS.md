# MODEL_STANDARDS.md

This document defines the code standards and templates for implementing models, views, forms, templates, and URLs in this project. Following these standards ensures consistency, maintainability, and completeness across all gamelines.

## Table of Contents

1. [Model Standards](#model-standards)
2. [URL Standards](#url-standards)
3. [View Standards](#view-standards)
4. [Form Standards](#form-standards)
5. [Template Standards](#template-standards)
6. [Index Integration Standards](#index-integration-standards)
7. [Complete Implementation Checklist](#complete-implementation-checklist)

---

## Model Standards

### Base Model Inheritance

All polymorphic models should inherit from the appropriate base class:

```python
# Character models
from characters.models.core.character import Character
from characters.models.core.human import Human

class MyGamelineHuman(Human):
    """Base human for this gameline."""
    gameline = "mygameline"

    class Meta:
        verbose_name = "My Gameline Human"
        verbose_name_plural = "My Gameline Humans"

class MyCharacter(MyGamelineHuman):
    """Specific character type for this gameline."""
    type = "my_character"

    class Meta:
        verbose_name = "My Character"
        verbose_name_plural = "My Characters"

# Item models
from items.models.core.item import ItemModel

class MyItem(ItemModel):
    """Item for this gameline."""
    type = "my_item"
    gameline = "mygameline"

    class Meta:
        verbose_name = "My Item"
        verbose_name_plural = "My Items"

# Location models
from locations.models.core.location import LocationModel

class MyLocation(LocationModel):
    """Location for this gameline."""
    type = "my_location"
    gameline = "mygameline"

    class Meta:
        verbose_name = "My Location"
        verbose_name_plural = "My Locations"
```

### Required Model Methods

Every polymorphic model should implement these methods:

```python
class MyModel(BaseModel):
    # Required fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    # Standard methods
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return the canonical URL for this object."""
        return reverse("app:gameline:detail:model_name", kwargs={"pk": self.pk})

    def get_update_url(self):
        """Return the URL to edit this object."""
        return reverse("app:gameline:update:model_name", kwargs={"pk": self.pk})

    def get_heading(self):
        """Return the CSS heading class for gameline styling."""
        return f"{self.gameline}_heading"

    class Meta:
        ordering = ["name"]
        verbose_name = "My Model"
        verbose_name_plural = "My Models"
```

### Reference Model Pattern

For reference/lookup models (factions, clans, disciplines, etc.):

```python
from core.models import Model
from django.db import models
from django.urls import reverse


class MyReferenceModel(Model):
    """
    Reference model for gameline data.

    Inherited from Model:
    - name (CharField, max_length=100)
    - description (TextField)
    - owner, chronicle, status, display
    - sources (M2M to BookReference)
    - public_info, image, st_notes
    """

    type = "my_reference"
    gameline = "mygameline"

    # Add only gameline-specific fields
    nickname = models.CharField(max_length=100, blank=True)
    special_ability = models.TextField(blank=True)

    # FK relationships to other reference models
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        verbose_name = "My Reference"
        verbose_name_plural = "My References"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:mygameline:detail:my_reference", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:mygameline:update:my_reference", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mygameline:create:my_reference")

    def get_heading(self):
        return "mygameline_heading"
```

**Important:** Do NOT redefine fields that are inherited from `Model`:
- `name` - already defined in Model
- `description` - already defined in Model
- `sources` - M2M to BookReference, use `add_source(book_title, page_number)` method

### Through Model Pattern

For M2M relationships with extra data:

```python
class MyRating(models.Model):
    """Through model for character -> reference relationship."""
    character = models.ForeignKey(
        "MyCharacter",
        on_delete=models.CASCADE,
        related_name="my_ratings"
    )
    reference = models.ForeignKey(
        "MyReferenceModel",
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(default=0)
    note = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ["character", "reference"]
        ordering = ["reference__name"]

    def __str__(self):
        return f"{self.character.name} - {self.reference.name} ({self.rating})"
```

---

## URL Standards

### URL Namespace Structure

URLs should follow this namespace hierarchy:

```
app_name:gameline:action:model_type
```

Example: `characters:vampire:detail:vampire`

### Standard URL File Structure

Create separate URL files for each action type:

```
app/urls/
├── __init__.py           # Main router
├── gameline/
│   ├── __init__.py       # Gameline router
│   ├── list.py           # List views
│   ├── detail.py         # Detail views
│   ├── create.py         # Create views
│   ├── update.py         # Update views
│   └── ajax.py           # AJAX endpoints (optional)
```

### URL Pattern Templates

**Main Router (`app/urls/__init__.py`):**

```python
from django.urls import path, include

app_name = "app_name"

urlpatterns = [
    path("index/", IndexView.as_view(), name="index"),
    path("mygameline/", include("app.urls.mygameline", namespace="mygameline")),
]
```

**Gameline Router (`app/urls/mygameline/__init__.py`):**

```python
from django.urls import path, include

app_name = "mygameline"

urlpatterns = [
    path("", include("app.urls.mygameline.list", namespace="list")),
    path("", include("app.urls.mygameline.detail", namespace="detail")),
    path("create/", include("app.urls.mygameline.create", namespace="create")),
    path("update/", include("app.urls.mygameline.update", namespace="update")),
]
```

**List URLs (`list.py`):**

```python
from django.urls import path
from app.views.mygameline.list import (
    MyCharacterListView,
    MyReferenceListView,
)

app_name = "list"

urlpatterns = [
    path("my_character/", MyCharacterListView.as_view(), name="my_character"),
    path("my_reference/", MyReferenceListView.as_view(), name="my_reference"),
]
```

**Detail URLs (`detail.py`):**

```python
from django.urls import path
from app.views.mygameline.detail import (
    MyCharacterDetailView,
    MyReferenceDetailView,
)

app_name = "detail"

urlpatterns = [
    path("my_character/<int:pk>/", MyCharacterDetailView.as_view(), name="my_character"),
    path("my_reference/<int:pk>/", MyReferenceDetailView.as_view(), name="my_reference"),
]
```

**Create URLs (`create.py`):**

```python
from django.urls import path
from app.views.mygameline.create import (
    MyCharacterCreateView,
    MyReferenceCreateView,
)

app_name = "create"

urlpatterns = [
    path("my_character/", MyCharacterCreateView.as_view(), name="my_character"),
    path("my_reference/", MyReferenceCreateView.as_view(), name="my_reference"),
]
```

**Update URLs (`update.py`):**

```python
from django.urls import path
from app.views.mygameline.update import (
    MyCharacterUpdateView,
    MyReferenceUpdateView,
)

app_name = "update"

urlpatterns = [
    path("my_character/<int:pk>/", MyCharacterUpdateView.as_view(), name="my_character"),
    path("my_reference/<int:pk>/", MyReferenceUpdateView.as_view(), name="my_reference"),
]
```

---

## View Standards

### Import Pattern

Always import mixins from `core.mixins`:

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import (
    ViewPermissionMixin,
    EditPermissionMixin,
    MessageMixin,
    VisibilityFilterMixin,
)
```

### ListView Template

```python
class MyCharacterListView(VisibilityFilterMixin, ListView):
    """List view for MyCharacter with visibility filtering."""
    model = MyCharacter
    template_name = "app/mygameline/my_character/list.html"
    context_object_name = "objects"
    paginate_by = 50

    def get_queryset(self):
        """Optimize queryset with select_related and prefetch_related."""
        return (
            super()
            .get_queryset()
            .select_related("owner", "chronicle")
            .prefetch_related("my_ratings__reference")
        )
```

### DetailView Template

```python
class MyCharacterDetailView(ViewPermissionMixin, DetailView):
    """Detail view for MyCharacter with permission checking."""
    model = MyCharacter
    template_name = "app/mygameline/my_character/detail.html"
    context_object_name = "object"

    def get_queryset(self):
        """Optimize queryset with select_related and prefetch_related."""
        return (
            super()
            .get_queryset()
            .select_related("owner", "chronicle", "faction")
            .prefetch_related(
                "my_ratings__reference",
                "merits_and_flaws__meritflaw",
            )
        )

    def get_context_data(self, **kwargs):
        """Add additional context for the template."""
        context = super().get_context_data(**kwargs)
        context["related_items"] = self.object.items.all()
        return context
```

### CreateView Template

```python
class MyCharacterCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    """Create view for MyCharacter with owner assignment."""
    model = MyCharacter
    form_class = MyCharacterCreationForm
    template_name = "app/mygameline/my_character/form.html"
    success_message = "Character '{name}' created successfully!"

    def form_valid(self, form):
        """Assign owner to the new character."""
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Pass user to form for filtering options."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
```

### UpdateView Template

```python
class MyCharacterUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    """Update view for MyCharacter with permission-based form selection."""
    model = MyCharacter
    template_name = "app/mygameline/my_character/form.html"
    success_message = "Character '{name}' updated successfully!"

    def get_form_class(self):
        """Return different forms based on user permissions."""
        if self.request.user.profile.is_st() or self.request.user.is_staff:
            return MyCharacterForm
        return LimitedMyCharacterEditForm

    def get_queryset(self):
        """Optimize queryset."""
        return super().get_queryset().select_related("owner", "chronicle")
```

### Reference Model Views (with caching)

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 15), name="dispatch")
class MyReferenceDetailView(DetailView):
    """Cached detail view for reference data."""
    model = MyReference
    template_name = "app/mygameline/my_reference/detail.html"
```

### Mixin Stacking Order

Always stack mixins in this order (left to right):

```python
# Permission → Message → Base CBV
class MyView(EditPermissionMixin, MessageMixin, UpdateView):
    pass

# Visibility filtering for list views
class MyListView(VisibilityFilterMixin, ListView):
    pass

# Login required for create views
class MyCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    pass

# ST-only views
class MySTView(STRequiredMixin, MessageMixin, CreateView):
    pass
```

---

## Form Standards

### ModelForm Template

```python
from django import forms
from .models import MyCharacter

class MyCharacterCreationForm(forms.ModelForm):
    """Form for creating new characters."""

    class Meta:
        model = MyCharacter
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "chronicle",
            "faction",
            "image",
            "npc",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Enter character name",
                "class": "form-control",
            }),
            "concept": forms.TextInput(attrs={
                "placeholder": "Brief character concept",
                "class": "form-control",
            }),
            "chronicle": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        """Initialize form with user-specific filtering."""
        super().__init__(*args, **kwargs)
        if user:
            # Filter chronicles by user access
            self.fields["chronicle"].queryset = Chronicle.objects.filter(
                models.Q(allowed_users=user) | models.Q(storytellers=user)
            ).distinct()
```

### Limited Edit Form Template

```python
class LimitedMyCharacterEditForm(forms.ModelForm):
    """Limited form for character owners (non-ST users)."""

    class Meta:
        model = MyCharacter
        fields = [
            "notes",
            "description",
            "public_info",
            "image",
            "history",
            "goals",
        ]
        widgets = {
            "description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Physical description...",
            }),
            "history": forms.Textarea(attrs={
                "rows": 6,
                "placeholder": "Character history...",
            }),
            "notes": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Private notes (ST only)...",
            }),
        }
```

### FormSet Template

```python
from django.forms import inlineformset_factory

class BaseMyRatingFormSet(forms.BaseInlineFormSet):
    """Base formset for rating relationships."""

    def __init__(self, *args, character=None, **kwargs):
        self.character = character
        super().__init__(*args, **kwargs)

    def clean(self):
        """Validate formset data."""
        super().clean()
        # Add custom validation here

MyRatingFormSet = inlineformset_factory(
    MyCharacter,
    MyRating,
    form=MyRatingForm,
    formset=BaseMyRatingFormSet,
    extra=3,
    can_delete=True,
)
```

### XP/Freebies Form Template

```python
class MyFreebiesForm(HumanFreebiesForm):
    """Freebies spending form for this character type."""

    CATEGORY_CHOICES = [
        ("attributes", "Attributes"),
        ("abilities", "Abilities"),
        ("backgrounds", "Backgrounds"),
        ("my_power", "My Power"),
        ("willpower", "Willpower"),
        ("merits", "Merits"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize choices based on character state
        self.fields["category"].choices = self.CATEGORY_CHOICES
```

---

## Template Standards

### Directory Structure

```
app/templates/app/
├── index.html                    # Main app index
├── gameline/
│   ├── my_character/
│   │   ├── detail.html           # Detail view
│   │   ├── list.html             # List view
│   │   ├── form.html             # Create/Update form
│   │   ├── chargen.html          # Character generation (if applicable)
│   │   └── display_includes/
│   │       ├── basics.html       # Basic info card
│   │       ├── powers.html       # Powers section
│   │       └── buttons.html      # Action buttons
│   └── my_reference/
│       ├── detail.html
│       └── list.html
```

### Base Template Inheritance

**Character Detail Template:**

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

**Item Detail Template:**

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

**Location Detail Template:**

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

### Display Include Template

**Basics Display Include:**

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

            {% if object.rank %}
            <div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
                <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Rank:</span>
                <span style="font-weight: 700; color: var(--theme-text-primary);">{{ object.rank }}</span>
            </div>
            {% endif %}
        </div>
    </div>
</div>
```

### List Template

```html
{% extends "core/base.html" %}

{% block content %}
<div class="container mt-4">
    <div class="tg-card">
        <div class="tg-card-header d-flex justify-content-between align-items-center">
            <h4 class="tg-card-title mb-0">{{ model_name_plural }}</h4>
            {% if user.profile.is_st %}
            <a href="{% url 'app:gameline:create:model_name' %}" class="btn btn-primary btn-sm">
                Create New
            </a>
            {% endif %}
        </div>
        <div class="tg-card-body">
            <table class="tg-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Owner</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for obj in objects %}
                    <tr>
                        <td><a href="{{ obj.get_absolute_url }}">{{ obj.name }}</a></td>
                        <td>{{ obj.owner.username }}</td>
                        <td><span class="tg-badge badge-{{ obj.status|lower }}">{{ obj.get_status_display }}</span></td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="3" class="text-center">No items found.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    {% if page_obj.has_other_pages %}
    <nav aria-label="Page navigation" class="mt-4">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a>
            </li>
            {% endif %}
            <li class="page-item disabled">
                <span class="page-link">Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
            </li>
            {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}
</div>
{% endblock %}
```

### Form Template

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
                {% if form.name.errors %}
                <div class="text-danger">{{ form.name.errors }}</div>
                {% endif %}
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
    <a href="{% if object %}{{ object.get_absolute_url }}{% else %}{% url 'app:index' %}{% endif %}" class="btn btn-secondary">
        Cancel
    </a>
    <button type="submit" class="btn btn-primary">
        {% if object %}Update{% else %}Create{% endif %}
    </button>
</div>
</form>
{% endblock %}
```

### Gameline Heading Classes

Use these CSS classes for gameline-specific styling:

| Gameline | Class | Color |
|----------|-------|-------|
| Vampire | `vtm_heading` | Dark Red |
| Werewolf | `wta_heading` | Green |
| Mage | `mta_heading` | Purple |
| Wraith | `wto_heading` | Gray |
| Changeling | `ctd_heading` | Teal |
| Demon | `dtf_heading` | Dark Red |
| Mummy | `mtr_heading` | Gold |
| Hunter | `htr_heading` | Orange |

---

## Index Integration Standards

### Adding Models to Index Create Dropdown

**1. Update Character Creation Choices (`characters/forms/core/character.py`):**

```python
CHARACTER_TYPE_CHOICES = {
    "mygameline": [
        ("my_character", "My Character"),
        ("my_other", "My Other Type"),
    ],
}
```

**2. Register Create URL in Index View:**

The index view routes to create URLs based on the form's gameline and type selections.

### Adding List View to Reference Index

**1. Create List URL:**

```python
# characters/urls/mygameline/list.py
path("my_reference/", MyReferenceListView.as_view(), name="my_reference"),
```

**2. Add to Reference Index Template (if applicable):**

```html
<a href="{% url 'characters:mygameline:list:my_reference' %}" class="list-group-item">
    My References
</a>
```

---

## Complete Implementation Checklist

When implementing a new model, ensure all these items are completed:

### Model Layer
- [ ] Model class with proper inheritance
- [ ] Required fields (name, description, gameline, type)
- [ ] `__str__` method
- [ ] `get_absolute_url` method
- [ ] `get_update_url` method
- [ ] `get_heading` method
- [ ] Meta class with verbose_name and ordering
- [ ] Migration created and applied

### URL Layer
- [ ] List URL pattern
- [ ] Detail URL pattern
- [ ] Create URL pattern
- [ ] Update URL pattern
- [ ] Registered in gameline URL router
- [ ] URL names follow convention: `app:gameline:action:model_name`

### View Layer
- [ ] ListView with VisibilityFilterMixin and pagination
- [ ] DetailView with ViewPermissionMixin
- [ ] CreateView with LoginRequiredMixin and MessageMixin
- [ ] UpdateView with EditPermissionMixin and MessageMixin
- [ ] Queryset optimization (select_related, prefetch_related)
- [ ] Limited form selection in UpdateView for owners

### Form Layer
- [ ] Creation form (ModelForm)
- [ ] Limited edit form (for owners)
- [ ] Widget customization
- [ ] User-based queryset filtering
- [ ] Validation methods

### Template Layer
- [ ] Detail template extending appropriate base
- [ ] List template with pagination
- [ ] Form template for create/update
- [ ] Display includes for reusable sections
- [ ] Gameline heading class usage
- [ ] TG card/table classes (not Bootstrap defaults)

### Index Integration
- [ ] Model appears in create dropdown (if applicable)
- [ ] List view accessible from index
- [ ] Proper navigation links

### Testing
- [ ] Model tests
- [ ] View tests (permissions, CRUD)
- [ ] Form tests (validation)
- [ ] URL resolution tests

---

## Quick Reference: File Locations

| Component | Location Pattern |
|-----------|------------------|
| Model | `app/models/gameline/model_name.py` |
| List URL | `app/urls/gameline/list.py` |
| Detail URL | `app/urls/gameline/detail.py` |
| Create URL | `app/urls/gameline/create.py` |
| Update URL | `app/urls/gameline/update.py` |
| Views | `app/views/gameline/{list,detail,create,update}.py` |
| Forms | `app/forms/gameline/model_name.py` |
| Detail Template | `app/templates/app/gameline/model_name/detail.html` |
| List Template | `app/templates/app/gameline/model_name/list.html` |
| Form Template | `app/templates/app/gameline/model_name/form.html` |
| Display Includes | `app/templates/app/gameline/model_name/display_includes/` |
