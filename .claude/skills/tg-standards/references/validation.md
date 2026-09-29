# Validation, constraints and transactions

Where each kind of rule lives and how to write it: `clean()`, field validators, database
constraints, the status state machine, locking and transactions. Read it before you add a
rule that rejects data or a code path that changes points (XP, freebies, pools).

## Layers

| Rule | Put it in | Why |
|------|-----------|-----|
| Range of one value (rating 0 to 5) | Field validators and a named `CheckConstraint` | Forms show the validator message; the constraint stops raw SQL and `update()` |
| Relation between fields of one row (temporary <= permanent) | `clean()`, plus a `CheckConstraint` using `F()` when it is simple | `clean()` runs on every save |
| Uniqueness | Named `UniqueConstraint` with `violation_error_message` | `full_clean()` reports it as a field error |
| Allowed status transition | `Character.STATUS_TRANSITIONS`, checked in `Character.clean()` | One state machine for every character |
| Game rules across rows (point totals, prerequisites, costs) | A service in `characters/services/` or `game/`, or a chargen step form | Views stay thin; the same rule serves every entry point |
| Who may do it | `PermissionManager` (see [permissions.md](permissions.md)) | Not a validation concern |

## `clean()` and `save()`

- `core.models.Model.save()` and `core.base.ValidatedSaveMixin.save()` call
  `full_clean()` unless you pass `skip_validation=True`. Every save, including
  `save(update_fields=[...])`, runs `clean()`.
- Call `super().clean()` first, collect errors in a dict keyed by field name, and raise one
  `ValidationError(errors)` at the end. Use `NON_FIELD_ERRORS` only when no field fits.
- Do not query other rows in `clean()` unless the rule needs it; `Character.clean()` loads
  the stored row once to compare statuses.
- `skip_validation=True` also skips the status state machine. Use it only in migrations,
  fixtures (`core/tests/template_fixtures.py`), bulk jobs and tests that build invalid
  states on purpose.
- `QuerySet.update()` skips `clean()` and `save()` entirely; constraints still apply.

## Constraints

- Name every constraint with an app and model prefix and give it a
  `violation_error_message`:

```python
class Meta:
    constraints = [
        CheckConstraint(
            check=Q(xp__gte=0),
            name="characters_character_xp_non_negative",
            violation_error_message="XP cannot be negative",
        ),
    ]
```

- A constraint may only reference the model's own columns. In multi-table inheritance,
  `status` lives on the tree root's table, so a subclass cannot constrain it (the reason
  `Character` validates status transitions in `clean()`).
- Paired permanent/temporary stats: build both fields and their constraints with
  `core.linked_stat.linked_stat_fields(name, default=..., min_permanent=...)` and spread
  its `constraints(prefix)` into `Meta.constraints`.
- An existing database gets a new constraint only through a `tg_schema` migration that
  first repairs violating rows ([schema-changes.md](schema-changes.md), 0008).

## Status changes

- `core.constants.CharacterStatus`: `Un` (Unapproved, the default), `Rev` (Returned for
  revisions), `Sub`, `App`, `Ret`, `Dec`.
- Characters follow `Character.STATUS_TRANSITIONS`
  ([`characters/models/core/character.py`](../../../../characters/models/core/character.py));
  other `Model` subclasses only check that the value is a valid choice.
- Change status only through its owners: `core.services.approval.ApprovalService`
  (submit, return, approve) and `characters.services.status.change_character_status`
  (retire, decease). Views and forms never set `status` directly; the route policy's field
  guard rejects non-staff attempts.
- Moving a character into `Ret` or `Dec` runs `Character.remove_from_organizations()`.

## Transactions and locking

- `DATABASES["default"]["ATOMIC_REQUESTS"] = True` wraps every request in a transaction
  (`core/tests/test_settings.py` asserts it). Management commands and Channels consumers
  are not requests: open `transaction.atomic()` yourself.
- Anything that reads and then writes points (XP, freebies, pools, counters) locks the
  row: `Model.objects.select_for_update().get(pk=...)` inside `transaction.atomic()`, then
  saves with `update_fields`. Follow `Character.add_xp` / `Character.spend_xp`.
- `core.actions.ObjectActionView` runs `perform()` inside `transaction.atomic()`; set
  `lock = True` to re-read the subject with `select_for_update()` first.
- A service reports refusal by raising `ValidationError` or returning a result object
  with `success=False` and `error` (`characters/services/result.py`); `ObjectActionView`
  turns either into a flashed error.

## Testing validation

- Model rule: `with self.assertRaises(ValidationError): obj.full_clean()` (or `save()`).
- Constraint: `QuerySet.update()` or `save(skip_validation=True)` inside
  `self.assertRaises(IntegrityError)` wrapped in `transaction.atomic()`.
- Service rule: call the service; assert the refusal and that nothing changed.
- Concurrency-sensitive code: `core/tests/integration/test_transactions.py` shows the
  pattern.

## Checklist

- [ ] Single-value ranges have validators and a named constraint.
- [ ] Cross-field rules in `clean()`; one `ValidationError` with a field-keyed dict.
- [ ] Status changes go through `ApprovalService` or `change_character_status`.
- [ ] Point changes lock the row inside `transaction.atomic()`.
- [ ] `skip_validation` and `update()` only in migrations, fixtures, bulk jobs, tests.
- [ ] Tests for each rejection and for the success case.

## See also

- [docs/architecture/data-model.md](../../../../docs/architecture/data-model.md) (status lifecycle)
- [docs/architecture/xp-and-approvals.md](../../../../docs/architecture/xp-and-approvals.md)
- [`core/services/approval.py`](../../../../core/services/approval.py)
- [models.md](models.md), [schema-changes.md](schema-changes.md)
