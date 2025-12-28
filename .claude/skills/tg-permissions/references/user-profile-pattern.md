# User + Profile Pattern

This project uses Django's default `User` model with a `Profile` model extension.

## Architecture

```
┌──────────────────┐         ┌──────────────────┐
│   auth_user      │         │  accounts_profile│
├──────────────────┤         ├──────────────────┤
│ id (PK)          │◄───────┤│ user_id (FK)     │
│ username         │  1   1  │ preferred_heading│
│ email            │         │ theme            │
│ password         │         │ discord_id       │
│ is_staff         │         │ lines, veils     │
│ is_active        │         │ ...toggles       │
└──────────────────┘         └──────────────────┘
```

## Access Pattern

```python
# In views
if request.user.profile.is_st():
    # Show ST controls

# In templates
{{ user.profile.preferred_heading }}
{{ user.profile.theme }}

# Ownership queries
characters = request.user.profile.my_characters()
to_approve = request.user.profile.objects_to_approve()
```

## Profile Responsibilities

### 1. User Preferences
- Theme selection (light/dark)
- Preferred gameline heading style
- Text highlighting preferences

### 2. Storyteller Role Management
- `is_st()` - Check if user is ST for any chronicle
- `st_relations()` - Get ST relationships by chronicle
- Uses `STRelationship` model for caching

### 3. Ownership Queries
- `my_characters()`, `my_locations()`, `my_items()`
- Delegates to manager methods

### 4. Approval Workflows
- `objects_to_approve()` - Aggregate pending approvals
- `characters_to_approve()`, `items_to_approve()`, etc.
- `xp_spend_requests()`, `xp_requests()`

### 5. Social Features
- Discord ID storage
- Lines/veils (safety tools)
- Visibility toggles

## Why User + Profile (Not Custom User)

**Decision: Keep User + Profile for this project**

### Reasons
1. **Zero migration risk** - Already deployed and working
2. **Django compatibility** - Works with all admin/auth packages
3. **Team familiarity** - Established patterns throughout codebase
4. **Migration cost** - Would require 80-115 hours of work

### Trade-offs Accepted
- Query overhead (requires JOINs for `user.profile.*`)
- Verbose access pattern (`user.profile.is_st()` vs `user.is_st()`)
- Must use `select_related('profile')` to avoid N+1 queries

## Performance Optimization

### Always Prefetch Profile

```python
# BAD - N+1 queries
users = User.objects.all()
for user in users:
    print(user.profile.theme)

# GOOD - Single query
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.theme)
```

### Cache ST Status

```python
from django.core.cache import cache

def is_st_cached(user):
    cache_key = f'user_{user.id}_is_st'
    result = cache.get(cache_key)
    if result is None:
        result = STRelationship.objects.filter(user=user).exists()
        cache.set(cache_key, result, timeout=300)
    return result
```

## For New Django Projects

**Recommendation: Use `AbstractUser` instead**

```python
# For NEW projects only
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    theme = models.CharField(max_length=100, default="light")
    # ... other fields

# settings.py
AUTH_USER_MODEL = 'accounts.User'
```

Benefits for new projects:
- Better performance (no JOINs)
- Cleaner API (`user.theme` vs `user.profile.theme`)
- Django best practice since 2013
