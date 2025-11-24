# Test Coverage Plan

**Goal:** Achieve 80%+ test coverage across all apps

**Status:** In Progress
**Last Updated:** 2025-11-23

## Current Coverage Status

### Existing Tests
- **accounts/tests.py** - Comprehensive tests for Profile and SignUp views
- **game/tests.py** - Tests for Chronicle, Scene, Week, XP system
- **core/tests.py** - Functional tests and basic utility tests
- **characters/tests/core/** - Character forms, views, validation, and transactions
- **core/tests/test_permissions_comprehensive.py** - Comprehensive permission tests

### Test Coverage Targets

Each app should have tests covering:
1. **Models** - Field validation, methods, properties, save hooks
2. **Views** - All CRUD operations, permission checks, edge cases
3. **Forms** - Validation, field restrictions, save behavior
4. **Utils/Helpers** - All utility functions and helper methods
5. **Template Tags** - Custom filters and tags
6. **Mixins** - Permission mixins, message mixins, user check mixins

## App-by-App Test Plan

### 1. Core App
**Priority:** High
**Current Coverage:** ~30% (estimated)

#### Models to Test
- `Model` (base polymorphic model)
- `Book` - creation, string representation, filtering
- `HouseRule` - creation, validation, chronicle association
- `Language` - basic CRUD
- `NewsItem` - creation, ordering, display

#### Views to Test
- `HomeListView` - displays recent characters/items/locations
- `BookCreateView`, `BookDetailView`, `BookListView`, `BookUpdateView`
- `HouseRuleCreateView`, `HouseRuleDetailView`, `HouseRuleUpdateView`
- `LanguageCreateView`, `LanguageDetailView`, `LanguageListView`, `LanguageUpdateView`
- `NewsItemCreateView`, `NewsItemDetailView`, `NewsItemListView`, `NewsItemUpdateView`
- `CharacterTemplateCreateView`, `CharacterTemplateDetailView`, etc.

#### Forms to Test
- All model forms for validation
- Field restrictions and required fields
- Image upload handling

#### Utils to Test
- `dice` - all dice rolling functions
- `filepath` - file path generation
- Template tags: `dots`, `boxes`, `sanitize_html`

#### Permissions to Test
- PermissionManager - all permission types (VIEW, EDIT, SPEND_XP, etc.)
- Permission checking for different user roles (owner, ST, admin, viewer)
- Chronicle-based permissions

### 2. Accounts App
**Priority:** High
**Current Coverage:** ~70% (good existing tests)

#### Additional Tests Needed
- Profile creation on user signup
- ST relationship management
- `objects_to_approve()` method
- Theme preferences
- Permission cascading for STs

### 3. Characters App
**Priority:** Critical
**Current Coverage:** ~40% (some existing tests)

#### Core Models to Test
- `Character` - base character creation, XP system, status changes
- `Human` - human-specific fields
- `CharacterModel` - polymorphic character handling

#### Gameline-Specific Models to Test (each)
- `Mage`, `MtAHuman` - spheres, arete, paradox, quintessence
- `Vampire`, `VtMHuman` - disciplines, blood pool, generation
- `Werewolf`, `WtAHuman` - gifts, renown, rage/gnosis/willpower
- `Wraith`, `WtOHuman` - arcanoi, corpus, pathos, passions
- `Changeling`, `CtDHuman` - arts, glamour, banality
- `Demon`, `DtFHuman` - lores, torment, faith

#### Advantage Models to Test
- `MeritFlaw` and `MeritFlawRating`
- `Background` and `BackgroundRating`
- `Specialty`
- `Derangement`

#### Views to Test
- Character creation flow (all gamelines)
- Character update (limited vs full forms)
- Character detail views
- Permission-based access
- XP spending views
- Freebie spending views

#### Forms to Test
- `LimitedCharacterEditForm` - owner editing restrictions
- Full character forms - ST/Admin editing
- Character creation forms for each gameline
- Validation of attribute totals, freebie spending, etc.

### 4. Game App
**Priority:** High
**Current Coverage:** ~50% (decent existing tests)

#### Additional Tests Needed
- `Story` model and views
- `Journal` model and views
- `Week` and `WeeklyXPRequest` approval workflow
- Scene participant management
- XP distribution
- Message processing

### 5. Items App
**Priority:** Medium
**Current Coverage:** ~5% (very minimal)

#### Models to Test
- `ItemModel` - base item functionality
- Gameline-specific items (Fetish, Wonder, Talisman, Artifact, Relic, Gadget)

#### Views to Test
- Item CRUD operations
- Permission checks
- Chronicle association

### 6. Locations App
**Priority:** Medium
**Current Coverage:** ~5% (very minimal)

#### Models to Test
- `LocationModel` - base location functionality
- `City` - city-specific features
- Gameline-specific locations (Node, Caern, Haunt, Freehold, Font, Lair)

#### Views to Test
- Location CRUD operations
- Permission checks
- Chronicle association
- Reality zone management (for Nodes)

## Test Organization Structure

```
app_name/
└── tests/
    ├── __init__.py
    ├── test_models.py          # All model tests
    ├── test_views.py           # All view tests
    ├── test_forms.py           # All form tests
    ├── test_utils.py           # Utility function tests
    ├── test_permissions.py     # Permission-specific tests
    └── gameline/               # Gameline-specific tests
        ├── __init__.py
        ├── test_mage.py
        ├── test_vampire.py
        ├── test_werewolf.py
        ├── test_wraith.py
        ├── test_changeling.py
        └── test_demon.py
```

## Testing Best Practices

### Setup and Teardown
- Use `setUp()` to create common test data
- Use `setUpTestData()` for class-level test data (more efficient)
- Clean up in `tearDown()` if needed (usually handled by Django)

### Test Naming
- Use descriptive test names: `test_character_creation_validates_attributes`
- Group related tests in classes: `class TestCharacterCreation(TestCase)`

### Assertions
- Use specific assertions: `assertEqual`, `assertIn`, `assertContains`, etc.
- Test both positive and negative cases
- Test edge cases and boundary conditions

### Test Data
- Create minimal test data needed for each test
- Use factories or helper methods for complex objects
- Don't rely on database state from other tests

### Coverage Goals
- **Statements:** 80%+
- **Branches:** 75%+
- **Functions:** 90%+

### Common Test Patterns

#### Testing Models
```python
class TestCharacter(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.character = Character.objects.create(
            name='Test', owner=self.user
        )

    def test_character_creation(self):
        self.assertEqual(self.character.name, 'Test')
        self.assertEqual(self.character.owner, self.user)

    def test_character_xp_calculation(self):
        self.character.xp = 10
        self.assertEqual(self.character.total_xp(), 10)
```

#### Testing Views
```python
class TestCharacterDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.character = Character.objects.create(
            name='Test', owner=self.user
        )

    def test_view_requires_permission(self):
        response = self.client.get(self.character.get_absolute_url())
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_owner_can_view_character(self):
        self.client.login(username='test', password='pass')
        response = self.client.get(self.character.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
```

#### Testing Forms
```python
class TestLimitedCharacterForm(TestCase):
    def test_form_has_limited_fields(self):
        form = LimitedCharacterEditForm()
        self.assertIn('description', form.fields)
        self.assertNotIn('xp', form.fields)

    def test_form_validation(self):
        data = {'description': 'Test description'}
        form = LimitedCharacterEditForm(data=data)
        self.assertTrue(form.is_valid())
```

#### Testing Permissions
```python
class TestCharacterPermissions(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('owner', 'o@test.com', 'pass')
        self.st = User.objects.create_user('st', 'st@test.com', 'pass')
        self.other = User.objects.create_user('other', 'oth@test.com', 'pass')
        self.character = Character.objects.create(
            name='Test', owner=self.owner
        )

    def test_owner_has_view_permission(self):
        pm = PermissionManager()
        self.assertTrue(pm.check_permission(
            self.owner, self.character, 'view_full'
        ))

    def test_other_user_no_permission(self):
        pm = PermissionManager()
        self.assertFalse(pm.check_permission(
            self.other, self.character, 'view_full'
        ))
```

## Running Tests

### Run all tests
```bash
python manage.py test --verbosity=2
```

### Run specific app tests
```bash
python manage.py test accounts --verbosity=2
python manage.py test characters --verbosity=2
python manage.py test core --verbosity=2
python manage.py test game --verbosity=2
python manage.py test items --verbosity=2
python manage.py test locations --verbosity=2
```

### Run with coverage
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

### View coverage report
```bash
open htmlcov/index.html
```

## Priority Order

1. **Core permissions system** - Critical for security
2. **Character creation and editing** - Core functionality
3. **XP and freebie spending** - Core game mechanics
4. **Chronicle and ST management** - Core permissions
5. **Views with permission checks** - Security
6. **Forms with validation** - Data integrity
7. **Utility functions** - Reliability
8. **Template tags** - UI correctness
9. **Items and Locations** - Secondary features

## Success Criteria

- [ ] 80%+ statement coverage across all apps
- [ ] All critical paths tested (character creation, XP spending, permissions)
- [ ] All permission checks tested
- [ ] All forms validated
- [ ] All views tested for permission enforcement
- [ ] Edge cases and error conditions tested
- [ ] No critical bugs discovered during testing
