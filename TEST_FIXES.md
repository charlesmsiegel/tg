# Test Fixes Required

**Test Run Summary:** 400 tests, ~100 failures/errors remaining

This document classifies test failures into work units for systematic fixing.

---

## COMPLETED

### Unit 5: URL Route Names Changed ✓

**Status:** FIXED

**Changes Made:**
1. Fixed `get_short_gameline_name()` in `core/utils.py` to return empty string for 'wod' gameline (wod characters use base URL patterns without gameline namespace)
2. Updated `characters/tests/test_views.py`:
   - `TestCharacterListView`: Changed `reverse("characters:list")` to `reverse("characters:index")`
   - `TestCharacterCreateView`: Changed `reverse("characters:create")` to `reverse("characters:create:character")`
   - `TestCharacterDetailView`: Updated tests to handle redirect behavior for base Human characters
   - `TestCharacterUpdateView`: Updated to use `character.get_update_url()` and correct status code assertions

All 22 tests in `characters/tests/test_views.py` now pass.

---

## REMAINING WORK

---

## Unit 7: Character Model API Changes

**Severity:** MEDIUM
**Files:** `characters/tests/test_models.py` (TestCharacter)

**Tests Affected:** 4+

### Problem
```python
character.total_xp()      # AttributeError: no attribute 'total_xp'
character.available_xp()  # AttributeError: no attribute 'available_xp'
Character(spent_xp={})    # TypeError: unexpected keyword argument 'spent_xp'
```

Character XP-related methods and fields have changed.

### Fix
Update tests to use current Character API for XP tracking.

---

## Unit 9: Status Transition Validation

**Severity:** LOW
**Files:** `characters/tests/test_models.py`, `characters/tests/test_forms.py`

**Tests Affected:** 2

### Problem
```python
character.status = "Dec"  # from "Ret"
# ValidationError: Cannot transition from Ret to Dec. Valid transitions: App
```

New status transition rules prevent arbitrary status changes.

### Fix
Update test to use valid status transitions.

---

## Unit 10: NewsItem View Tests

**Severity:** LOW
**Files:** `core/tests.py` (TestNewsItemDetailView, TestNewsItemCreateView, TestNewsItemUpdateView)

**Tests Affected:** 3+

### Problem
Views return 404 or different status codes than expected.

### Fix
Verify URL patterns and view logic match test expectations.

---

## Unit 11: Profile Signal Conflicts

**Severity:** LOW
**Files:** Various integration tests

**Tests Affected:** 4+

### Problem
```python
# ValidationError: {'user': ['Profile with this User already exists.']}
```

Tests create Users which auto-create Profiles via signals, then try to create Profiles manually.

### Fix
Update tests to use `get_or_create` or access existing profiles.

---

## Unit 12: Home/Landing Page Tests

**Severity:** LOW
**Files:** `core/tests.py` (TestHomeListView)

**Tests Affected:** 4

### Problem
Template name or content changed - tests expect content that isn't there.

### Fix
Update assertions to match current home page implementation.

---

## Unit 13: Deprecated/Architecture Change Tests

**Severity:** CONSIDER REMOVAL

These tests may need to be rewritten or removed as they test features that have fundamentally changed:

1. **XP Migration Tests** (`game/tests_xp_freebie_migration.py`)
   - Tests dual XP system that may be deprecated
   - `has_pending_xp_or_model_requests()`, `has_pending_xp_model_requests()`

2. **WebSocket Tests** (`game/tests/test_websocket.py`)
   - Many require specific setup that may have changed
   - Character/scene interaction patterns changed

3. **Integration Tests** (`game/tests_integration.py`, `core/tests_integration.py`)
   - Test complex workflows that span multiple changed components

### Recommendation
Review each test class to determine if:
- The feature still exists and tests need updating
- The feature was removed and tests should be deleted
- The feature was replaced and new tests should be written

---

## Priority Order

1. **Unit 7** - Character API updates
2. **Unit 5** - URL fixes
3. **Unit 9-12** - Minor test updates
4. **Unit 13** - Evaluate for deprecation

---

## Needs Investigation

- Unit 13: Review which tests to keep vs deprecate
