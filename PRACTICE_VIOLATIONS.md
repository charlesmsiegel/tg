# Django Best Practice Violations

This document outlines Django best practice violations found in the codebase, organized by severity and category.

## Critical Severity

### 1. Security Configuration Issues

**Location:** `tg/settings.py:27-29`

```python
DEBUG = True
ALLOWED_HOSTS = ["*"]
```

**Problem:** Production-level security settings are insecure:
- `DEBUG = True` exposes sensitive error information
- `ALLOWED_HOSTS = ["*"]` allows any host, enabling HTTP host header attacks

**Solution:**
```python
import os

DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')
```

Create environment-specific settings files:
- `settings/base.py` - shared settings
- `settings/development.py` - DEBUG=True for local
- `settings/production.py` - production security settings

---

### 2. Missing Authentication on Views

**Location:** Multiple views across `game/views.py`, `characters/views/`, `locations/views/`

**Problem:** Critical views lack authentication requirements:
- `ChronicleDetailView` - no login required
- `SceneDetailView` - allows unauthenticated POST operations
- `ChronicleScenesDetailView` - no protection

**Example:** `game/views.py:25`
```python
class ChronicleDetailView(View):
    def get(self, request, *args, **kwargs):
        # No authentication check
        context = self.get_context(kwargs["pk"])
```

**Solution:**
```python
from django.contrib.auth.mixins import LoginRequiredMixin

class ChronicleDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context(kwargs["pk"])
```

---

### 3. No Permission/Authorization Checks

**Location:** Throughout `game/views.py`, `accounts/views.py`

**Problem:** No validation that users have permission to perform actions. Users can:
- Close any scene (not just their own)
- Post as any character
- Approve XP requests without being a storyteller

**Example:** `game/views.py:113-119`
```python
def post(self, request, *args, **kwargs):
    if "close_scene" in request.POST.keys():
        context["object"].close()  # No permission check!
```

**Solution:**
```python
from django.core.exceptions import PermissionDenied

def post(self, request, *args, **kwargs):
    scene = self.get_object()
    if "close_scene" in request.POST.keys():
        if not request.user.profile.is_st() and request.user not in scene.get_participants():
            raise PermissionDenied("You don't have permission to close this scene")
        scene.close()
```

Create a permission mixin:
```python
class StorytellerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.is_st()
```

---

### 4. Using `.get()` Instead of `get_object_or_404()`

**Location:** `game/views.py:27, 76, 87, 121, 134, 250`

**Problem:** Using `.get()` raises `DoesNotExist` exception causing 500 errors instead of proper 404 responses.

**Example:**
```python
chronicle = Chronicle.objects.get(pk=pk)  # Can raise DoesNotExist
scene = Scene.objects.get(pk=pk)  # Can raise DoesNotExist
```

**Solution:**
```python
from django.shortcuts import get_object_or_404

chronicle = get_object_or_404(Chronicle, pk=pk)
scene = get_object_or_404(Scene, pk=pk)
```

---

## High Severity

### 5. N+1 Query Problems

**Location:** Multiple files (see detailed list below)

**Problem:** Code patterns that cause O(n) database queries instead of O(1).

**Examples:**

#### `accounts/models.py:115-121` - st_relations()
```python
def st_relations(self):
    str = STRelationship.objects.filter(user=self.user)
    d = {}
    for chron in Chronicle.objects.all():  # Query 1: all chronicles
        if str.filter(chronicle=chron).count() > 0:  # Query per chronicle!
            d[chron] = str.filter(chronicle=chron)  # Another query!
    return d
```

**Solution:**
```python
def st_relations(self):
    relationships = STRelationship.objects.filter(
        user=self.user
    ).select_related('chronicle', 'gameline')

    d = {}
    for rel in relationships:
        if rel.chronicle not in d:
            d[rel.chronicle] = []
        d[rel.chronicle].append(rel)
    return d
```

#### `game/models.py:117` - storyteller_list()
```python
def storyteller_list(self):
    return ", ".join([x.username for x in self.storytellers.all()])
```

**Solution:** Ensure queryset has `prefetch_related('storytellers')`:
```python
# In view:
chronicle = Chronicle.objects.prefetch_related('storytellers').get(pk=pk)
```

#### `game/models.py:196-205` - weekly_characters()
```python
def weekly_characters(self):
    scenes = self.finished_scenes()
    q = Human.objects.none()
    for scene in scenes:  # Loop through scenes
        q |= scene.characters.filter(npc=False)  # Query per scene!
```

**Solution:**
```python
def weekly_characters(self):
    from characters.models.core.human import Human
    scene_ids = self.finished_scenes().values_list('id', flat=True)
    return Human.objects.filter(
        scenes__id__in=scene_ids,
        npc=False
    ).distinct().order_by('name')
```

#### `accounts/models.py:163-170` - rotes_to_approve()
```python
def rotes_to_approve(self):
    d = {}
    for r in Rote.objects.filter(...):
        d[r] = Mage.objects.filter(rotes__in=[r])  # Query per rote!
    return d
```

**Solution:**
```python
from django.db.models import Prefetch

def rotes_to_approve(self):
    rotes = Rote.objects.filter(
        status__in=["Un", "Sub"],
        chronicle__in=self.user.chronicle_set.all(),
    ).prefetch_related(
        Prefetch('mage_set', queryset=Mage.objects.all())
    ).order_by("name")

    return {r: list(r.mage_set.all()) for r in rotes}
```

---

### 6. Business Logic in Forms

**Location:** `accounts/forms.py`, `game/forms.py`

**Problem:** Forms contain business logic that should be in models or services.

**Example:** `accounts/forms.py:89-96` - SceneXP.save()
```python
def save(self):
    self.scene.xp_given = True
    self.scene.save()
    for char in self.cleaned_data.keys():
        if self.cleaned_data[char]:
            char.xp += 1  # Business logic in form!
            char.save()
```

**Solution:**
Move to model method:
```python
# In Scene model
def award_xp(self, character_awards):
    """Award XP to characters based on dict of {character: bool}"""
    self.xp_given = True
    for char, should_award in character_awards.items():
        if should_award:
            char.add_xp(1)  # Delegate to character model
    self.save()

# In Character model
def add_xp(self, amount):
    self.xp += amount
    self.save()

# In form
def save(self):
    self.scene.award_xp(self.cleaned_data)
```

---

### 7. Fat Models with Complex Inheritance

**Location:** `characters/models/core/`, `accounts/models.py`

**Problem:** Models have too many responsibilities and complex multiple inheritance.

**Example:** Human class inheritance chain:
```python
class Human(HumanUrlBlock, AbilityBlock, MeritFlawBlock, HealthBlock,
            BackgroundBlock, AttributeBlock, Character):
    # 7+ parent classes!
```

**Solution:**
1. Use composition over inheritance where possible
2. Split large models into related models
3. Create service layer for complex operations
4. Consider using Django's proxy models for polymorphic behavior

```python
# Instead of multiple inheritance, use composition:
class Human(Character):
    abilities = models.OneToOneField(AbilitySet, on_delete=models.CASCADE)
    health = models.OneToOneField(HealthTracker, on_delete=models.CASCADE)
    # etc.
```

---

### 8. Signal Registration in models.py

**Location:** `accounts/models.py:264-268`

**Problem:** Signal is registered directly in models.py which can cause import issues.

```python
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
```

**Solution:**
Move to `accounts/apps.py`:
```python
# accounts/apps.py
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Import signals module

# accounts/signals.py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from accounts.models import Profile
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```

---

## Medium Severity

### 9. Missing Database Indexes

**Location:** Throughout models

**Problem:** Foreign keys and frequently queried fields lack indexes.

**Example:** `game/models.py:322-328`
```python
class Post(models.Model):
    character = models.ForeignKey(...)
    scene = models.ForeignKey(...)
    datetime_created = models.DateTimeField(default=now)
    # No index on datetime_created despite ordering by it
```

**Solution:**
```python
class Post(models.Model):
    character = models.ForeignKey(...)
    scene = models.ForeignKey(...)
    datetime_created = models.DateTimeField(default=now, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['-datetime_created']),
            models.Index(fields=['scene', '-datetime_created']),
        ]
```

---

### 10. Lack of Model Validation

**Location:** Most models lack `clean()` methods

**Problem:** Models don't validate data integrity at the model level.

**Example:** `game/models.py:527-549` - WeeklyXPRequest has no validation

**Solution:**
```python
class WeeklyXPRequest(models.Model):
    # ... fields ...

    def clean(self):
        super().clean()
        if self.learning and not self.learning_scene:
            raise ValidationError("Learning scene required when learning is True")
        if self.rp and not self.rp_scene:
            raise ValidationError("RP scene required when rp is True")
        # etc.

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

---

### 11. Typo in Class Name

**Location:** `accounts/forms.py:24`

```python
class CustomUSerCreationForm(UserCreationForm):  # USerCreationForm should be UserCreationForm
```

**Solution:**
```python
class CustomUserCreationForm(UserCreationForm):
```

Update all references accordingly.

---

### 12. Incomplete Test Coverage

**Location:** `accounts/tests.py`, `game/tests.py`, `core/tests.py`

**Problem:** Test files exist but have minimal coverage. Only `accounts/tests.py` has actual tests.

**Solution:**
1. Add comprehensive test suite using pytest-django
2. Test all views, forms, and model methods
3. Add integration tests for workflows
4. Aim for 80%+ coverage

```python
# Example test structure
class TestSceneModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'password')
        self.chronicle = Chronicle.objects.create(name='Test')
        self.location = LocationModel.objects.create(name='Test Location')

    def test_close_scene_sets_finished(self):
        scene = Scene.objects.create(
            name='Test Scene',
            chronicle=self.chronicle,
            location=self.location
        )
        scene.close()
        self.assertTrue(scene.finished)

    def test_add_post_requires_character_in_scene(self):
        # Test that character must be in scene
        pass
```

---

### 13. Using Function-Based Views with Class-Based Logic

**Location:** `game/views.py`

**Problem:** Views inherit from `View` but don't follow proper CBV patterns.

**Example:**
```python
class ChronicleDetailView(View):
    def get_context(self, pk):  # Not standard CBV pattern
        chronicle = Chronicle.objects.get(pk=pk)
        ...
```

**Solution:**
Use proper Django CBV patterns:
```python
from django.views.generic import DetailView

class ChronicleDetailView(LoginRequiredMixin, DetailView):
    model = Chronicle
    template_name = 'game/chronicle/detail.html'
    context_object_name = 'chronicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character_list'] = self.get_characters()
        context['items'] = self.get_items()
        context['form'] = SceneCreationForm(chronicle=self.object)
        return context

    def get_queryset(self):
        return Chronicle.objects.prefetch_related('storytellers', 'allowed_objects')
```

---

### 14. Hardcoded Choices in Models

**Location:** `game/models.py:18-35`, `accounts/models.py:28-48`

**Problem:** Choices are hardcoded multiple times across models.

**Solution:**
Create a constants module:
```python
# core/constants.py
class GameLine:
    WOD = 'wod'
    VTM = 'vtm'
    WTA = 'wta'
    MTA = 'mta'
    WTO = 'wto'
    CTD = 'ctd'

    CHOICES = [
        (WOD, 'World of Darkness'),
        (VTM, 'Vampire: the Masquerade'),
        (WTA, 'Werewolf: the Apocalypse'),
        (MTA, 'Mage: the Ascension'),
        (WTO, 'Wraith: the Oblivion'),
        (CTD, 'Changeling: the Dreaming'),
    ]

# In models:
from core.constants import GameLine

class ObjectType(models.Model):
    gameline = models.CharField(
        max_length=100,
        choices=GameLine.CHOICES,
        default=GameLine.WOD,
    )
```

---

### 15. Missing Migrations Best Practices

**Location:** Not explicitly checked but implied

**Problem:** No evidence of:
- Data migrations for schema changes
- Squashed migrations for production
- Migration testing

**Solution:**
1. Create data migrations for data transformations
2. Squash old migrations periodically
3. Test migrations in CI/CD pipeline
4. Document migration strategy

---

## Low Severity

### 16. Inconsistent Code Style

**Location:** Throughout codebase

**Problems:**
- `str` used as variable name in `accounts/models.py:116` (shadows built-in)
- Inconsistent use of single vs double quotes
- Missing docstrings on complex methods

**Solution:**
```python
# Bad
def st_relations(self):
    str = STRelationship.objects.filter(user=self.user)  # shadows built-in

# Good
def st_relations(self):
    """Get all storyteller relationships organized by chronicle."""
    relationships = STRelationship.objects.filter(user=self.user)
```

Use tools:
- `black` for formatting
- `flake8` or `ruff` for linting
- `mypy` for type checking

---

### 17. No Django Debug Toolbar

**Location:** `tg/settings.py`

**Problem:** No debugging tools configured for development.

**Solution:**
```python
# settings/development.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

---

### 18. No Logging Configuration

**Location:** `tg/settings.py`

**Problem:** No logging configured.

**Solution:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'tg': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

---

### 19. No Custom User Model

**Location:** `accounts/models.py`

**Problem:** Using Django's built-in User model with Profile extension instead of custom User model.

**Solution:** (Note: This is a significant change for an existing project)
For new projects:
```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    preferred_heading = models.CharField(...)
    theme = models.CharField(...)
    # Move Profile fields here

# settings.py
AUTH_USER_MODEL = 'accounts.User'
```

For existing projects, the Profile approach is acceptable but document the trade-offs.

---

### 20. Missing Cache Configuration

**Location:** `tg/settings.py`

**Problem:** No caching configured for performance optimization.

**Solution:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Use caching in views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def chronicle_list(request):
    ...
```

---

## Summary Table

| Issue | Severity | Files Affected | Effort to Fix |
|-------|----------|----------------|---------------|
| Security Settings | Critical | 1 | Low |
| Missing Authentication | Critical | 10+ | Medium |
| Missing Authorization | Critical | 10+ | High |
| get() vs get_object_or_404 | Critical | 6+ | Low |
| N+1 Queries | High | 15+ | Medium |
| Business Logic in Forms | High | 5+ | Medium |
| Fat Models | High | 10+ | High |
| Signal Registration | High | 1 | Low |
| Missing DB Indexes | Medium | 20+ | Low |
| Lack of Model Validation | Medium | 20+ | Medium |
| Class Name Typo | Medium | 1 | Low |
| Test Coverage | Medium | All | High |
| CBV Patterns | Medium | 5+ | Medium |
| Hardcoded Choices | Medium | 10+ | Low |
| Code Style | Low | All | Low |
| No Debug Toolbar | Low | 1 | Low |
| No Logging | Low | 1 | Low |
| No Custom User | Low | 1 | High |
| No Caching | Low | 1 | Medium |

## Priority Recommendations

### Immediate (Security Critical)
1. Fix security settings (DEBUG, ALLOWED_HOSTS)
2. Add authentication to all views
3. Implement authorization checks
4. Replace `.get()` with `get_object_or_404()`

### Short-term (Performance & Reliability)
5. Fix N+1 query issues
6. Add database indexes
7. Move signal registration to apps.py
8. Add model validation

### Medium-term (Maintainability)
9. Refactor business logic out of forms
10. Improve test coverage
11. Standardize CBV patterns
12. Add logging and monitoring

### Long-term (Technical Debt)
13. Address fat model issues
14. Implement proper caching
15. Consider microservices for complex logic
16. Set up CI/CD with code quality checks
