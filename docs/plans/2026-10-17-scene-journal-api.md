# Read-only scene/journal API first increment (#204)

Parent: a330223 / dependent compatibility PR1653. Implement inline, no subagents or publishing.

- Add failing real SQLite permission/privacy, pagination, revocation/race and read-only tests.
- Add seven session-authenticated v1 read routes: scene list/detail/posts; journal
  list/detail/entries; character-to-journal lookup. Use actual TG scene/private-record
  audiences plus full-character policy; normalize hidden/missing JSON denials.
- Explicit minimal projections omit both ambiguous st_message fields, linked private
  character/location fields and raw roll metadata. Never invoke command processing or
  HTML read-marker effects. No writes, WebSocket client, schema changes or Rust transport.
- Validate native IDs and query/pagination bounds. Cover role changes, orphan chronicles,
  native retired-character visibility and partial-only observers.
- Document scope and native privacy mismatch; run API/model security guards, lint and full
  suite using documented external execution-only browser limitation settings; review with
  controller, fix findings, commit/report. No push or PR from this worker.
