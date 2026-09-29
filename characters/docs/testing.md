# Testing the characters app

This page describes the layout of [`characters/tests/`](../tests/), the helpers and golden
files the tests rely on, and the contract tests you are most likely to trip when you change
models, views or chargen. It is for developers adding or updating tests in this app. How to
run the suite, the test runner and project-wide conventions are in
[Testing](../../docs/development/testing.md).

## Running

```bash
python manage.py test characters                                  # the whole app
python manage.py test characters.tests.models.vampire             # one package
python manage.py test characters.tests.views.core.test_shared_character_crud
```

The project runner `tg.test_runner.LocalMigrationTestRunner` builds tables straight from
the models for apps that have no migration files, which includes `characters`.

## Layout

| Path | Covers |
|------|--------|
| `tests/models/<gameline>/` | One `test_<model>.py` per model module (fields, helpers, rules on the model) |
| `tests/models/core/` | `Character`, `Human`, the blocks, groups, `test_human_urls.py` (gameline URL prefixes) |
| `tests/managers/` | `BackgroundManager`, `MeritFlawManager` |
| `tests/forms/<gameline>/`, `tests/forms/core/` | Form validation, allocation, freebie and XP forms, limited forms, `LinkedNPCForm`, `NPCProfileForm` |
| `tests/views/<gameline>/` | Detail, create, update and chargen views per type and catalogue (`test_<type>_chargen.py`, `test_<type>_sheet.py`) |
| `tests/views/core/` | Shared behaviour: `test_shared_character_crud.py`, `test_shared_chargen.py`, `test_shared_spending_allocations.py`, `test_shared_forms_spread.py`, backgrounds, NPCs |
| `tests/views/` (top level) | Cross-cutting view tests: `test_auth_required.py`, `test_public_detail_authorization.py`, `test_character_actions.py`, `test_chargen_back.py`, `test_chargen_htmx.py`, `test_chargen_nojs_walkthrough.py`, `test_chargen_priority.py`, `test_known_by.py`, `test_reference_pages.py`, `test_sheet_cover_facts.py` |
| `tests/services/` | XP and freebie spending services |
| `tests/rules/` | `AllocationRule` and `PriorityRule` |
| `tests/templatetags/` | `character_edit`, `startswith`, specialty lookup |
| `tests/urls/` | Core URL patterns resolve |
| `tests/integration/` | Multi-step flows |
| `tests/browser/` | Real-browser (Playwright) tests of interactive chargen |
| `tests/test_chargen_registry.py`, `test_chargen_transitions.py`, `test_chargen_workflow.py` | Workflow registry, `advance()` / `previous_position()`, end-to-end workflow behaviour |
| `tests/test_view_rules_guard.py` | Static (AST) guard over view modules in `characters`, `items`, `locations`, `game` and `core`: `form_invalid()` never calls `form_valid()` |
| `tests/test_static_page_assets.py` | Page configuration handed to static scripts renders as inert, escaped data |
| `tests/test_utils.py` | `characters.utils` |

## Helpers

[`tests/utils.py`](../tests/utils.py) holds setup functions that create the reference rows
a test needs. `human_setup()` uses `get_or_create`; the gameline helpers call it first and
then create their own rows, several with plain `create()`, so call each gameline helper at
most once per test database state:

| Function | Creates |
|----------|---------|
| `human_setup()` | `ObjectType` `human`, the nine `Attribute` rows, Contacts and Mentor `Background`s |
| `vampire_setup()`, `wraith_setup()` | The gameline's `Background` rows |
| `werewolf_setup()` | Werewolf reference rows and sample characters (tribes, camps, Gifts and permissions, rites, totems, renown incidents, battle scars, fetishes) |
| `mage_setup()` | Mage reference rows (the Mage `Ability` and `Background` rows, Spheres, factions, Focus models, Resonance, Effects, materials and media) |
| `changeling_setup()` | The `changeling` `ObjectType`, sample `Changeling` characters, Backgrounds, kiths and other Changeling rows |

Most tests build their own rows in `setUp()` or `setUpTestData()`; call these helpers when a
test needs a full reference set.

## Golden files

Two JSON files pin behaviour that must not change by accident. Update them only after
reviewing the change they record.

### `tests/fixtures/chargen_order.json`

Maps each character `type` to the ordered list of step view paths of its workflow.
`test_chargen_registry.RegistryTests.test_all_persisted_positions_are_preserved` compares
every workflow's `view_path`s with it, checks that there is exactly one freebies step at
`workflow.freebie_step` and that every step template exists. Because saved
`creation_status` values are positions, a change here means unfinished characters need a
data migration (see [Chargen](chargen.md)).

### `tests/views/core/shared_character_crud_baseline.json`

Keyed by view path (for example `characters.views.vampire.vampire.VampireUpdateView`). Each
entry holds some of:

- `field_count` and `fields_sha256`: the number of fields and the SHA-256 of
  `"\n".join(fields)` for the view's reviewed `fields` list (duplicates removed, order kept).
- `limited_form`: the name of the class in `characters.forms.core.limited_edit` that a
  non-editor must receive.

`test_shared_character_crud.CharacterCRUDFieldContracts` checks both: the field list has not
drifted from the review (see [Forms](forms.md#update-allowlists-crud_fields)), and
`get_form_class()` returns the full form for a scoped editor and the limited form (without
`st_notes`, `owner` or `status`) for anyone else. When you deliberately change an
allowlist, recompute the entry:

```python
import hashlib
from django.utils.module_loading import import_string

fields = list(dict.fromkeys(import_string("characters.views.vampire.vampire.VampireUpdateView").fields))
print(len(fields), hashlib.sha256("\n".join(fields).encode()).hexdigest())
```

`CharacterCRUDSecurityTests` in the same file covers forged owner fields, unrelated
storytellers, retire / decease permissions and the public projection.

## Browser tests

[`tests/browser/`](../tests/browser/) drives interactive Vampire chargen and the PRI / SEC /
TER picker in Chromium through Playwright (`StaticLiveServerTestCase`). Playwright and the
browser are development-only: the tests skip when the `playwright` package or a Chromium
binary is missing. The binary comes from `TG_BROWSER_BINARY`, then Playwright's own
install, then `/opt/pw-browsers/chromium-*/chrome-linux/chrome`. The module docstring says
never to run `playwright install`.

## What to update when you change...

| Change | Tests to check or extend |
|--------|--------------------------|
| A model field or helper | `tests/models/<gameline>/test_<model>.py`; the allowlist baseline if a view's `fields` changes |
| A chargen workflow | `fixtures/chargen_order.json`, `test_chargen_registry.py`, `test_chargen_workflow.py`, the type's `test_<type>_chargen.py` |
| An allocation rule or point value | `tests/rules/test_allocation.py`, `tests/views/core/test_shared_spending_allocations.py`, `tests/views/test_chargen_priority.py` |
| A spending handler or cost | `tests/services/test_xp_spending.py`, `tests/services/test_freebie_spending.py` |
| A view's authorization | `tests/views/test_auth_required.py`, `test_public_detail_authorization.py`, and the project route-policy tests in `core` |
| A reference page | `tests/views/test_reference_pages.py`, `tests/views/test_known_by.py` |

## See also

- [Testing](../../docs/development/testing.md)
- [Chargen](chargen.md)
- [Forms](forms.md)
- [Services](services.md)
- [`tg/test_runner.py`](../../tg/test_runner.py)
