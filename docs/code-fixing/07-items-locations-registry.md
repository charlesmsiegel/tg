# Task: Design a model-type registry that generates item and location CRUD views and URLs in `tg` (Step 7)

You are designing, **not implementing**, a replacement for roughly 270 hand-written, mostly identical view classes and about 250 hand-written routes in the `items` and `locations` apps. The replacement is a declarative registry: one declaration per model generates its views, URLs, polymorphic detail dispatch and index menus. The repository is `charlesmsiegel/tg`: Django 5.2 with django-polymorphic 4.1, a World of Darkness manager with 8 gamelines. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/model-standards/SKILL.md` (it describes the current per-model view/form/URL conventions you'll be replacing or codifying), `.claude/skills/tg-permissions/SKILL.md` and `.claude/skills/tg-testing/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/`. Read the Step 0 authorization design if it exists: each registry entry must declare its permission policy, deny by default. Write:
  - `docs/superpowers/specs/2026-09-25-items-locations-registry-design.md`
  - `docs/superpowers/plans/2026-09-25-items-locations-registry.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed.
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## Current state

- **Boilerplate** (Reported):
  - `items/views/` has 113 classes (29 Detail, 28 Create, 28 Update, 27 List). 101 of them (89%) contain only `model`, `form_class`, `template_name`, `fields`, `ordering` or messages, a placeholder `get_form`, or `get_success_url`.
  - `locations/views/` has 155 classes, of which 123 (79%) are that trivial; the rest are mostly the multi-step chantry and freehold flows.
  - There are 63 Create/Update pairs; 44 repeat an identical inline `fields = [...]` (e.g. `locations/views/wraith/haunt.py:~19-28` and `~37-46`). There are 104 `fields = [` literals in total.
- **An unused factory.** `core/views/reference.py` (`create_reference_views`, `ReferenceViewSet`) exists and is only re-exported from `core/views/__init__.py`. **Confirmed.** Evaluate adopting or extending it.
- **URLs** (Reported):
  - Gameline packages are mounted by a loop over `GameLine.URL_PATTERNS` (`items/urls/__init__.py:~13-24`, `locations/urls/__init__.py:~13-24`). It wraps the import in `except (ImportError, AttributeError): pass`, so a broken import silently drops a whole gameline's URLs.
  - Per-model routes are written by hand in `create.py`, `update.py`, `detail.py` and `index.py`: about 112 routes for items and 143 for locations.
  - 116 routes use an untyped `<pk>`, so `/items/foo/` fails with a 500 instead of a 404.
  - There are 62 no-op `app_name` assignments (Step 1 may remove them).
  - Paths are inconsistent (`create/meleeweapon/` vs `melee_weapon/<pk>/`).
- **Model URLs.**
  - 11 item models and 18 location models hand-write `get_absolute_url`, `get_update_url` and `get_creation_url` (Reported).
  - `URLMethodsMixin` (`core/models.py:104-172`) already generates these, but only three character reference models use it (Resonance, Derangement, Archetype). **Confirmed.**
- **Polymorphic detail dispatch.**
  - `GenericItemDetailView` (`items/views/core/__init__.py:~88-133`) and `GenericLocationDetailView` (`locations/views/core/__init__.py:~68-122`) are `DictView`s (`core/views/generic.py:43-75`). They map the class attribute `type` to a detail view and are mounted at `/<pk>/`.
  - Reported: the object is loaded twice, and `view_mapping` is a property rebuilt on every request.
- **`type` collisions** (**Confirmed**):
  - `items/models/mage/artifact.py:9` and `items/models/wraith/artifact.py:8` both declare `type = "artifact"`.
  - `items/models/wraith/relic.py:8` and `items/models/demon/relic.py:10` both declare `type = "relic"`.

  Reported: as a result, WraithArtifact and DemonRelic 404 through `/items/<pk>/`, and the mapping keys `"wraith_artifact"` and `"demon_relic"` can never match. `material` and `medium` are missing from the mapping.
- **The list of types is maintained in about 5 places** (Reported):
  - model `type` attributes;
  - the DictView mappings;
  - `ItemIndexView.items` / `LocationIndexView.locs`, which are dead;
  - `ObjectType` database rows (seeded by `populate_db/`);
  - the index-view redirect if/elif chains, plus a fuller 9-gameline map in `game/views.py` `ChronicleDetailView._get_create_redirect_url` (`~:184-213`).
- **Other drift** (Reported):
  - 11 location views set `success_message` without `MessageMixin`, so the messages never show.
  - Only 3 create views set `owner`.
  - Detail views mostly lack `ViewPermissionMixin`.
  - Step 0 closes the auth gaps. Your registry must make them impossible to reintroduce.

## What the design must deliver

1. **The registry API.** One declaration per model: model, form (or generated form fields), gameline, URL slug, templates (with fallback to shared templates), permission policy per action, list ordering, and index menu label and grouping. Show 3–4 real entries: a trivial item (Weapon), a mage item with extra logic (Wonder), a trivial location, and one with custom views.
2. **What is generated from it:** Detail/List/Create/Update views (with hooks for custom logic), URL patterns (typed converters, failing loudly on import errors), `get_absolute_url` and related methods (or adoption of `URLMethodsMixin`), the polymorphic detail dispatch, and index menus and redirects.
3. **Backward compatibility:** keep existing URL **names** so `reverse()` and `{% url %}` calls keep working. Inventory them with a script and show that the generated set is a superset. State any path changes and whether redirects are needed.
4. **A fix for the `type` collisions.** Include any data implications: check whether `type` is stored anywhere, the `ObjectType` rows, and `populate_db` scripts.
5. **Escape hatches** for non-trivial views (chantry and freehold creation flows, the Wonder form), and an explicit list of which classes stay hand-written.
6. **Tests:** a URL-name parity test; per-model smoke tests generated from the registry (list, detail, create, update for an authorized user; denial for an unauthorized one); and a test that every concrete Item/Location subclass is registered.
7. **PR slicing:** registry plus one gameline as the pilot, then one gameline per PR, then delete the old modules.
8. **Future reuse:** say whether character reference models (Clans, Spheres, Gifts, …) could later use the same registry, without doing it now.

## Constraints and scope

- Design only. Don't modify application code.
- Keep reference data publicly readable per CLAUDE.md. Write access follows Step 0's policy.
- Out of scope: template visual deduplication (Step 8) beyond the shared-template fallback the registry needs; characters views.
