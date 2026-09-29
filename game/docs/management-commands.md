# game management commands

This page documents the management commands in
[`game/management/commands/`](../management/commands/). There is one:
`migrate_jsonfield_to_models`. Read it before running the command on a database or
changing the spending record models it writes. The project-wide list of commands is in
the [management commands reference](../../docs/reference/management-commands.md).

## migrate_jsonfield_to_models

```bash
python manage.py migrate_jsonfield_to_models [--dry-run]
```

Source: [`migrate_jsonfield_to_models.py`](../management/commands/migrate_jsonfield_to_models.py).

Copies spending history kept in character JSON fields into rows of the spending record
models:

| Phase | Reads | Writes |
|-------|-------|--------|
| `migrate_xp_spending` | `Character.spent_xp` (a list of dicts with `trait`, `cost`, `approved`, `value`) on every character whose list is not empty | One `XPSpendingRequest` per entry: `trait_name` from `trait`, `cost`, `approved` (default `"Pending"`), and `value` stored in both `trait_type` and `trait_value` |
| `migrate_freebie_spending` | `Human.spent_freebies` (dicts with `trait`, `cost`, `value`) | One `FreebieSpendingRecord` per entry with `trait_type=""`; `approved` keeps its default `"Pending"` |

| Option | Effect |
|--------|--------|
| `--dry-run` | Prints what would be migrated and writes nothing |

Behaviour:

- An entry is skipped as a duplicate when a record with the same character, trait name
  and cost already exists (plus the same `approved` for XP, or the same value for
  freebies), so the command can be run again.
- Each phase runs in its own transaction (`@transaction.atomic`).
- Output lists every migrated or skipped entry and a `migrated/total` count per phase.

Current state of the models: `CharacterModel` no longer has a `spent_xp` field, so the
first phase fails at its first query with `FieldError: Cannot resolve keyword
'spent_xp'`, and the command stops before the freebie phase. `Human.spent_freebies`
still exists (marked deprecated in
[`characters/models/core/human.py`](../../characters/models/core/human.py)).

## See also

- [XP](xp.md)
- [game models](models.md#spending-records)
- [Management commands reference](../../docs/reference/management-commands.md)
- [Maintenance](../../docs/operations/maintenance.md)
