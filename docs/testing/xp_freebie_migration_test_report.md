# XP/Freebie Migration Testing Report

## Overview

This document provides comprehensive testing guidance for the XP/Freebie migration from JSONField to model-based tracking.

**Migration Status:** In Progress (Dual-system support active)

**Testing Checklist** (from VIEW_TEMPLATE_MIGRATION_GUIDE.md):
- [ ] Display of XP/freebie history works correctly
- [ ] Total spent calculations are accurate
- [ ] New requests are created properly
- [ ] Approval workflow functions (if applicable)
- [ ] Both JSONField and model data display during transition
- [ ] No regressions in existing functionality

## Test Files Created

### Automated Tests
- **File:** `game/tests_xp_freebie_migration.py`
- **Coverage:**
  - XPSpendingRequest model CRUD operations
  - FreebieSpendingRecord model CRUD operations
  - Dual-system support (JSONField + Model)
  - Approval/denial workflows
  - Total spent calculations
  - Database indexes and performance
  - Edge cases and backward compatibility
- **Total Test Cases:** 30+

## Running the Tests

### Setup Environment
```bash
# Create virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate
```

### Run All Migration Tests
```bash
# Run all XP/freebie migration tests
pytest game/tests_xp_freebie_migration.py -v

# Run with coverage report
pytest game/tests_xp_freebie_migration.py -v --cov=game --cov-report=html

# Run specific test class
pytest game/tests_xp_freebie_migration.py::TestXPSpendingRequest -v

# Run specific test
pytest game/tests_xp_freebie_migration.py::TestXPSpendingRequest::test_create_xp_spending_request -v
```

### Run Related Tests
```bash
# Run existing XP transaction tests
pytest characters/tests/core/test_validation_constraints.py::TestXPTransactions -v

# Run all game tests
pytest game/tests.py game/tests_integration.py -v
```

## Manual Testing Guide

### Prerequisites
1. Access to Django admin panel
2. Test user account with character(s)
3. Storyteller account for approval workflows

### Test Scenario 1: Creating XP Spending Requests

**Purpose:** Verify new XP spending requests are created correctly

**Steps:**
1. Create a character with XP > 0
2. Use the Python shell:
   ```python
   from characters.models.core.character import Character
   from django.contrib.auth.models import User

   user = User.objects.first()
   char = Character.objects.filter(owner=user).first()

   # Create XP spending request
   request = char.create_xp_spending_request(
       trait_name="Alertness",
       trait_type="ability",
       trait_value=3,
       cost=6
   )

   print(f"Created request: {request}")
   print(f"Status: {request.approved}")
   print(f"Created at: {request.created_at}")
   ```

**Expected Results:**
- Request is created successfully
- Status is "Pending"
- `created_at` timestamp is set
- Request appears in `char.xp_spendings.all()`

**Verification:**
```python
# Check pending requests
pending = char.get_pending_xp_requests()
print(f"Pending requests: {pending.count()}")

# Check full history
history = char.get_xp_spending_history()
print(f"Total history: {history.count()}")
```

### Test Scenario 2: Approving XP Requests

**Purpose:** Verify XP request approval workflow

**Steps:**
1. Create a pending XP request (see Scenario 1)
2. Approve it:
   ```python
   from django.contrib.auth.models import User

   st_user = User.objects.get(username='st_username')  # ST account

   # Get pending request
   request = char.get_pending_xp_requests().first()
   print(f"Request to approve: {request}")

   # Approve it
   approved_request = char.approve_xp_request(request.id, st_user)

   print(f"Approved: {approved_request.approved}")
   print(f"Approved by: {approved_request.approved_by}")
   print(f"Approved at: {approved_request.approved_at}")
   ```

**Expected Results:**
- Request status changes to "Approved"
- `approved_by` is set to ST user
- `approved_at` timestamp is set
- Request no longer appears in `get_pending_xp_requests()`

**Verification:**
```python
# Check it's no longer pending
assert char.get_pending_xp_requests().count() == 0

# Check it appears in history
assert char.get_xp_spending_history().filter(approved='Approved').count() > 0
```

### Test Scenario 3: Dual-System Total Calculation

**Purpose:** Verify total XP spent is calculated correctly from both systems

**Steps:**
1. Add XP spending to JSONField:
   ```python
   char.spent_xp = [
       {
           "trait": "Strength",
           "value": 4,
           "cost": 8,
           "approved": "Approved",
           "index": "0",
       },
       {
           "trait": "Dexterity",
           "value": 3,
           "cost": 6,
           "approved": "Approved",
           "index": "1",
       }
   ]
   char.save()
   ```

2. Add XP spending via model:
   ```python
   request = char.create_xp_spending_request("Alertness", "ability", 3, 4)
   char.approve_xp_request(request.id, st_user)
   ```

3. Calculate total:
   ```python
   total = char.total_spent_xp_combined()
   print(f"Total spent XP (combined): {total}")
   ```

**Expected Results:**
- Total should be: 8 + 6 + 4 = 18
- Only approved requests count
- Both systems are included

**Verification:**
```python
# Verify JSONField contribution
jsonfield_total = sum(x['cost'] for x in char.spent_xp if x.get('approved') == 'Approved')
print(f"JSONField total: {jsonfield_total}")  # Should be 14

# Verify model contribution
from django.db.models import Sum
model_total = char.xp_spendings.filter(approved='Approved').aggregate(Sum('cost'))['cost__sum'] or 0
print(f"Model total: {model_total}")  # Should be 4

# Combined should match
assert total == jsonfield_total + model_total
```

### Test Scenario 4: Freebie Spending Records

**Purpose:** Verify freebie spending records are created and tracked correctly

**Steps:**
1. Create a Human character:
   ```python
   from characters.models.core.human import Human

   human = Human.objects.filter(owner=user).first()
   print(f"Starting freebies: {human.freebies}")
   ```

2. Create freebie spending records:
   ```python
   record1 = human.create_freebie_spending_record(
       trait_name="Strength",
       trait_type="attribute",
       trait_value=4,
       cost=5
   )

   record2 = human.create_freebie_spending_record(
       trait_name="Alertness",
       trait_type="ability",
       trait_value=2,
       cost=2
   )

   print(f"Record 1: {record1}")
   print(f"Record 2: {record2}")
   ```

3. Calculate total:
   ```python
   total = human.total_freebies_from_model()
   print(f"Total freebies: {total}")
   ```

**Expected Results:**
- Records are created with all fields populated
- Total equals starting freebies + sum of costs
- Records appear in history

**Verification:**
```python
history = human.get_freebie_spending_history()
print(f"Freebie history count: {history.count()}")  # Should be 2

expected_total = human.freebies + 5 + 2
assert total == expected_total
```

### Test Scenario 5: Migration Command

**Purpose:** Verify data migration from JSONField to models

**Steps:**
1. Create character with JSONField data:
   ```python
   char.spent_xp = [
       {
           "trait": "Wits",
           "value": 4,
           "cost": 8,
           "approved": "Approved",
           "index": "0",
       }
   ]
   char.save()
   ```

2. Run migration command (dry-run first):
   ```bash
   python manage.py migrate_jsonfield_to_models --dry-run
   ```

3. Run actual migration:
   ```bash
   python manage.py migrate_jsonfield_to_models
   ```

4. Verify migration:
   ```python
   # Check that model records were created
   migrated = char.xp_spendings.filter(trait_name="Wits", cost=8).exists()
   print(f"Migration successful: {migrated}")
   ```

**Expected Results:**
- Dry run shows what would be migrated
- Actual migration creates XPSpendingRequest records
- JSONField data is preserved
- No duplicates are created on repeated runs

### Test Scenario 6: Template Display

**Purpose:** Verify XP/freebie data displays correctly in templates

**Steps:**
1. Visit character detail page
2. Check XP section displays:
   - Total XP spent (from both systems)
   - Pending requests (from both systems)
   - XP history

**Expected Results:**
- Both JSONField and model data are visible
- Totals are accurate
- No duplicate entries

**Files to Check:**
- Character detail templates
- XP approval templates
- Freebie forms

## Test Coverage Summary

### Unit Tests (Automated)

| Test Class | Test Count | Coverage |
|------------|-----------|----------|
| TestXPSpendingRequest | 7 | Create, read, approve, deny, pending checks |
| TestFreebieSpendingRecord | 4 | Create, read, calculate totals |
| TestDualSystemSupport | 7 | JSONField + Model integration |
| TestXPSpendingIndexes | 2 | Database index usage |
| TestFreebieSpendingIndexes | 2 | Database index usage |
| TestMigrationEdgeCases | 5 | Error handling, edge cases |
| TestBackwardCompatibility | 2 | JSONField still works |
| **Total** | **29** | **Comprehensive** |

### Integration Tests (Manual)

| Scenario | Status | Notes |
|----------|--------|-------|
| Creating XP requests | ⚠️ Needs testing | Use Python shell |
| Approving XP requests | ⚠️ Needs testing | Requires ST account |
| Dual-system totals | ⚠️ Needs testing | Critical for migration |
| Freebie records | ⚠️ Needs testing | Similar to XP |
| Migration command | ⚠️ Needs testing | Test with real data |
| Template display | ⚠️ Needs testing | UI/UX verification |

## Known Issues and Limitations

### Current State
1. **Dual-system is active** - Both JSONField and model systems are in use
2. **JSONField still required** - Cannot be removed until migration complete
3. **Views not fully updated** - Some views still use only JSONField

### Migration Risks
1. **Data loss** - If migration command fails midway
2. **Performance** - Querying both systems may be slower
3. **Inconsistency** - If one system updated without the other

## Next Steps

### Before Production Deployment

1. **Run all automated tests**
   ```bash
   pytest game/tests_xp_freebie_migration.py -v --cov
   ```

2. **Perform manual testing**
   - Follow all 6 test scenarios above
   - Test with multiple character types
   - Test with different approval states

3. **Update views and templates**
   - Migrate remaining views to use model system
   - Update templates to show both systems during transition
   - See `docs/guides/view_template_migration.md`

4. **Data migration**
   - Backup database
   - Run migration command with --dry-run
   - Review output
   - Run actual migration
   - Verify data integrity

5. **Monitor in production**
   - Watch for errors in logs
   - Monitor database performance
   - Check user reports

### Future Work

1. **Complete view migration**
   - High priority: Character detail displays
   - Medium priority: Freebie forms
   - Low priority: XP approval forms (complex)

2. **Remove JSONField**
   - After all views updated
   - After confirming model system works
   - Create migration to drop columns

3. **Add features**
   - XP request notes/comments
   - Denial reasons
   - XP source tracking (weekly, story, etc.)

## Rollback Plan

If issues are discovered:

1. **Keep JSONField** - Don't drop columns yet
2. **Regenerate JSONField from models** (if needed):
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
4. **Continue dual-system** - No rush to complete migration

## Test Execution Checklist

### Before Testing
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database migrations run (`python manage.py migrate`)
- [ ] Test database configured (use `pytest.ini` or `settings.py`)

### Automated Tests
- [ ] Run all migration tests: `pytest game/tests_xp_freebie_migration.py -v`
- [ ] Run validation tests: `pytest characters/tests/core/test_validation_constraints.py -v`
- [ ] Run game integration tests: `pytest game/tests_integration.py -v`
- [ ] All tests passing
- [ ] Coverage > 80% for migration code

### Manual Tests
- [ ] Test Scenario 1: Creating XP requests
- [ ] Test Scenario 2: Approving XP requests
- [ ] Test Scenario 3: Dual-system totals
- [ ] Test Scenario 4: Freebie records
- [ ] Test Scenario 5: Migration command
- [ ] Test Scenario 6: Template display

### Data Verification
- [ ] Check database for XPSpendingRequest records
- [ ] Check database for FreebieSpendingRecord records
- [ ] Verify indexes exist on tables
- [ ] Verify foreign keys are correct
- [ ] No orphaned records

### Performance
- [ ] Query performance acceptable (< 100ms for history)
- [ ] No N+1 queries in views
- [ ] Database indexes being used (check EXPLAIN)

### User Acceptance
- [ ] ST can approve XP requests
- [ ] Players can view their XP history
- [ ] Totals display correctly
- [ ] No duplicate data shown
- [ ] UI is intuitive

## Success Criteria

The migration is considered successful when:

1. ✅ **All automated tests pass** (29 tests)
2. ✅ **Manual scenarios verified** (6 scenarios)
3. ✅ **No data loss** - All existing XP/freebie data preserved
4. ✅ **Accurate calculations** - Totals match between systems
5. ✅ **Workflow functions** - Approval/denial works correctly
6. ✅ **Performance acceptable** - No significant slowdown
7. ✅ **No regressions** - Existing functionality still works

## Contact

For questions or issues:
- Check: `docs/guides/view_template_migration.md`
- Check: `docs/guides/jsonfield_migration.md`
- File issue in project tracker

---

**Document Version:** 1.0
**Last Updated:** 2025-11-23
**Status:** Ready for Testing
