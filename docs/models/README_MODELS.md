# Model Documentation Index

This directory contains comprehensive documentation of all models in the World of Darkness RPG Management System.

## Generated Reports

### 1. **MODEL_IMPLEMENTATION_REPORT.txt** (13KB)
Complete structural analysis with detailed implementation status for every model.

**Sections:**
- Project overview and structure
- All models organized by app and gameline  
- Admin registration status (87 registered, 11 missing)
- Views, URLs, templates status by app
- Template coverage analysis
- URL pattern organization
- Critical gaps and missing implementations
- Model metrics and statistics
- Implementation checklist for Demon gameline

**Best for:** Understanding what's missing and what needs to be done

---

### 2. **MODELS_COMPLETE_LIST.md** (10KB)
Complete inventory of all 186+ models with descriptions.

**Content:**
- Summary statistics
- Core & shared models (34 models)
- Character models by gameline (121 models)
- Item models by gameline (18 models)
- Location models by gameline (14 models)
- Models grouped by admin registration status
- Models grouped by view implementation status
- Models grouped by template coverage
- URL patterns by app

**Best for:** Finding specific models and understanding the complete inventory

---

### 3. **FILE_PATH_REFERENCE.txt** (7.8KB)
Quick reference guide with all important file paths.

**Contains:**
- Model definition file paths
- Admin file paths
- View file paths
- URL file paths
- Template file paths
- Form file paths
- Key development insights

**Best for:** Quickly navigating to relevant files

---

### 4. **IMPLEMENTATION_GAPS.md** (6.3KB)
Actionable todo list for completing incomplete implementations.

**Sections:**
- Critical issues (Demon, Wraith locations, Game app)
- Medium priority issues
- Low priority enhancements
- Implementation checklists with steps
- File references
- Development notes
- Testing instructions

**Best for:** Planning development work and tracking progress

---

## Quick Stats

| Metric | Count |
|--------|-------|
| **Total Models** | 186+ |
| **Admin Registered** | 87 (82%) |
| **Missing Admin** | 11 (18%) |
| **Full CRUD Views** | 45 models |
| **Partial CRUD** | 35 models |
| **No Views** | 11 models |
| **Complete Templates** | 107 models (95%) |
| **Missing Templates** | 11 models (5%) |

---

## Key Findings

### Models by App
- **Characters:** 121 models (65% of total)
- **Items:** 18 models (10% of total)
- **Locations:** 14 models (8% of total)
- **Game:** 15 models (8% of total)
- **Core:** 13 models (7% of total)
- **Accounts:** 1 model (1% of total)

### Models by Game Line
- **Mage:** 40 models (most complex)
- **Werewolf:** 35 models
- **Core/General:** 66 models
- **Wraith:** 12 models
- **Changeling:** 11 models
- **Vampire:** 1 model
- **Demon:** 11 models (UNIMPLEMENTED)

---

## Critical Gaps

### HIGH PRIORITY
1. **Demon Game Line** - 9 character models + 1 item model
   - Models defined but no admin registration, views, URLs, or templates
   - File: `/home/user/tg/characters/models/demon/`
   - Work: Full CRUD UI implementation needed

2. **Wraith Locations** - 2 models (Haunt, Necropolis)
   - Models defined but no admin registration, views, or templates
   - File: `/home/user/tg/locations/models/wraith/`
   - Work: Add to admin, create views and templates

3. **Game App Models** - Journal, JournalEntry
   - Models functional but not registered in admin
   - Work: Add admin registration

### MEDIUM PRIORITY
4. **Game App CRUD** - XP request workflows
5. **Core App** - HouseRule (no views)

### LOW PRIORITY
6. **Wraith** - Additional list views
7. **Vampire** - Minimal implementation
8. **Template enhancements** - Some trait models

---

## File Organization Pattern

All apps follow this structure:

```
app/
├── models/
│   ├── core/
│   ├── vampire/
│   ├── werewolf/
│   ├── mage/
│   ├── wraith/
│   ├── changeling/
│   └── demon/
├── views/
│   ├── core/
│   ├── vampire/
│   ├── werewolf/
│   ├── mage/
│   ├── wraith/
│   ├── changeling/
│   └── demon/ (MISSING)
├── urls/
│   ├── core/
│   ├── vampire/
│   ├── werewolf/
│   ├── mage/
│   ├── wraith/
│   ├── changeling/
│   └── demon/ (MISSING)
├── templates/
│   ├── app/
│   │   ├── core/
│   │   ├── vampire/
│   │   ├── werewolf/
│   │   ├── mage/
│   │   ├── wraith/
│   │   ├── changeling/
│   │   └── demon/ (MISSING)
├── forms/
├── admin.py
├── urls.py (main router)
└── views.py (if not using views/ directory)
```

---

## Polymorphic Model Pattern

The codebase uses **django-polymorphic** for inheritance:

```
core.models.Model (abstract base)
├── Character
│   └── Human
│       ├── VtMHuman (Vampire)
│       ├── WtAHuman (Werewolf)
│       ├── MtAHuman (Mage)
│       ├── WtOHuman (Wraith)
│       ├── CtDHuman (Changeling)
│       └── DtFHuman (Demon) - UNIMPLEMENTED
├── ItemModel
│   ├── Weapon
│   ├── Artifact
│   ├── Wonder
│   ├── Fetish
│   └── ...
└── LocationModel
    ├── City
    ├── Node
    ├── Chantry
    ├── Caern
    └── ...
```

---

## Development Workflow

### To add a new model implementation:

1. **Check if model exists** in `/models/` directory
   - If not, create it
   
2. **Add admin registration** in `/admin.py`
   ```python
   @admin.register(ModelName)
   class ModelNameAdmin(admin.ModelAdmin):
       list_display = ("name",)
   ```

3. **Create views** in `/views/gameline/modelname.py`
   - Follow Mage or Werewolf pattern for examples
   
4. **Add URL patterns** in `/urls/gameline/`
   - Create/update create.py, update.py, detail.py, index.py

5. **Create templates** in `/templates/app/gameline/modelname/`
   - Create form.html, detail.html, list.html

6. **Update __init__.py** files to import new views/forms

---

## Testing Your Implementation

```bash
# Run all tests
pytest

# Test specific app
pytest characters/tests/demon/
pytest items/tests/demon/
pytest locations/tests/wraith/

# Test views
pytest characters/tests/demon/test_demon_views.py

# Test models
pytest characters/tests/demon/test_demon_models.py
```

---

## Additional Resources

- **CLAUDE.md** - Project guidelines and conventions
- **PRACTICE_VIOLATIONS.md** - Known technical debt
- **SOURCES/STYLE.md** - UI/CSS styling guide

---

## Last Updated
November 17, 2025

Generated by comprehensive codebase analysis
- 186+ models identified
- 6 apps analyzed
- 6 game lines covered
- File paths verified

