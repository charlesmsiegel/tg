# Testing

What each change must test, where the tests go, and the guard tests you must keep green.
How the runner and test database work, and every command-line option, are in
[docs/development/testing.md](../../../../docs/development/testing.md).

## Running

```bash
python manage.py test                                  # whole suite
python manage.py test characters.tests.models.vampire  # one package
python manage.py test core.tests.test_query_budgets    # one module
python manage.py test --parallel                       # one worker per core
```

- The runner is `tg.test_runner.LocalMigrationTestRunner`: it builds local-app tables from
  the current models (no `makemigrations` needed) and runs the `tg_schema` migrations.
- Use `python manage.py test`, not bare `pytest`, so the runner and settings apply.
- Browser tests need the `playwright` package and a Chromium binary (`TG_BROWSER_BINARY`,
  else `/opt/pw-browsers/chromium-*/chrome-linux/chrome`); they skip without them. Never
  run `playwright install`.

## Layout

Tests mirror the source path inside the app's `tests/` package:

| Source | Test |
|--------|------|
| `characters/models/vampire/clan.py` | `characters/tests/models/vampire/test_clan.py` |
| `characters/views/vampire/clan.py` | `characters/tests/views/vampire/test_clan.py` |
| `items/forms/...` | `items/tests/forms/...` |
| `characters/services/xp_spending/...` | `characters/tests/services/...` |
| `tg_schema/migrations/0005_story_chronicle.py` | `tg_schema/tests/test_story_chronicle.py` |
| Cross-cutting access rules | `core/tests/security/` |
| Real-browser behaviour | `<app>/tests/browser/` |

Every test directory has an `__init__.py`. Use `SimpleTestCase` when no database is
touched, `TestCase` otherwise, `TransactionTestCase` for schema editors, `on_commit` or
concurrency, `StaticLiveServerTestCase` for browsers.

## What each change must test

| Change | Tests |
|--------|-------|
| Model | Creation with defaults, `__str__`, URL methods, each `clean()` rule and constraint, custom methods and querysets |
| Schema (`tg_schema`) | Adds when missing, no SQL when present, backfill result, skip when the model/field is gone ([schema-changes.md](schema-changes.md)) |
| Form | Valid data saves; each rule rejects; scoped querysets exclude other users' rows; no protected fields |
| View | Status and template for each audience (anonymous, owner, other player, scoped ST, other-chronicle ST, other-gameline ST, staff); context; redirect and message after POST |
| Action | `core.tests.action_audience.ActionAudienceMixin` audience; GET is 405; hidden subject is 404; refusal flashes and changes nothing |
| Route | Policy declared (the route test fails otherwise); a denial test per refused audience |
| Service | Success result and each refusal; nothing written on refusal; locking for point changes |
| Template | Renders in the fixture set; no policy regressions |
| Cached page | `core/tests/test_cache_per_visitor.py` case proving it is not shared between users |
| Management command | `call_command(..., stdout=StringIO())` for output, `--dry-run` writes nothing, errors raise `CommandError` |
| Bug fix | A test that fails before the fix |

## Shared fixtures and helpers

- `core.tests.template_fixtures.seed()` builds one approved instance of every concrete
  character, item and location model, the reference rows they point at, a chronicle and a
  scene with posts. The render smoke test, the query budgets and
  `scripts/template_screenshots.py` all use it. A new model must be buildable by it
  (`test_fixture_set_covers_the_models` allows only `characters.CharacterModel`,
  `characters.Rote` and `game.Journal` to be skipped).
- `core.tests.action_audience.ActionAudienceMixin` creates the seven-user audience with
  chronicles, gamelines and `STRelationship`s; set `gameline_code`.
- Create users with `User.objects.create_user(...)`; create `game.Gameline` rows named as
  in `settings.GAMELINES` when a test needs scoped ST roles.
- Cache-dependent tests override `CACHES` with `LocMemCache` and call `cache.clear()`.

## Guard tests (ratchets)

These encode the architecture. Change an allowlist, ceiling or baseline only on purpose,
in the same diff, with the reason in the commit message.

| Guard | Holds |
|-------|-------|
| `core/tests/security/test_route_policies.py` | One policy per routed view; no stale entries; `PUBLIC_READ` views read-only; routers check first |
| `core/tests/test_action_guard.py` | No POST on detail views; no dispatch on posted button names |
| `characters/tests/test_view_rules_guard.py` | `form_invalid` never calls `form_valid` |
| `core/tests/test_query_budgets.py` | `SHEET_CEILINGS` per concrete character model, `SCENE_CEILING`, `INDEX_CEILING`, and constant cost as rows grow |
| `core/tests/test_template_policy.py` | Inline-style budget, `<style>` allowlist, extends depth |
| `core/tests/test_routed_templates.py`, `test_template_render_smoke.py` | Every routed template exists; every fixture page renders |
| `characters/tests/views/core/test_shared_character_crud.py` + `shared_character_crud_baseline.json` | Character CRUD field lists and limited-form selection |
| `characters/tests/test_chargen_registry.py` + `fixtures/chargen_order.json` | Chargen step order per workflow; router coverage |
| `core/tests/test_model_registry.py` + `fixtures/model_routes.json` | Every item/location registered; route names and paths stable |
| `core/tests/test_dead_code_removed.py` | Removed modules stay removed; URL leaf modules have no `app_name` |
| `tg_schema/tests/test_schema_helpers.py` | Migrations import no app models and skip when models are gone |
| `core/tests/test_htmx.py` | Vendored scripts match `VENDOR.md` hashes |

A new character type therefore adds: a `SHEET_CEILINGS` entry, a golden
`chargen_order.json` entry (if it has a workflow), a router entry, and a baseline entry for
its CRUD views.

## Query budgets

- Measure with `django.test.utils.CaptureQueriesContext(connection)` or
  `self.assertNumQueries(n)` for a fixed count.
- For lists, assert the count does not grow with rows (add rows of types already present:
  polymorphic hydration costs one query per concrete type).

## Checklist

- [ ] Tests mirror the source path; one behaviour per test method, descriptive names.
- [ ] Every denial covered, not only the happy path.
- [ ] Guards untouched, or changed on purpose with the reason recorded.
- [ ] New model buildable by `seed()`; new sheet has a ceiling.
- [ ] The affected apps' tests pass locally.

## See also

- [docs/development/testing.md](../../../../docs/development/testing.md)
- [`tg/test_runner.py`](../../../../tg/test_runner.py), [`core/tests/template_fixtures.py`](../../../../core/tests/template_fixtures.py)
- [permissions.md](permissions.md), [schema-changes.md](schema-changes.md)
