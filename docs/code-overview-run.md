# Code overview run

Generated 2026-10-16 from product commit `6e29f3bc`, using coding-skills revision `319291e` and Django target **5.2**. The analysis used a clean local Git snapshot, excluding ignored local migration files, databases and installed skill payloads from application source. The health roll-up covers the union of the confirmed package roots; the repository atlas also shows root-level launch/configuration files.

Start at [summary.html](summary.html). Each package has the same five linked documents. Navigation was checked across all 60 pages. The complete merged detector envelope is retained in [code-overview-findings.json.gz](code-overview-findings.json.gz); the HTML shows a bounded sample of unscored candidates, with total/shown/omitted counts.

## Goal status

**The requested B+ floor has not been reached.** No scoring weights or grade bands were changed. Health measures mechanically reported finding density, not an independently verified defect count. Candidates are unscored. Theory is the median of three independent judgments and remains partly model-dependent; the exact session model identifier was unavailable. Measurement is null because the reviewed application values are game state rather than an empirical quality-scoring pipeline. JavaScript has no specialist grade, and no execution-coverage artifact was supplied.

| Unit | Health | Theory |
|---|---:|---:|
| accounts | F (40.2) | C (75.0) |
| characters | F (37.3) | D+ (67.5) |
| core | F (25.9) | D+ (67.5) |
| game | F (37.3) | B (85.0) |
| items | F (42.2) | C- (72.5) |
| locations | F (39.7) | D- (62.5) |
| tg_schema | F (22.5) | B (85.0) |
| widgets | F (38.0) | B (85.0) |
| tg | F (43.6) | B (85.0) |
| populate_db | C (75.2) | D+ (67.5) |
| scripts | F (21.4) | C (75.0) |
| repository | F (36.7) | C (75.0) |

## Reproduce

Install the pinned coding-skills revision locally. Run all doctors from the **repository root**, not from individual app folders. Use `python-code-doctor/scripts/analyze_all.py . --jobs 2 --format json` and `django-code-doctor/scripts/analyze_django.py . --target-version 5.2 --format json`, together with the raw doctor; merge with `code-doctor/scripts/merge_reports.py`. Build package health with that merged envelope and the roots in `code-overview.json`, then build root health with `--root --map docs/code-overview.json`. See the pinned code-overview skill for atlas, measurement and independent theory-panel workflows.

Theory judgments and authored atlas fragments are evidence-based prose, not reproducible numeric measurements. The three verdicts are embedded in each theory page. Query-budget tests measure fixture behavior, not production latency. Production telemetry and empirical game-balance studies were not available.

## Changes from this review

Legacy XP/freebie spending now propagates unexpected catalogue and validation failures instead of silently changing category. Populate scripts execute through `runpy.run_path` inside their existing transaction, with source filenames and `__file__` preserved. The local-app import guard now distinguishes installed repository-virtualenv dependencies from project apps without changing its app allowlist.

The toolkit fixes distinguish framework conventions from defect evidence: lazy querysets, inherited model contracts, validation contexts, uniqueness protection, centralized authorization, type-only imports, assertion contexts and quoted SQL identifiers. Regression tests preserve runtime/rebinding danger cases.

## Validation

Coding-skills: 2,705 tests passed; 143 bug-detector ratchet checks passed; Ruff and skill/style validators passed. The product's focused regression tests and seven import-guard tests passed. The first full product run completed with 8,273 executed tests, one guard-classification failure and 55 errors in the restricted environment; the guard classification was corrected and its seven tests pass. A network-enabled retry ran 103 tests: 13 Chromium widget tests timed out and three tests skipped; the remaining 87 passed, including the WebSocket cases. Even a blank-page Chromium probe timed out outside the sandbox. The product suite is therefore **not green locally**; browser execution is an environment limitation and is not reported as a passing check. Product PRs remain drafts pending browser-capable validation.
