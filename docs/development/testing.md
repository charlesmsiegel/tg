# Testing

This page explains how the test suite is built and run: the custom test runner and the
test database, running all or part of the suite, parallel runs, browser tests, where
tests live, the shared helpers, the guard tests that hold the architecture in place, and
pytest and coverage. It is for anyone changing code in this repository, human or agent.

## Running tests

`python manage.py test` is the supported way to run the suite. The runner is
`tg.test_runner.LocalMigrationTestRunner` (`TEST_RUNNER` in
[`tg/settings/base.py`](../../tg/settings/base.py)), a subclass of Django's
`DiscoverRunner`, so every standard `manage.py test` option works.

```bash
python manage.py test                                    # everything
python manage.py test characters                         # one app
python manage.py test characters.tests.models.vampire    # one package
python manage.py test core.tests.test_query_budgets      # one module
python manage.py test core.tests.test_query_budgets.QueryBudgetTest                # one class
python manage.py test core.tests.test_query_budgets.QueryBudgetTest.test_index_within_ceiling
python manage.py test characters -k chargen              # names matching a pattern
python manage.py test --parallel                         # one worker per CPU core
python manage.py test --parallel 4 --failfast -v 2
```

Tests run with the development settings unless `DJANGO_ENVIRONMENT` says otherwise. The
settings package calls `load_dotenv()`, so a `.env` file affects tests too, including a
`DJANGO_ENVIRONMENT` line in it. See
[Configuration](../getting-started/configuration.md#envexample).

## How the test database is built

The local apps (`accounts`, `characters`, `core`, `game`, `items`, `locations`) keep only
`migrations/__init__.py` in git; their migration files are generated per install and
ignored (see [Schema migrations](../architecture/schema-migrations.md)). A plain
`DiscoverRunner` would run `migrate`, find no migrations for those apps and create no
tables for them.

`LocalMigrationTestRunner.setup_databases` ([`tg/test_runner.py`](../../tg/test_runner.py))
fixes that before the test database is created. For every installed app whose code lies
under `BASE_DIR` and whose `migrations/` directory holds no `.py` file other than
`__init__.py`, it sets `MIGRATION_MODULES[app_label] = None`. Django then treats the app
as unmigrated and creates its tables directly from the current models (the "syncdb"
path). `tg_schema` has real migrations and runs them as usual; they find every column
already present and change nothing. `widgets` has no models.

Consequences:

- Tests always see the current models; you never need `makemigrations` to run them.
- If you have generated migrations locally (`makemigrations`, `update.sh`,
  `setup_db.sh`), the runner leaves those apps alone and applies your local migration
  files instead. Keep them current (`python manage.py makemigrations`) or tests run
  against a stale schema.

The test database is a file, `db_test.sqlite3` in the repository root
(`DATABASES["default"]["TEST"]["NAME"]`), not an in-memory database. Django creates it at
the start of a run and deletes it at the end; `--keepdb` keeps it for the next run. It is
listed in [`.gitignore`](../../.gitignore). `ATOMIC_REQUESTS = True` applies in tests as
it does in the site.

### Parallel runs

With `--parallel`, Django builds `db_test.sqlite3` once and copies it for each worker as
`db_test_1.sqlite3`, `db_test_2.sqlite3` and so on (Django's SQLite backend inserts the
worker number before the extension). The copies are deleted when the run ends, unless
you pass `--keepdb`; an interrupted run leaves them behind, and the next run overwrites
them. `.gitignore` ignores all of them (`db_test*.sqlite3` and their `-journal` files).

Tests that need exclusive resources are written to work in parallel workers: the scene
chat browser test starts its Daphne server with `subprocess` rather than
`multiprocessing` because parallel workers are daemonic processes.

### Tests that skip on SQLite

Five test classes in
[`characters/tests/integration/test_integration.py`](../../characters/tests/integration/test_integration.py)
(`TestCharacterConstraints`, `TestAttributeConstraints`, `TestAbilityConstraints`,
`TestWillpowerConstraints`, `TestAgeConstraints`) are decorated
`@skipIf(USING_SQLITE, "SQLite does not enforce check constraints")`. With the project's
SQLite configuration they always skip.

## Browser tests

A few tests drive a real browser. They skip, rather than fail, when the browser or
driver is missing, so a plain `python manage.py test` passes without them.

| Test module | Driver | Server | What it covers |
|-------------|--------|--------|----------------|
| [`characters/tests/browser/test_chargen_interactive.py`](../../characters/tests/browser/test_chargen_interactive.py) | Playwright, Chromium | `StaticLiveServerTestCase` | Interactive (htmx and Alpine) Vampire character creation. |
| [`characters/tests/browser/test_chargen_priority.py`](../../characters/tests/browser/test_chargen_priority.py) | Playwright, Chromium | same base class | The PRI/SEC/TER priority picker and clickable dots in character creation (Mage and Vampire). |
| [`game/tests/browser/test_scene_chat.py`](../../game/tests/browser/test_scene_chat.py) | Playwright, Chromium | Daphne in a child process on the test database | Live scene chat over websockets and the HTTP fallback. |
| [`widgets/tests/test_static_assets_browser.py`](../../widgets/tests/test_static_assets_browser.py) | Chromium run directly (`--headless=new --dump-dom`), no Playwright, no database | a local `http.server` | The widget JavaScript in `widgets/static/widgets/`. |
| `FunctionalTest` subclasses in [`core/tests/views/test_home.py`](../../core/tests/views/test_home.py) | Selenium, Firefox (headless via `MOZ_HEADLESS=1`) | `LiveServerTestCase` | Home page flows. |

### Setting them up

- **Playwright tests** need the `playwright` Python package, which is not in
  [`requirements.txt`](../../requirements.txt) (`pip install playwright`), and a Chromium
  binary. `chromium_binary()` in `test_chargen_interactive.py` takes the first existing
  file among: `$TG_BROWSER_BINARY`, `/opt/pw-browsers/chromium-*/chrome-linux/chrome`
  (newest first), and `chromium` or `chromium-browser` on `PATH`. Without the package the
  tests skip with "Install the playwright package to run browser tests"; without a binary,
  with "Set TG_BROWSER_BINARY to a Chromium binary". The test modules ask you not to run
  `playwright install`; point `TG_BROWSER_BINARY` at an existing Chromium instead.
- **The widget browser test** looks for `$TG_BROWSER_BINARY`, then `chromium`,
  `chromium-browser` and `google-chrome` on `PATH`, then the standard Chrome and Edge
  paths on Windows. It can also run on its own:
  `python -m widgets.tests.test_static_assets_browser`.
- **The Selenium tests** skip with "Firefox WebDriver unavailable" when Firefox or
  geckodriver cannot start.

```bash
pip install playwright
TG_BROWSER_BINARY=/usr/bin/chromium python manage.py test characters.tests.browser game.tests.browser
```

The Playwright tests set `DJANGO_ALLOW_ASYNC_UNSAFE=true` in their process, because
Playwright's sync API runs an event loop in the test thread while the tests make ORM
calls. The chargen browser tests raise `CHARGEN_PARTIAL_LIMIT` with `override_settings`
so a walkthrough is not throttled.

## Where tests live

Each app has a `tests/` package that mirrors the source tree. Every test directory is a
package (`__init__.py`; only the JSON `fixtures/` folders are not), and Django's runner
discovers files named `test*.py`.

| Source | Test |
|--------|------|
| `characters/models/vampire/vampire.py` | `characters/tests/models/vampire/test_vampire.py` |
| `characters/forms/mage/...` | `characters/tests/forms/mage/test_*.py` |
| `items/views/mage/...` | `items/tests/views/mage/test_*.py` |
| `locations/models/wraith/...` | `locations/tests/models/wraith/test_*.py` |
| `game/consumers.py` | `game/tests/consumers/` |
| `tg_schema/migrations/NNNN_name.py` | `tg_schema/tests/test_*.py` |

Common subpackages: `models/`, `forms/`, `views/`, `urls/`, `integration/`,
`services/`, `templatetags/`, `browser/`, and in `core/tests/` also `security/`,
`permissions/`, `middleware/`, `mixins/`. Cross-cutting and guard tests sit directly in
`<app>/tests/`. Every change ships its tests in the matching place; a new route also
needs a security test (under the app's tests or `core/tests/security/`).

## Helpers

| Helper | Use it for |
|--------|------------|
| [`core/tests/template_fixtures.py`](../../core/tests/template_fixtures.py) | `seed()` creates one approved instance of every concrete character, item and location model (plus the reference rows they need), a storyteller (`fixture_st`, superuser), a player, a chronicle and a scene with posts, and returns a `Fixtures` dataclass (`st`, `player`, `chronicle`, `scene`, `objects` by model label, `skipped` with the reason for each model it could not create). `create_instance(model, cache, **overrides)` fills every required field generically. `fixture_pages(fixtures)` returns `{slug: url}` for every fixture detail and edit page, every argument-free list page, the character index and the scene. The render smoke test, the query budgets and `scripts/template_screenshots.py` all use it. |
| [`core/tests/action_audience.py`](../../core/tests/action_audience.py) | `ActionAudienceMixin` creates the standard audience for action endpoints in `setUp`: owner, another player, an ST of this chronicle and gameline, an ST of the chronicle for another gameline, an ST of another chronicle, staff and anonymous (`AUDIENCE`). Set `gameline_code` on the subclass. |
| [`characters/tests/utils.py`](../../characters/tests/utils.py) | `human_setup()`, `vampire_setup()`, `werewolf_setup()`, `mage_setup()`, `wraith_setup()`, `changeling_setup()` create the reference rows (attributes, abilities, backgrounds, tribes, spheres...) a gameline's forms and character creation need. |
| `characters/tests/fixtures/chargen_order.json`, `core/tests/fixtures/model_routes.json` | Golden files compared by `characters/tests/test_chargen_registry.py` and `core/tests/test_model_registry.py`. |

A page test with the shared fixtures (the pattern `test_query_budgets.py` uses):

```python
from django.test import TestCase

from core.tests.template_fixtures import seed


class ScenePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fixtures = seed()

    def test_scene_renders_for_the_storyteller(self):
        self.client.force_login(self.fixtures.st)
        response = self.client.get(self.fixtures.scene.get_absolute_url(), follow=True)
        self.assertEqual(response.status_code, 200)
```

`seed()` builds a large object graph; call it once per class in `setUpTestData`, not in
`setUp`.

## Guard tests

Some tests do not test a feature; they stop the architecture from drifting. They fail
when a rule is broken anywhere in the code base. Change their allowlists, ceilings or
baselines only on purpose, in the same change, and give the reason in the commit
message.

| Test | Rule it enforces |
|------|------------------|
| [`core/tests/test_query_budgets.py`](../../core/tests/test_query_budgets.py) | **Query ceilings**: `SHEET_CEILINGS` gives the maximum number of queries for the detail page of every concrete character model (measured as the fixture storyteller on `seed()` data); `SCENE_CEILING` and `INDEX_CEILING` cover the scene page and the character index. Every character model must have a ceiling. **Scaling** tests assert that a sheet costs the same with more specialties, the scene page the same with more posts, and the index and chronicle pages the same with more grouped characters (the N+1 patterns). A page that legitimately needs more queries gets a reviewed ceiling change. |
| [`core/tests/test_template_policy.py`](../../core/tests/test_template_policy.py) | Over the templates of `accounts`, `characters`, `core`, `game`, `items` and `locations`: the number of inline `style="` attributes may not exceed `INLINE_STYLE_BUDGET` (3, all in the password-reset e-mail template, because mail clients need inline styles); `<style>` blocks may only appear in `STYLE_BLOCK_TEMPLATES`; no template may sit more than `MAX_EXTENDS_DEPTH` (5) `{% extends %}` hops below its root. Put styles in `core/static/core/tl/tl.css`. |
| [`core/tests/test_template_render_smoke.py`](../../core/tests/test_template_render_smoke.py) | Every fixture page renders with real objects (`EXPECTED_ERRORS` lists the known exceptions). |
| [`core/tests/test_routed_templates.py`](../../core/tests/test_routed_templates.py) | Every routed page's template and each template it extends or includes exists (`KNOWN_MISSING` lists the exceptions). |
| [`core/tests/security/test_route_policies.py`](../../core/tests/security/test_route_policies.py) | Every project URL has a reviewed policy in `core/route_policy_manifest.py`. See [Authorization](../architecture/authorization.md). |
| [`core/tests/test_action_guard.py`](../../core/tests/test_action_guard.py) | Views do not pick an action from POST keys, and detail views do not handle POST. |
| [`characters/tests/test_view_rules_guard.py`](../../characters/tests/test_view_rules_guard.py) | Views never route an invalid form into `form_valid`. |
| [`core/tests/test_tl_css.py`](../../core/tests/test_tl_css.py) | Every block in `tl.css` is closed, so a bad merge cannot swallow later rules into an `@media` block. |
| [`core/tests/test_htmx.py`](../../core/tests/test_htmx.py) | The htmx helpers, and the SRI hashes of the vendored libraries in `source_static/vendor/` match the bytes and `VENDOR.md`. |
| [`tg_schema/tests/test_schema_helpers.py`](../../tg_schema/tests/test_schema_helpers.py) | `tg_schema` migrations import no app model and survive a later rename or removal. See [Schema migrations](../architecture/schema-migrations.md). |
| [`core/tests/test_dead_code_removed.py`](../../core/tests/test_dead_code_removed.py) | Deleted code stays deleted. |

## pytest

`pytest` and `pytest-django` are installed by `requirements.txt`, but the repository has
no pytest configuration: `pytest.ini` is listed in `.gitignore` and `pyproject.toml` has
no `[tool.pytest]` section. pytest-django also does not use `TEST_RUNNER`, so the local
apps' tables are not created the way `LocalMigrationTestRunner` creates them. If you run
pytest, pass the settings module and disable migrations so every table is built from the
models:

```bash
pytest --ds=tg.settings --nomigrations core/tests/test_query_budgets.py
```

`manage.py test` remains the reference: when the two disagree, trust `manage.py test`.

## Coverage

`coverage` is in `requirements.txt`; the repository has no coverage configuration.

```bash
coverage run manage.py test
coverage report
coverage html          # writes htmlcov/, which is gitignored
```

Run coverage without `--parallel`: without a configuration that enables coverage's
multiprocessing support, the worker processes are not measured.

## See also

- [Code style](code-style.md)
- [Schema migrations](../architecture/schema-migrations.md)
- [Authorization](../architecture/authorization.md)
- [Front end](../architecture/frontend.md)
- [`tg/` project package](../../tg/README.md)
- [Local development](../getting-started/local-development.md)
