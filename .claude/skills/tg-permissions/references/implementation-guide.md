# Permissions Implementation Guide

Detailed implementation patterns for the WoD permission system.

## PermissionManager Implementation

```python
# core/permissions.py
from typing import Set
from enum import Enum
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class Role(Enum):
    OWNER = "owner"
    ADMIN = "admin"
    CHRONICLE_HEAD_ST = "chronicle_head_st"
    GAME_ST = "game_st"
    PLAYER = "player"
    OBSERVER = "observer"
    AUTHENTICATED = "authenticated"
    ANONYMOUS = "anonymous"

class VisibilityTier(Enum):
    FULL = "full"
    PARTIAL = "partial"
    NONE = "none"

class Permission(Enum):
    VIEW_FULL = "view_full"
    VIEW_PARTIAL = "view_partial"
    EDIT_FULL = "edit_full"
    EDIT_LIMITED = "edit_limited"
    SPEND_XP = "spend_xp"
    SPEND_FREEBIES = "spend_freebies"
    DELETE = "delete"
    APPROVE = "approve"
    MANAGE_OBSERVERS = "manage_observers"

class PermissionManager:
    ROLE_PERMISSIONS = {
        Role.OWNER: {
            Permission.VIEW_FULL, Permission.VIEW_PARTIAL,
            Permission.EDIT_LIMITED,  # Notes/journals only
            Permission.SPEND_XP, Permission.SPEND_FREEBIES,
            Permission.DELETE, Permission.MANAGE_OBSERVERS,
        },
        Role.ADMIN: {
            Permission.VIEW_FULL, Permission.VIEW_PARTIAL,
            Permission.EDIT_FULL, Permission.EDIT_LIMITED,
            Permission.SPEND_XP, Permission.SPEND_FREEBIES,
            Permission.DELETE, Permission.APPROVE, Permission.MANAGE_OBSERVERS,
        },
        Role.CHRONICLE_HEAD_ST: {
            Permission.VIEW_FULL, Permission.VIEW_PARTIAL,
            Permission.EDIT_FULL, Permission.EDIT_LIMITED,
            Permission.SPEND_XP, Permission.SPEND_FREEBIES,
            Permission.DELETE, Permission.APPROVE, Permission.MANAGE_OBSERVERS,
        },
        Role.GAME_ST: {
            Permission.VIEW_FULL, Permission.VIEW_PARTIAL,
            # No edit permissions - read-only
        },
        Role.PLAYER: {Permission.VIEW_PARTIAL},
        Role.OBSERVER: {Permission.VIEW_PARTIAL},
        Role.AUTHENTICATED: set(),
        Role.ANONYMOUS: set(),
    }

    @staticmethod
    def get_user_roles(user: User, obj) -> Set[Role]:
        roles = set()
        
        if not user.is_authenticated:
            roles.add(Role.ANONYMOUS)
            return roles
        
        roles.add(Role.AUTHENTICATED)
        
        if user.is_superuser or user.is_staff:
            roles.add(Role.ADMIN)
        
        # Owner check
        if hasattr(obj, 'owner') and obj.owner == user:
            roles.add(Role.OWNER)
        elif hasattr(obj, 'user') and obj.user == user:
            roles.add(Role.OWNER)
        
        # Chronicle ST checks
        if hasattr(obj, 'chronicle') and obj.chronicle:
            if hasattr(obj.chronicle, 'head_st') and obj.chronicle.head_st == user:
                roles.add(Role.CHRONICLE_HEAD_ST)
            if hasattr(obj.chronicle, 'game_storytellers'):
                if obj.chronicle.game_storytellers.filter(id=user.id).exists():
                    roles.add(Role.GAME_ST)
            if user.characters.filter(chronicle=obj.chronicle).exists():
                roles.add(Role.PLAYER)
        
        # Observer check
        if hasattr(obj, 'observers'):
            ct = ContentType.objects.get_for_model(obj)
            from core.models import Observer
            if Observer.objects.filter(content_type=ct, object_id=obj.id, user=user).exists():
                roles.add(Role.OBSERVER)
        
        return roles
```

## Query Optimization

### Preventing N+1 Queries

```python
# BAD - N+1 queries
for character in Character.objects.all():
    if character.user_can_view(request.user):  # Queries each time
        print(character.name)

# GOOD - Prefetch related data
characters = Character.objects.select_related(
    'owner', 'chronicle'
).prefetch_related(
    'chronicle__storytellers',
    'observers'
)
```

### Optimized Queryset Filtering

```python
@staticmethod
def filter_queryset_for_user(user: User, queryset):
    from django.db.models import Q, Exists, OuterRef
    
    if not user.is_authenticated:
        return queryset.filter(visibility='PUB')
    
    if user.is_superuser or user.is_staff:
        return queryset.select_related('owner', 'chronicle')
    
    model_class = queryset.model
    ct = ContentType.objects.get_for_model(model_class)
    
    # Subquery for observer check
    observer_subquery = Observer.objects.filter(
        content_type=ct,
        object_id=OuterRef('pk'),
        user=user
    )
    
    filters = Q()
    
    if hasattr(model_class, 'owner'):
        filters |= Q(owner=user)
    
    if hasattr(model_class, 'chronicle'):
        filters |= Q(chronicle__storytellers=user)
        filters |= Q(chronicle__game_storytellers=user)
    
    filters |= Q(Exists(observer_subquery))
    
    return queryset.filter(filters).select_related(
        'owner', 'chronicle'
    ).distinct()
```

## View Integration Patterns

### Class-Based View Mixin

```python
# core/mixins.py
class PermissionRequiredMixin:
    required_permission = None
    raise_404_on_deny = True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            if self.raise_404_on_deny:
                raise Http404("Object not found")
            else:
                raise PermissionDenied("Insufficient permissions")
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        obj = self.get_object()
        return PermissionManager.user_has_permission(
            self.request.user, obj, self.required_permission
        )

class ViewPermissionMixin(PermissionRequiredMixin):
    required_permission = Permission.VIEW_FULL
    raise_404_on_deny = True

class EditPermissionMixin(PermissionRequiredMixin):
    required_permission = Permission.EDIT_FULL
    raise_404_on_deny = False
```

### View Pattern Examples

```python
# DetailView with permissions
class CharacterDetailView(ViewPermissionMixin, VisibilityFilterMixin, DetailView):
    model = Character
    template_name = 'characters/character/detail.html'

# ListView with filtering
class CharacterListView(VisibilityFilterMixin, ListView):
    model = Character
    # get_queryset() automatically filtered

# UpdateView with permissions
class CharacterUpdateView(EditPermissionMixin, UpdateView):
    model = Character
    
    def get_form_class(self):
        # Owner gets limited form, ST gets full form
        if self.request.user.profile.is_st():
            return CharacterForm
        return LimitedCharacterEditForm
```

## Template Integration

### Template Tags

```python
# core/templatetags/permissions.py
from django import template
from core.permissions import PermissionManager, VisibilityTier

register = template.Library()

@register.simple_tag(takes_context=True)
def visibility_tier(context, obj):
    user = context['request'].user
    return obj.get_visibility_tier(user)

@register.filter
def is_full(tier):
    return tier == VisibilityTier.FULL
```

### Template Usage

```html
{% load permissions %}

{% visibility_tier object as tier %}

{% if tier|is_full %}
    {# Show complete character sheet #}
    <div class="tg-card">
        <h6>Private Notes</h6>
        {{ object.notes|sanitize_html }}
    </div>
    <div class="tg-card">
        <h6>Experience Points</h6>
        <p>Total XP: {{ object.xp }}</p>
    </div>
{% elif tier|is_partial %}
    {# Show limited info #}
    <div class="tg-card">
        <h6>Public Information</h6>
        <p>Name: {{ object.name }}</p>
        <p>Concept: {{ object.concept }}</p>
    </div>
{% endif %}

{% if user_can_edit object %}
    <a href="{% url 'characters:update' object.pk %}">Edit</a>
{% endif %}
```

## Status-Based Restrictions

```python
@staticmethod
def _check_status_restrictions(user, obj, permission, roles):
    status = obj.status
    
    # Deceased: read-only except for admin/head ST
    if status == 'Dec':
        if permission in [Permission.EDIT_FULL, Permission.EDIT_LIMITED,
                        Permission.DELETE, Permission.SPEND_XP]:
            return (Role.ADMIN in roles or Role.CHRONICLE_HEAD_ST in roles)
    
    # Submitted: owner has no permissions
    if status == 'Sub':
        if permission in [Permission.EDIT_LIMITED, Permission.SPEND_XP,
                        Permission.SPEND_FREEBIES]:
            if Role.OWNER in roles:
                return False
    
    # Unfinished: freebies only, no XP
    if status == 'Un':
        if permission == Permission.SPEND_XP and Role.OWNER in roles:
            return False
    
    # Approved: XP only, no freebies
    if status == 'App':
        if permission == Permission.SPEND_FREEBIES and Role.OWNER in roles:
            return False
    
    return True
```

## Database Indexes

```python
class Migration(migrations.Migration):
    operations = [
        migrations.AddIndex(
            model_name='character',
            index=models.Index(fields=['chronicle'], name='char_chronicle_idx'),
        ),
        migrations.AddIndex(
            model_name='character',
            index=models.Index(fields=['owner'], name='char_owner_idx'),
        ),
        migrations.AddIndex(
            model_name='character',
            index=models.Index(fields=['status', 'chronicle'], name='char_status_chron_idx'),
        ),
    ]
```
