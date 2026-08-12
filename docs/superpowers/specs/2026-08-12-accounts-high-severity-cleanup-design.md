# Accounts High-Severity Cleanup Design

## Goal

Reduce the 20 remaining high-severity `accounts` health records by fixing the
real application risks, correcting detector false positives at their canonical
source, and simplifying the profile-dashboard code without changing behavior.

Every implementation commit is a separately testable slice. Work pauses before
each commit so the user can inspect the diff and verification evidence.

## Finding Model

The 20 records represent five workstreams rather than 20 independent defects:

- one HTML password-reset email escaping boundary;
- one notification-context orchestration problem, reported by two complexity metrics;
- one oversized `Profile` dashboard/query responsibility, overlapping three
  production duplication findings;
- two test-duplication clusters; and
- eleven detector false positives: eight Django class declarations, two
  plain-text autoescape blocks, and one signal-registration import.

The health score is a density of detectable findings. It is useful for measuring
this cleanup, but it is not the design acceptance criterion. Behavioral tests,
query-count tests, and detector regressions are the acceptance criteria.

## Approaches Considered

### 1. Change application syntax until every detector is quiet

Convert lists to tuples, disguise signal imports through `import_module`, and
remove every autoescape block. This is small locally, but it teaches the tools
that framework configuration is a defect and risks degrading plain-text email
output. Rejected.

### 2. Suppress each finding in project configuration

Add per-file ignores for the eleven false positives and fix only the obvious
application findings. This keeps the project report clean but leaves the
canonical skills producing the same noise for every Django project. Rejected.

### 3. Fix code and detectors at their proper boundaries

Fix the HTML template, simplify dashboard orchestration, and reduce meaningful
duplication in `tg`; add framework-aware regression cases to the canonical
skills in `coding-skills`. This is the chosen approach because each change has
an observable contract and benefits the correct scope.

## Commit Boundaries

### 1. Secure the HTML password-reset email

Remove block-wide `autoescape off` only from the HTML email template. Retain it
in the text body and subject, where HTML entity escaping is not a security
boundary. Add a password-reset email rendering test with hostile HTML in the
username and site name; assert the HTML body escapes it and the reset URL remains
usable.

### 2. Correct detector classification

In canonical `coding-skills` sources:

- treat standard Django declarative attributes such as `Meta.fields` and
  `View.http_method_names` as configuration rather than shared-state defects;
- make the Django autoescape detector context-aware so plain-text templates are
  not high-severity HTML findings; and
- honor `# noqa: F401` and Django `AppConfig.ready()` registration imports in
  unused-import analysis.

Each correction starts with a failing minimal fixture, passes the affected skill
suite, and is installed with `install.sh --codex` before the health report is
regenerated.

### 3. Extract dashboard notification orchestration

Keep the context processor responsible for authentication, cache lookup/storage,
and returning a context dictionary. Move breakdown construction into a focused
accounts service or selector with explicit player and storyteller sections.
Preserve notification labels, counts, the 60-second cache contract, and current
fail-soft behavior through characterization and query-count tests before
narrowing exception handling.

### 4. Move dashboard selectors out of `Profile`

Keep persistent preference validation, URL behavior, and storyteller
authorization on `Profile`. Move owned-object, approval-queue, image-approval,
weekly-XP, and journal dashboard queries behind a focused selector/dashboard
object. Existing `Profile` methods remain as forwarding adapters during this
campaign so templates and callers do not break. Consolidate the three repeated
model-family query recipes behind private typed helpers.

### 5. Consolidate duplicated tests

Use `subTest()` tables for equivalent invalid-type/nonexistent-object cases and
a shared fixture or mixin for repeated profile owner/staff authorization setup.
Keep each authorization behavior visible as a distinct assertion; reducing line
count is not allowed to obscure which access rule failed.

### 6. Regenerate health artifacts

Run the installed doctors once from the repository root, rebuild only health and
summary pages whose counts or rollups changed, inject navigation, and verify it
is idempotent. Report the before/after counts and distinguish findings from
unscored candidates.

## Testing Strategy

- TDD for every behavior or detector change: observe RED, implement the minimal
  change, then run focused and affected suites.
- Render the password-reset email through Django rather than testing template
  source text.
- Preserve notification and selector query behavior with real database tests and
  `assertNumQueries` where query count is part of the contract.
- Run `manage.py check`, focused Ruff correctness checks, skill Ruff, and each
  affected skill test suite before presenting a commit.
- Independently review non-trivial refactors before their commit checkpoint.

## Non-Goals

- Migrating from Django's default `User` to a custom user model.
- Redesigning notification product behavior or labels.
- Removing `Profile` forwarding methods in the same campaign.
- Refactoring unrelated medium/low findings.
- Editing generated HTML by hand.

## Acceptance Criteria

- Hostile username/site-name HTML is escaped in the HTML reset email.
- Plain-text reset templates render without unwanted HTML entities and are not
  reported as high-severity autoescape defects.
- Django declarative class configuration and intentional signal imports are not
  scored as unused/mutable defects.
- Notification output and cache behavior are unchanged, with lower measured
  complexity.
- Dashboard queries have one implementation per model-family recipe and retain
  their query-count guarantees.
- All affected application and skill suites pass, or unrelated pre-existing
  failures are named with evidence.
- The refreshed accounts report contains no remaining high-severity record from
  these workstreams unless verified behavior still justifies it.
