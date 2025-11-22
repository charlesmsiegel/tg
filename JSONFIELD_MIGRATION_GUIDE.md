# JSONField to Model Migration Guide

## Overview

This guide documents the migration from JSONField-based XP and freebie tracking to proper Django model instances.

## Problem

The previous implementation used JSONFields for tracking XP and freebie spending:
- `Character.spent_xp` (JSONField) - tracked XP expenditures
- `Human.spent_freebies` (JSONField) - tracked freebie point usage

**Issues with JSONField approach:**
1. Cannot efficiently query JSONField contents
2. Entire JSON loaded into memory on every access
3. Index-based updates are fragile and error-prone
4. No database-level referential integrity
5. Difficult to add features like approval tracking, timestamps, etc.

## Solution

Two new models replace the JSONField usage:

###  `XPSpendingRequest` Model

Located in: `game/models.py`

**Fields:**
- `character` - ForeignKey to CharacterModel
- `trait_name` - Display name (e.g., "Alertness")
- `trait_type` - Category (e.g., "ability", "attribute")
- `trait_value` - New value after spending
- `cost` - XP cost
- `approved` - Status: Pending/Approved/Denied
- `created_at` - Timestamp
- `approved_at` - When approved/denied
- `approved_by` - User who approved

**Indexed Fields:**
- `(character, approved)` - Fast queries for pending requests
- `(character, created_at)` - Chronological history

### `FreebieSpendingRecord` Model

Located in: `game/models.py`

**Fields:**
- `character` - ForeignKey to CharacterModel
- `trait_name` - Display name
- `trait_type` - Category
- `trait_value` - Value gained
- `cost` - Freebie cost
- `created_at` - Timestamp

**Indexed Fields:**
- `(character, created_at)` - Chronological history

## Migration Steps

### 1. Run Migrations

```bash
python manage.py migrate game
```

This creates the new `XPSpendingRequest` and `FreebieSpendingRecord` tables.

### 2. Migrate Existing Data

```bash
# Dry run first to preview changes
python manage.py migrate_jsonfield_to_models --dry-run

# Actually migrate the data
python manage.py migrate_jsonfield_to_models
```

This converts all existing JSONField data to model instances. It:
- Migrates `spent_xp` records to `XPSpendingRequest` instances
- Migrates `spent_freebies` records to `FreebieSpendingRecord` instances
- Skips duplicates if the command is run multiple times

### 3. Update Code to Use New Models

#### For XP Spending (in views/forms):

**Old way (deprecated):**
```python
# Creating XP spend record
record = character.xp_spend_record(trait, trait_type, value, cost)
character.spent_xp.append(record)
character.save()

# Checking for pending XP
for d in character.spent_xp:
    if d["approved"] == "Pending":
        # ...

# Approving XP (fragile index-based update)
index = character.spent_xp.index(d)
character.spent_xp[index]["approved"] = "Approved"
character.save()
```

**New way:**
```python
# Creating XP spend request
request = character.create_xp_spending_request(
    trait_name="Alertness",
    trait_type="ability",
    trait_value=3,
    cost=6
)

# Checking for pending XP
pending_requests = character.get_pending_xp_requests()

# Approving XP
character.approve_xp_request(request.id, approver=request.user)
```

#### For Freebie Spending (in views/forms):

**Old way (deprecated):**
```python
# Creating freebie record
record = character.freebie_spend_record(trait, trait_type, value, cost)
character.spent_freebies.append(record)
character.save()

# Calculating total
total = character.freebies + sum([x["cost"] for x in character.spent_freebies])
```

**New way:**
```python
# Creating freebie record
record = character.create_freebie_spending_record(
    trait_name="Strength",
    trait_type="attribute",
    trait_value=4,
    cost=5
)

# Calculating total
total = character.total_freebies_from_model()

# Getting history
history = character.get_freebie_spending_history()
```

### 4. Update Templates

**Old way:**
```django
{% for xp_spend in character.spent_xp %}
    <li>{{ xp_spend.trait }}: {{ xp_spend.cost }} XP ({{ xp_spend.approved }})</li>
{% endfor %}
```

**New way:**
```django
{% for request in character.get_xp_spending_history %}
    <li>{{ request.trait_name }}: {{ request.cost }} XP ({{ request.approved }})</li>
{% endfor %}
```

### 5. Eventually Remove JSONFields

After all code is updated and tested, you can:

1. Add a final data verification step
2. Remove the `spent_xp` and `spent_freebies` fields from models
3. Create a migration to drop those columns

## Benefits of New Approach

1. **Queryable**: Can efficiently find all pending requests across all characters
   ```python
   pending = XPSpendingRequest.objects.filter(approved='Pending')
   ```

2. **Indexed**: Fast lookups by character, approval status, date
   ```python
   recent = character.xp_spendings.filter(created_at__gte=last_week)
   ```

3. **Atomic**: No race conditions from index-based updates

4. **Extensible**: Easy to add new fields like:
   - Denial reason
   - Notes from storyteller
   - XP type (weekly, story, etc.)

5. **Reportable**: Can generate analytics:
   ```python
   XPSpendingRequest.objects.values('trait_type').annotate(total=Sum('cost'))
   ```

## Backward Compatibility

During the transition period:
- Both JSONField and model-based methods work
- Old JSONField methods are marked as deprecated
- Data exists in both places until migration is complete

Once fully migrated:
- Remove JSONField columns
- Remove deprecated methods
- Update all views/templates to use new methods

## Files Modified

- `game/models.py` - Added XPSpendingRequest and FreebieSpendingRecord models
- `game/migrations/0001_add_xp_freebie_spending_models.py` - Database migration
- `game/management/commands/migrate_jsonfield_to_models.py` - Data migration command
- `characters/models/core/character.py` - Added new XP spending methods
- `characters/models/core/human.py` - Added new freebie spending methods
- `core/models.py` - Fixed missing ModelManager and ModelQuerySet definitions
- `core/admin.py` - Commented out references to unimplemented models

## Testing

After migration, verify:

1. All existing XP/freebie records are preserved
2. New requests can be created
3. Approval workflow works
4. Queries are performant
5. Templates display correctly

## Rollback Plan

If issues arise:
1. Keep JSONField columns during transition
2. Can regenerate JSONField data from models if needed:
   ```python
   for char in Character.objects.all():
       char.spent_xp = list(char.xp_spendings.values(
           'trait_name', 'cost', 'approved', ...
       ))
       char.save()
   ```
