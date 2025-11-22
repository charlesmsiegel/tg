# View and Template Migration Guide

## Overview

This guide explains how to migrate views and templates from the deprecated JSONField approach to the new model-based XP/freebie tracking system.

## Migration Strategy

Due to the complexity of existing views (especially `characters/views/mage/mage.py`), we recommend a **gradual migration** approach using a dual-system strategy.

### Phase 1: Dual System Support (Current)

Both JSONField and model-based systems run in parallel:
- **New** XP/freebie requests use the model system
- **Existing** pending requests in JSONField remain until approved/rejected
- Helper methods support querying both systems

### Phase 2: Migrate Existing Data

Run the migration command to convert existing JSONField data:
```bash
python manage.py migrate_jsonfield_to_models
```

### Phase 3: Update Views Gradually

Update views one at a time, starting with simpler ones.

### Phase 4: Deprecate JSONField

Once all pending requests are cleared and views are updated, remove JSONField columns.

## Helper Methods (Already Implemented)

### Character Model

**Dual-system queries:**
```python
# Check if character has any pending XP (either system)
if character.has_pending_xp_or_model_requests():
    ...

# Get total spent XP (both systems combined)
total_spent = character.total_spent_xp_combined()
```

**New model-based methods:**
```python
# Create XP request
request = character.create_xp_spending_request(
    trait_name="Alertness",
    trait_type="ability",
    trait_value=3,
    cost=6
)

# Query pending requests
pending = character.get_pending_xp_requests()

# Get all XP history
history = character.get_xp_spending_history()

# Approve/deny
character.approve_xp_request(request_id, approver=request.user)
character.deny_xp_request(request_id, approver=request.user)
```

### Human Model

```python
# Create freebie record
record = human.create_freebie_spending_record(
    trait_name="Strength",
    trait_type="attribute",
    trait_value=4,
    cost=5
)

# Get history
history = human.get_freebie_spending_history()

# Calculate total (model-based only)
total = human.total_freebies_from_model()
```

## Template Migration Examples

### Example 1: Display Total Spent XP

**Old way (displays raw JSONField):**
```django
<div class="col-sm-3">{{ object.spent_xp }}</div>
```

**New way (uses combined helper):**
```django
<div class="col-sm-3">{{ object.total_spent_xp_combined }}</div>
```

**Updated in:** `characters/templates/characters/werewolf/garou/detail.html:260`

### Example 2: List Freebie Spending History

**Old way (JSONField only):**
```django
{% for item in object.spent_freebies %}
    <div class="row">
        <div class="col-sm">{{ item.trait }} {{ item.value }}</div>
        <div class="col-sm">{{ item.cost }} freebies</div>
    </div>
{% endfor %}
```

**Dual-system way (shows both):**
```django
<!-- Legacy JSONField entries -->
{% for item in object.spent_freebies %}
    <div class="row">
        <div class="col-sm">{{ item.trait }} {{ item.value }}</div>
        <div class="col-sm">{{ item.cost }} freebies</div>
    </div>
{% endfor %}

<!-- New model-based entries -->
{% for record in object.get_freebie_spending_history %}
    <div class="row">
        <div class="col-sm">{{ record.trait_name }} {{ record.trait_value }}</div>
        <div class="col-sm">{{ record.cost }} freebies</div>
    </div>
{% endfor %}
```

**Updated in:** `characters/templates/characters/changeling/changeling/freebies_form.html:78-83`

### Example 3: XP Approval Form (Complex - Not Yet Updated)

This is the most complex case. See `MAGE_VIEW_MIGRATION_STRATEGY.md` for detailed approach.

**Current JSONField approach:**
```django
{% for xp_spend in character.spent_xp %}
    {% if xp_spend.approved == "Pending" %}
        <button name="{{ xp_spend.index }}_approve" value="Approve">Approve</button>
    {% endif %}
{% endfor %}
```

**Recommended new approach:**
```django
{% for request in character.get_pending_xp_requests %}
    <div class="xp-request">
        <span>{{ request.trait_name }}: {{ request.cost }} XP</span>
        <button name="approve_{{ request.id }}" value="Approve">Approve</button>
        <button name="deny_{{ request.id }}" value="Deny">Deny</button>
    </div>
{% endfor %}
```

## View Migration Patterns

### Pattern 1: Simple Display (Easy)

**Old:**
```python
context['spent_xp'] = character.spent_xp
```

**New:**
```python
context['xp_history'] = character.get_xp_spending_history()
context['total_spent'] = character.total_spent_xp_combined()
```

### Pattern 2: Creating XP Request (Medium)

**Old:**
```python
record = character.xp_spend_record(trait, trait_type, value, cost)
character.spent_xp.append(record)
character.save()
```

**New:**
```python
request = character.create_xp_spending_request(
    trait_name=trait_display,
    trait_type=trait_type,
    trait_value=new_value,
    cost=cost
)
```

### Pattern 3: Approval Flow (Complex)

**Old (fragile index-based update):**
```python
# Get index from form
index = "_".join(xp_index.split("_")[:-1])
d = [x for x in character.spent_xp if x["index"] == index][0]
i = character.spent_xp.index(d)

# Update JSONField
character.spent_xp[i]["approved"] = "Approved"
character.save()
```

**New (database-backed):**
```python
# Get request ID from form
request_id = int(form.data.get('approve_request_id'))

# Approve using helper method
character.approve_xp_request(request_id, approver=request.user)
```

## Files Requiring Updates

### High Priority (Simple Display)

1. **Character Detail Templates**
   - ✅ `characters/templates/characters/werewolf/garou/detail.html:260` - UPDATED
   - Similar templates in other gamelines (vampire, changeling, etc.)

2. **Freebie Forms**
   - ✅ `characters/templates/characters/changeling/changeling/freebies_form.html:78` - UPDATED
   - Other freebie form templates (20+ files)

### Medium Priority (Form Handling)

3. **Freebie View Logic**
   - `characters/views/core/human.py` (HumanFreebiesView)
   - Update to use `create_freebie_spending_record()`

### Low Priority (Complex Refactoring)

4. **XP Approval Views**
   - `characters/views/mage/mage.py:500-760` - Complex approval logic
   - `characters/views/mage/companion.py` - Similar pattern
   - `characters/views/mage/sorcerer.py` - Similar pattern

5. **XP Approval Templates**
   - `characters/templates/characters/mage/mage/mage_xp_form.html`
   - `characters/templates/characters/mage/companion/companion_xp_form.html`
   - `characters/templates/characters/mage/sorcerer/sorcerer_xp_form.html`

See `MAGE_VIEW_MIGRATION_STRATEGY.md` for detailed strategy on complex views.

## Testing Checklist

After updating each view/template:

- [ ] Display of XP/freebie history works correctly
- [ ] Total spent calculations are accurate
- [ ] New requests are created properly
- [ ] Approval workflow functions (if applicable)
- [ ] Both JSONField and model data display during transition
- [ ] No regressions in existing functionality

## Rollback Plan

If issues occur:

1. **Keep JSONField columns** - Don't drop them yet
2. **Regenerate JSONField from models if needed:**
   ```python
   for char in Character.objects.all():
       char.spent_xp = list(
           char.xp_spendings.values(
               'trait_name', 'cost', 'approved', 'created_at'
           )
       )
       char.save()
   ```
3. **Revert template changes** - Templates can be easily reverted
4. **Keep both systems running** - No need to rush migration

## Current Status

### ✅ Completed
- Models created (XPSpendingRequest, FreebieSpendingRecord)
- Database migrations created
- Data migration command created
- Helper methods added to Character/Human models
- Two template examples updated

### ⚠️ In Progress
- Documenting migration strategy
- Creating examples for different patterns

### ❌ Not Started
- Complex view refactoring (mage XP approval)
- Bulk template updates
- Testing with real data
- JSONField removal

## Recommendations

1. **Start with display-only templates** - Lowest risk
2. **Update freebie forms next** - Medium complexity
3. **Tackle XP approval views last** - Highest complexity
4. **Test thoroughly at each step** - Don't batch all changes
5. **Keep JSONField during transition** - Safety net
6. **Use dual-system helpers** - Smooth migration
7. **Consider feature flag** - Toggle between systems if needed

## Next Steps

1. Update remaining display templates (character details)
2. Update freebie form views to use new models
3. Create helper function for XP approval migration
4. Gradually refactor complex approval views
5. Run comprehensive tests
6. Remove JSONField when safe

## Questions?

See also:
- `JSONFIELD_MIGRATION_GUIDE.md` - Overall migration guide
- `MAGE_VIEW_MIGRATION_STRATEGY.md` - Complex view strategy
- `JSONFIELD_REMOVAL_SUMMARY.md` - Implementation summary
