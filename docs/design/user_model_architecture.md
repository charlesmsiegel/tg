# User Model Architecture Design
## World of Darkness Character Management Application

**Version:** 1.0
**Date:** 2025-11-23
**Status:** Design Documentation - Current Implementation Analysis

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Implementation](#current-implementation)
3. [Alternative: Custom User Model](#alternative-custom-user-model)
4. [Trade-off Analysis](#trade-off-analysis)
5. [Migration Considerations](#migration-considerations)
6. [Recommendations](#recommendations)
7. [References](#references)

---

## Executive Summary

This document analyzes the current User/Profile architecture in the WoD application and documents the trade-offs between using Django's default User model with a OneToOne Profile extension versus implementing a custom User model via `AbstractUser` or `AbstractBaseUser`.

**Current Approach:** Django's default `User` model + `Profile` model with OneToOne relationship

**Key Finding:** For this mature project, the current Profile approach is appropriate and migration would be high-risk with minimal benefit. For new Django projects, `AbstractUser` is strongly preferred.

### Quick Reference

| Aspect | Current (User + Profile) | Custom User (AbstractUser) |
|--------|-------------------------|---------------------------|
| **Migration Risk** | None (already implemented) | Very High - requires full DB migration |
| **Query Complexity** | Higher (requires joins) | Lower (single table) |
| **Flexibility** | Limited by Django User constraints | Full control over user fields |
| **Third-party Compatibility** | Excellent (Django default) | Variable - some packages assume default User |
| **Development Speed** | Fast (established pattern) | Slower (more upfront design) |
| **Best Practice (2024+)** | Legacy approach | Recommended for new projects |

---

## Current Implementation

### Architecture Overview

```python
# accounts/models.py
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="The user this profile belongs to"
    )

    # Theme preferences
    preferred_heading = models.CharField(...)
    theme = models.CharField(...)
    highlight_text = models.BooleanField(...)

    # Social/communication
    discord_id = models.CharField(...)
    discord_toggle = models.BooleanField(...)

    # Safety tools (lines/veils)
    lines = models.TextField(...)
    veils = models.TextField(...)
    lines_toggle = models.BooleanField(...)
    veils_toggle = models.BooleanField(...)
```

### Access Pattern

Throughout the codebase, user profile data is accessed via `user.profile`:

```python
# In views
if request.user.profile.is_st():
    # Show ST controls

# In templates
{{ user.profile.preferred_heading }}
{{ user.profile.theme }}

# In models/managers
characters = Character.objects.owned_by(request.user)
to_approve = request.user.profile.objects_to_approve()
```

### Profile Responsibilities

The Profile model handles:

1. **User Preferences** (90 total usages across codebase)
   - Theme selection (light/dark)
   - Preferred gameline heading style
   - Text highlighting preferences

2. **Storyteller Role Management**
   - `is_st()` - Check if user is an ST for any chronicle
   - `st_relations()` - Get ST relationships by chronicle
   - Cached role lookups via `STRelationship` model

3. **Ownership Queries**
   - `my_characters()`, `my_locations()`, `my_items()`
   - Delegates to manager methods: `Character.objects.owned_by(user)`

4. **Approval Workflows**
   - `objects_to_approve()` - Aggregate pending approvals
   - `characters_to_approve()`, `items_to_approve()`, etc.
   - `freebies_to_approve()`, `*_images_to_approve()`
   - `xp_spend_requests()`, `xp_requests()`

5. **XP/Freebie Request Tracking**
   - `get_unfulfilled_weekly_xp_requests()`
   - `get_unfulfilled_weekly_xp_requests_to_approve()`
   - Complex queries across Character, Week, WeeklyXPRequest models

6. **Social Features**
   - Discord ID storage
   - Lines/veils (safety tools)
   - Visibility toggles for personal information

### Database Schema

```
┌──────────────────┐         ┌──────────────────┐
│   auth_user      │         │  accounts_profile│
├──────────────────┤         ├──────────────────┤
│ id (PK)          │◄───────┤│ user_id (FK)     │
│ username         │  1   1  │ preferred_heading│
│ email            │         │ theme            │
│ password         │         │ discord_id       │
│ first_name       │         │ lines            │
│ last_name        │         │ veils            │
│ is_staff         │         │ ...toggles       │
│ is_active        │         └──────────────────┘
│ date_joined      │
└──────────────────┘
```

### Strengths of Current Approach

1. **Zero Migration Risk**
   - Already deployed and working in production
   - No data migration needed
   - Established patterns throughout codebase

2. **Django Default Compatibility**
   - Works with all Django admin functionality
   - Compatible with all third-party auth packages
   - Well-documented pattern with extensive community support

3. **Separation of Concerns**
   - Core auth fields (username, password) separate from app-specific data
   - Profile can be extended independently
   - Clear boundary between authentication and user preferences

4. **Easy to Understand**
   - Standard Django pattern
   - New developers immediately recognize the structure
   - Extensive documentation and tutorials available

5. **Low Coupling**
   - Profile logic isolated from User model
   - Can modify profile fields without touching authentication
   - Third-party packages that reference User continue to work

### Weaknesses of Current Approach

1. **Query Overhead**
   - Every profile access requires a JOIN
   - 90+ usages of `user.profile` across codebase means 90+ potential JOIN points
   - Example: `request.user.profile.is_st()` = User table + Profile table + STRelationship table (3 queries/joins)

2. **N+1 Query Risks**
   ```python
   # Bad - N+1 queries
   users = User.objects.all()
   for user in users:
       print(user.profile.theme)  # Separate query each iteration

   # Must remember to prefetch
   users = User.objects.select_related('profile').all()
   ```

3. **Verbose Access Pattern**
   - `user.profile.is_st()` instead of `user.is_st()`
   - `user.profile.preferred_heading` instead of `user.preferred_heading`
   - Extra indirection in templates and views

4. **OneToOne Integrity Issues**
   - Must ensure Profile exists for every User
   - Requires signals or migration to create Profiles for existing Users
   - Can break if Profile accidentally deleted

5. **Not Django Best Practice (2024+)**
   - Django documentation recommends custom User for all new projects since 1.5
   - Community consensus has shifted to AbstractUser
   - Risk of eventual deprecation or compatibility issues

---

## Alternative: Custom User Model

### AbstractUser Approach

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model with integrated profile fields."""

    # Theme preferences
    preferred_heading = models.CharField(
        max_length=30,
        choices=...,
        default="wod_heading",
    )
    theme = models.CharField(max_length=100, default="light")
    highlight_text = models.BooleanField(default=True)

    # Social/communication
    discord_id = models.CharField(max_length=100, blank=True, default="")
    discord_toggle = models.BooleanField(default=False)

    # Safety tools
    lines = models.TextField(blank=True, default="")
    veils = models.TextField(blank=True, default="")
    lines_toggle = models.BooleanField(default=False)
    veils_toggle = models.BooleanField(default=False)

    def is_st(self):
        """Check if user is a storyteller for any chronicle."""
        return STRelationship.objects.filter(user=self).exists()

    # ... other Profile methods moved here

# settings.py
AUTH_USER_MODEL = 'accounts.User'
```

### AbstractBaseUser Approach (Maximum Flexibility)

```python
# For projects that need to completely replace username/email behavior
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    """Fully custom user model."""
    email = models.EmailField(unique=True)  # Use email as username
    # Must implement: USERNAME_FIELD, REQUIRED_FIELDS, etc.
    # Much more complex - only if you need to change core auth behavior
```

### Benefits of Custom User

1. **Performance**
   - Single table lookup: `user.is_st()` instead of `user.profile.is_st()`
   - No JOINs needed for user-related data
   - Simpler query optimization

2. **Cleaner API**
   - Direct attribute access: `user.theme` instead of `user.profile.theme`
   - More intuitive for developers
   - Shorter template expressions

3. **Django Best Practice**
   - Recommended by Django docs since version 1.5
   - Future-proof against Django evolution
   - Easier to extend later

4. **Type Safety**
   - No OneToOne.DoesNotExist errors
   - User always has all fields
   - Better IDE autocomplete

5. **Atomic Operations**
   - Single model save() for user changes
   - No transaction coordination between User and Profile
   - Simpler migration scripts

### Drawbacks of Custom User (for this project)

1. **Migration Complexity** ⚠️ CRITICAL
   - Requires custom data migration for all ForeignKey(User) references
   - All tables with user FKs must be updated
   - High risk of data loss if migration fails
   - Downtime required for large databases
   - Cannot be easily reversed

2. **Third-party Compatibility**
   - Some packages hard-code `django.contrib.auth.models.User`
   - Must verify all dependencies support custom User
   - Potential issues with admin extensions, auth packages

3. **Development Effort**
   - Must update 90+ usages of `user.profile.*` across codebase
   - Template changes needed
   - Form updates required
   - Testing overhead significant

4. **Team Knowledge**
   - Current team knows Profile pattern
   - Custom User requires different debugging approaches
   - More complex for new contributors

---

## Trade-off Analysis

### For This Project (Mature, Production)

**Should we migrate to custom User?**

**NO** - The costs far outweigh the benefits:

| Factor | Weight | User+Profile | Custom User | Winner |
|--------|--------|--------------|-------------|---------|
| Migration Risk | HIGH | ✅ No risk | ❌ Very high risk | User+Profile |
| Performance | MEDIUM | ⚠️ Requires JOINs | ✅ Single table | Custom User |
| Code Clarity | LOW | ⚠️ Verbose (.profile) | ✅ Cleaner | Custom User |
| Team Velocity | HIGH | ✅ Known pattern | ❌ Learning curve | User+Profile |
| Maintenance | MEDIUM | ⚠️ Need prefetch_related | ✅ Simpler queries | Custom User |
| Future-proofing | LOW | ⚠️ Old pattern | ✅ Best practice | Custom User |

**Decision: Keep User + Profile**

Rationale:
- Zero migration risk vs. high-risk database migration
- Performance is acceptable (no reported issues)
- Team is productive with current pattern
- Migration would require extensive testing with no critical business benefit

### For New Django Projects

**Should new projects use custom User?**

**YES** - Absolutely, always:

| Factor | Weight | User+Profile | Custom User | Winner |
|--------|--------|--------------|-------------|---------|
| Migration Risk | N/A | ✅ No migration | ✅ No migration | Tie |
| Setup Complexity | LOW | ✅ Simpler initial | ⚠️ More upfront work | User+Profile |
| Long-term Performance | HIGH | ❌ Always requires JOINs | ✅ Optimal | Custom User |
| Best Practice | HIGH | ❌ Legacy approach | ✅ Recommended | Custom User |
| Flexibility | HIGH | ❌ Hard to migrate later | ✅ Easy to extend | Custom User |
| Django Compatibility | HIGH | ⚠️ May deprecate | ✅ Official recommendation | Custom User |

**Decision: Use AbstractUser for New Projects**

Rationale:
- No migration cost (project is new)
- Better long-term performance
- Follows Django best practices
- Easier to extend in future
- Cleaner API for developers

---

## Migration Considerations

### If Migration Is Required (Not Recommended)

**Complexity: VERY HIGH**
**Risk: CRITICAL**
**Recommended: NO**

#### Migration Steps (if absolutely necessary)

1. **Pre-migration Analysis**
   ```bash
   # Find all ForeignKey references to User
   grep -r "ForeignKey.*User" --include="*.py"
   grep -r "OneToOneField.*User" --include="*.py"

   # Expected updates needed:
   # - characters/models/core/character.py - owner field
   # - game/models.py - STRelationship, Scene.participants, etc.
   # - items/models/core/item.py - owner field
   # - locations/models/core/location.py - owner field
   # - Multiple other models with user relationships
   ```

2. **Create Custom User Model**
   - Create `accounts/models.py` with AbstractUser
   - Move all Profile fields to User
   - Move all Profile methods to User
   - Update AUTH_USER_MODEL setting

3. **Generate Migration**
   ```bash
   python manage.py makemigrations accounts
   ```

4. **Custom Data Migration** ⚠️
   - Cannot use automated migration for User model changes
   - Must write custom migration to:
     - Create new user table
     - Copy data from auth_user + accounts_profile
     - Update all foreign key references
     - Preserve user permissions and groups

   ```python
   # This is complex and error-prone
   # Example structure only - DO NOT USE AS-IS
   def migrate_users_forward(apps, schema_editor):
       OldUser = apps.get_model('auth', 'User')
       Profile = apps.get_model('accounts', 'Profile')
       NewUser = apps.get_model('accounts', 'User')

       for old_user in OldUser.objects.all():
           profile = Profile.objects.get(user=old_user)
           # Create new user with merged data
           # Update all ForeignKey references
           # Preserve permissions, groups, etc.
   ```

5. **Update All User References**
   - Change 90+ instances of `user.profile.*` to `user.*`
   - Update all forms
   - Update all templates
   - Update all views
   - Update all tests

6. **Testing Requirements**
   - Full test suite must pass
   - Manual QA of all user workflows
   - Test all authentication flows
   - Test all permission checks
   - Test all approval workflows
   - Test XP/freebie spending
   - Test ST relationship management

7. **Deployment Strategy**
   - Requires database downtime
   - Must backup database before migration
   - Need rollback plan
   - Staging environment mandatory
   - Consider blue-green deployment

#### Estimated Effort

- **Development**: 40-60 hours
- **Testing**: 20-30 hours
- **Documentation**: 10-15 hours
- **Deployment**: 4-8 hours
- **Total**: ~80-115 hours (2-3 weeks full-time)

#### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data loss during migration | MEDIUM | CRITICAL | Full backup, staging testing, rollback plan |
| ForeignKey reference errors | HIGH | HIGH | Comprehensive testing, phased rollback |
| Permission/group loss | MEDIUM | HIGH | Explicit permission preservation in migration |
| Downtime exceeds window | MEDIUM | MEDIUM | Practice migration in staging, optimize |
| Third-party package breaks | LOW | MEDIUM | Audit all dependencies beforehand |
| User session invalidation | HIGH | LOW | Force re-login, communicate to users |

---

## Recommendations

### For Current WoD Project

**Recommendation: Maintain User + Profile Architecture**

**Justification:**
1. Production system is stable
2. No critical performance issues reported
3. Migration risk is very high
4. Development effort is substantial (80-115 hours)
5. Business value is minimal (no new features, minor performance gain)
6. Team is productive with current pattern

**If Performance Becomes an Issue:**

Instead of migrating to custom User, optimize queries:

```python
# Add select_related/prefetch_related to critical views
users = User.objects.select_related('profile').all()

# Cache ST status if checked frequently
from django.core.cache import cache

def is_st_cached(user):
    cache_key = f'user_{user.id}_is_st'
    result = cache.get(cache_key)
    if result is None:
        result = STRelationship.objects.filter(user=user).exists()
        cache.set(cache_key, result, timeout=300)  # 5 min cache
    return result
```

**Documentation Action Items:**
- ✅ Document current architecture (this document)
- ✅ Document trade-offs vs. custom User
- ✅ Document why migration is not recommended
- ✅ Document query optimization strategies
- ✅ Add code comments explaining Profile pattern

### For New Django Projects

**Recommendation: Always Use Custom User Model (AbstractUser)**

**Implementation:**

```python
# accounts/models.py - NEW PROJECT TEMPLATE
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user model - easier to extend later."""
    # Add custom fields from day 1
    pass

# settings.py
AUTH_USER_MODEL = 'accounts.User'
```

**Rationale:**
- Django best practice since 2013 (Django 1.5+)
- No migration cost (project is new)
- Better performance from the start
- Easier to extend later
- Official Django recommendation

**When to Use AbstractBaseUser (Rare):**
- Need email as primary identifier instead of username
- Need to completely change authentication mechanism
- Requires significantly more code - only if truly necessary

---

## References

### Django Documentation

- [Customizing authentication](https://docs.djangoproject.com/en/5.1/topics/auth/customizing/)
- [Substituting a custom User model](https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#substituting-a-custom-user-model)
- [AbstractUser vs AbstractBaseUser](https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)

### Community Best Practices

- [Two Scoops of Django - Custom User Model](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Django Best Practices: Custom User Model](https://learndjango.com/tutorials/django-custom-user-model)
- [When to use AbstractUser vs AbstractBaseUser](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)

### Project-Specific Files

- `accounts/models.py` - Current Profile implementation
- `core/permissions.py` - Permission checks using user.profile
- `docs/design/permissions_system.md` - Permission system architecture
- `CLAUDE.md` - Coding standards and patterns

---

## Appendix: Code Examples

### Current Pattern Usage

```python
# View example
class CharacterDetailView(ViewPermissionMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_st'] = self.request.user.profile.is_st()
        context['theme'] = self.request.user.profile.theme
        return context

# Template example
{% if user.profile.is_st %}
    <div class="st-controls">...</div>
{% endif %}

# Form example
class CharacterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.profile.is_st():
            # Show ST-only fields
            pass
```

### Custom User Pattern (Alternative)

```python
# View example - cleaner access
class CharacterDetailView(ViewPermissionMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_st'] = self.request.user.is_st()
        context['theme'] = self.request.user.theme
        return context

# Template example - shorter
{% if user.is_st %}
    <div class="st-controls">...</div>
{% endif %}

# Form example - direct access
class CharacterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_st():
            # Show ST-only fields
            pass
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-23 | Claude Code | Initial documentation of User/Profile architecture trade-offs |

---

**Status:** Complete
**Next Review:** When considering major architecture changes or Django upgrades
