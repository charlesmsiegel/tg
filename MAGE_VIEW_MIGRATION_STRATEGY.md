# Mage XP View - Migration Strategy

Due to the complexity of the XP approval system in `characters/views/mage/mage.py`, a phased approach is recommended:

## Current Implementation Issues

The mage XP view (lines 500-760) has complex approval logic that:
1. Uses index-based JSONField lookups
2. Handles multiple trait types (attribute, ability, sphere, arete, background, willpower, meritflaw, tenet, practice, rotes, resonance)
3. Mixes JSONField updates with database operations

## Recommended Migration Approach

### Phase 1: Create Helper Functions (Immediate)

Create helper functions to bridge old and new systems:

```python
def get_xp_request_from_index(character, index):
    """Bridge function: Get XPSpendingRequest from old-style index."""
    # Parse index: "{char_id}_{trait_type}_{trait}_{value}"
    parts = index.split("_")
    if len(parts) >= 4:
        trait_type = parts[1]
        trait = "_".join(parts[2:-1])
        value = parts[-1]

        # Find matching request
        from game.models import XPSpendingRequest
        return XPSpendingRequest.objects.filter(
            character=character,
            trait_type=trait_type,
            trait_value=value,
            approved='Pending'
        ).first()
    return None

def approve_xp_by_trait_type(character, request, trait_type, trait, value, user):
    """Approve XP and apply trait increase based on type."""
    from django.db import transaction

    with transaction.atomic():
        if trait_type == "attribute":
            att = Attribute.objects.get(name=trait)
            setattr(character, att.property_name, value)

        elif trait_type == "ability":
            abb = Ability.objects.get(name=trait)
            setattr(character, abb.property_name, value)

        elif trait_type == "background":
            trait, note = trait.replace("-", " ").split(" (")
            note = note[:-1]
            bgr = character.backgrounds.filter(bg__name=trait, note=note).first()
            bgr.rating += 1
            bgr.save()

        # ... handle other trait types

        character.save()
        request.approved = 'Approved'
        request.approved_by = user
        request.approved_at = timezone.now()
        request.save()
```

### Phase 2: Update Form Handling

Change the approval form to pass XPSpendingRequest IDs instead of index strings:

**Template Change:**
```django
<!-- Old way -->
<button name="{{ request.index }}_approve" value="Approve">Approve</button>

<!-- New way -->
<button name="approve_{{ request.id }}" value="Approve">Approve</button>
```

**View Change:**
```python
# Old way
if "Approve" in form.data.values():
    xp_index = [x for x in form.data.keys() if form.data[x] == "Approve"][0]
    index = "_".join(xp_index.split("_")[:-1])
    d = [x for x in self.object.spent_xp if x["index"] == index][0]

# New way
approve_keys = [k for k, v in form.data.items() if v == "Approve" and k.startswith("approve_")]
if approve_keys:
    request_id = int(approve_keys[0].replace("approve_", ""))
    xp_request = XPSpendingRequest.objects.get(id=request_id, character=self.object)
```

### Phase 3: Full Refactoring

Eventually refactor to use a proper form with individual approval actions per request.

## Files Requiring Updates

1. **Views (High Priority)**
   - `characters/views/mage/mage.py` (lines 500-760) - Most complex
   - `characters/views/mage/companion.py` - Similar pattern
   - `characters/views/mage/sorcerer.py` - Similar pattern
   - `characters/views/core/human.py` (lines 435-450) - Freebie handling

2. **Templates (High Priority)**
   - `characters/templates/characters/mage/mage/mage_xp_form.html`
   - `characters/templates/characters/mage/companion/companion_xp_form.html`
   - `characters/templates/characters/mage/sorcerer/sorcerer_xp_form.html`
   - All freebie_form.html templates

3. **Templates (Display Only - Lower Priority)**
   - Character detail templates that show XP history
   - Need to iterate over `character.get_xp_spending_history()` instead of `character.spent_xp`

## Implementation Status

- ✅ Models created (XPSpendingRequest, FreebieSpendingRecord)
- ✅ Helper methods added to Character/Human models
- ✅ Data migration command created
- ⚠️ Views NOT YET updated (requires careful refactoring)
- ⚠️ Templates NOT YET updated (requires coordination with view changes)

## Recommendation

Given the complexity, I recommend:

1. **Keep current implementation working** with JSONField for now
2. **Add new XP spending flow** using the new models for NEW requests
3. **Migrate existing data** using the migration command
4. **Gradually phase out** JSONField as old requests get approved
5. **Eventually remove** JSONField once all pending requests are cleared

This allows for a gradual transition without breaking existing functionality.

## Alternative: Dual System Approach

Run both systems in parallel:
- New XP requests go to XPSpendingRequest model
- Old pending requests in JSONField stay until cleared
- Views check both systems
- Eventually deprecate JSONField when it's empty

This is safer but more complex during transition period.
