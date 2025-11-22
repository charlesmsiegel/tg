# Core App - Model Design Patterns

## Overview

The core app provides base models that implement the polymorphic inheritance pattern used throughout the TG project. This document explains the model architecture and design patterns.

## Base Model: `Model`

The `Model` class is the foundation for all polymorphic models in the project.

```python
from polymorphic.models import PolymorphicModel

class Model(PolymorphicModel):
    """Base polymorphic model for Characters, Items, and Locations."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
```

### Three Main Inheritance Trees

1. **Character** → VtMHuman, Garou, Mage, Wraith, Changeling, Demon
2. **ItemModel** → Gameline-specific items
3. **LocationModel** → Gameline-specific locations

All three extend `core.models.Model` and use Django Polymorphic for type-preserving queries.

## Shared Models

### Book

Represents source books for game content.

```python
class Book(models.Model):
    name = models.CharField(max_length=100)
    gameline = models.CharField(max_length=20, choices=GAMELINE_CHOICES)
    edition = models.IntegerField(default=1)

    class Meta:
        ordering = ['gameline', 'name']
        unique_together = ['name', 'gameline', 'edition']

    def __str__(self):
        return f"{self.name} ({self.gameline})"
```

**Usage:**
- Referenced by game mechanics (Merits, Flaws, Backgrounds, etc.)
- Enables source filtering
- Supports multiple editions

### MeritFlaw

Character advantages and disadvantages shared across all gamelines.

```python
class MeritFlaw(models.Model):
    name = models.CharField(max_length=100)
    ratings = models.JSONField(default=list)
    gameline = models.CharField(max_length=20)
    merit_or_flaw = models.CharField(max_length=1, choices=[('M', 'Merit'), ('F', 'Flaw')])
    allowed_types = models.JSONField(default=list)  # Character types that can take this
    requires = models.JSONField(default=dict)       # Prerequisites

    class Meta:
        ordering = ['name']
```

**Key Features:**
- JSON field for flexible ratings (e.g., [1, 2, 3, 5] for Social Merit)
- Supports prerequisites checking
- Type restrictions (e.g., only Mages can take Avatar merit)

### Specialty

Represents skill specializations (e.g., "Computers: Hacking").

```python
class Specialty(models.Model):
    name = models.CharField(max_length=100)
    ability = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Specialties"
        ordering = ['ability', 'name']

    def __str__(self):
        return f"{self.ability}: {self.name}"
```

### Language

System for character languages.

```python
class Language(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
```

### ArchetypeModel

Base for Natures and Demeanors.

```python
class ArchetypeModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True
        ordering = ['name']
```

**Concrete Implementations:**
- `Nature` - Character's true personality
- `Demeanor` - Character's outward behavior

## Design Patterns

### 1. Polymorphic Queries

Django Polymorphic ensures queries return the correct subclass:

```python
# Returns actual subclass instances, not base Model instances
characters = Character.objects.all()
# → [<VtMHuman>, <Garou>, <Mage>, ...]

# Type-specific queries still work
mages = Mage.objects.filter(tradition="Verbena")
```

### 2. Status Field Pattern

All major models use consistent status tracking:

```python
STATUS_CHOICES = [
    ('Un', 'Unfinished'),
    ('Sub', 'Submitted'),
    ('App', 'Approved'),
    ('Ret', 'Retired'),
    ('Dec', 'Deceased'),
]

class MyModel(Model):
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='Un'
    )
```

### 3. Owner/Chronicle Pattern

Models track ownership and campaign association:

```python
class MyModel(Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_set"
    )
    chronicle = models.ForeignKey(
        'game.Chronicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
```

**Benefits:**
- Permission checking (owner can edit)
- Chronicle-based filtering
- Dynamic related names avoid conflicts

### 4. JSONField for Flexibility

Use JSONField for variable structure data:

```python
class Character(Model):
    # Tracks XP spending with approval status
    spent_xp = models.JSONField(default=dict)
    # Example: {"disciplines": {"Celerity 1": 7, "approved": False}}

    # Flexible trait storage
    merits_and_flaws = models.JSONField(default=dict)
    # Example: {"Iron Will": 3, "Enemy": -2}
```

**When to Use:**
- Variable number of items
- Need for nested structure
- Approval workflows
- Version-specific data

### 5. Abstract Base Classes

For shared behavior without polymorphism:

```python
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MyModel(TimeStampedModel):
    # Inherits timestamp fields
    pass
```

## Model Method Conventions

### Display Methods

```python
def get_absolute_url(self):
    """Return canonical URL for this object."""
    return reverse('myapp:detail', kwargs={'pk': self.pk})

def get_heading(self):
    """Return CSS class for gameline-specific styling."""
    return f"{self.gameline}_heading"

def get_update_url(self):
    """Return URL for editing this object."""
    return reverse('myapp:update', kwargs={'pk': self.pk})
```

### Validation Methods

```python
def is_approved(self):
    """Check if object is approved."""
    return self.status == 'App'

def can_be_edited_by(self, user):
    """Check if user can edit this object."""
    if user.is_superuser:
        return True
    if self.owner == user:
        return True
    return False
```

### Business Logic Methods

```python
def add_xp(self, amount, reason=""):
    """Add XP to character."""
    self.xp += amount
    self.save()

def spend_xp(self, trait, cost):
    """Record XP spending (requires ST approval)."""
    if self.xp < cost:
        raise ValueError("Insufficient XP")

    self.spent_xp[trait] = cost
    self.spent_xp['approved'] = False
    self.save()
```

## Common Model Fields

### Standard Metadata

Every major model should include:

```python
class MyModel(Model):
    # Identity
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # Ownership
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Status
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='Un'
    )

    # Campaign
    chronicle = models.ForeignKey(
        'game.Chronicle',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
```

### Gameline-Specific Fields

```python
class GamelineModel(Model):
    gameline = models.CharField(
        max_length=20,
        choices=[
            ('vtm', 'Vampire: The Masquerade'),
            ('wta', 'Werewolf: The Apocalypse'),
            # ...
        ]
    )
```

## Relationships

### ForeignKey

For many-to-one relationships:

```python
# Character belongs to one Nature
nature = models.ForeignKey(
    'core.Nature',
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
```

### ManyToManyField

For many-to-many relationships:

```python
# Character can have multiple Specialties
specialties = models.ManyToManyField(
    'core.Specialty',
    blank=True,
    related_name='characters'
)
```

### Through Tables

For many-to-many with extra data:

```python
class CharacterMerit(models.Model):
    character = models.ForeignKey('characters.Character', on_delete=models.CASCADE)
    merit = models.ForeignKey('core.MeritFlaw', on_delete=models.CASCADE)
    rating = models.IntegerField()
    notes = models.TextField(blank=True)

class Character(Model):
    merits = models.ManyToManyField(
        'core.MeritFlaw',
        through='CharacterMerit'
    )
```

## Migration Best Practices

### Adding Fields

Always provide defaults for new fields:

```python
# Good
new_field = models.IntegerField(default=0)

# Also good for optional fields
new_field = models.CharField(max_length=100, blank=True, null=True)
```

### Changing Fields

Use multi-step migrations for data preservation:

```python
# Step 1: Add new field
operations = [
    migrations.AddField('MyModel', 'new_field', ...),
]

# Step 2: Migrate data (in separate migration)
def migrate_data(apps, schema_editor):
    MyModel = apps.get_model('core', 'MyModel')
    for obj in MyModel.objects.all():
        obj.new_field = transform(obj.old_field)
        obj.save()

# Step 3: Remove old field
operations = [
    migrations.RemoveField('MyModel', 'old_field'),
]
```

## Performance Considerations

### Query Optimization

```python
# Use select_related for ForeignKey
characters = Character.objects.select_related('nature', 'demeanor')

# Use prefetch_related for ManyToMany
characters = Character.objects.prefetch_related('specialties')

# Combined
characters = Character.objects.select_related(
    'nature', 'demeanor', 'chronicle'
).prefetch_related('specialties', 'merits')
```

### Indexing

Add database indexes for frequently queried fields:

```python
class MyModel(Model):
    name = models.CharField(max_length=100, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'chronicle']),
        ]
```

## Testing Models

### Basic Model Tests

```python
class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            name="Guide to the Traditions",
            gameline="mta"
        )

    def test_create(self):
        """Test model creation."""
        self.assertIsNotNone(self.book.pk)

    def test_str(self):
        """Test string representation."""
        self.assertEqual(
            str(self.book),
            "Guide to the Traditions (mta)"
        )

    def test_unique_constraint(self):
        """Test unique_together constraint."""
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                name="Guide to the Traditions",
                gameline="mta",
                edition=1
            )
```

## Summary

- Use `Model` as base for polymorphic inheritance
- Follow consistent patterns for status, ownership, and chronicles
- Leverage JSONField for flexible data structures
- Provide helpful model methods for common operations
- Optimize queries with select_related/prefetch_related
- Test model creation, validation, and constraints
