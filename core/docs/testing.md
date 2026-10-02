# Core tests

This page describes the tests in [`core/tests/`](../tests/): the unit tests for the core
modules and the project-wide guard tests that live here because they protect rules every
app follows (route policies, template policy, query budgets, action endpoints). It also
covers the shared fixtures other apps import. For how to run tests and the general
conventions see [testing](../../docs/development/testing.md).

## Running

```bash
python manage.py test core                          # every core test
python manage.py test core.tests.security           # route policy and access tests
python manage.py test core.tests.test_query_budgets # one module
```

The project's test runner is `tg.test_runner.LocalMigrationTestRunner` (see
[test runner](../../tg/docs/test-runner.md)): app tables are created from the models
because the apps have no migration files.

## Layout

| Path | Covers |
|------|--------|
| `models/` | `Model`, `ModelQuerySet`/`ModelManager`, `URLMethodsMixin`, `ValidatedSaveMixin`, the rating base classes |
| `permissions/` | `PermissionManager` roles and status rules, `filter_queryset_for_user` results and SQL, `ObjectPermissions` snapshots, and a deployment check suite (`test_permissions_deployment.py`) |
| `security/` | Route policies and access to real views (below) |
| `mixins/` | Every mixin in `core/mixins.py` |
| `views/` | Core views: home, books, languages, news, house rules, character templates, errors, generic views, the reference-view factory, Spread pages, mass-assignment protection |
| `services/` | `ApprovalService` (including the model hooks and the Chantry flow), `ChronicleDataService` |
| `templatetags/` | `tl`, `dots`, `field`, `get_specialty` (`test_includes.py`), `json_filters`, `object_actions`, `permissions`, `sanitize_text` |
| `forms/`, `widgets/` | Character template and language forms, `AutocompleteTextInput` |
| `middleware/` | `AuthErrorHandlerMiddleware` |
| `integration/` | Permission behaviour across roles, and transaction behaviour |
| `urls/` | URL namespaces |
| `test_*.py` at the top level | One module each for `actions`, `ajax`, `cache`, `context_processors`, `htmx`, `linked_stat`, `model_registry`, `template_resolution`, `validators`, `xp_utils`, management commands and settings, plus the guards below |

## Security tests

[`security/`](../tests/security/) tests authorization end to end:

| Module | Asserts |
|--------|---------|
| `test_route_policies.py` | Every project URL and registry action has exactly one policy (manifest or registry, never both); an undeclared view is refused; `PUBLIC_READ` views define no `post`, `put`, `patch` or `delete`; every `ROUTER` over a player-object model authorizes before handing off |
| `test_scoped_roles.py` | Storyteller roles are scoped to chronicle and gameline |
| `test_object_workflow.py` | Submit, return and approve through the real endpoints |
| `test_object_st_write.py` | `OBJECT_ST_WRITE` adds a scoped-storyteller requirement to the `OBJECT_WRITE` checks |
| `test_object_list_discovery.py` | Public list pages come from the route policy, independently of the list view's mixins |
| `test_reference_writes.py` | Anonymous users and players cannot create or update reference data |
| `test_index_redirects.py` | Type selection is a GET resolved only through seeded types and registries |

When you add a view, add its policy to the manifest; `test_route_policies.py` fails
until you do. See [permissions and policies](permissions-and-policies.md#declaring-a-policy-for-a-new-view).

## Template and frontend guards

| Module | Asserts |
|--------|---------|
| `test_template_policy.py` | Inline `style="..."` attributes across app templates stay within `INLINE_STYLE_BUDGET` (3, all in the password-reset e-mail); `<style>` blocks only in `STYLE_BLOCK_TEMPLATES`; no template more than `MAX_EXTENDS_DEPTH` (5) `{% extends %}` hops deep |
| `test_routed_templates.py` | Every template a routed view (or a `DictView` target) names, and every constant `{% extends %}`/`{% include %}` it reaches, exists and compiles. `KNOWN_MISSING` (empty) is the allowlist |
| `test_template_render_smoke.py` | Every fixture page (detail and edit page of one object per concrete model, every argument-free list page, the character index, the scene page) renders. `EXPECTED_ERRORS` (empty) is the allowlist |
| `test_tl_css.py` | `tl.css` braces are balanced, so an unclosed `@media` block cannot swallow later rules |
| `test_htmx.py` | htmx helpers; each vendored script in `source_static/vendor/` matches its SRI hash in `core/includes/interactive_scripts.html` and ships its licence; the htmx config disables `eval` and injected styles |
| `test_cache_per_visitor.py` | Cached pages are never served to a different visitor |

Lower `INLINE_STYLE_BUDGET` when you remove inline styles; never raise it.

## Query budgets

[`test_query_budgets.py`](../tests/test_query_budgets.py) logs in as the fixture
storyteller and counts queries per page:

- **Ceilings**: `SHEET_CEILINGS` maps every concrete character model label to the
  maximum number of queries its detail page may run; `SCENE_CEILING` and `INDEX_CEILING`
  cover the scene page and `/characters/index/`. A new character model must be added to
  `SHEET_CEILINGS` (`test_every_character_model_has_a_ceiling`).
- **Scaling**: a sheet costs the same with more specialties, the scene page the same with
  more posts, the character index and the chronicle page the same with more grouped
  characters. These catch N+1 patterns.

If a change legitimately needs more queries, raise the ceiling in the same change and
say why in review. Otherwise fix the query (`select_related`, `prefetch_related`,
`prepare_permission_objects`).

## Action and code guards

| Module | Asserts |
|--------|---------|
| `test_action_guard.py` | No view module in the project apps chooses an action by testing for a posted key (`"approve" in request.POST`); routed `DetailView`s do not handle POST. Give each action its own endpoint (see [action endpoints](views.md#action-endpoints)) |
| `test_dead_code_removed.py` | Removed modules, templates, URL names and dependencies stay removed |
| `test_import_graph.py` | Every import in the project packages sits at module scope (the only exceptions are the signal registrations in `AppConfig.ready()`), and the module-level import graph has no cycles. Break a cycle structurally (string model references, reverse accessors, `apps.get_model()`, a service) rather than by deferring an import; see [code style](../../docs/development/code-style.md#imports) |
| `test_dead_code_heuristics.py`, `test_find_dead_code_script.py` | The dead-code finder in `scripts/` (`find_dead_code.py` runs in a subprocess because it repoints the database when imported) |
| `test_model_registry.py` | Item and location registry contracts: every concrete model registered, every action with a policy and messages, route names and paths unchanged against `fixtures/model_routes.json` |

## Helpers for other apps

### `template_fixtures.seed()`

[`core/tests/template_fixtures.py`](../tests/template_fixtures.py) builds one deterministic
data set used by the render smoke test, the query budgets and
`scripts/template_screenshots.py`:

- a superuser storyteller (`fixture_st`) and a player (`fixture_player`), a chronicle
  headed by the storyteller with an `STRelationship`;
- one approved instance of every concrete model in `characters`, `items`, `locations`,
  `core` and `game` that has a URL, owned by the player and placed in the chronicle,
  with required fields filled generically and a few ratings and specialties set;
- a scene with two characters and six posts.

It returns a `Fixtures` dataclass (`st`, `player`, `chronicle`, `scene`, `objects` keyed
by model label, `skipped` with the reason for any model that could not be created).
`fixture_pages(fixtures)` returns `{slug: url}` for every page the smoke test renders.

```python
from core.tests.template_fixtures import seed

class MyPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fixtures = seed()
```

### `action_audience.ActionAudienceMixin`

[`core/tests/action_audience.py`](../tests/action_audience.py) creates, in `setUp`, the
seven users every action endpoint is tested against (`AUDIENCE`): `owner`, `player`,
`st` (storyteller of this chronicle and gameline), `other_line_st` (this chronicle,
another gameline), `other_chronicle_st`, `staff` and `anonymous`, plus `self.chronicle`
and `self.other_chronicle`. Set `gameline_code` on the test class; call
`self.login_as(name)` to switch users. The character and game action tests use it.

## See also

- [Testing guide](../../docs/development/testing.md)
- [Permissions and policies](permissions-and-policies.md)
- [Templates and static files](templates-and-static.md)
- [Test runner](../../tg/docs/test-runner.md)
- [`core/tests/`](../tests/)
