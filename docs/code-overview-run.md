# Latest code-overview rerun — 2026-10-17

Analysis source: `67d7990bc5ac00dc371a7a382e4c637acdb8e629`. Toolkit source: `eaef08c735c77861931581a170a9b4d430076a9b`. Django target: **5.2**. These source snapshots are deliberate: generated reports are committed afterward.

**The B+ goal remains unmet.** Health measures detector finding density. Theory is independent three-judge architectural judgment, not an objective acceptance test. Null measurement and ungraded JavaScript/execution coverage are not zero or successful grades.

| Unit | Health | Theory |
|---|---|---|
| accounts | F (44.0) | B (85.0) |
| characters | F (39.9) | C (75.0) |
| core | F (26.4) | C (75.0) |
| game | F (37.1) | B- (80.0) |
| items | F (43.8) | C+ (77.5) |
| locations | F (41.4) | D- (62.5) |
| tg_schema | F (23.0) | A+ (100.0) |
| widgets | F (40.3) | B- (80.0) |
| tg | F (43.6) | B- (80.0) |
| populate_db | C (75.2) | D- (62.5) |
| scripts | F (21.4) | C (75.0) |
| repository | F (38.0) | C- (70.0) |

## Changes and review boundaries

- Profile action tests use fixture authentication; password-authentication and anonymous behavior checks remain intact.
- 100 deprecated CheckConstraint keywords now use condition; all loaded model constraint serializations match the pre-change snapshot exactly, with no schema change.
- Dynamic formset attributes and conditional labels now escape plain values while retaining rendered form markup and explicitly trusted labels. Injection regressions failed before the repair.
- Eight Dynasty records reuse the stable-key catalogue loader. Original data/exports are unchanged; reload content is authoritative, preserving primary keys and character references. The nullable key/index rollout is guarded migration 0014; migrate before population. The original mutable-description reload IntegrityError was reproduced.
- Character creation choices share grouping/sorting/setup while preserving role, unknown/empty catalogue, initial/bound/prefixed form behavior. Initializer cognitive complexity falls from 40 to 2.
- Background totals use one grouped query while retaining allowed keys, order, zeros and ownership scope; the regression originally issued five queries.

## Detector corrections

Toolkit PRs [#22](https://github.com/charlesmsiegel/coding-skills/pull/22), [#23](https://github.com/charlesmsiegel/coding-skills/pull/23) and [#24](https://github.com/charlesmsiegel/coding-skills/pull/24) correct named numeric attribute values, required imported unittest/Django lifecycle hooks, and form-save receiver identity/validation claims. Missing explicit is_valid is a candidate because ModelForm.save can trigger validation through errors; custom saves can validate or avoid writes. Scope/rebinding regressions found in independent review were reproduced and fixed. Proven declarative Django classes and their immediate Model/ModelForm Meta configuration are not DTOs; unresolved inheritance is retained as candidates without a replacement fix. The analysis is deliberately source-ordered, not a control-flow dominance proof.

The health difference includes detector precision corrections as well as application changes; it is not an isolated causal measure of application improvement. Rubric weights, severity weights, density curve and B+ threshold 87 are unchanged. Candidate rows remain bounded to 100 per health page; the complete archive retains every record. Static SQL reports whose provenance cannot be established by the current detector remain visible.

## Verification

- Toolkit final suite: **2,877 passed**. Final ratchet: **143 checks, zero failures**. Ruff, 15 skill validators and 7 style validators pass.
- Profile action module: 42 passed. Constraint-related model/helper suites: 1,213 passed. Widget non-browser suite: 150 passed including 7 new regressions; independent widget verification: 53 passed.
- Dynasty-related source 4c0d0a73: 246 passed on isolated in-memory databases, including 16 new regressions. Original catalogue content and exports independently compared against the prior AST.
- Character choices: 49 focused form, redirect, router and architecture tests passed after 36 characterization/baseline tests passed before the refactor. The strengthened non-character catalogue fixture regression also passed. Initializer cognitive complexity fell from 40 to 2; cyclomatic complexity fell from 13 to 3.
- Background totals: four new regressions pass (five queries before versus one afterward; empty input uses zero). Standalone query budgets pass with both implementations. The final identical 329-test rerun passed with two existing skips; an earlier run's Companion budget failure (51 versus 36 queries) remains unexplained and recorded. Companion tracing measured 34 queries with either implementation and no calls to the changed method. The combined final stack passed 61 form, routing, architecture and budget tests.
- Full repository run on source 4c0d0a73: Ran 8334 tests in 1040.418s; FAILED (errors=13, skipped=40) (current-model local-app synchronization; five parallel workers). Subsequent behavior-preserving refactors have their focused and guard validation listed above.

Full-run failures/errors retained without added skips:

- `test_attribute_validator_allocation_and_constraints (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_chained_ajax_request_protocol_and_response_metadata (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_chained_select_populates_and_clears (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_conditional_fields_change_visibility (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_create_or_select_toggle (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_filterable_list_count_token_select_and_hidden_empty_state (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_filterable_list_search_and_clear (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_form_choice_map_updates_child_on_change (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_formset_add_remove_and_delete (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_formset_remove_middle_row_renumbers_the_rest (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_formset_tag_initializes_new_row_widgets_with_bottom_media (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_option_metadata_change_event (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_page_media_at_bottom_combines_chained_metadata_and_conditional_fields (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`

## Rebuild and interpretation

The existing eleven-package map was retained; no subsystem-directory drift required a new scope decision. Run raw/Python/Django doctors once at repository scope against a clean tracked Git snapshot, merge the attributed reports, then build package health before the root roll-up. Ignored generated local migrations/databases and installed tooling are excluded from source. Local ignored migrations remain intact in the working checkout; test overrides use the documented current-model synchronization path.

All 60 pages are regenerated: automated atlas tabs rerun with docs excluded, authored architecture fragments reviewed and citations checked, fresh independent theory panels for all 12 units with affected catalogue judgments refreshed, measurement discovery rerun and its inventory reviewed. Measurement still has no audited empirical quality pipeline; game ratings, dice rolls and test fixtures are not such a pipeline. New theory scores reflect independent judgment and must not be presented as causal improvements from these small changes.

The full merged archive contains 22326 findings and 35879 candidates, with no doctor errors. [Compressed evidence](code-overview-findings.json.gz) preserves all locations; [summary](summary.html) links the complete navigable set. Below-B+ categories remain stated on each summary page.

Further work requires triaging the remaining findings and coherent architectural boundaries, rather than renaming literals or changing thresholds solely to raise a score.

---

## Earlier run record
# Code overview run

Refreshed 2026-10-16 from product source `5d20f9aa7f48e211ba96d8bfc7a0cad85b1269e8`, using coding-skills `497038d1fc32fdf61b1387e9c5f897d50a3daead` and Django target **5.2**. Analysis used a clean Git snapshot, excluding ignored generated local migrations, databases and installed tooling from application source. Later approval bookkeeping and the test-only socket timing repair are outside this analysis snapshot; application runtime code is unchanged by those follow-ups.

Start at [summary.html](summary.html). Every health and summary page was refreshed. Code maps, measurement pages and three-judge theory panels were refreshed for characters, core, populate_db, tg_schema and the repository. Other units retain earlier map/measurement/theory snapshots, whose metadata identifies their source. The complete latest merged detector envelope is in [code-overview-findings.json.gz](code-overview-findings.json.gz). Candidate display remains bounded at 100 rows per health page; all candidates are retained in the archive and unscored.

## Completed batch

Twelve Mummy titles now load structured JSON through an explicit, validated loader. Immutable seed identities adopt existing rows by original unique name, then update declared content without changing primary keys or character relations. Adoption conflicts and validation/database errors roll back the catalogue. The wrapper includes export binding in its transaction, so failed direct imports also roll back. A guarded schema migration adds the nullable key and historical named unique index. Run `migrate` before populating an existing installation. Reloads overwrite staff edits to the declared catalogue fields; removed JSON entries do not delete rows.

Coding-skills now treats unresolved documented Django metadata operations as candidates, recognizes imported generic-view configuration, and resolves quoted annotation references while excluding typing metadata. Relative framework lookalikes, alias shadowing and ordinary strings have counterexample tests. Scoring weights, grade bands and detector coverage were not relaxed.

## Goal status

**The requested B+ floor is not reached.** Health scores describe detector finding density, not an independently verified defect count. Theory grades are fresh independent judgments: changes from the previous panel are not measured regressions or causal estimates of this small title migration. Five dimensions use a coarse ladder and three judges; their full rationales remain embedded in the pages. Exact session-default model identifiers were unavailable.

| Unit | Health | Theory |
|---|---:|---:|
| accounts | F (41.4) | C (75.0) |
| characters | F (37.5) | D+ (67.5) |
| core | F (25.8) | D+ (67.5) |
| game | F (37.3) | B (85.0) |
| items | F (42.2) | C- (72.5) |
| locations | F (39.7) | D- (62.5) |
| tg_schema | F (25.6) | A (95.0) |
| widgets | F (38.0) | B (85.0) |
| tg | F (43.6) | B (85.0) |
| populate_db | C (75.2) | D- (62.5) |
| scripts | F (21.4) | C (75.0) |
| repository | F (36.5) | F (55.0) |

Measurement remains null: the inspected numbers are game state, test fixtures and query ceilings rather than an empirical quality-scoring pipeline. Production telemetry and empirical game-balance studies are unavailable. Plain JavaScript has no specialist grade; no execution-coverage artifact was generated. These gaps are ungraded, not passes.

## Validation

Product focused verification: **185 tests passed**, including population, Mummy, schema and CRUD/view-rule guards. The final full suite found 8,333 tests and executed **8309 tests in 1207.293 seconds**: **FAILED (failures=1, errors=13, skipped=40)**. It ran with socket/network access enabled. A separate blank-page Chromium probe timed out after 12 seconds. Browser failures remain visible; none were converted to skips or passing checks. Product PRs remain drafts pending browser-capable validation.

The full run's live-roll failure was then reproduced with a controlled rendering delay and fixed in the test harness: wait for the required frame rather than treating a 0.3-second idle gap as completion. The follow-up ran the entire `game` app: **582 tests: OK (one skipped)** in 44.396 seconds, including the delayed-broadcast regression. Runtime message ordering and all per-viewer HTML assertions are preserved. The full repository suite was not repeated after this test-only change; its original failure remains listed below, with this subsequent verification.

Coding-skills: **2,768 tests passed** in 265.44 seconds; **143 detector ratchet checks passed**. Repository Ruff, all 15 skill validators and all 7 style validators passed. Product Django checks, repository Ruff and Black on changed Python files passed. All affected atlas citations resolve; fragment lint, navigation across all 60 pages, health metadata and compressed report integrity were checked.

### Full-suite failures

- `test_attribute_validator_allocation_and_constraints (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_chained_ajax_request_protocol_and_response_metadata (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_chained_select_populates_and_clears (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_conditional_fields_change_visibility (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_create_or_select_toggle (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_filterable_list_count_token_select_and_hidden_empty_state (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_filterable_list_search_and_clear (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_form_choice_map_updates_child_on_change (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_formset_add_remove_and_delete (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_formset_remove_middle_row_renumbers_the_rest (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_formset_tag_initializes_new_row_widgets_with_bottom_media (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_option_metadata_change_event (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_page_media_at_bottom_combines_chained_metadata_and_conditional_fields (widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests)`
- `test_a_live_roll_renders_the_strip_for_every_viewer (game.tests.consumers.test_scene_socket_rolls_and_reads.LiveRollStripTests) (viewer='owner')`

Independent product review found a failed-import transaction gap and a historical migration dependency on mutable constraint metadata. Both were reproduced by tests before fixes. Independent toolkit review similarly caught relative-import and local typing-scope mistakes; regressions preceded those fixes. No known review findings remain deferred.

## Reproduce

Install coding-skills revision `497038d` with `bash install.sh --codex --skills --dest <checkout>`. Analyze a clean source snapshot from its root:

```bash
python <skills>/code-doctor/scripts/analyze_all.py . --format json
python <skills>/python-code-doctor/scripts/analyze_all.py . --jobs 2 --format json
python <skills>/django-code-doctor/scripts/analyze_django.py . --target-version 5.2 --format json
```

Retain each JSON output and combine it with `code-doctor/scripts/merge_reports.py --report <doctor>:<file>`. Build package health with that envelope and the confirmed roots in `code-overview.json`; use `--root --map docs/code-overview.json` for repository health. Do not skip detectors or alter weights. Django contributes findings as a bare list; Python's complete analyzer inventory supplies the evidence for coverage, rather than inferring it from Django's list.

The package map, source/tool revisions and partial-refresh provenance are in [code-overview.json](code-overview.json). Atlas judgment fragments and theory panels require fresh source reading; they are not reproducible numeric measurements.

## Implementation rulings

- Continued in the established dedicated checkout and feature branch; this requires serial product edits rather than separate worktrees.
- Used a manual ledger for cloud-backed skill helpers without local executable paths; the cost is manual tracking.
- Preserved ignored generated migrations outside the checkout during testing so the documented current-model synchronization path ran; private generated-history behavior is not established by that run. Original generated files were restored afterward.
- Added `--noinput` for noninteractive tests, replacing only disposable configured test databases.
- Treated the historical migration naming issue as important and froze the original index name. A later intentional constraint removal must explicitly remove that historical index.
- Put the newly exposed timing defect in a separate test-only stack entry, retaining bounded required-frame waits and exact HTML assertions so missing delivery still fails.
- Supplemented the retained full-run result with whole-game verification after that test-only repair. The cost is that a final globally green full-suite result remains unestablished; PRs stay drafts.

## Remaining work

Most catalogues still use descriptive lookup payloads, and positional chargen progress, registry special cases, complexity and duplication remain substantial. The next proposed bounded batch is eight Mummy dynasties using the verified identity contract; its design was sent for user review. No additional catalogue has been converted in this batch.
