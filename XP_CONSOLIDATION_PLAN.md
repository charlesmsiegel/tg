# XP Tracking Consolidation Plan

## Overview
Consolidating dual XP tracking systems from JSONField to model-based XPSpendingRequest.

## Current State Analysis

### Files Using Old JSONField System

1. **characters/models/core/character.py** (lines 294-374, 491-530)
   - `spent_xp = models.JSONField(default=list)` (line 117)
   - Methods to remove:
     - `xp_spend_record()` (294-303)
     - `waiting_for_xp_spend()` (305-309)
     - `add_to_spend()` (320-330)
     - `spend_xp()` (332-374) - UPDATE: This atomically handles XP deduction + record creation
     - `approve_xp_spend()` (376-408) - UPDATE: This atomically approves and applies trait changes
   - Compatibility methods to remove (491-530):
     - `has_pending_xp_or_model_requests()`
     - `total_spent_xp_combined()`

2. **characters/views/mage/mage.py** (lines 430-763)
   - MageDetailView uses old system for:
     - Creating XP spend records (lines 430-512)
     - Checking duplicate spends (line 513)
     - Approving XP spends (lines 605-743)
     - Rejecting XP spends (lines 744-762)

3. **Templates** (5 files)
   - `characters/templates/characters/mage/companion/companion_xp_form.html`
   - `characters/templates/characters/mage/mage/mage_xp_form.html`
   - `characters/templates/characters/mage/sorcerer/sorcerer_xp_form.html`
   - `characters/templates/characters/werewolf/garou/detail.html`
   - `characters/templates/characters/werewolf/garou/form.html`

4. **accounts/models.py** (line 286)
   - `Profile.objects_pending_approval()` uses `waiting_for_xp_spend()`

5. **Other character models** (potentially)
   - changeling, demon, vampire, werewolf, wraith models may have similar patterns

### New Model-Based System (Already Implemented)

**game/models.py** (lines 925-975):
- `XPSpendingRequest` model with fields:
  - character, trait_name, trait_type, trait_value, cost
  - approved (Pending/Approved/Denied)
  - created_at, approved_at, approved_by

**character.py** (lines 412-489):
- `create_xp_spending_request()` - CREATE new XP spend request
- `get_pending_xp_requests()` - GET pending requests
- `get_xp_spending_history()` - GET all requests
- `approve_xp_request()` - APPROVE request (sets status only)
- `deny_xp_request()` - DENY request (sets status only)

**Migration Command** (already exists):
- `game/management/commands/migrate_jsonfield_to_models.py`
- Converts JSONField data to XPSpendingRequest records

## Implementation Plan

### Phase 1: Update Character Model Methods

**CRITICAL INSIGHT**: The old `spend_xp()` and `approve_xp_spend()` methods do TWO things:
1. Track the request (in JSONField) - TO BE REPLACED
2. Deduct XP / Apply trait changes - MUST BE PRESERVED

**Action**: Refactor to use new XPSpendingRequest model for tracking while preserving atomic XP handling.

1. **Update `spend_xp()` method** (lines 332-374):
   - Replace JSONField append with `create_xp_spending_request()`
   - Keep atomic XP deduction logic
   - Return XPSpendingRequest instance instead of dict

2. **Update `approve_xp_spend()` method** (lines 376-408):
   - Change signature to accept XPSpendingRequest ID instead of index
   - Use `approve_xp_request()` instead of JSONField manipulation
   - Keep atomic trait application logic

3. **Remove deprecated methods**:
   - `xp_spend_record()` (294-303) - no longer needed
   - `waiting_for_xp_spend()` (305-309) - replace with `get_pending_xp_requests().exists()`
   - `add_to_spend()` (320-330) - replace with `create_xp_spending_request()`

4. **Remove compatibility methods** (491-530):
   - `has_pending_xp_or_model_requests()` → `get_pending_xp_requests().exists()`
   - `total_spent_xp_combined()` → calculate from XPSpendingRequest only

### Phase 2: Update Views

**characters/views/mage/mage.py**:

1. **Update XP spending logic** (lines 430-526):
   - Replace `xp_spend_record()` calls with `create_xp_spending_request()`
   - Replace `spend_xp()` calls with updated method
   - Replace duplicate check `if d not in self.object.spent_xp` with query check

2. **Update approval logic** (lines 605-743):
   - Parse request ID instead of JSONField index
   - Call `approve_xp_request(request_id, request.user)` to update status
   - Keep all trait application logic (background creation, sphere increases, etc.)

3. **Update rejection logic** (lines 744-762):
   - Get XPSpendingRequest by ID
   - Call `deny_xp_request(request_id, request.user)`
   - Refund XP atomically
   - Delete or mark as denied

### Phase 3: Update Templates

Update all templates to iterate over `object.get_xp_spending_history` instead of `object.spent_xp`:

```html
<!-- OLD -->
{% for item in object.spent_xp %}
    {{ item.trait }} - {{ item.cost }} XP - {{ item.approved }}
    <input type="submit" name="{{ item.index }}_approve" value="Approve" />
{% endfor %}

<!-- NEW -->
{% for request in object.get_xp_spending_history %}
    {{ request.trait_name }} - {{ request.cost }} XP - {{ request.approved }}
    <input type="submit" name="xp_request_{{ request.id }}_approve" value="Approve" />
{% endfor %}
```

Files to update:
- `characters/templates/characters/mage/companion/companion_xp_form.html`
- `characters/templates/characters/mage/mage/mage_xp_form.html`
- `characters/templates/characters/mage/sorcerer/sorcerer_xp_form.html`
- `characters/templates/characters/werewolf/garou/detail.html`
- `characters/templates/characters/werewolf/garou/form.html`

### Phase 4: Update accounts/models.py

Replace `waiting_for_xp_spend()` call:

```python
# OLD (line 286)
return [x for x in chars if x.waiting_for_xp_spend()]

# NEW
return Character.objects.filter(
    xp_spendings__approved='Pending'
).distinct()
```

### Phase 5: Remove spent_xp Field

1. **Remove field** from `characters/models/core/character.py` (line 117):
   ```python
   # DELETE THIS LINE
   spent_xp = models.JSONField(default=list)
   ```

2. **Create Django migration**:
   ```bash
   python manage.py makemigrations characters --name remove_spent_xp_field
   ```

   The migration should:
   - Remove `spent_xp` field from Character model
   - Include a data migration check to ensure all data is migrated

### Phase 6: Testing

1. Run existing transaction tests:
   - `characters/tests/core/test_transaction_integration.py`
   - Update tests to verify XPSpendingRequest creation instead of JSONField

2. Run XP/freebie migration tests:
   - `game/tests_xp_freebie_migration.py`

3. Manual testing:
   - Create character
   - Spend XP on various traits
   - Approve/deny as ST
   - Verify XP balance accuracy

## Migration Strategy

1. **Pre-deployment**: Run `python manage.py migrate_jsonfield_to_models` to convert existing data
2. **Deploy code** with new model-based system
3. **Verify** all old JSONField data is in XPSpendingRequest table
4. **Remove field** via migration after verification period

## Files to Modify

### Python Files
1. `characters/models/core/character.py` - Update methods, remove field
2. `characters/views/mage/mage.py` - Update XP spending/approval logic
3. `accounts/models.py` - Update pending approval query
4. Other character model files (changeling, demon, vampire, werewolf, wraith) - Check for similar patterns

### Template Files
1. `characters/templates/characters/mage/companion/companion_xp_form.html`
2. `characters/templates/characters/mage/mage/mage_xp_form.html`
3. `characters/templates/characters/mage/sorcerer/sorcerer_xp_form.html`
4. `characters/templates/characters/werewolf/garou/detail.html`
5. `characters/templates/characters/werewolf/garou/form.html`

### Migration Files
1. New migration to remove `spent_xp` field

## Rollback Plan

If issues arise:
1. Revert code deployment
2. JSONField data remains intact (not deleted, just not updated)
3. Re-run `migrate_jsonfield_to_models` to sync any new records
4. Investigate and fix issues
5. Redeploy

## Success Criteria

- [ ] All XP spending creates XPSpendingRequest records
- [ ] No code references `spent_xp` JSONField
- [ ] All ST approvals update XPSpendingRequest status
- [ ] XP balances remain accurate
- [ ] All existing tests pass
- [ ] Migration successfully removes `spent_xp` field
