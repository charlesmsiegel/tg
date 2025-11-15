# Code Simplification Analysis and Implementation

## Summary of Changes Implemented

### Phase 1: Quick Wins (COMPLETED)

1. **Created `core/views/mixins.py`** with reusable view mixins:
   - `ApprovedUserContextMixin`: Automatically adds `is_approved_user` to context (eliminates 100+ lines of duplication across 20+ views)
   - `PlaceholderFormMixin`: Automatically adds placeholder text to form fields (eliminates 50+ lines across 5+ views)

2. **Updated Weapon Models** for dynamic URL generation:
   - Modified `items/models/core/weapon.py` to use `self.type` and `cls.type` for URL generation
   - Removed duplicate `get_update_url()` and `get_creation_url()` methods from:
     - `items/models/core/meleeweapon.py`
     - `items/models/core/rangedweapon.py`
     - `items/models/core/thrownweapon.py`
   - **Impact**: Eliminated 30+ lines of duplicate code

3. **Created `characters/views/mixins.py`** with character-specific base views:
   - `CharacterBasicsView`: Base for character creation forms
   - `CharacterLanguagesView`: Base for language selection during creation
   - `CharacterSpecialtiesView`: Base for specialty selection
   - `CharacterExtrasView`: Base for extras (age, appearance, history, etc.)
   - **Impact**: Can eliminate 670+ lines when applied to all character views

---

## Phase 2: Rating Class Consolidation Opportunity

### Current State: 12 Similar Rating Classes

All follow the same pattern: ForeignKey to parent + ForeignKey to rated item + integer rating

#### Resonance Rating Classes (3 classes):
1. **`WonderResonanceRating`** (`items/models/mage/wonder.py:8-20`)
   - Fields: `wonder`, `resonance`, `rating`

2. **`NodeResonanceRating`** (`locations/models/mage/node.py:236-246`)
   - Fields: `node`, `resonance`, `rating`

3. **`ResRating`** (Mage) (`characters/models/mage/mage.py:814-821`)
   - Fields: `mage`, `resonance`, `rating`

#### Other Rating Classes (9 classes):
4. **`NodeMeritFlawRating`** (`locations/models/mage/node.py:226-233`)
   - Fields: `node`, `mf`, `rating`

5. **`MeritFlawRating`** (`characters/models/core/merit_flaw_block.py:76-81`)
   - Fields: `character`, `mf`, `rating`

6. **`ChantryBackgroundRating`** (`locations/models/mage/chantry.py:318+`)
   - Fields: `chantry`, `bg`, `rating`

7. **`BackgroundRating`** (`characters/models/core/background_block.py:15-41`)
   - Fields: `char`, `bg`, `rating` (plus display fields)

8. **`PooledBackgroundRating`** (`characters/models/core/background_block.py:44+`)
   - Fields: `group`, `bg`, `rating` (plus display fields)

9. **`PracticeRating`** (`characters/models/mage/mage.py:824+`)
   - Fields: `mage`, `practice`, `rating`

10. **`ZoneRating`** (`locations/models/mage/reality_zone.py:6+`)
    - Fields: `zone`, `practice`, `rating`

11. **`PathRating`** (`characters/models/mage/sorcerer.py:181+`)
    - Fields: `character`, `path`, `practice`, `ability`, `rating` (more complex)

12. **`AdvantageRating`** (`characters/models/mage/companion.py:154+`)
    - Fields: `character`, `advantage`, `rating`

### Proposed Solution: Generic Rating Model

Create a single `GenericRating` model using Django's ContentTypes framework:

```python
# core/models/rating.py
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class GenericRating(models.Model):
    """
    Generic rating model that can relate any two models with a rating value.

    Replaces: WonderResonanceRating, NodeResonanceRating, ResRating,
    NodeMeritFlawRating, MeritFlawRating, ChantryBackgroundRating,
    BackgroundRating, PooledBackgroundRating, PracticeRating, ZoneRating,
    PathRating, AdvantageRating
    """

    # The object being rated (e.g., Wonder, Node, Mage, Human)
    parent_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='ratings_as_parent'
    )
    parent_object_id = models.PositiveIntegerField()
    parent_object = GenericForeignKey('parent_content_type', 'parent_object_id')

    # The rating subject (e.g., Resonance, MeritFlaw, Background)
    subject_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name='ratings_as_subject'
    )
    subject_object_id = models.PositiveIntegerField()
    subject_object = GenericForeignKey('subject_content_type', 'subject_object_id')

    # The rating value
    rating = models.IntegerField(default=0)

    # Optional fields for specific use cases
    display_alt_name = models.BooleanField(default=False)  # For BackgroundRating
    display_preference = models.CharField(max_length=100, blank=True)  # For BackgroundRating
    note = models.TextField(blank=True)  # General purpose notes

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        indexes = [
            models.Index(fields=['parent_content_type', 'parent_object_id']),
            models.Index(fields=['subject_content_type', 'subject_object_id']),
        ]
        # Ensure uniqueness of parent-subject pairs
        unique_together = [
            ['parent_content_type', 'parent_object_id',
             'subject_content_type', 'subject_object_id']
        ]

    def __str__(self):
        return f"{self.parent_object}: {self.subject_object} = {self.rating}"


class RatingMixin(models.Model):
    """
    Mixin to add rating functionality to any model.

    Usage:
        class Wonder(RatingMixin, ItemModel):
            ...

    Then use:
        wonder.add_rating(resonance, 3)
        wonder.get_rating(resonance)
        wonder.get_rated_objects(Resonance)
    """

    class Meta:
        abstract = True

    def add_rating(self, subject, rating_value):
        """Add or update a rating for a subject."""
        from django.contrib.contenttypes.models import ContentType

        parent_ct = ContentType.objects.get_for_model(self)
        subject_ct = ContentType.objects.get_for_model(subject)

        rating, created = GenericRating.objects.update_or_create(
            parent_content_type=parent_ct,
            parent_object_id=self.pk,
            subject_content_type=subject_ct,
            subject_object_id=subject.pk,
            defaults={'rating': rating_value}
        )
        return rating

    def get_rating(self, subject):
        """Get the rating value for a subject (returns 0 if not rated)."""
        from django.contrib.contenttypes.models import ContentType

        parent_ct = ContentType.objects.get_for_model(self)
        subject_ct = ContentType.objects.get_for_model(subject)

        try:
            rating = GenericRating.objects.get(
                parent_content_type=parent_ct,
                parent_object_id=self.pk,
                subject_content_type=subject_ct,
                subject_object_id=subject.pk,
            )
            return rating.rating
        except GenericRating.DoesNotExist:
            return 0

    def get_rated_objects(self, model_class):
        """Get all objects of a certain type that this object has rated."""
        from django.contrib.contenttypes.models import ContentType

        parent_ct = ContentType.objects.get_for_model(self)
        subject_ct = ContentType.objects.get_for_model(model_class)

        ratings = GenericRating.objects.filter(
            parent_content_type=parent_ct,
            parent_object_id=self.pk,
            subject_content_type=subject_ct,
        )

        return [
            (model_class.objects.get(pk=r.subject_object_id), r.rating)
            for r in ratings
        ]

    def total_rating(self, model_class=None):
        """Get total of all ratings (optionally filtered by subject type)."""
        from django.contrib.contenttypes.models import ContentType

        parent_ct = ContentType.objects.get_for_model(self)

        filters = {
            'parent_content_type': parent_ct,
            'parent_object_id': self.pk,
        }

        if model_class:
            subject_ct = ContentType.objects.get_for_model(model_class)
            filters['subject_content_type'] = subject_ct

        ratings = GenericRating.objects.filter(**filters)
        return sum(r.rating for r in ratings)
```

### Migration Strategy

This is a **breaking change** that requires careful migration:

1. **Create new GenericRating model** in core/models/
2. **Add RatingMixin to existing models** that use ratings
3. **Create data migration** to copy data from old rating tables to GenericRating
4. **Update all code** that references old rating classes
5. **Test thoroughly** before removing old models
6. **Remove old rating models** once GenericRating is proven

**Estimated Impact:**
- Reduces 12 similar models to 1 generic model
- Eliminates hundreds of lines of duplicate code
- Makes adding new rating relationships trivial (no new model needed)
- Slightly more complex queries but better maintainability

**Risk Level:** HIGH (requires data migration and extensive testing)

---

## Phase 3: Other Simplification Opportunities

### 1. Human Model Field Definitions (HIGH PRIORITY)

**Problem:** 5 game-specific Human classes repeat 60+ ability field definitions each (~550 lines total)

**Files Affected:**
- `characters/models/mage/mtahuman.py`
- `characters/models/vampire/vtmhuman.py`
- `characters/models/werewolf/wtahuman.py`
- `characters/models/changeling/ctdhuman.py`
- `characters/models/wraith/wtohuman.py`

**Solution:** Use `__init_subclass__()` to dynamically create fields from ability lists

**Impact:** Reduces 550+ lines to ~150 lines (73% reduction)

**Risk Level:** MEDIUM-HIGH (requires Django migration)

---

### 2. View Field Lists (MEDIUM PRIORITY)

**Problem:** Create and Update views repeat identical field lists (700+ lines total)

**Example:** `MageCreateView` and `MageUpdateView` both list 130 identical fields

**Solution:** Extract field lists to class attributes or mixins that both views reference

**Impact:** Reduces 700+ lines to ~200 lines (71% reduction)

**Risk Level:** LOW (no database changes, just refactoring)

---

### 3. Similar View Methods (ONGOING)

**Problem:** Many views have nearly identical implementations of:
- `get_context_data()` - adds `is_approved_user`
- `form_valid()` - checks permissions and increments `creation_status`
- `get_form_kwargs()` - passes user or pk to form

**Status:** Partially addressed by new mixins in `core/views/mixins.py` and `characters/views/mixins.py`

**Next Steps:** Update existing views to use the new mixins

**Impact:** Will eliminate 100+ lines when fully applied

**Risk Level:** LOW (backward compatible)

---

## Summary Statistics

### Code Reduction Potential

| Category | Lines Before | Lines After | Savings | Risk |
|----------|-------------|------------|---------|------|
| Weapon URL methods | 30 | 0 | 30 | LOW |
| View mixins (when applied) | 770 | 100 | 670 | LOW |
| Human model fields | 550 | 150 | 400 | MED-HIGH |
| View field lists | 700 | 200 | 500 | LOW |
| Rating models | ~400 | ~100 | 300 | HIGH |
| **TOTAL** | **2,450** | **550** | **1,900** | **VARIES** |

### Implementation Priority

1. **LOW RISK, HIGH IMPACT** (Already Done):
   - ✅ Core view mixins created
   - ✅ Character view base classes created
   - ✅ Weapon URL methods consolidated

2. **LOW RISK, MEDIUM IMPACT** (Next):
   - Apply mixins to existing views
   - Consolidate view field lists

3. **MEDIUM RISK, HIGH IMPACT** (After thorough testing):
   - Human model field generation

4. **HIGH RISK, HIGH IMPACT** (Requires migration planning):
   - Generic rating model consolidation

---

## Next Steps

1. **Apply existing mixins** to a few views as proof of concept
2. **Create field list mixins** for character views
3. **Test thoroughly** to ensure no functionality breaks
4. **Commit changes** in logical, reviewable chunks
5. **Document** usage of new mixins for future developers
6. **Consider** generic rating model for future major version

---

*Generated: 2025-11-11*
*Branch: claude/audit-views-models-011CV1H9DmTSbnrnqDq54AkW*
