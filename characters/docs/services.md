# Services

This page is the reference for [`characters/services/`](../services/): the XP and freebie
spending services (one per character type, chosen by a factory), and the small
single-purpose services that chargen steps and sheet actions call. It is for developers
changing how a spend is priced, recorded, approved or denied, or adding a character type.
The player and storyteller flow around these services (queues, approval pages, weekly XP)
is in [XP, freebies and approvals](../../docs/architecture/xp-and-approvals.md).

## Shape of a service call

Services take a model instance, do all their writes in one transaction, and return a
result object instead of raising for expected failures:

| Result | Fields | Returned by |
|--------|--------|-------------|
| `services.result.ServiceResult` | `success`, `message`, `error`, `object`; constructors `ok(message="", obj=None)` and `fail(error)` | The single-purpose services below |
| `xp_spending.XPSpendResult` / `XPApplyResult` | `success`, `trait`, `cost` (spend only), `message`, `error` | XP services |
| `freebie_spending.FreebieSpendResult` / `FreebieApplyResult` | Same shape | Freebie services |

Views flash `message` on success and add `error` to the form otherwise.

## Spending services

Two parallel packages share one design:
[`xp_spending/`](../services/xp_spending/) and
[`freebie_spending/`](../services/freebie_spending/). Each has a `base.py` with the
framework and the `Human...` service, and one module per gameline.

### Handlers and appliers

A service class declares methods with two decorators:

- `@handler("<Category>")` handles `spend(category=..., example=..., value=..., note=...,
  **kwargs)` for one form category (`"Attribute"`, `"Sphere"`, `"Discipline"`, ...).
- `@applier("<trait_type>")` handles approval (and, for freebies, reversal) of a stored
  record whose `trait_type` matches (`"attribute"`, `"sphere"`, ...).

A metaclass (`XPSpendingServiceMeta`, `FreebieSpendingServiceMeta`) builds per-class
`_handlers` and `_appliers` registries and merges the parents', so a subclass inherits
every category and can add or override one. `spend()` returns a failed result for an
unknown category; a `ValidationError` raised inside a handler becomes a failed result too.
`available_categories` and `available_appliers` list what a service supports.

### Factories

`XPSpendingServiceFactory` and `FreebieSpendingServiceFactory` map `character.type` to a
service class. Each gameline module calls `Factory.register(type, ServiceClass)` at import
time, and the package `__init__` imports every gameline module so the registry is complete.

- `get_service(character)` returns the registered service, or the `Human...` service for
  an unregistered type.
- `locked(character)` is a context manager: it opens a transaction, re-reads the
  character with `select_for_update()` and yields a service around that fresh row, so
  concurrent spends serialize. Views spend through `locked()`; the service's `character`
  attribute is the up-to-date instance afterwards.

```python
from characters.services.freebie_spending import FreebieSpendingServiceFactory

with FreebieSpendingServiceFactory.locked(character) as service:
    result = service.spend(category="Attribute", example=strength, value=None, note="")
if not result.success:
    form.add_error(None, result.error)
```

### XP: spend, then approve or deny

An XP handler computes the cost (see [Costs and rules](costs-and-rules.md)) and calls
`Character.spend_xp(trait_name=..., trait_display=..., cost=..., category=...,
trait_value=...)`, which deducts the XP and creates a `Pending`
`game.models.XPSpendingRequest`. The trait does not change yet.

A storyteller decides the request through `game.spending_approval.decide_spending_request()`
(called by `XPRequestApproveView` / `XPRequestRejectView` and the approval pages). It locks
the request and the character, then calls:

- `service.apply(request, approver)`: the applier sets the trait (usually through
  `Character.approve_xp_spend()`) and marks the request `Approved`. An applier that
  cannot make the change returns `success=False` without touching the request;
  `decide_spending_request()` then raises `SpendingDecisionError`, the request stays
  `Pending` and the XP stays reserved until the storyteller denies it. The `background`
  applier does this when no `BackgroundRating` matches the recorded name and note
  (`characters.services.trait_names.split_background_trait_name` parses the stored
  `"Name (note)"` string) or when the rating is no longer one dot below the value the
  request paid for; on success it writes that value rather than adding a dot.
- `service.deny(request, denier)`: refunds the cost and marks the request `Denied`.

Player-facing XP spending goes through `game.xp_spend` and `game.forms.XPSpendForm`, and
through `MageXPSpendView` for the Mage sheet.

### Freebies: spend immediately, record, reverse on denial

A freebie handler checks the budget and trait maximum, changes the trait at once, records
a `game.models.FreebieSpendingRecord` (`_record_spending()`) and deducts the cost
(`_deduct_freebies()`). The record's `trait_value` is the value the spend set, and its
`trait_type` names the applier that reverts it: a background the spend created is recorded
as `new-background`, a raise of one the character already had as `background`. `apply()`
marks the record approved (through an applier when one exists). The chargen freebie step
calls the service from `FreebieSpendingView.form_valid()` and advances once `freebies`
reaches 0.

`deny()` runs three writes in one transaction, in this order: it calls the applier with
`deny=True` to **revert** the trait, then **refunds** the cost to `freebies`, then
**marks** the record `Denied`. The revert is driven by the record, not by the trait's
current value: the shared helpers `_revert_column()` (an integer column such as an
attribute, a Sphere or Rage, with `step` for spends that add four points or lower a
trait), `_revert_catalogue_column()` (a column named by an `Attribute`, `Sphere`,
`Discipline` or similar row looked up by display name) and `_revert_rating_row()` (a
`BackgroundRating`, practice or path rating) refuse unless the trait still holds
`trait_value`, then restore the value before the spend, deleting a rating row the spend
created. A temporary pool the spend raised with its trait (Willpower, Glamour) loses the
same point and is clamped to the restored value, so points spent from the pool since are
not refilled. A player who raised the same trait again therefore cannot have the later raise
undone in place of the denied one: two pending spends on one trait are denied newest
first, and the refusal message says so. The same check applies to pools the character
spends in play (Quintessence, Rote Points, temporary Renown, Pathos, Corpus): a pool that
has moved since the spend is not reverted relative to its current value, the denial
refuses, and the storyteller corrects the sheet by hand. Records written before this
check used the same `trait_value` convention (the value the spend set, the lowered value
for a Banality or Torment reduction), so they revert the same way; one whose trait no
longer matches refuses rather than guessing. Catalogue names carry no unique constraint,
so a display name matching more than one `Attribute`, `Sphere` or similar row refuses too.

A failed revert leaves nothing behind. When the applier returns `success=False`, raises,
or no applier is registered for the record's `trait_type`, `deny()` rolls the transaction
back, logs the failure and returns `success=False` with the reason in `error` (a
`ValidationError`'s message, or a generic sentence when the failure was unexpected; the
detail stays in the log): the trait keeps its value, `freebies` is not refunded and the
record stays `Pending`.
`decide_spending_request()` turns that result into a `SpendingDecisionError`, so the
storyteller sees the failure and can correct the character by hand.

### Services per type

Categories available through `spend()` (both packages register the same types; freebie
and XP category lists differ slightly where noted):

| `type` | Service classes | Categories beyond the common set |
|--------|-----------------|----------------------------------|
| `human` | `HumanXPSpendingService`, `HumanFreebieSpendingService` | Common set: Attribute, Ability, Background, New Background, Existing Background, Willpower, MeritFlaw |
| `vtm_human`, `dtf_human`, `htr_human` | `VtMHuman...`, `DtFHuman...`, `HtRHuman...` | Virtue |
| `vampire`, `ghoul`, `revenant` | `Vampire...`, `Ghoul...`, `Revenant...` | Discipline, Virtue; XP: Morality; freebies: Humanity, Path Rating |
| `wta_human`, `kinfolk` | `WtAHuman...`, `Kinfolk...` | none |
| `werewolf` | `Garou...` | Gift, Rite, Rage, Gnosis; freebies also Glory, Honor, Wisdom |
| `fera` and every breed (`ajaba` ... `rokea`) | `Fera...`; `bastet`, `corax`, `gurahl`, `mokole`, `nuwisha`, `ratkin` have a subclass each | As `werewolf` (Rites go to `rites_known`) |
| `mta_human` | `MtAHuman...` | none |
| `mage` | `Mage...` | Sphere, Arete, Practice, Tenet, Resonance, Rote Points; XP: Remove Tenet; freebies: Quintessence |
| `companion` | `Companion...` | Advantage, Charm |
| `sorcerer` | `Sorcerer...` | Path, Ritual; freebies also Create Ritual, Select Ritual |
| `wto_human` | `WtOHuman...` | none |
| `wraith` | `Wraith...` | Arcanos, Pathos, Corpus |
| `ctd_human` | `CtDHuman...` | none |
| `changeling`, `inanimae`, `nunnehi` | `Changeling...`, `Inanimae...`, `Nunnehi...` | Art, Realm, Glamour, Banality Reduction |
| `demon`, `earthbound` | `Demon...`, `Earthbound...` | Lore, Faith, Virtue, Torment Reduction |
| `thrall` | `Thrall...` | Faith Potential, Virtue |
| `hunter` | `Hunter...` | Edge, Virtue |
| `mtr_human` | `MtRHuman...` | none |
| `mummy` | `Mummy...` | Hekau, Sekhem, Balance |

No service is registered for `fomor`, `drone`, `autumn_person` or `spirit_character`;
they get the `Human...` services.

To add a type: subclass the closest service, add `@handler` / `@applier` methods, call
`XPSpendingServiceFactory.register(...)` (and the freebie equivalent) in the module, and
make sure the package `__init__` imports it.

## Single-purpose services

| Module | Function | Called by | Behaviour |
|--------|----------|-----------|-----------|
| [`status.py`](../services/status.py) | `change_character_status(character, target)` | `CharacterRetireView`, `CharacterDeceaseView` | Checks `Character.STATUS_TRANSITIONS` and saves; `Character.save()` then removes a retired or deceased character from its organizations. The caller holds the row lock |
| [`specialties.py`](../services/specialties.py) | `record_specialties(character, cleaned_data)` | `CharacterSpecialtiesView` | `get_or_create`s a `Specialty` for each filled field and adds it |
| [`rotes.py`](../services/rotes.py) | `learn_rote(mage, cleaned_data)` | Mage `rote` chargen step, `spend_mage_xp()` | Locks and re-reads `rote_points`; creates or selects the Effect and Rote (new rows are `Sub`, owned by the mage's owner); fails when the mage cannot learn or afford the Effect, or already knows the chosen rote; deducts `effect.cost()` |
| [`mage_xp.py`](../services/mage_xp.py) | `spend_mage_xp(mage, cleaned_data, rote_data=None)` | `MageXPSpendView` | `Image` stores the upload, `Rote` calls `learn_rote()`, anything else spends through the locked XP service |
| [`mage_chargen.py`](../services/mage_chargen.py) | `set_starting_practices(focus_form)` | `MageFocusView` | Saves the Focus form and one `PracticeRating` per chosen practice in one transaction |
| [`sorcerer_chargen.py`](../services/sorcerer_chargen.py) | `set_starting_numina(sorcerer, rows, *, with_practice)` | `SorcererPsychicView`, `SorcererPathView` | Creates `PathRating` rows (no practice or ability for psychic phenomena), sets Willpower to `STARTING_WILLPOWER` (5) and freebies to `STARTING_FREEBIES` (21) |
| [`demon_chargen.py`](../services/demon_chargen.py) | `apply_apocalyptic_form(demon, low_traits, high_traits)` | `DemonApocalypticFormView` | Edits the demon's own `ApocalypticForm`, or creates one named `"<demon name>'s Apocalyptic Form"` when it has none or its form is shared with another demon, an Earthbound or a Visage default; sets both trait lists and links it; the caller advances and saves |

## Legacy model hooks

Several models still carry older spending methods: `Human.spend_xp(trait)` /
`spend_freebies(trait)` called with a single trait name, gameline `spend_freebies(trait)`
overrides, and per-category `*_freebies(form)` methods (`attribute_freebies`,
`discipline_freebies`, ...). Application code does not call them; the services above are
the supported path. The XP handlers call `character.spend_xp(trait_name=..., cost=...)`
with keyword arguments, which `Human.spend_xp()` delegates to `Character.spend_xp()`, so a
gameline model must not override `spend_xp` with a single-argument signature: that
override would shadow the keyword path and every XP spend for the type would raise
`TypeError` (`characters/tests/services/test_xp_spending_gamelines.py`). Only
`Mage.spend_xp()` overrides it, and it keeps the keyword form.

## See also

- [XP, freebies and approvals](../../docs/architecture/xp-and-approvals.md)
- [Costs and rules](costs-and-rules.md)
- [Chargen](chargen.md)
- [Character models](models.md#xp-methods)
- [`game/spending_approval.py`](../../game/spending_approval.py)
