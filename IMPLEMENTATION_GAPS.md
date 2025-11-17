# Implementation Gaps Summary

Quick reference for what needs to be completed in the codebase.

## Critical Issues (Must Fix)

### 1. DEMON Game Line - Completely Unimplemented
**Status:** Models exist but no UI/admin functionality

**Missing Components:**
- Admin registration in `/home/user/tg/characters/admin.py`
- Views in `/home/user/tg/characters/views/demon/`
- URL patterns in `/home/user/tg/characters/urls/demon/`
- Templates in `/home/user/tg/characters/templates/characters/demon/`

**Models needing implementation (9 character models, 1 item model):**
- Characters: Demon, DtFHuman, DemonFaction, DemonHouse, Visage, Lore, Pact, Thrall, Thorn
- Items: Relic

**What to do:**
1. Add admin registration for all Demon models to `characters/admin.py`
2. Create view classes in `characters/views/demon/` following Mage pattern:
   - DemonCreateView, DemonDetailView, DemonUpdateView
   - DtFHumanCreateView, DtFHumanDetailView, DtFHumanUpdateView
   - List/detail views for traits: Visage, Lore, Pact, Thrall, Thorn
3. Add URL patterns in `characters/urls/demon/` with create.py, update.py, detail.py, index.py
4. Create templates in `characters/templates/characters/demon/` following gameline pattern

---

### 2. Wraith Locations - Partial Implementation
**Status:** Models exist but missing admin/views/templates

**Missing Components:**
- Admin registration for Haunt, Necropolis
- Views for Haunt and Necropolis
- Templates for Haunt and Necropolis

**Models:**
- Haunt, Necropolis

**What to do:**
1. Add to `locations/admin.py`:
   ```python
   @admin.register(Haunt)
   class HauntAdmin(admin.ModelAdmin):
       list_display = ("name", "parent")
   
   @admin.register(Necropolis)
   class NecropolisAdmin(admin.ModelAdmin):
       list_display = ("name",)
   ```

2. Create views in `locations/views/wraith/` (if not already present)
3. Create templates in `locations/templates/locations/wraith/haunt/` and `.../necropolis/`

---

### 3. Game App Models - Limited Admin Coverage
**Status:** Models are functional but hidden from admin

**Missing Components:**
- Admin registration: Journal, JournalEntry

**What to do:**
1. Add to `game/admin.py`:
   ```python
   @admin.register(Journal)
   class JournalAdmin(admin.ModelAdmin):
       list_display = ("character",)
   
   admin.site.register(JournalEntry)
   ```

---

## Medium Priority Issues

### 4. Core App - HouseRule Not Exposed
**Status:** Model exists, no views/admin customization

**What to do:**
- Add basic create/update/detail views (or leave admin-only)

### 5. Game App - XP Request Management
**Status:** Models exist with forms, limited UI

**What to do:**
- Create views for WeeklyXPRequest approval workflow
- Create views for StoryXPRequest management
- Consider admin customization for better UX

---

## Low Priority Enhancements

### 6. Wraith Models - Additional List Views
- Arcanos could use a list view
- Other Wraith trait models might benefit from organization

### 7. Vampire Game Line - Minimal Implementation
- Currently only has VtMHuman
- Could benefit from expanded traits/powers if added to models

---

## Implementation Checklist

### For Demon Game Line:
```
Characters:
  [ ] Register Demon in admin.py
  [ ] Register DtFHuman in admin.py
  [ ] Register DemonFaction in admin.py
  [ ] Register DemonHouse in admin.py
  [ ] Register Visage in admin.py
  [ ] Register Lore in admin.py
  [ ] Register Pact in admin.py
  [ ] Register Thrall in admin.py
  [ ] Register Thorn in admin.py

Views:
  [ ] Create characters/views/demon/ directory
  [ ] Create demoncharacter.py with Demon views
  [ ] Create dtfhuman.py with DtFHuman views
  [ ] Create trait views for Visage, Lore, Pact, Thrall, Thorn
  [ ] Create __init__.py with imports

URLs:
  [ ] Create characters/urls/demon/ directory
  [ ] Create create.py, update.py, detail.py, index.py
  [ ] Add to characters/urls/__init__.py

Templates:
  [ ] Create characters/templates/characters/demon/ directory
  [ ] Create subdirs: demon, dtfhuman, visage, lore, pact, thrall, thorn
  [ ] Create form.html, detail.html, list.html for each
  [ ] Create chargen.html for DtFHuman

Items:
  [ ] Register Relic in items/admin.py
  [ ] Consider views/templates for demon items
```

### For Wraith Locations:
```
Admin:
  [ ] Register Haunt in locations/admin.py
  [ ] Register Necropolis in locations/admin.py

Views:
  [ ] Check if locations/views/wraith/ exists
  [ ] Create or update haunt.py
  [ ] Create or update necropolis.py

Templates:
  [ ] Create locations/templates/locations/wraith/haunt/
  [ ] Create locations/templates/locations/wraith/necropolis/
  [ ] Create form.html, detail.html, list.html for each
```

### For Game App:
```
Admin:
  [ ] Register Journal in game/admin.py
  [ ] Register JournalEntry in game/admin.py
```

---

## File References

**Main Admin Files:**
- `/home/user/tg/characters/admin.py` - Character models admin
- `/home/user/tg/items/admin.py` - Item models admin
- `/home/user/tg/locations/admin.py` - Location models admin
- `/home/user/tg/game/admin.py` - Game models admin
- `/home/user/tg/core/admin.py` - Core models admin
- `/home/user/tg/accounts/admin.py` - Account models admin

**View Pattern Examples:**
- Mage pattern: `/home/user/tg/characters/views/mage/*.py`
- Werewolf pattern: `/home/user/tg/characters/views/werewolf/*.py`
- Items pattern: `/home/user/tg/items/views/mage/*.py`

**URL Pattern Examples:**
- Characters: `/home/user/tg/characters/urls/mage/*.py`
- Items: `/home/user/tg/items/urls/mage/*.py`
- Locations: `/home/user/tg/locations/urls/mage/*.py`

**Template Pattern Examples:**
- Characters: `/home/user/tg/characters/templates/characters/mage/`
- Items: `/home/user/tg/items/templates/items/mage/`
- Locations: `/home/user/tg/locations/templates/locations/mage/`

---

## Notes

1. **Demon models are production-ready in database** - they're just not exposed in UI/admin
2. **Polymorphic pattern is established** - new implementations should follow Mage or Werewolf pattern
3. **Template inheritance works** - base templates in `core/` extend to gamelines
4. **Admin registration is straightforward** - most models just need `admin.site.register()`
5. **No database migrations needed** - just UI layer additions

---

## Testing

After implementation, test with:
```bash
pytest characters/tests/demon/
pytest items/tests/demon/
pytest locations/tests/wraith/
pytest game/tests/
```

