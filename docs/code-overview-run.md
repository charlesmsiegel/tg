# Code health refresh — 2026-10-17

The user requested code-health work and paused theory work. This run rebuilds the
12 health pages and 12 summaries only. Theory, measurement and codemap pages are
retained unchanged from source `67d7990bc5ac00dc371a7a382e4c637acdb8e629`.
The previous complete overview record is retained in Git at `998fba61`.

## Reproducible scope

- Product source: `69d96519ee43d39aa5f7471367cf97ced1b28cd2`; clean tracked checkout, without local databases,
  ignored generated migrations, virtual environments or scratch files.
- coding-skills: `7ce994fffb3d1f6c61b7745e101618f0f018712a`; Django target **5.2**, the declared project version.
- Existing 11-package map retained; the repository score uses their union.
- Final reports use one complete run of each doctor from the repository root. No doctor or analyzer
  errors. Findings and candidates retain their separate classifications.
- Rubric weights, grade bands, detector thresholds and test ceilings unchanged.
- Plain JavaScript and execution coverage remain ungraded. The Django specialist
  emits a flat report without a coverage manifest; the envelope retains
  `coverage_unknown: ["django-code-doctor"]` rather than claiming completeness.

Review stack: [account fixtures #1656](https://github.com/charlesmsiegel/tg/pull/1656) → [group background queries #1657](https://github.com/charlesmsiegel/tg/pull/1657). Both remain unmerged.

## Reviewed product changes

1. Account profile, approval and permission view tests authenticate the same
   50 fixture users with `force_login`. Anonymous and credential-based login
   endpoint tests remain intact. All 60 module tests pass before and after.
2. Group pooled-background updates select the contribution's background in
   the initial query. Existing aggregation, order, validation, save signals,
   stale rows and metadata are preserved. For one versus nine contributions
   to an existing pool, the original query count grew from 4 to 12; the fixed
   count is 3 in both cases. Six characterization regressions and 42 related
   tests pass. Writes still scale with distinct pools to preserve save behavior.

Both changes passed independent review, Ruff, Black100 and diff checks.
The query tests are correctness/performance regressions, not a coverage claim.

## Proven detector false positives

[coding-skills #25](https://github.com/charlesmsiegel/coding-skills/pull/25)
distinguishes multi-valued relation writes and direct assignment targets from
reads that prefetching could eliminate. It retains RHS and argument reads,
nested descriptor reads, augmented assignments and ambiguous FK/O2O or duplicate
class names. Independent review caught the duplicate-class ambiguity; regression
cases now protect it. No scoring rules changed.

The full-suite run passed 2,899 tests. Review added eight cases after that run's
collection; 60 focused tests cover the final follow-ups. All 143 detector ratchet
checks, Ruff, skill/style validators and diff checks pass. Installed Django
detector source matches this revision.

The practice seed loops still contain real repeated reads. A proposed eager-load
change was discarded after review demonstrated valid parent chains would lose
relations and benefits inherited earlier in the same loop. Their sequential
behavior is retained; those remaining findings were not suppressed.

## Results

Findings: **22,278**, down from **22,326**. Candidates: **35,879**,
unchanged. N+1 warnings: **8**, down from **18**, due to proven false-positive
corrections. The tested group optimization addresses an additional real query
problem that the original static detector did not identify. Counts and scores
reflect both application changes and detector precision; they are not a causal
application-only improvement measure.

| Scope | Health score | Grade |
|---|---:|:---:|
| accounts | 49.3 | F |
| characters | 40.5 | F |
| core | 26.4 | F |
| game | 37.1 | F |
| items | 43.8 | F |
| locations | 41.4 | F |
| tg_schema | 23.0 | F |
| widgets | 40.3 | F |
| tg | 43.6 | F |
| populate_db | 77.1 | C+ |
| scripts | 21.4 | F |
| repository | 38.5 | F |

**B+ remains unmet.** The repository score rose from 38.0 to 38.5. There are no
new theory judgments in this run.

## Full product verification

At product source `69d96519`, the full-suite runner discovered 8,377 tests and
reported **8,353 tests run in 1194.584 seconds**, **13 errors**, **40 skips**, and
**zero assertion failures**. Every error is a 30-second Chromium subprocess
`TimeoutExpired` in `widgets.tests.test_static_assets_browser.StaticAssetsBrowserTests`,
matching the previously recorded browser-environment limitation. The suite is
**not green**; product PRs remain drafts. No test was disabled and no ceiling or
skip condition changed.

The full run used `parallel=8` and the documented current-model synchronization
path (`MIGRATION_MODULES=None` for accounts, characters, core, game, items,
locations and widgets), so ignored per-install generated migration files could
not hide newly declared fields. The user database was not migrated.


## Report verification

All 24 rebuilt health/summary pages retain navigation. Navigation's check mode
reports zero required updates. All 12 health source pins match the product
source above. The compressed archive round-trips to the exact merged envelope,
including every candidate. The retained theory, measurement and codemap pages
have no diff. No generated local migration or database is included.
