# Toolkit REST API first increment (#195)

Authorized scope: native TG integer-ID JSON reads, owner-safe descriptive character
updates, staff-only chronicle creation. This is a first increment, not completion of #195.
No schema changes, arbitrary polymorphic writes, token infrastructure, character creation,
stat updates, or lossy toolkit archive conversion.

- Add route-level denial and data-fidelity regressions; observe missing routes fail.
- Add DRF JSON/session read views, explicit projections and bounded pagination.
- Add dedicated POST action for descriptive updates using ObjectActionView/PermissionManager;
  reject unknown fields, preserve mechanics and relations. Staff chronicle creation uses
  the existing can_manage_chronicle(None) rule and binds head ST server-side.
- Document session/CSRF use, mappings, supported projections and deferred API/Store gaps.
- Run focused/security guards, full Django suite, targeted black and repository ruff;
  commit locally and report. Controller reviews/publishes; no push or subagents.

## Verification outcome

Independent review found a pre-lock authorization race; both status-change and ownership-
transfer regressions failed first and now pass after locked-object reauthorization.
Focused API/security/action/import checks:31 passed. Repository Ruff and targeted Black
checks passed. The standard full run hit an unchanged optional Chromium test timeout,
reproduced standalone. An external execution-only runner explicitly skipped that unavailable
browser class and used a fast test hasher (no production settings changed):8317 discovered,
8293 ran, OK with53 skips,209.241s. This is the first increment of #195; documented API and
Store-compatibility gaps remain open. No schema changes were required.
