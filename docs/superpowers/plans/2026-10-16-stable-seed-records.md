# Stable Seed Records Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Reload the twelve Mummy titles by permanent identity while preserving existing rows and references.

**Architecture:** Add a nullable seed key to MummyTitle and a guarded legacy-schema patch. A shared, explicitly configured JSON loader adopts existing rows and updates declared fields; the existing script remains the compatibility entry point.

**Tech Stack:** Python 3.10, Django 5.2, standard-library JSON, existing Django test runner and Ruff/Black. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-10-16-stable-seed-records-design.md`

## Global Constraints

- The first implementation covers the twelve records in `populate_db/mummy/titles.py`.
- Existing rows keep their primary keys; unseeded staff-created rows have NULL keys.
- Never merge, delete, or silently choose a row.
- Content in converted records is authoritative: reloads overwrite staff edits to the declared content fields.
- Rows removed from JSON remain in the database; deletion and duplicate repair are separate operations.
- Key renames are not supported; a rename requires an explicit reviewed data migration.
- JSON cannot select a model, import code, set primary keys, set seed keys through fields, or write relationships.
- Detector thresholds and weights remain unchanged.
- Local apps commit no migrations; schema support ships through `tg_schema`.

## Review Focus

- Duplicate JSON object properties must fail, rather than letting the JSON parser silently overwrite data (Task 2).
- Empty/oversized keys and non-object records must fail before writes (Task 2).
- A renamed seeded title must not adopt a different existing title with its new name; uniqueness failure must roll back (Task 3).
- A JSON name collision late in the catalogue must undo earlier updates (Task 3).
- A missing or malformed JSON file must fail with its path and retain the database unchanged (Task 2).

---

### Task 1: Database identity and guarded rollout

**Files:** Modify `characters/models/mummy/mummy_title.py`; create `tg_schema/migrations/0013_mummy_title_seed_key.py`, `tg_schema/tests/test_mummy_title_seed_key.py`; extend `characters/tests/models/mummy/test_mummy_title.py` (create if absent).

**Interfaces:** Produces `MummyTitle.seed_key`: CharField(max_length=150, null=True, blank=True, editable=False), plus `UniqueConstraint(fields=["seed_key"], name="unique_mummy_title_seed_key")`. Migration entry point: `add_mummy_title_seed_key(apps, schema_editor) -> None`, dependent on `0012_protect_player_reality_zones`.

- [x] Write failing model tests: two NULL keys succeed; repeated `mummy.title.pharaoh` raises IntegrityError inside a savepoint; the field is non-editable and length 150.
- [x] Run `.venv/bin/python manage.py test characters.tests.models.mummy.test_mummy_title` and confirm missing-field/constraint failure.
- [x] Add the model field/constraint. Write migration tests using TransactionTestCase and actual schema introspection: missing column is added without losing an existing title; missing unique index is added; a second run adds nothing; removed model/field/table skips; duplicate non-NULL keys are rejected, multiple NULL keys allowed. Restore modified schema in cleanup.
- [x] Run `.venv/bin/python manage.py test tg_schema.tests.test_mummy_title_seed_key` and confirm the missing migration fails.
- [x] Implement the migration using live_model/live_field/table_names/table_columns and guarded DDL. Quote identifiers through the connection; add a unique index if no equivalent unique constraint exists. Import no app models, ignore historical apps, use RunPython.noop reverse, and do not adopt data here.
- [x] Run both new test modules plus `tg_schema.tests.test_schema_helpers`; require all passing, including removed-model guards.
- [x] Commit: `Add stable seed identities to Mummy titles`.

### Task 2: Validated input contract

**Files:** Create `core/seed_data.py`, `core/tests/test_seed_data.py`.

**Interfaces:** `SeedDataError(ValueError)`; `read_seed_records(model, path: Path, *, allowed_fields: frozenset[str], legacy_fields: frozenset[str]) -> list[dict]`. Each record has exactly `key`, `export`, `legacy_lookup`, `fields`. Task 3 consumes this validated list. Require every record's fields to equal the configured allowed_fields; legacy_lookup is a nonempty subset of legacy_fields. Both configurations must reference concrete, non-relational model fields and exclude PK/seed_key.

- [x] Write failing SimpleTestCase tests using temporary JSON files and MummyTitle metadata. A valid Pharaoh record returns unchanged. Parameterize invalid top-level type, non-object records, missing/extra properties, duplicate object properties, duplicate keys/exports, invalid identifiers or Python keywords, empty/malformed/over-150-character keys, empty legacy selectors, unknown fields, missing allowed fields, relation/PK/seed_key injection and invalid configuration. Assert SeedDataError with file path and no database access.
- [x] Run `.venv/bin/python manage.py test core.tests.test_seed_data` and confirm missing reader failure.
- [x] Implement the reader using json.load with duplicate-property detection. Keys follow `[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+`, maximum 150 characters. Validate types before using sets/dicts. Wrap file/JSON/contract errors in SeedDataError with path and record index where available. Do not catch database/programming exceptions in this layer.
- [x] Add missing-file and malformed-JSON tests; require path-bearing errors and zero writes. Run the module and require all passing.
- [x] Commit: `Validate structured seed catalogue records`.

### Task 3: Atomic adoption and updates

**Files:** Extend `core/seed_data.py`, `core/tests/test_seed_data.py`.

**Interfaces:** `load_seed_records(model, path: Path, *, allowed_fields: frozenset[str], legacy_fields: frozenset[str]) -> dict[str, models.Model]`. It calls Task 2's reader before opening a write transaction, uses the default database, and returns export names mapped to saved objects.

- [x] Write failing TestCase tests: fresh create; repeat load retains count/PK; adoption by original unique name retains PK despite changed rank/description; key lookup supports display-name change; unrelated fields/rows are retained; removed records are not deleted; title remains linked to a Mummy. Use existing Mummy fixture conventions from `characters/tests/models/mummy/test_mummy.py`.
- [x] Run `.venv/bin/python manage.py test core.tests.test_seed_data` and confirm loader tests fail.
- [x] Implement the loader with one atomic block for the catalogue. Lock matches with select_for_update. Resolve by seed_key first, otherwise evaluate the legacy selector and reject multiple matches or a match with another key. Assign the immutable key on adoption/creation, assign declared content fields, call full_clean then save; return objects by export. Do not suppress errors or retry conflicts automatically. Error messages for adoption failures include the record key and selector.
- [x] Add tests using rank_level as a permitted nonunique legacy selector to prove ambiguity rejection. Test conflicting keys, invalid model values, a later unique-name collision rolling back earlier adoption/update, and database exceptions propagating. Test an existing keyed title renamed onto another title's name: both original rows remain unchanged after failure. Update/create failures may surface ValidationError or IntegrityError; both must roll back.
- [x] Run the complete module and Mummy model tests; require all passing.
- [x] Commit: `Load seed catalogues atomically by permanent identity`.

### Task 4: Convert Mummy titles and preserve command behavior

**Files:** Create `populate_db/mummy/titles.json`, `core/tests/management/commands/test_populate_mummy_titles.py`; modify `populate_db/mummy/titles.py`, `populate_db/README.md`, `populate_db/docs/loading.md`, `populate_db/docs/conventions.md`, `populate_db/docs/adding-data.md`; update the relevant Mummy model documentation under `characters/docs/`.

**Interfaces:** Wrapper invokes Task 3 with MummyTitle, `Path(__file__).with_suffix(".json")`, allowed_fields `{name, rank_level, description}`, legacy_fields `{name}`. Preserve twelve explicit exports: pharaoh, high_priest, vizier, keeper_of_balance, judge_of_souls, guardian, preserver, lorekeeper, elder, mentor, seeker, neophyte. Keys use `mummy.title.<export>`. Legacy names and initial fields exactly match the original script.

- [x] Add a static expected-data fixture in the integration test copied from the original twelve entries. Test Command.load_file against the real wrapper: exactly twelve correct titles and all exports from runpy.run_path. Re-run after modifying database descriptions and prove authoritative restoration with unchanged PKs. Test an imported wrapper in isolated sys.modules state, cleaning up after the test.
- [x] Run `.venv/bin/python manage.py test core.tests.management.commands.test_populate_mummy_titles`; confirm structured-file/seed-key assertions fail against the old wrapper.
- [x] Move the twelve records into JSON without editing their content. Replace repeated ORM calls with the loader and explicit export assignments. Do not change discovery or command filtering.
- [x] Test `populate_gamedata --gameline mummy --only titles` through call_command; assert the selected wrapper loads and JSON/helper files are not discovered as scripts. Ensure temporary import cache state never leaks into other tests.
- [x] Document immutable keys, authoritative content updates, legacy adoption, conflict/rollback behavior and required migrate-before-populate rollout. Clearly distinguish unchanged Python catalogues from this pilot.
- [x] Run new integration tests, existing population command/source tests, model CRUD field guards, all schema tests and lint/checks. Require green focused checks.
- [x] Commit: `Separate Mummy title content from seed execution`.

### Task 5: Verify, review and publish the next stack entry

**Files:** Update `docs/code-overview-run.md`; regenerate affected overview artifacts using the pinned installed toolkit and existing confirmed scope in `docs/code-overview.json`.

**Interfaces:** Consumes Tasks 1–4. Produces a reviewable branch stacked above `quality/code-overview-final`, a verification record, refreshed grades and a PR only after the branch is complete.

- [x] Run `.venv/bin/python manage.py check`, `.venv/bin/ruff check . --extend-exclude .codex`, `.venv/bin/black --check` on touched Python files, and `git diff --check`; require no errors.
- [x] Run `.venv/bin/python manage.py test --parallel 4` with network/socket access enabled and capture the full log in `work/`. Report exact failures; fix regressions rather than masking them. If Chromium still fails independently, retain that limitation and keep the PR a draft.
- [x] Apply requesting-code-review and verification-before-completion skills. Review identity adoption, rollback, schema guards and authorization/CRUD exposure; resolve important findings and rerun affected tests.
- [x] Re-run root and affected package overview scopes using the prior report's documented commands and current-version Django target. Validate linked report navigation and archive integrity. Record source/tool commits and unchanged scoring, and identify remaining B+ gaps honestly.
- [x] Commit refreshed reports: `Record stable seed migration verification and quality results`.
- [x] Push branch and create the next stacked PR with concrete behavior, adoption/rollout guidance, validation counts and remaining limitations. Never merge; the user lands stack entries.
- [x] Select the next confirmed quality issue using the refreshed evidence. Bring behavior or architecture changes through the applicable design process before implementation.

## Self-review and handoff

The plan covers all spec components, preserves the loader/wrapper interfaces, and adds each
Review Focus case to its owning task. No broader catalogue conversion, duplicate repair,
relationship language or automatic concurrency retry is included. The user approved the
written specification and this plan, selecting native execution. Implementation and review
fixes are complete; see `docs/code-overview-run.md` for final verification and remaining gaps.
