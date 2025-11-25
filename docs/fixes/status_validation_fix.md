# Status Validation Redundancy Fix

## Problem

Status validation was happening in three places with contradictory behavior:

1. **Django field choices** - Soft validation at the ORM level
2. **Model `clean()` method** - Redundant validation of status values AND transition logic
3. **Model `save()` method** - Called `full_clean()` but swallowed `ValidationError` exceptions

This created confusion:
- Validation would run but wouldn't actually prevent invalid saves
- Multiple validation layers doing the same work
- No clear opt-out mechanism for bulk operations or migrations

## Solution

### 1. Added Database Constraint (Strict Validation)

**Migration**: `characters/migrations/0001_initial.py`
```python
CheckConstraint(
    check=Q(status__in=['Un', 'Sub', 'App', 'Ret', 'Dec']),
    name='characters_character_valid_status',
    violation_error_message="Status must be one of: Un, Sub, App, Ret, Dec",
)
```

**Model**: `characters/models/core/character.py` Meta class
- Added constraint directly to model definition
- Ensures database-level enforcement

### 2. Removed Try/Except in save()

**Before**:
```python
def save(self, *args, **kwargs):
    if not kwargs.pop("skip_validation", False):
        try:
            self.full_clean()
        except ValidationError:
            # Swallowed the error - confusing!
            pass
```

**After**:
```python
def save(self, *args, **kwargs):
    """
    Save the character.

    Args:
        skip_validation: If True, skip model validation (full_clean). Use with caution.

    Raises:
        ValidationError: If validation fails (unless skip_validation=True)
    """
    if not kwargs.pop("skip_validation", False):
        self.full_clean()  # Now properly raises ValidationError
```

### 3. Removed Redundant Status Value Validation from clean()

**Before**:
```python
def clean(self):
    # Validate status is in valid choices
    valid_statuses = ["Un", "Sub", "App", "Ret", "Dec"]
    if self.status not in valid_statuses:
        raise ValidationError(...)

    # Validate status transition
    if self.pk:
        ...
```

**After**:
```python
def clean(self):
    """
    Validate character data before saving.

    Status value validation is handled by:
    - Django field choices (soft validation)
    - Database constraint (hard validation via migration)

    This method focuses on:
    - Status transition validation (state machine logic)
    - XP balance validation
    """
    # Only validate status transitions (business logic)
    if self.pk:
        ...
```

## Validation Strategy

The final validation strategy is **strict with clear opt-out**:

### Normal Operation (Strict)
```python
character.status = "App"
character.save()  # Raises ValidationError if transition invalid
```

### Bulk Operations (Opt-out)
```python
# For migrations or bulk operations
character.save(skip_validation=True)  # Bypasses full_clean()
# Database constraint still enforces valid values
```

## Validation Layers

Now validation happens at the right levels:

1. **Field Choices** - Soft validation, developer convenience
2. **Model `clean()`** - Business logic (status transitions, XP checks)
3. **Database Constraint** - Hard enforcement (valid status values, XP >= 0)

## Testing

All existing tests pass:
- `test_valid_status_values_db_constraint` - Database rejects invalid status
- `test_status_transition_valid` - Valid transitions allowed
- `test_status_transition_invalid` - Invalid transitions blocked
- `test_status_transition_deceased_is_final` - Deceased is final state

## Migration Notes

If database already exists:
```bash
python manage.py migrate characters 0001_initial
```

This adds the constraint without requiring data changes (assuming all existing data is valid).
