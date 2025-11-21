# Applying Permissions to Existing Views - Guide

This guide shows how to update existing views to use the new permissions system.

## Views Updated

✅ **characters/views/core/character.py** - Complete example implementation

## Pattern for Updating Other Views

### Before (Old Pattern with SpecialUserMixin)

```python
from core.views.approved_user_mixin import SpecialUserMixin

class MyDetailView(SpecialUserMixin, DetailView):
    model = MyModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_approved_user"] = self.check_if_special_user(
            self.object, self.request.user
        )
        return context
```

### After (New Pattern with Permission Mixins)

```python
from core.mixins import ViewPermissionMixin, EditPermissionMixin, VisibilityFilterMixin
from core.permissions import Permission, PermissionManager

class MyDetailView(ViewPermissionMixin, DetailView):
    """
    ViewPermissionMixin automatically:
    - Checks if user can view
    - Returns 404 if no permission (security)
    - Adds visibility_tier to context
    - Adds user_can_edit to context
    """
    model = MyModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # visibility_tier and user_can_edit already in context!
        # Backward compatibility:
        context["is_approved_user"] = context.get("user_can_edit", False)
        return context
```

## View Type Examples

### 1. Detail Views (Show Individual Object)

```python
from core.mixins import ViewPermissionMixin

class CharacterDetailView(ViewPermissionMixin, DetailView):
    model = Character
    template_name = "path/to/template.html"
    # That's it! Permission checking is automatic
```

### 2. Update Views (Edit Object)

```python
from core.mixins import EditPermissionMixin

class CharacterUpdateView(EditPermissionMixin, UpdateView):
    model = Character
    fields = "__all__"  # Or specific fields
    template_name = "path/to/form.html"
    # Automatically checks EDIT_FULL permission
    # Returns 403 if user doesn't have permission
```

### 3. List Views (Show Multiple Objects)

```python
from core.mixins import VisibilityFilterMixin

class CharacterListView(VisibilityFilterMixin, ListView):
    model = Character
    template_name = "path/to/list.html"
    # Automatically filters to only viewable objects!
    # Players see only approved characters in their chronicles
    # STs see all characters in their chronicles
    # Owners see their own characters
```

### 4. Create Views

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class CharacterCreateView(LoginRequiredMixin, CreateView):
    model = Character
    fields = "__all__"

    def form_valid(self, form):
        # Automatically set owner to current user
        if not form.instance.owner:
            form.instance.owner = self.request.user
        return super().form_valid(form)
```

### 5. Views with Different Permissions Based on Role

```python
from core.mixins import EditPermissionMixin
from core.permissions import Permission, PermissionManager

class CharacterUpdateView(EditPermissionMixin, UpdateView):
    model = Character
    template_name = "path/to/form.html"

    def get_form_class(self):
        """Return different forms for owners vs STs."""
        has_full_edit = PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        )

        if has_full_edit:
            # STs get full form
            from .forms import FullCharacterForm
            return FullCharacterForm
        else:
            # Owners get limited form
            from .forms import LimitedCharacterForm
            return LimitedCharacterForm
```

## Creating Limited Forms for Owners

Owners should NOT be able to directly edit stats. Create a limited form:

```python
# characters/forms.py

from django import forms
from characters.models import Character

class LimitedCharacterForm(forms.ModelForm):
    """
    Form for character owners.
    Can only edit notes, description, goals, etc.
    Cannot edit stats directly - must use XP spending.
    """
    class Meta:
        model = Character
        fields = [
            'name',
            'description',
            'notes',
            'goals',
            'history',
            'public_info',
            # DO NOT include: strength, dexterity, abilities, etc.
        ]

class FullCharacterForm(forms.ModelForm):
    """
    Form for Chronicle Head STs and Admins.
    Can edit everything including stats.
    """
    class Meta:
        model = Character
        fields = '__all__'
```

Then use it in your view:

```python
class CharacterUpdateView(EditPermissionMixin, UpdateView):
    model = Character
    template_name = "characters/form.html"

    def get_form_class(self):
        if PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        ):
            return FullCharacterForm
        else:
            return LimitedCharacterForm
```

## XP Spending Views

Create separate views for XP spending:

```python
from core.mixins import SpendXPPermissionMixin

class CharacterSpendXPView(SpendXPPermissionMixin, UpdateView):
    """
    View for spending XP on character improvements.
    Only owners of approved characters can access this.
    """
    model = Character
    template_name = "characters/spend_xp.html"
    form_class = SpendXPForm

    # Permission check is automatic via SpendXPPermissionMixin
```

## Freebie Spending Views

```python
from core.mixins import SpendFreebiesPermissionMixin

class CharacterSpendFreebiesView(SpendFreebiesPermissionMixin, UpdateView):
    """
    View for spending freebie points during character creation.
    Only owners of unfinished characters can access this.
    """
    model = Character
    template_name = "characters/spend_freebies.html"
    form_class = SpendFreebiesForm
```

## Template Updates

### In Detail Templates

```django
{% load permissions %}

{# Check visibility tier #}
{% visibility_tier object as tier %}

{% if tier|is_full %}
    {# Show everything - owner/ST/admin view #}
    <h2>Character Sheet - Full Access</h2>

    <div class="stats">
        <p>XP: {{ object.xp }}</p>
        <p>Spent XP: {{ object.spent_xp }}</p>
        <p>Notes: {{ object.notes }}</p>
    </div>

    {% if user_can_edit object %}
        <a href="{% url 'characters:update' object.pk %}">Edit Character</a>
    {% endif %}

    {% if user_can_spend_xp object %}
        <a href="{% url 'characters:spend_xp' object.pk %}">Spend XP</a>
    {% endif %}

{% elif tier|is_partial %}
    {# Show public info only - player view #}
    <h2>Character Sheet - Public View</h2>

    <div class="public-info">
        <p>Name: {{ object.name }}</p>
        <p>Concept: {{ object.concept }}</p>
        {# Only show public information #}
    </div>

{% else %}
    {# Should not happen if permissions work correctly #}
    <p>You don't have permission to view this character.</p>
{% endif %}
```

### In List Templates

```django
{% load permissions %}

<h1>Characters</h1>

{# List is already filtered by VisibilityFilterMixin #}
{% for character in characters %}
    <div class="character-card">
        <h3>{{ character.name }}</h3>

        {# Check visibility for this specific character #}
        {% visibility_tier character as tier %}

        {% if tier|is_full %}
            <span class="badge">Full Access</span>
            <p>Status: {{ character.get_status_display }}</p>
            <p>XP: {{ character.xp }}</p>
        {% elif tier|is_partial %}
            <span class="badge">Public View</span>
            <p>{{ character.concept }}</p>
        {% endif %}

        <a href="{% url 'characters:detail' character.pk %}">View</a>

        {% if user_can_edit character %}
            <a href="{% url 'characters:update' character.pk %}">Edit</a>
        {% endif %}
    </div>
{% empty %}
    <p>No characters found.</p>
{% endfor %}
```

## Files That Need Updating

To complete the migration, update these view files:

### Characters
- ✅ `characters/views/core/character.py` - DONE
- `characters/views/core/human.py`
- `characters/views/vampire/*.py`
- `characters/views/werewolf/*.py`
- `characters/views/mage/*.py`
- `characters/views/wraith/*.py`
- `characters/views/changeling/*.py`
- `characters/views/demon/*.py`

### Items
- `items/views/core/*.py`
- `items/views/{gameline}/*.py`

### Locations
- `locations/views/core/*.py`
- `locations/views/{gameline}/*.py`

### Game
- `game/views.py` - Chronicle, Scene, etc.

## Testing Your Changes

After updating a view:

1. Test as **Owner**:
   - Can view own character
   - Can edit limited fields
   - Can spend XP (if approved)
   - Cannot edit stats directly
   - Cannot see other characters

2. Test as **Chronicle Head ST**:
   - Can view all characters in chronicle
   - Can edit everything
   - Can approve characters
   - Can modify stats directly

3. Test as **Game ST**:
   - Can view all characters in chronicle
   - Cannot edit characters
   - Read-only access

4. Test as **Player**:
   - Can view own character (full)
   - Can view others (partial - public info only)
   - Cannot edit others' characters

5. Test as **Stranger** (different chronicle):
   - Cannot see characters at all
   - Gets 404 on detail views

## Migration Checklist

For each view file you update:

- [ ] Replace `SpecialUserMixin` with appropriate permission mixin
- [ ] Update `get_context_data` to remove `check_if_special_user` calls
- [ ] Add `from core.mixins import ...` imports
- [ ] Add `from core.permissions import Permission, PermissionManager` if needed
- [ ] Update templates to use `{% load permissions %}` tags
- [ ] Create limited forms for owner editing
- [ ] Test all permission scenarios
- [ ] Update corresponding tests

## Common Pitfalls

1. **Don't forget to load permissions template tag**: `{% load permissions %}`
2. **Use the right mixin**:
   - `ViewPermissionMixin` for detail views
   - `EditPermissionMixin` for update views
   - `VisibilityFilterMixin` for list views
3. **Remember backward compatibility**: Keep `is_approved_user` in context for existing templates
4. **Create separate XP/freebie spending views**: Don't try to edit stats in the main update view
5. **Filter querysets**: Use `VisibilityFilterMixin` on list views to auto-filter

## Example: Complete View File After Migration

```python
# characters/views/vampire/vtmhuman.py (example)

from characters.models.vampire import VtMHuman
from core.mixins import (
    ViewPermissionMixin,
    EditPermissionMixin,
    VisibilityFilterMixin,
    SpendXPPermissionMixin
)
from core.permissions import Permission, PermissionManager
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class VtMHumanDetailView(ViewPermissionMixin, DetailView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/detail.html"

class VtMHumanListView(VisibilityFilterMixin, ListView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/list.html"

class VtMHumanUpdateView(EditPermissionMixin, UpdateView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/form.html"

    def get_form_class(self):
        if PermissionManager.user_has_permission(
            self.request.user, self.get_object(), Permission.EDIT_FULL
        ):
            from .forms import FullVtMHumanForm
            return FullVtMHumanForm
        else:
            from .forms import LimitedVtMHumanForm
            return LimitedVtMHumanForm

class VtMHumanSpendXPView(SpendXPPermissionMixin, UpdateView):
    model = VtMHuman
    template_name = "characters/vampire/vtmhuman/spend_xp.html"
    form_class = VtMHumanSpendXPForm
```

## Next Steps

1. Update remaining character views (follow pattern from character.py)
2. Create limited forms for each character type
3. Create XP spending views
4. Update templates to use visibility tiers
5. Test thoroughly with different user roles
6. Run migrations
7. Deploy!
