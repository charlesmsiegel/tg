# JSONField Removal - Implementation Summary

## Issue Addressed

**Problem:** Inefficient and fragile use of JSONField for XP and freebie tracking

**Files:**
- `characters/models/core/character.py:82` - `spent_xp = models.JSONField(default=list)`
- `characters/models/core/human.py:113` - `spent_freebies = models.JSONField(default=list)`

**Issues:**
1. Cannot query JSONField contents efficiently
2. Entire JSON loaded into memory on access
3. Index-based updates in views are fragile
4. No referential integrity or proper indexing

## Solution Implemented

Created two new Django models to replace JSONField usage:

### 1. XPSpendingRequest Model
**Location:** `game/models.py`

Tracks XP expenditures with proper database relations:
- Character reference (ForeignKey)
- Trait information (name, type, value)
- Cost and approval status
- Timestamps and approver tracking
- Indexed for efficient queries

### 2. FreebieSpendingRecord Model
**Location:** `game/models.py`

Tracks freebie point usage during character creation:
- Character reference (ForeignKey)
- Trait information
- Cost tracking
- Timestamp
- Indexed for efficient queries

## Files Created/Modified

### New Files:
1. **game/migrations/0001_add_xp_freebie_spending_models.py**
   - Database migration for new models

2. **game/management/commands/migrate_jsonfield_to_models.py**
   - Data migration command to convert existing JSONField data to model instances
   - Supports `--dry-run` flag for testing

3. **JSONFIELD_MIGRATION_GUIDE.md**
   - Complete migration guide for developers
   - Before/after code examples
   - Testing instructions

4. **JSONFIELD_REMOVAL_SUMMARY.md** (this file)
   - High-level summary of changes

### Modified Files:
1. **game/models.py**
   - Added `XPSpendingRequest` model (lines 915-963)
   - Added `FreebieSpendingRecord` model (lines 966-995)

2. **characters/models/core/character.py**
   - Added deprecation comment to `spent_xp` field (line 82)
   - Added new methods:
     - `create_xp_spending_request()` - Create XP request
     - `get_pending_xp_requests()` - Query pending requests
     - `get_xp_spending_history()` - Get all requests
     - `approve_xp_request()` - Approve a request
     - `deny_xp_request()` - Deny a request

3. **characters/models/core/human.py**
   - Added deprecation comment to `spent_freebies` field (line 113)
   - Added new methods:
     - `create_freebie_spending_record()` - Create freebie record
     - `get_freebie_spending_history()` - Get all records
     - `total_freebies_from_model()` - Calculate total using new model

4. **core/models.py**
   - Fixed missing `ModelQuerySet` and `ModelManager` definitions (lines 15-21)
   - This was a preexisting bug preventing Django from starting

5. **core/admin.py**
   - Commented out references to unimplemented `CharacterTemplate` and `TemplateApplication` models
   - This was a preexisting bug

## Migration Path

### Phase 1: Coexistence (Current State)
- Both JSONField and model-based systems exist
- JSONFields marked as deprecated
- New helper methods available on Character and Human models
- Old code continues to work

### Phase 2: Data Migration (Manual Step Required)
```bash
# Preview changes
python manage.py migrate_jsonfield_to_models --dry-run

# Perform migration
python manage.py migrate_jsonfield_to_models
```

### Phase 3: Code Updates (Future Work)
Update views and templates to use new model-based methods:
- Replace `character.spent_xp` with `character.get_xp_spending_history()`
- Replace `human.spent_freebies` with `human.get_freebie_spending_history()`
- Update approval logic to use `approve_xp_request()` method
- Update templates to iterate over model instances instead of JSON dicts

**Files to Update (identified but not yet modified):**
- `characters/views/mage/mage.py` (lines 610-660)
- `characters/views/core/human.py` (lines 435-450)
- Various templates in `characters/templates/`

### Phase 4: Cleanup (Future)
Once all code is updated:
1. Remove JSONField columns from models
2. Create migration to drop database columns
3. Remove deprecated methods
4. Remove migration command

## Benefits

1. **Queryable**
   ```python
   # Find all pending XP requests across all characters
   XPSpendingRequest.objects.filter(approved='Pending')
   ```

2. **Efficient**
   - Database indexes on common queries
   - Only load needed data
   - No JSON parsing overhead

3. **Safe**
   - No index-based updates
   - Atomic operations
   - Referential integrity

4. **Extensible**
   - Easy to add new fields (denial reason, notes, etc.)
   - Can add constraints and validations
   - Support for complex queries and aggregations

5. **Maintainable**
   - Standard Django patterns
   - Type-safe in code
   - Better IDE support

## Testing Recommendations

1. **Data Integrity**
   - Verify all existing records migrated correctly
   - Check counts: JSONField entries == Model instances
   - Spot-check specific characters

2. **Functionality**
   - Create new XP/freebie requests
   - Approve/deny requests
   - Query pending requests
   - Verify history display

3. **Performance**
   - Compare query times for large datasets
   - Verify indexes are used
   - Test with realistic data volumes

## Next Steps

1. Run database migrations: `python manage.py migrate game`
2. Run data migration: `python manage.py migrate_jsonfield_to_models`
3. Begin updating views to use new model-based methods
4. Update templates to use new model instances
5. Test thoroughly before removing JSONFields

## Notes

- JSONFields are NOT removed in this implementation
- Both systems coexist during transition
- Backward compatibility maintained
- No breaking changes to existing functionality
- Fixed two preexisting bugs (ModelManager, CharacterTemplate admin)

## References

- Issue description in `PRACTICE_VIOLATIONS.md` section 6
- Existing `WeeklyXPRequest` model (game/models.py:839) - different purpose (earning XP vs spending XP)
- Migration guide: `JSONFIELD_MIGRATION_GUIDE.md`
