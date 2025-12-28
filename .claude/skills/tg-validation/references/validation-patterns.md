# Validation Patterns Reference

Detailed implementation patterns for data validation in the WoD application.

## Transaction Patterns

### XP Spending (Full Implementation)

```python
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

class Character(CharacterModel):
    @transaction.atomic
    def spend_xp(self, trait_name, trait_display, cost, category):
        """
        Atomically spend XP and record the transaction.
        Rolls back entirely if any step fails.
        """
        # Lock row to prevent race conditions
        char = Character.objects.select_for_update().get(pk=self.pk)
        
        if char.xp < cost:
            raise ValidationError(f"Insufficient XP: need {cost}, have {char.xp}")
        
        # Deduct XP
        char.xp -= cost
        
        # Record spending
        record = {
            'index': len(char.spent_xp),
            'trait': trait_display,
            'value': trait_name,
            'cost': cost,
            'category': category,
            'approved': 'Pending',
            'timestamp': timezone.now().isoformat(),
        }
        char.spent_xp.append(record)
        
        char.save(update_fields=['xp', 'spent_xp'])
        return record

    @transaction.atomic
    def approve_xp_spend(self, spend_index, trait_property_name, new_value):
        """Atomically approve XP spend and apply trait increase."""
        char = Character.objects.select_for_update().get(pk=self.pk)
        
        if spend_index >= len(char.spent_xp):
            raise ValidationError("Invalid spend index")
        
        if char.spent_xp[spend_index]['approved'] != 'Pending':
            raise ValidationError("XP spend already processed")
        
        char.spent_xp[spend_index]['approved'] = 'Approved'
        char.spent_xp[spend_index]['approved_at'] = timezone.now().isoformat()
        
        setattr(char, trait_property_name, new_value)
        char.save()
```

### Scene XP Award Transaction

```python
class Scene(models.Model):
    @transaction.atomic
    def award_xp(self, character_awards):
        """
        Atomically award XP to all characters in a scene.
        Either all get XP or none do (rollback on error).
        """
        if self.xp_given:
            raise ValidationError("XP already awarded for this scene")
        
        scene = Scene.objects.select_for_update().get(pk=self.pk)
        
        awarded_chars = []
        for char, should_award in character_awards.items():
            if should_award:
                locked_char = Character.objects.select_for_update().get(pk=char.pk)
                locked_char.xp += 1
                locked_char.save(update_fields=['xp'])
                awarded_chars.append(locked_char.name)
        
        scene.xp_given = True
        scene.xp_awarded_at = timezone.now()
        scene.save(update_fields=['xp_given', 'xp_awarded_at'])
        
        return awarded_chars
```

### Freebie Spending Transaction

```python
class AttributeBlock(models.Model):
    @transaction.atomic
    def spend_freebies_on_attribute(self, attribute_name, cost):
        """Atomically spend freebies and increase attribute."""
        char = type(self).objects.select_for_update().get(pk=self.pk)
        
        if char.freebies < cost:
            raise ValidationError(f"Insufficient freebies: need {cost}, have {char.freebies}")
        
        current_value = getattr(char, attribute_name)
        if current_value >= 5:
            raise ValidationError(f"{attribute_name} is already at maximum")
        
        char.freebies -= cost
        setattr(char, attribute_name, current_value + 1)
        char.save()
```

## Database Constraints

### Character Core Constraints

```python
class Character(CharacterModel):
    class Meta:
        constraints = [
            # XP cannot go negative
            CheckConstraint(
                check=Q(xp__gte=0),
                name='%(app_label)s_%(class)s_xp_non_negative',
                violation_error_message="XP cannot be negative"
            ),
            # Freebies reasonable range
            CheckConstraint(
                check=Q(freebies__gte=-10),
                name='%(app_label)s_%(class)s_freebies_reasonable',
                violation_error_message="Freebies cannot be less than -10"
            ),
            # Valid status values
            CheckConstraint(
                check=Q(status__in=['Un', 'Sub', 'App', 'Ret', 'Dec']),
                name='%(app_label)s_%(class)s_valid_status',
                violation_error_message="Invalid character status"
            ),
        ]
```

### Attribute Range Constraints

```python
class AttributeBlock(models.Model):
    class Meta:
        abstract = True
        constraints = [
            CheckConstraint(
                check=Q(strength__gte=1, strength__lte=10),
                name='%(app_label)s_%(class)s_strength_range',
                violation_error_message="Strength must be between 1 and 10"
            ),
            # Repeat for: dexterity, stamina, charisma, manipulation,
            # appearance, perception, intelligence, wits
        ]
```

### Willpower Constraints (Cross-Field)

```python
class Human(Character):
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(willpower__gte=1, willpower__lte=10),
                name='%(app_label)s_%(class)s_willpower_range'
            ),
            CheckConstraint(
                check=Q(temporary_willpower__gte=0, temporary_willpower__lte=10),
                name='%(app_label)s_%(class)s_temp_willpower_range'
            ),
            # Temporary cannot exceed permanent
            CheckConstraint(
                check=Q(temporary_willpower__lte=models.F('willpower')),
                name='%(app_label)s_%(class)s_temp_not_exceeds_max',
                violation_error_message="Temporary willpower cannot exceed permanent willpower"
            ),
        ]
```

### Uniqueness Constraints

```python
class STRelationship(models.Model):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'chronicle', 'gameline'],
                name='unique_st_per_chronicle_gameline',
                violation_error_message="User is already a storyteller for this gameline"
            ),
        ]

class Character(CharacterModel):
    class Meta:
        constraints = [
            # Unique character names per chronicle (optional)
            UniqueConstraint(
                fields=['name', 'chronicle'],
                condition=Q(chronicle__isnull=False) & ~Q(status='Dec'),
                name='unique_char_name_per_chronicle'
            ),
        ]
```

## Model Validation (clean() Methods)

### Status State Machine

```python
class Character(CharacterModel):
    STATUS_TRANSITIONS = {
        'Un': ['Sub', 'Ret'],
        'Sub': ['Un', 'App', 'Ret'],
        'App': ['Ret', 'Dec'],
        'Ret': ['App'],
        'Dec': [],
    }

    def clean(self):
        super().clean()
        
        if self.pk:
            old_instance = Character.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                self._validate_status_transition(old_instance.status, self.status)

    def _validate_status_transition(self, old_status, new_status):
        valid_transitions = self.STATUS_TRANSITIONS.get(old_status, [])
        if new_status not in valid_transitions:
            raise ValidationError({
                'status': f"Cannot transition from {old_status} to {new_status}. "
                         f"Valid transitions: {', '.join(valid_transitions) or 'none'}"
            })
```

### Age and Date Validation

```python
class Human(Character):
    def clean(self):
        super().clean()
        
        if self.age is not None and self.date_of_birth is not None:
            today = timezone.now().date()
            calculated_age = (today - self.date_of_birth).days // 365
            if abs(calculated_age - self.age) > 1:
                raise ValidationError({
                    'age': f"Age ({self.age}) doesn't match date of birth "
                           f"(calculated: {calculated_age})"
                })
        
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError({
                'date_of_birth': "Date of birth cannot be in the future"
            })
```

### Gameline-Specific Validation (Vampire Generation)

```python
class Vampire(Human):
    GENERATION_LIMITS = {
        3: {'max_trait': 10, 'max_blood_pool': 100},
        4: {'max_trait': 9, 'max_blood_pool': 50},
        5: {'max_trait': 8, 'max_blood_pool': 40},
        13: {'max_trait': 5, 'max_blood_pool': 10},
    }

    def clean(self):
        super().clean()
        
        limits = self.GENERATION_LIMITS.get(self.generation)
        if not limits:
            raise ValidationError({'generation': f"Invalid generation: {self.generation}"})
        
        max_trait = limits['max_trait']
        for attr in ['strength', 'dexterity', 'stamina', 'charisma',
                     'manipulation', 'appearance', 'perception', 'intelligence', 'wits']:
            value = getattr(self, attr)
            if value > max_trait:
                raise ValidationError({
                    attr: f"Generation {self.generation} vampires cannot have "
                          f"{attr} above {max_trait}"
                })
```

## Migration Strategy

### Adding Constraints to Existing Models

**Never add constraints without validating existing data first:**

```python
# migrations/XXXX_add_xp_constraints.py
from django.db import migrations, models
from django.db.models import Q, CheckConstraint

def validate_existing_data(apps, schema_editor):
    """Fix any existing data that violates constraints"""
    Character = apps.get_model('characters', 'Character')
    
    negative_xp = Character.objects.filter(xp__lt=0)
    count = negative_xp.count()
    if count > 0:
        print(f"WARNING: Found {count} characters with negative XP")
        negative_xp.update(xp=0)  # Fix automatically

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(validate_existing_data, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='character',
            constraint=CheckConstraint(
                check=Q(xp__gte=0),
                name='characters_character_xp_non_negative'
            ),
        ),
    ]
```

## Testing Patterns

### Constraint Tests

```python
class TestCharacterConstraints(TestCase):
    def test_xp_cannot_be_negative_db_constraint(self):
        """Database constraint prevents negative XP"""
        character = Character.objects.create(name="Test", xp=10)
        character.xp = -100
        
        with self.assertRaises(IntegrityError):
            character.save()

    def test_xp_cannot_be_negative_model_validation(self):
        """Model validation prevents negative XP"""
        character = Character(name="Test", xp=-100)
        
        with self.assertRaises(ValidationError):
            character.full_clean()
```

### Transaction Tests

```python
class TestXPTransactions(TransactionTestCase):
    def test_xp_spending_is_atomic(self):
        """XP spending rolls back entirely on error"""
        character = Character.objects.create(name="Test", xp=10, strength=3)
        initial_xp = character.xp
        initial_strength = character.strength
        
        with self.assertRaises(ValidationError):
            with transaction.atomic():
                character.xp -= 5
                character.strength += 1
                character.save()
                raise ValidationError("Simulated error")
        
        character.refresh_from_db()
        self.assertEqual(character.xp, initial_xp)
        self.assertEqual(character.strength, initial_strength)
```

### Concurrent Access Tests

```python
from concurrent.futures import ThreadPoolExecutor

class TestConcurrentXP(TransactionTestCase):
    def test_concurrent_xp_spending_no_race_condition(self):
        """Two threads spending XP - one succeeds, one fails"""
        character = Character.objects.create(name="Test", xp=10)
        
        def spend_xp(char_id):
            char = Character.objects.get(pk=char_id)
            try:
                char.spend_xp('alertness', 'Alertness', cost=10, category='abilities')
                return True
            except (ValidationError, IntegrityError):
                return False
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(spend_xp, character.pk),
                executor.submit(spend_xp, character.pk),
            ]
            results = [f.result() for f in futures]
        
        # Exactly one should succeed
        self.assertEqual(sum(results), 1)
        
        character.refresh_from_db()
        self.assertEqual(character.xp, 0)
```
