# tg view/render refactor: design prompts

Each file here is a standalone prompt for a design agent. Every agent writes a design doc and an implementation plan under `docs/superpowers/specs/` and `docs/superpowers/plans/` and **does not change application code**.

The findings in these prompts come from a code-reading audit at commit `c1c509a`. Items marked **Confirmed** were re-checked against the source; items marked **Reported** must be verified by the design agent.

## Steps

| # | Prompt | Output spec | Depends on (read its design first) |
|---|---|---|---|
| 00 | `00-authorization-hardening.md` | `2026-09-25-authorization-hardening-design.md` | none. **Do this first; it fixes live security holes.** |
| 01 | `01-dead-code-removal.md` | `2026-09-25-dead-code-removal-design.md` | 00 (for permission mixins it may reuse) |
| 02 | `02-chargen-step-registry.md` | `2026-09-25-chargen-step-registry-design.md` | 00 |
| 03 | `03-generic-chargen-steps.md` | `2026-09-25-generic-chargen-steps-design.md` | 00, 02 |
| 04 | `04-game-rules-out-of-views.md` | `2026-09-25-game-rules-out-of-views-design.md` | 00; ideally 02 and 03 |
| 05 | `05-action-endpoints.md` | `2026-09-25-action-endpoints-design.md` | 00, 04 |
| 06 | `06-permission-context.md` | `2026-09-25-permission-context-design.md` | 00 |
| 07 | `07-items-locations-registry.md` | `2026-09-25-items-locations-registry-design.md` | 00 |
| 08 | `08-template-consolidation.md` | `2026-09-25-template-consolidation-design.md` | 02, 06, 07 (for boundaries only) |
| 09 | `09-js-static-assets.md` | `2026-09-25-js-static-assets-design.md` | 00 (chained-select allowlist) |
| 10 | `10-htmx-chargen-pilot.md` | `2026-09-25-htmx-chargen-design.md` | 00, 02, 03, 04, 09 |
| 11 | `11-scene-chat-htmx.md` | `2026-09-25-scene-chat-htmx-design.md` | 00, 09; reuses 10's htmx conventions if that design exists |

## Suggested waves for running the design agents

Designs depend on earlier designs, not on implementation. Each wave can run in parallel.

1. **Wave 1:** 00 and 01.
2. **Wave 2:** 02, 06, 07 and 09.
3. **Wave 3:** 03, 08 and 11.
4. **Wave 4:** 04, then 05.
5. **Wave 5:** 10.

If you run everything at once, each prompt tells the agent to state its assumptions about any missing upstream design. Reconcile those assumptions afterwards.

## Ownership boundaries (so agents don't overlap)

- **Permission gates:** 00. **Permission info in templates and list filtering:** 06.
- **Chargen step order, routing, advancement and step templates:** 02. **Merging duplicate step view classes:** 03. **Game rules:** 04.
- **Multi-button POST handlers:** 05. **Item and location CRUD, URLs and type dispatch:** 07.
- **Template deduplication and hidden queries:** 08. **Chargen templates** stay with 02, and **permission flags in templates** with 06.
- **Relocating JS without changing behaviour:** 09. **Rewriting chargen interactivity:** 10. **Rewriting scene chat:** 11.
- **Deferred deletions:** 01 does not delete code claimed by another step: permission mixins (00), permission template tags (06), `core/views/reference.py` (07) and the point-pool attribute form (10).
