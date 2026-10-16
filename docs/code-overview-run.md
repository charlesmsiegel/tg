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
