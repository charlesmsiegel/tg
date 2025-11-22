# TODO List

This document consolidates all remaining TODOs across the codebase with context about what needs to be done.

---

## 🔴 High Priority - Code TODOs

### Python Code TODOs

1. **Create LimitedCharacterForm for owner editing**
   - **File**: `characters/views/core/character.py:142`
   - **Context**: Currently, character owners can edit all fields when they should only be able to edit descriptive fields (notes, description, etc.). Need to create a limited form that restricts editing to non-mechanical fields.
   - **Related**: Part of permissions system - owners should have limited edit access
   - **Impact**: Security/gameplay integrity

2. **Add tribal restrictions for Kinfolk backgrounds**
   - **File**: `characters/views/werewolf/kinfolk.py:255`
   - **Context**: `KinfolkBackgroundsView` doesn't enforce tribal restrictions on background choices. Some backgrounds may be restricted based on the Kinfolk's associated tribe.
   - **Impact**: Character creation rules enforcement

3. **Find source for "Slow Healing" merit**
   - **File**: `populate_db/merits_and_flaws_INC.py:14`
   - **Context**: The "Slow Healing" merit (3 pt flaw) for Mage/Sorcerer needs source book verification and page number.
   - **Impact**: Documentation completeness

---

## 🟡 Medium Priority - Testing & Quality

### Permissions System Testing

**File**: `APPLYING_PERMISSIONS_GUIDE.md`

- [ ] **Create limited forms for owner editing**
  - Implement forms that restrict owners to editing only descriptive fields
  - Apply to all character/item/location edit views
  - Test that mechanical fields are properly protected

- [ ] **Test all permission scenarios**
  - Test as Owner, Chronicle Member, Storyteller, Stranger
  - Verify visibility tiers work correctly
  - Ensure 404s are returned for unauthorized access

- [ ] **Update corresponding tests**
  - Add unit tests for permission checks
  - Add integration tests for view access
  - Test permission edge cases

### Validation System Testing

**File**: `VALIDATION_IMPLEMENTATION_SUMMARY.md`

- [ ] **Add integration tests for transactions**
  - Test `spend_xp()` atomicity with concurrent requests
  - Test `approve_xp_spend()` rollback on failure
  - Test `award_xp()` all-or-nothing behavior
  - Verify race condition prevention with `select_for_update()`

### XP/Freebie Migration Testing

**File**: `VIEW_TEMPLATE_MIGRATION_GUIDE.md`

Generic testing checklist for any XP/freebie view updates:
- [ ] Display of XP/freebie history works correctly
- [ ] Total spent calculations are accurate
- [ ] New requests are created properly
- [ ] Approval workflow functions (if applicable)
- [ ] Both JSONField and model data display during transition
- [ ] No regressions in existing functionality

---

## 🟢 Low Priority - Feature Completeness

### Django Messages Framework - Remaining Views

**File**: `MESSAGING_IMPLEMENTATION.md`

The following views still need `MessageMixin` added for user feedback:

#### Characters
- [ ] `characters/views/core/npc.py` - NPCCreateView, NPCUpdateView
- [ ] `characters/views/core/human.py` - Base views (consider inheritance implications)

#### Items

**Vampire Items:**
- [ ] `items/views/vampire/*.py` - Haven components, Domain views

**Werewolf Items:**
- [ ] `items/views/werewolf/rite.py`
- [ ] Other werewolf item views

**Changeling Items:**
- [ ] `items/views/changeling/*.py` - Treasure views, Token views

**Wraith Items:**
- [ ] `items/views/wraith/*.py` - Artifact views, Relic views

#### Locations

**Mage Locations:**
- [ ] `locations/views/mage/chantry.py` - ChantryCreateView, ChantryUpdateView
- [ ] `locations/views/mage/node.py` - Node CRUD views
- [ ] `locations/views/mage/sanctum.py` - Sanctum CRUD views
- [ ] `locations/views/mage/library.py` - Library CRUD views
- [ ] Other mage location views

**Vampire Locations:**
- [ ] `locations/views/vampire/haven.py` - HavenCreateView, HavenUpdateView
- [ ] `locations/views/vampire/domain.py` - Domain CRUD views
- [ ] Other vampire location views

**Werewolf Locations:**
- [ ] `locations/views/werewolf/caern.py` - Caern CRUD views
- [ ] Other werewolf location views

**Changeling Locations:**
- [ ] `locations/views/changeling/freehold.py` - Freehold CRUD views
- [ ] Other changeling location views

**Wraith Locations:**
- [ ] `locations/views/wraith/haunt.py` - Haunt CRUD views
- [ ] Other wraith location views

#### Core/Reference Data
- [ ] `core/views/*.py` - Book, SourceMaterial, HouseRule views

#### Game-Specific Reference Data
- [ ] Mage spheres, practices, tenets, factions
- [ ] Werewolf gifts, rites, breeds, tribes
- [ ] Vampire clans, disciplines, paths
- [ ] Changeling arts, realms, kiths
- [ ] Wraith arcanoi, guilds, circles
- [ ] Demon lores, factions, houses

### Character Template System Enhancements

**File**: `TEMPLATE_SYSTEM_README.md`

Future enhancements for the CharacterTemplate system:

- [ ] **User-created templates (Storyteller-only)**
  - Allow STs to create custom templates for their chronicles
  - Restrict template creation to users with ST permissions
  - Add template management interface

- [ ] **Template variations by clan/tribe/tradition**
  - Create specialized templates for each faction
  - E.g., "Brujah Brawler", "Glass Walker Hacker", "Verbena Herbalist"
  - Populate with faction-appropriate backgrounds and powers

- [ ] **Template import/export (JSON)**
  - Export templates as JSON for sharing
  - Import community-created templates
  - Validation on import to prevent malicious data

- [ ] **Template voting/ratings**
  - Let users rate templates they've used
  - Display popular templates first
  - Add comments/feedback on templates

- [ ] **NPC quick-creation from templates**
  - One-click NPC creation from template
  - Auto-populate NPC fields from template data
  - Faster ST workflow for creating multiple NPCs

---

## 🔵 Deployment & Environment

### Permissions System Deployment

**File**: `PERMISSIONS_IMPLEMENTATION_COMPLETE.md`

- [ ] **Create and activate virtual environment**
  - Set up clean Python virtual environment
  - Isolate dependencies from system Python

- [ ] **Install dependencies**
  - Run `pip install -r requirements.txt`
  - Verify all packages install correctly

- [ ] **Test with different user roles**
  - Manual testing with Owner, Chronicle Member, ST, Stranger accounts
  - Verify visibility tiers and edit permissions
  - Check that 404s are returned appropriately

- [ ] **Deploy to staging**
  - Deploy permissions system to staging environment
  - Run full test suite in staging
  - Performance testing under load

- [ ] **User acceptance testing**
  - Get feedback from real users
  - Test edge cases in production-like environment
  - Verify no usability issues

- [ ] **Deploy to production**
  - Final deployment of permissions system
  - Monitor error logs closely
  - Be ready to rollback if issues arise

### Validation System Deployment

**File**: `VALIDATION_IMPLEMENTATION_SUMMARY.md`

- [ ] **Deploy to staging**
  - Deploy transaction protection and constraints
  - Test XP spending workflows
  - Verify constraint violations are caught

- [ ] **Monitor for validation errors**
  - Watch logs for CheckConstraint violations
  - Monitor for transaction rollbacks
  - Track performance impact

- [ ] **Deploy to production**
  - Final deployment of validation system
  - Monitor database constraint violations
  - Alert on any data integrity issues

- [ ] **Monitor database constraint violations**
  - Set up alerts for constraint violations
  - Log violations for analysis
  - Fix any existing invalid data

---

## 🎨 Design System - Modern Site Redesign

**Files**: `.kiro/specs/modern-site-redesign/tasks.md`, `.kiro/specs/modern-site-redesign/design.md`

This is a separate design system overhaul project.

### Template Updates
- [ ] **Update characters app form templates**
  - Use STYLE.md as a guide
  - Apply tg-card, tg-table, tg-badge classes
  - Implement gameline-specific heading styles

- [ ] **Update items app form templates**
  - Use STYLE.md as a guide
  - Consistent with character template patterns

### Testing
- [ ] **Perform visual and functional testing**
  - Test all templates in light theme mode
  - Cross-browser: Chrome, Firefox, Safari, Edge
  - Verify responsive layouts

- [ ] **Perform accessibility testing**
  - Test keyboard navigation through all interactive elements
  - Screen reader compatibility
  - WCAG compliance

- [ ] **Final review and refinement**
  - Review all updated templates for consistency
  - Fix any visual bugs
  - Ensure gameline theming works throughout

### Visual QA Checklist

**Characters:**
- [ ] Character index page displays correctly with tabs
- [ ] Character detail page shows all sections properly
- [ ] Character creation form works
- [ ] Gameline fonts apply to character names
- [ ] Status badges display correctly

**Locations:**
- [ ] Location index page displays correctly
- [ ] Location detail page shows all attributes
- [ ] Location forms work properly
- [ ] Gameline fonts apply to location names

**Items:**
- [ ] Item index page displays correctly
- [ ] Item detail page shows all properties
- [ ] Item forms work properly
- [ ] Gameline fonts apply to item names

**Game:**
- [ ] Chronicle pages display correctly
- [ ] Scene pages display correctly
- [ ] Game-related forms work properly

**Accounts:**
- [ ] Profile pages display correctly
- [ ] Login/signup forms work properly
- [ ] Theme selection works

**Core:**
- [ ] Home page displays correctly
- [ ] Navigation works across all pages
- [ ] House rules pages display correctly

---

## 📊 Priority Summary

| Category | High Priority | Medium Priority | Low Priority |
|----------|--------------|-----------------|--------------|
| Code TODOs | 3 items | - | - |
| Testing | - | 9 items | 6 items |
| Feature Completeness | - | - | 35+ views |
| Template Enhancements | - | - | 5 features |
| Deployment | - | 8 items | - |
| Design System | - | - | 25+ items |

---

## 🎯 Recommended Next Steps

1. **Code Quality** (High Priority)
   - Implement `LimitedCharacterForm` for owner editing
   - Add tribal restrictions for Kinfolk backgrounds

2. **Testing** (Medium Priority)
   - Add integration tests for atomic transactions
   - Test all permission scenarios
   - Update test coverage

3. **Deployment** (Medium Priority)
   - Set up staging environment
   - Deploy permissions and validation systems
   - Monitor for issues

4. **Feature Completeness** (Low Priority)
   - Add MessageMixin to remaining views
   - Implement template system enhancements
   - Complete design system overhaul
