# Stable identities for reference seed records

## Purpose and scope

Make reference-data reloads update the intended record without changing its primary key
or breaking character references. Separate catalogue content from execution, preserve the
existing command and script imports, and migrate in small reviewable batches. This is the
first architectural step toward the requested B+ quality goal; it does not establish that
goal by itself. Detector thresholds and weights remain unchanged.

The first implementation covers the twelve records in `populate_db/mummy/titles.py`.
It establishes a small reusable loader, not a replacement framework for all seed scripts.
Further catalogues require their own identity and relationship review before conversion.

## Existing behavior and confirmed defect

`populate_gamedata` discovers Python scripts, filters and sorts them, and executes each
inside a transaction. Imports can execute a script before its scheduled turn. Other scripts
can depend on module-level object exports.

Mummy titles currently use `get_or_create(name=..., rank_level=..., description=...)`.
The model has a unique name. A changed description or rank therefore attempts a new insert
and can raise an integrity error, rather than updating the existing title. For catalogues
without a uniqueness constraint the same pattern can instead produce duplicates. This pilot
must describe and test the title-specific failure accurately.

## Approach

Use JSON records and an explicitly configured Python loader, retaining the existing script
as a compatibility wrapper. Give each converted model a nullable, unique, non-editable
`seed_key` field. A title key such as `mummy.title.pharaoh` is permanent even when its
display name changes. Existing rows keep their primary keys; unseeded staff-created rows
have NULL keys. Do not put seed keys in public CRUD field lists.

Alternatives considered:

- Lookup by unique name and update defaults: smaller, but a name change loses identity.
- A generic identity table: avoids per-model columns, but adds model/content-type dispatch
  and stale-pointer handling that this pilot does not need.

The direct field makes identity a database-enforced property of the target record. Reuse
the loader only for models explicitly adapted to this contract.

## Components and record contract

`populate_db/mummy/titles.json` holds an ordered list of records. Each record contains
`key`, `export`, `legacy_lookup`, and `fields`. For Pharaoh, `legacy_lookup` is
`{"name": "Pharaoh"}`, and `fields` contains name, rank_level and description. The
legacy lookup is a frozen adoption selector, not something regenerated when names change.
The twelve export names and content initially match the current script exactly.

`core/seed_data.py` provides the shared loader. Callers supply the model, JSON path,
allowed mutable fields, and allowed legacy lookup fields explicitly. JSON cannot select a
model, import code, set primary keys, set seed keys through fields, or write relationships.
Validate the whole input before writing: reject unknown/missing record properties, duplicate
keys or exports, malformed keys, invalid export identifiers, empty legacy lookups, and
unknown or disallowed fields. Use ordinary JSON values and Django model validation;
there are no executable expressions or dynamic imports.

`populate_db/mummy/titles.py` resolves JSON relative to `__file__`, invokes the loader,
and binds the twelve existing export names explicitly. The loader returns an export-to-object
mapping. Keep helpers outside `populate_db` because the command executes every Python file
under that directory. JSON files are loaded only by their wrapper, preserving discovery,
ordering, filters, script counts and transaction boundaries.

## Adoption and updates

The loader wraps each catalogue in `transaction.atomic()`, including when called through
an import outside the command. Process records in declared order:

1. Find the row by seed key. If present, update only declared content fields.
2. Otherwise find rows by the explicit legacy selector. Adopt exactly one unkeyed row.
   If the matching row has another key, or multiple rows match, fail with the record key
   and selector. Never merge, delete, or silently choose a row.
3. If nothing matches, create a row with its permanent key and content.
4. Validate and save through the normal model API. Return the same database identity
   on every successful reload. Leave fields outside the allowed content set unchanged.

Content in converted records is authoritative: reloads overwrite staff edits to the
declared content fields. State this in loading and editing documentation. Rows removed
from JSON remain in the database; deletion and duplicate repair are separate operations.
Key renames are not supported; a rename requires an explicit reviewed data migration.

Lock existing rows while updating. Database uniqueness protects keys and existing title
names against concurrent inserts. Conflicting concurrent adoption/creation may fail and
roll back the catalogue; it must never silently attach the wrong row. Automatic retry and
cross-database concurrent-loader guarantees are outside this pilot.

## Schema and rollout

Declare `seed_key` as a nullable, blank, non-editable CharField of length 150 with a named
unique constraint. NULL allows multiple unseeded rows. Add it to old databases through the
next guarded `tg_schema` migration, following the existing live-model/introspection rules.
The migration must add a missing column and missing constraint safely, do nothing when
already present, and skip a removed model, field or table. It does not read JSON or adopt
rows: adoption happens during the explicit population command.

Land schema support before running the converted loader. Do not remove the column on
rollback; old script code can still use the existing model data. Reverting the loader does
not undo updated catalogue text. Conversion of the other catalogues is a later batch,
after this loader and its adoption semantics have been verified.

## Verification and documentation

Cover record validation without writes; fresh load; repeated load; changed description,
rank and name; adoption of an existing unique-name row; conflicting keys; ambiguous
selectors; full-catalogue rollback; unexpected database errors; and preservation of a
Mummy-to-title relation and primary key after reload. Exercise the actual wrapper and
management-command filter. Assert all twelve exports and unchanged initial content.

Test the guarded migration against missing/present schema and removed models, including
uniqueness enforcement and multiple NULL keys. Run relevant command, model, schema and
CRUD guards, then repository lint/system checks and the full suite before a new PR.
Keep browser failures visible if the existing environment limitation persists.

Update the populate README, loading/conventions/adding-data guides and model documentation
with authoritative updates, immutable keys, legacy adoption, failure behavior and rollout.
Re-run the affected overview scopes and root overview with unchanged scoring. Publish
remaining grades and limitations honestly; use verified findings to select the next batch.

## Review status

The user approved this specification and its implementation plan, and selected the
recommended native execution approach. The title pilot and independent review fixes are
implemented; validation and remaining quality gaps are recorded in `docs/code-overview-run.md`.
