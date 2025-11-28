# Test Fixes Required

**Test Run Summary:** 400 tests, ~100 failures/errors remaining

This document classifies test failures into work units for systematic fixing.

---

## COMPLETED

### Unit 1: Production Bug - datetime.date.today() Error (FIXED)
- Added `date` to imports in `game/models.py`
- Changed `datetime.date.today()` to `date.today()`

### Unit 2: Import Path Changes - Character Model (FIXED)
- Added `from .core.character import Character, CharacterModel` to `characters/models/__init__.py`

### Unit 3: Import Path Changes - LimitedCharacterEditForm (FIXED)
- Added `from .limited_edit import LimitedCharacterEditForm, LimitedHumanEditForm` to `characters/forms/core/__init__.py`

---

## REMAINING WORK

## Unit 4: PermissionManager API Change

**Severity:** HIGH
**Files:**
- `core/permissions.py`
- `characters/tests/test_views.py` (TestCharacterPermissions)
- `items/tests/test_models.py`
- `locations/tests/test_models.py`

**Tests Affected:** 8+

### Problem
```python
pm.check_permission(user, obj, "view_full")
# AttributeError: 'PermissionManager' object has no attribute 'check_permission'
```

Tests expect a `check_permission()` method that doesn't exist on PermissionManager.

### Fix
Either:
1. Add the `check_permission()` method to PermissionManager, OR
2. Update tests to use the current PermissionManager API

---

## Unit 5: URL Route Names Changed

**Severity:** MEDIUM
**Files:**
- `characters/urls.py`
- `characters/tests/test_views.py` (TestCharacterListView, TestCharacterCreateView)

**Tests Affected:** 6+

### Problem
```python
reverse("characters:list")
reverse("characters:create")
# NoReverseMatch: Reverse for 'list' not found
```

URL patterns have changed but tests still use old route names.

### Fix
Update tests to use current URL names, or verify and add missing URL patterns.

---

## Unit 6: Model Field Changes - Tests Out of Sync

**Severity:** MEDIUM
**Tests Affected:** 15+

### 6a: Journal Model
**File:** `game/tests/test_models.py` (TestJournal)
```python
Journal(title="...", content="...")
# TypeError: Journal() got unexpected keyword arguments: 'title', 'content'
```
Journal model schema changed; tests use old field names.

### 6b: Story Model
**File:** `game/tests/test_models.py` (TestStory)
```python
Story(chronicle=..., description=...)
# TypeError: Story() got unexpected keyword arguments: 'chronicle', 'description'
```

### 6c: Scene Model
**File:** `game/tests/test_models.py` (TestSceneAdvanced)
```python
Scene(xp=3)
# TypeError: Scene() got unexpected keyword arguments: 'xp'
```

### 6d: Week Model
**File:** `game/tests/test_models.py` (TestWeekAndXPRequests)
```python
Week(chronicle=..., week_number=1)
# TypeError: Week() got unexpected keyword arguments
```

### 6e: WeeklyXPRequest Model
```python
WeeklyXPRequest(xp_spent=5, description=...)
# TypeError: got unexpected keyword arguments
```

### Fix
Update all model instantiations in tests to match current model schemas.

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

## Unit 8: Validation Changes - Empty Names Now Rejected

**Severity:** LOW
**Files:** `core/tests.py` (TestModel)

**Tests Affected:** 11

### Problem
```python
CharacterModel.objects.create(name="")
# ValidationError: {'name': ['This field cannot be blank.', 'Name is required']}
```

Tests create models with empty names, but validation now requires non-empty names.

### Fix
Update `setUp()` to use valid model data:
```python
self.model = CharacterModel.objects.create(name="Test Model")
```

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

1. **Unit 4** - Core permission system tests
2. **Unit 8** - Quick fix, unblocks 11 tests
3. **Unit 6** - Model schema updates
4. **Unit 7** - Character API updates
5. **Unit 5** - URL fixes
6. **Unit 9-12** - Minor test updates
7. **Unit 13** - Evaluate for deprecation

---

## Quick Wins (Estimated < 30 min each)

- Unit 8: Change `name=""` to `name="Test"` in setUp

## Medium Effort (1-2 hours each)

- Unit 4: Document PermissionManager API, update tests
- Unit 6: Update model instantiations across test files
- Unit 7: Update Character XP method calls

## Needs Investigation

- Unit 13: Review which tests to keep vs deprecate
