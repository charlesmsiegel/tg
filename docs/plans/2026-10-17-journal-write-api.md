# Bounded journal writes — next #204 increment

Base: 60d83b9. Scope approved by controller from exact toolkit #204 and native TG
journal policies. Execute inline; no push/PR/subagents; preserve auth contracts.

## Contract

- POST `/api/v1/journals/{pk}/entries/append/`: JSON `{date:"YYYY-MM-DD",message}`.
  Native journal full-read gate and exact owner-only append policy (no staff/ST override).
  Bounded prose only, native JournalEntryForm validation/stripping/date semantics, but
  no Journal.add_post/message_processing/dice/resource execution. Reject native reserved
  command/spend syntax as unsupported, preserving other prose.201 projected new entry.
- GET `/api/v1/journals/{pk}/entries/{entry_pk}/`: native private journal/entry read
  audience, canonical parent binding; explicit entry fields plus owner-visible st_message.
  Existing minimal read projections and auth facade remain unchanged.
- POST `/api/v1/journals/{pk}/entries/{entry_pk}/response/`: JSON `{st_message}`.
  Exact native full-read + Permission.APPROVE policy; first response only.409 if answered;
  atomic conditional update avoids overwriting another answer. This is not an ST-only note.
- Explicit scalar allowlists, strict ISO dates, 10,000-character text and64KiB request
  bounds; malformed/unknown/duplicate/wrong-type fields receive structured400,415 for
  non-JSON. Session+CSRF; POST-only ACTION policies; hidden/missing404 before validation.
- Reload/lock canonical journal, character, actor, chronicle and existing relevant role
  rows; invalidate cached permissions and reauthorize after lock. Entry locks and nested
  parent checks prevent cross-journal/reparent writes. No general edits/deletes, no
  schema/version fields, no scene mutations. Append is non-idempotent; uncertain network
  failures must not auto-retry. Existing HTML behavior and command support remain unchanged.

## Execution and evidence

1. TDD real audience/CSRF/field/command/error/concurrency regressions; observe missing
   routes fail. Source of truth: game.actions.JournalEntryCreateView/JournalResponseView,
   game.forms.JournalEntryForm/STResponseForm, native private-record policy.
2. Implement dedicated action subclasses plus bounded game service and explicit detail
   projection. Tests include status parity, reparent/owner/role races, first-answer409,
   public-character privacy and command syntax/case/whitespace. No arbitrary model writes.
3. Run focused API/native game/auth/policy/action/import checks; lint/format; update API
   and native docs. Independent controller review; full Django suite using authorized
   external browser exclusion and existing compat venv. Commit/report after actual pass.

Ruling: native Journal.add_post executes mechanics, so prose API reuses form validation
and equivalent aware-midnight date conversion but never invokes the parser. Source
commands remain on the native site. First-response-only intentionally narrows native
response replacement to prevent lost updates without introducing an unsafe edit version.

Review ruling: real simultaneous SQLite response requests exposed a losing500 from
read-to-write lock upgrade. Handle only SQLite BUSY/LOCKED codes as structured409 after
atomic rollback; no broad DB-error masking. Add independent-client TransactionTestCase
and verify nonconflict database errors still propagate. Stop pre-fix full run (exit143)
and rerun complete focused/full suites after fix. Both contending upgrades may abort;
no partial write and explicit post-refresh submission must remain safe.

Compatibility ruling: repository tooling targets Python3.10, where sqlite3 lacks the
modern error-code attributes/constants. Use stable numeric base codes when present and
exact native lock messages only for actual sqlite3 causes without codes. Legacy-cause
regressions reproduced three500 cases, then passed; unrelated I/O errors still propagate.
No actual3.10 interpreter was installed, so test the missing-code path under3.12 honestly.
Stop/restart the in-progress full run after this fix as well; preserve terminated logs.
