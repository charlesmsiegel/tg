# Demon ritual data repair (#1607, #1608, #1527)

The ritual catalogue must preserve the declared lore requirements across reloads and
across databases. Secondary requirements use unique Lore.property_name values; citations
use the existing sources relation. Keep source_page only as a legacy/manual fallback,
because unstructured existing citations cannot all be converted without guessing.

1. Reproduce data loss by executing the existing DPG script in the test database;
   assert Hadrisel primary rating 2, Awakening 1, and two other rituals. Add source
   attribute/JSON guards and model tests for stable resolution and invalid requirements.
2. Fix and rename the DPG script; convert all nine ritual scripts to stable lore keys
   and add_source citations, recording each page of existing ranges.
3. Validate the JSON shape, integer ratings 1?5 and existing lore keys in Ritual.clean;
   resolve secondary lores in one query and raise ValidationError for unknown keys.
   Render structured book citations, falling back to source_page for legacy entries.
4. Ship a guarded data migration converting old IDs to property names, preserving
   unresolved legacy entries for explicit repair instead of silently dropping them.
   Cover mixed old/new data, missing rows/columns, idempotency and form validation.
5. Update relevant app/seed documentation. Run focused tests, full suite, pre-commit
   and repo-wide ruff; review final diff, commit, push feature branch and open draft PR.

Review focus: malformed JSON, bool ratings, deleted Lore rows, repeated keys, old IDs
that no longer resolve, page ranges, reloads retaining existing ritual identities.

Baseline: 30 ritual model/view tests passed before changes.
