# Human Model Refactoring Plan

## Problem Statement

The `Human` class currently has 7 parent classes, creating a complex inheritance hierarchy that is difficult to maintain and reason about. This violates the principle of composition over inheritance and creates tight coupling between components.

## Current Inheritance Structure

```python
class Human(
    HumanUrlBlock,        # 1. URL generation utilities
    AbilityBlock,         # 2. 15 ability fields + methods
    MeritFlawBlock,       # 3. Merit/Flaw management via through table
    HealthBlock,          # 4. Health tracking fields + methods
    BackgroundBlock,      # 5. Background management via through table
    AttributeBlock,       # 6. 9 attribute fields + methods
    Character,            # 7. Base polymorphic model
):
```

### Analysis of Each Parent Class

#### 1. **HumanUrlBlock** (Pure utility methods)
- **Type**: Mixin with no fields
- **Purpose**: URL generation for character CRUD operations
- **Dependencies**: Requires `self.gameline`, `self.type`, `self.pk`
- **Fields**: None
- **Methods**: 4 URL generation methods
- **Recommendation**: **Refactor to model methods** - These should be methods directly on Human
- **Rationale**: No state, purely derived from existing fields

#### 2. **AbilityBlock** (Data + behavior)
- **Type**: Abstract model with fields
- **Purpose**: Stores 15 core abilities (alertness, athletics, brawl, etc.)
- **Fields**: 15 IntegerFields with validators and constraints
- **Methods**: 12 methods for getting/filtering/totaling abilities
- **Recommendation**: **Keep as mixin** - Core WoD character data
- **Rationale**:
  - These fields are genuinely part of the character data model
  - Shared across ALL character types (Human, Vampire, Mage, Werewolf, etc.)
  - Converting to composition would require complex foreign key relationships
  - Methods are tightly coupled to the fields

#### 3. **MeritFlawBlock** (Primarily composition)
- **Type**: Abstract model with M2M relationship
- **Purpose**: Many-to-many relationship with MeritFlaw through MeritFlawRating
- **Fields**: 1 M2M field (`merits_and_flaws`)
- **Methods**: 8 methods for managing merits/flaws
- **Recommendation**: **Convert to manager class** - Already uses composition internally
- **Rationale**:
  - The M2M relationship is already compositional
  - Methods operate on related objects, not the model itself
  - Could be extracted to a `MeritFlawManager` class

#### 4. **HealthBlock** (Simple data + behavior)
- **Type**: Abstract model with fields
- **Purpose**: Health level tracking and wound penalties
- **Fields**: 2 fields (`current_health_levels`, `max_health_levels`)
- **Methods**: 7 methods for health management
- **Recommendation**: **Keep as mixin** - Core character data
- **Rationale**:
  - Simple, focused responsibility
  - Tightly coupled data and behavior
  - Used by all character types

#### 5. **BackgroundBlock** (Complex composition)
- **Type**: Abstract model with dynamic properties
- **Purpose**: Manages backgrounds through BackgroundRating model
- **Fields**: None (dynamic properties created in __init__)
- **Methods**: 9 methods for background management
- **Recommendation**: **Convert to manager class** - Already uses composition
- **Rationale**:
  - No actual database fields (just dynamic properties)
  - All data stored in related BackgroundRating model
  - Could be extracted to a `BackgroundManager` class

#### 6. **AttributeBlock** (Data + behavior)
- **Type**: Abstract model with fields
- **Purpose**: Stores 9 core attributes (strength, dexterity, stamina, etc.)
- **Fields**: 9 IntegerFields with validators and constraints
- **Methods**: 11 methods for getting/filtering/totaling attributes
- **Recommendation**: **Keep as mixin** - Core WoD character data
- **Rationale**:
  - These fields are genuinely part of the character data model
  - Shared across ALL character types
  - Converting to composition would be overly complex
  - Methods are tightly coupled to the fields

#### 7. **Character** (Required base)
- **Type**: Polymorphic model
- **Purpose**: Base class for all characters with core fields
- **Fields**: 5 core fields (concept, creation_status, notes, xp, spent_xp)
- **Methods**: 35+ methods for character management
- **Recommendation**: **Must keep** - Required for polymorphism
- **Rationale**: This is the foundation of the polymorphic character system

## Refactoring Strategy

### Phase 1: Extract Managers (Low Risk)

#### 1.1 Create MeritFlawManager

**New file**: `characters/managers/merit_flaw_manager.py`

```python
class MeritFlawManager:
    """Manages merit and flaw operations for a character."""

    def __init__(self, character):
        self.character = character

    def num_languages(self):
        """Calculate number of language merits."""
        mf_list = self.character.merits_and_flaws.all().values_list("name", flat=True)
        if "Language" not in mf_list:
            return 0
        language_rating = self.mf_rating(MeritFlaw.objects.get(name="Language"))
        if "Natural Linguist" in mf_list:
            language_rating *= 2
        return language_rating

    def get_mf_and_rating_list(self):
        """Get list of tuples (merit/flaw, rating)."""
        return [(x, self.mf_rating(x)) for x in self.character.merits_and_flaws.all()]

    def add_mf(self, mf, rating):
        """Add a merit or flaw with specified rating."""
        if rating in mf.get_ratings():
            mfr, _ = MeritFlawRating.objects.get_or_create(
                character=self.character, mf=mf
            )
            mfr.rating = rating
            mfr.save()
            return True
        return False

    def filter_mfs(self):
        """Filter available merits/flaws for this character."""
        character_type = self.character.type
        if character_type in ["fomor"]:
            character_type = "human"

        new_mfs = MeritFlaw.objects.exclude(pk__in=self.character.merits_and_flaws.all())

        non_max_mf = MeritFlawRating.objects.filter(character=self.character).exclude(
            Q(rating=F("mf__max_rating"))
        )

        had_mfs = MeritFlaw.objects.filter(pk__in=non_max_mf)
        mf = new_mfs | had_mfs
        if self.has_max_flaws():
            mf = mf.filter(max_rating__gt=0)
        character_type_object = ObjectType.objects.get(name=character_type)
        return mf.filter(allowed_types=character_type_object)

    def mf_rating(self, mf):
        """Get rating for a specific merit/flaw."""
        try:
            return MeritFlawRating.objects.get(
                character=self.character, mf=mf
            ).rating
        except MeritFlawRating.DoesNotExist:
            return 0

    def has_max_flaws(self):
        """Check if character has maximum flaws."""
        return self.total_flaws() <= -7

    def total_flaws(self):
        """Calculate total flaw points."""
        from django.db.models import Sum

        result = MeritFlawRating.objects.filter(
            character=self.character, rating__lt=0
        ).aggregate(Sum("rating"))
        return result["rating__sum"] or 0

    def total_merits(self):
        """Calculate total merit points."""
        from django.db.models import Sum

        result = MeritFlawRating.objects.filter(
            character=self.character, rating__gt=0
        ).aggregate(Sum("rating"))
        return result["rating__sum"] or 0
```

**Usage in Human model**:

```python
class Human(...):
    merits_and_flaws = models.ManyToManyField(
        MeritFlaw, blank=True, through=MeritFlawRating, related_name="flawed"
    )

    @property
    def merit_flaw_manager(self):
        """Lazy-loaded manager for merit/flaw operations."""
        if not hasattr(self, '_merit_flaw_manager'):
            self._merit_flaw_manager = MeritFlawManager(self)
        return self._merit_flaw_manager

    # Backward compatibility methods (delegates to manager)
    def num_languages(self):
        return self.merit_flaw_manager.num_languages()

    def get_mf_and_rating_list(self):
        return self.merit_flaw_manager.get_mf_and_rating_list()

    # ... etc for all other methods
```

#### 1.2 Create BackgroundManager

**New file**: `characters/managers/background_manager.py`

Similar approach to MeritFlawManager, extracting all background-related logic.

### Phase 2: Refactor HumanUrlBlock (Low Risk)

Move URL generation methods directly into Human model:

```python
class Human(...):
    # Remove HumanUrlBlock from inheritance

    @staticmethod
    def get_gameline_for_url(gameline):
        g = get_short_gameline_name(gameline)
        if g:
            g += ":"
        return g

    def get_full_update_url(self):
        return reverse(
            f"characters:{self.get_gameline_for_url(self.gameline)}:update:{self.type}_full",
            kwargs={"pk": self.pk},
        )

    def get_update_url(self):
        return reverse(
            f"characters:{self.get_gameline_for_url(self.gameline)}:update:{self.type}",
            kwargs={"pk": self.pk},
        )

    @classmethod
    def get_full_creation_url(cls):
        return reverse(
            f"characters:{cls.get_gameline_for_url(cls.gameline)}:create:{cls.type}_full"
        )

    @classmethod
    def get_creation_url(cls):
        return reverse(
            f"characters:{cls.get_gameline_for_url(cls.gameline)}:create:{cls.type}"
        )
```

### Phase 3: Keep Core Data Mixins (No Change)

**AttributeBlock**, **AbilityBlock**, and **HealthBlock** remain as mixins because:
- They provide actual database fields that are core to the character data model
- They're shared across all character types
- Converting to composition would add unnecessary complexity
- The tight coupling between fields and methods is appropriate here

### Final Structure

```python
class Human(
    AbilityBlock,         # Core ability fields (keep)
    HealthBlock,          # Core health fields (keep)
    AttributeBlock,       # Core attribute fields (keep)
    Character,            # Required polymorphic base (keep)
):
    """
    Base human character class for World of Darkness.

    Uses composition for:
    - Merit/Flaw management (via MeritFlawManager)
    - Background management (via BackgroundManager)
    """

    # Merits/Flaws (managed by MeritFlawManager)
    merits_and_flaws = models.ManyToManyField(
        MeritFlaw, blank=True, through=MeritFlawRating, related_name="flawed"
    )

    @property
    def merit_flaw_manager(self):
        if not hasattr(self, '_merit_flaw_manager'):
            self._merit_flaw_manager = MeritFlawManager(self)
        return self._merit_flaw_manager

    @property
    def background_manager(self):
        if not hasattr(self, '_background_manager'):
            self._background_manager = BackgroundManager(self)
        return self._background_manager

    # URL methods (moved from HumanUrlBlock)
    @staticmethod
    def get_gameline_for_url(gameline):
        ...

    def get_full_update_url(self):
        ...

    # Backward compatibility delegates
    def num_languages(self):
        return self.merit_flaw_manager.num_languages()

    def add_mf(self, mf, rating):
        return self.merit_flaw_manager.add_mf(mf, rating)

    # ... etc
```

## Benefits

1. **Reduced complexity**: From 7 parent classes to 4
2. **Better separation of concerns**: Managers handle complex operations
3. **Easier testing**: Managers can be tested independently
4. **More maintainable**: Clear boundaries between data and behavior
5. **Backward compatible**: Old method calls still work via delegation
6. **Gradual migration**: Can migrate code to use managers over time

## Migration Strategy

1. **Phase 1**: Create manager classes and add them as properties
2. **Phase 2**: Add backward-compatible delegation methods
3. **Phase 3**: Update tests to pass
4. **Phase 4**: Update views/forms to use managers (optional, gradual)
5. **Phase 5**: Eventually deprecate delegation methods (optional, long-term)

## Risks and Mitigations

### Risk 1: Breaking existing code
**Mitigation**: Maintain backward compatibility via delegation methods

### Risk 2: Performance impact from lazy-loaded managers
**Mitigation**: Use `@property` with caching (shown above)

### Risk 3: Complex refactoring across codebase
**Mitigation**: Phased approach with backward compatibility

## Considerations for Future

### Option: Extract to separate models (more aggressive)

For a more aggressive refactoring, could create separate models:

```python
class CharacterAbilities(models.Model):
    character = models.OneToOneField('Human', on_delete=models.CASCADE)
    alertness = models.IntegerField(default=0)
    # ... all abilities

class CharacterAttributes(models.Model):
    character = models.OneToOneField('Human', on_delete=models.CASCADE)
    strength = models.IntegerField(default=1)
    # ... all attributes
```

**Not recommended because**:
- Adds join overhead to most queries
- Attributes/abilities are truly core to the character concept
- Would require massive migration effort
- No clear benefit over current approach

## Conclusion

The recommended refactoring:
1. **Reduces inheritance from 7 to 4 parent classes**
2. **Extracts composition-like functionality to proper managers**
3. **Maintains backward compatibility**
4. **Low risk, high maintainability gain**

This approach balances pragmatism with good design principles. The remaining mixins (AttributeBlock, AbilityBlock, HealthBlock, Character) are appropriate uses of inheritance for shared data fields.
