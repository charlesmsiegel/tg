# Game rules out of views (Step 4)

## Intent and compatibility

Implement the Step 4 brief (`docs/code-fixing/04-game-rules-out-of-views.md`),
superseding its historical design-only restriction, as Steps 0, 2, 3, 6, 7 and 9
were. After this step a chargen or game view binds a form, calls a model method,
selector or service, and maps the result to a message and a response. The game
rules themselves stay the same except where this document names a defect and says
what was done about it.

Upstream designs this builds on (all implemented on `main`):

* **Step 0 (authorization):** gates stay where they are. `decide_spending_request`
  already locks and applies spending decisions. This step adds no permission
  checks and removes none.
* **Step 2 (registry):** `advance(character, user=...)` is still the only
  navigation operation. Views, not services, call it.
* **Step 3 (generic steps):** duplicate step views are already merged.
  `HumanAbilityView`, `FreebieSpendingView`, `PointAllocationView` and the
  others are the shared bases that this step changes. Companion and Sorcerer
  freebies already use `FreebieSpendingServiceFactory`.

Out of scope: splitting multi-action POST handlers (Step 5; this step makes
their bodies one call each), permission policy (Step 0), rewriting the client
JavaScript (Step 10), and schema changes. There are **no migrations**.

## Audit: confirmed and refuted findings (HEAD `a0e23a0`)

The audit was taken at `c1c509a`, before Steps 3, 6, 7 and 9 landed, so several
"Reported" findings are already gone.

| Brief finding | Status now | Evidence |
|---|---|---|
| Mage module-level XP-cost helpers (`mage.py:10-34`) | **Refuted**: removed | `mage.py` imports `XPSpendingServiceFactory`; there are no cost helpers |
| `MageDetailView.post` Rote validation ladder | **Confirmed** | `mage.py:163-222`, 15 checks |
| Ladder duplicated in `MageRoteView.form_valid` | **Confirmed** | `mage.py:536-587` |
| `MageFocusView` practices = Arete, 2 ability dots per practice dot, creates `PracticeRating` | **Confirmed**, with more defects: tenets are saved *before* the practice checks, and rows are created one at a time, so a later failure leaves earlier rows behind | `mage.py:359-402` |
| `MageSpheresView` `freebies -= 4` per Arete dot | **Confirmed** | `mage.py:432-451` |
| `form_invalid → form_valid`: `mage.py` ×2, `sorcerer.py` ×2, `companion.py` | **Confirmed** at `mage.py` (Spheres, Rote) and `sorcerer.py:80` (Basics). **Refuted** at `companion.py` and at the second `sorcerer.py` site: Step 3 removed both | `grep "def form_invalid" -A8` |
| Companion freebie math in `CompanionFreebiesView` | **Refuted**: it goes through the service (Step 3). **New finding:** budget setup moved to `CompanionExtrasView.prepare_character` (`companion.py:230-254`) | |
| Attribute distribution in the view | **Confirmed** | `HumanAttributeView.form_valid`, `human.py:107-147` |
| Ability distribution in the view | **Confirmed** | `HumanAbilityView.form_valid`, `human.py:178-212` |
| Background total in the view | **Confirmed** | `HumanBackgroundsView.form_valid`, `backgrounds.py:29-48` |
| Changeling arts = 3, realms = 5 in the view | **Confirmed** | `ChangelingArtsRealmsView.form_valid`, `changeling.py:166-242` |
| Merit/flaw cost rules written twice in `human.py` | **Refuted**: the rules now live only in `characters/costs.py` (`get_meritflaw_xp_cost`) and the services | |
| Kinfolk tribe restrictions keyed on name strings | **Confirmed**, and duplicated in `Kinfolk.add_background` | `kinfolk.py:114-223`, `models/werewolf/kinfolk.py:97-120` |
| Vampire `set_willpower()` vs Demon direct assignment | **Confirmed**. Thrall also assigns directly. See defect D1 | `vampire_chargen.py:250`, `demon_chargen.py:308`, `thrall_chargen.py:103` |
| Fera `isinstance` dispatch | **Confirmed**: 48 calls across 3 methods (`get_form_class`, `get_form`, `form_valid`) plus `FeraGiftsView.get_context_data` (139 lines) | `fera.py` |
| `ChronicleDetailView.get_context_data` builds many querysets | **Confirmed**: 8 base querysets and 11 grouped projections | `game/views.py:96-222` |
| `WeekListView` counts scenes in Python | **Confirmed**: a linear scan per week | `game/views.py:584-619` |
| `WeeklyXPRequestCreateView.form_valid` saves twice | **Confirmed**: `player_save()` commits, then `ModelFormMixin.form_valid` saves again | `game/views.py:733-743` |
| `XPSpendingRequestApproveView` skips the service | **Refuted**: it calls `decide_spending_request` (Step 0) | `game/views.py:1020-1041` |
| `straighten_quotes` defined twice | **Confirmed**. The two copies behave identically over U+0000–U+2FFF and U+FF00–U+FF0F | `game/views.py:386`, `game/consumers.py:224` |
| Client-side validators copy the rules | **Confirmed**. The totals come in as data attributes, but the per-trait maxima are hardcoded in JS (for example ability max 3) | `characters/static/characters/js/*-validation.js` |

Rule-bearing views that the brief did not list:

* Vampire disciplines (exactly 3, clan only), Vampire virtues (total 7; derives
  Humanity or Path).
* Ghoul disciplines (at most 2, available only).
* Demon lores (exactly 3), Demon and Thrall virtues (total 6; Willpower =
  Courage).
* Wraith arcanoi (exactly 5, each at most 5).
* Sorcerer Psychic and Path numina (exactly 5; Willpower 5; freebies 21).
  These read raw POST data through `MultipleFormsetsMixin.get_form_data`, and
  `int()` on that data raises a 500 on bad input.
* Sorcerer rituals.
* The Demon Apocalyptic Form (4 low, 4 high, at most 16 points, no overlap). It
  **clears the existing trait selections before validating**.
* Fera gifts (exactly 3, allowed) and Fera history.
* Mage detail specialties. These read raw `request.POST` and `get_or_create`
  arbitrary `stat` keys even though `SpecialtiesForm` exists.

## Placement taxonomy

| Kind of rule | Destination | Test |
|---|---|---|
| **Input validation.** Anything decidable from submitted data plus the character's current state, with no writes: distribution totals, per-trait bounds, required-choice ladders, "only clan disciplines", tribe background limits | `Form.clean()` / `Formset.clean()`, raising `ValidationError` with the existing message text | Is it a yes/no about *this submission*? |
| **State-changing operation.** Writes more than the bound form's own fields, spends a pool, creates related rows, or must be atomic: learning a rote, starting practices, buying Arete with freebies, applying an Apocalyptic Form, awarding weekly XP | A **service** function or class in `characters/services/` or `game/services`, running in one transaction and returning a result object | Does it change state beyond `form.save()`? |
| **Derived value.** A value computed from other traits of the same object: Willpower from Courage, Humanity or Path from virtues, Fera breed and aspect side effects, starting gift groups | A **model method** on the most specific polymorphic class that owns the rule | Is it a function of the object's own fields? |
| **Read-side aggregation.** Querysets grouped or counted for display | A **selector** (`game/selectors.py`) or QuerySet method | Is it read-only and presentation-shaped? |
| **Rule data.** Totals, bounds, costs, tribe limits | `characters/rules/` (limits) and `characters/costs.py` (costs, unchanged) | Could a client-side hint need it? |

A view may only: pick the form or formset and its rule data, call
`is_valid()`, call **one** model method or service, call `advance()` (Step 2
owns navigation), flash the result's message, and redirect. A view may not
compute a sum, compare against a limit, or write a trait.

## Rule data: `characters/rules/`

Costs stay in `characters/costs.py`, which the spending services already share;
this step does not rewrite it. Allocation limits get one home:

```
characters/rules/__init__.py      # re-exports
characters/rules/allocation.py    # AllocationRule, PriorityRule, RuleViolation
characters/rules/limits.py        # named rule instances + tribe background limits
```

```python
@dataclass(frozen=True)
class RuleViolation:
    message: str          # form error (non-field unless `field` is set)
    field: str | None = None
    flash: str | None = None   # optional extra messages.error text, kept verbatim

@dataclass(frozen=True)
class AllocationRule:          # "these fields sum to exactly/at most N, each in [min, max]"
    name: str
    fields: tuple[str, ...]
    total: int
    comparison: Literal["exact", "at_most"] = "exact"
    minimum: int = 0
    maximum: int | None = None
    # message templates, formatted with total= and current=
    def violations(self, values: Mapping[str, int]) -> list[RuleViolation]: ...
    def client_data(self) -> dict[str, int | str]: ...    # for Step 10 data-* attributes

@dataclass(frozen=True)
class PriorityRule:            # "groups sorted equal primary/secondary/tertiary (+ base per field)"
    name: str
    groups: tuple[tuple[str, ...], ...]
    points: tuple[int, int, int]
    base: int = 0              # 1 for attributes (every attribute starts at 1)
    minimum: int = 0
    maximum: int = 5
    def violations(self, values) -> list[RuleViolation]: ...
    def client_data(self) -> dict: ...
```

The rules are plain data with pure functions, so they need no database for unit
tests. `client_data()` returns primitives (`{"total": 3, "max": 5, ...}`). Step
10 renders these as `data-*` attributes, and existing templates keep their
`primary`/`secondary`/`tertiary` context keys (they now come from
`rule.points`). **Per-type values stay as the view adapter configuration they
already are** (`primary = 13` on `MageAbilityView`). Step 3 made those adapters
the per-type configuration surface, and moving 40 of them into a dict would add
churn for no gain. The view turns them into a rule with `get_allocation_rules()`,
and the form enforces it. A second consumer, such as the client, reads the same
object from the context.

Tribe background limits become data rather than name-keyed `if` chains:

```python
KINFOLK_TRIBE_BACKGROUND_LIMITS = {
    "Bone Gnawers": {"forbidden": {"pure_breed"}, "max": {"resources": 3}},
    "Glass Walkers": {"forbidden": {"pure_breed", "mentor"}},
    "Red Talons": {"forbidden": {"resources", "allies", "contacts"}},
    "Shadow Lords": {"forbidden": {"mentor"}},
    "Silent Striders": {"max": {"resources": 3}},
    "Stargazers": {"max": {"resources": 3}},
    "Wendigo": {"max": {"resources": 3}},
    "Silver Fangs": {"required": {"pure_breed"}},
}
```

The table is still keyed on the tribe *name*, because `Tribe` has no slug and
this step adds no migrations. What changes is that one table replaces two
parallel `if` chains: the view's and `Kinfolk.add_background`'s. A later schema
step can move it onto `Tribe` rows.

## Forms

`characters/forms/core/allocation.py`:

* `AllocationFormMixin`: a `clean()` that evaluates `self.allocation_rules`
  (passed as the `allocation_rules=` kwarg) against `cleaned_data`, adds each
  `RuleViolation` as a field or non-field error, and collects `flash` texts in
  `form.flash_errors` so that `AllocationStepMixin.form_invalid` can emit the
  same `messages.error` calls the views make today. Rule checks run in the
  order the views run them, so the **first** error message stays the same.
* `allocation_modelform(model, fields)`: a cached `modelform_factory` with
  the mixin, used by every `UpdateView` step that sets `fields = [...]`.
* `AllocationStepMixin` (views, in `characters/views/core/allocations.py`):
  its `get_form_kwargs` passes `get_allocation_rules()` and its `form_invalid`
  flashes `form.flash_errors`. Steps with dynamic rules, such as Vampire's
  clan disciplines or the Ghoul's available disciplines, override
  `get_allocation_rules()` or supply a `extra_clean(form, cleaned_data)` model
  hook.

`BackgroundRatingFormSet.clean()` gains the background-points total and asks
the character for extra limits through `character.background_violations(ratings)`.
`Human` returns `[]` and `Kinfolk` returns the tribe table checks. The
Silver Fangs check (a requirement across rows) runs after the per-row checks,
as it does today.

`RoteCreationForm.clean()` absorbs the 15-step ladder with the exact same
messages and order. It is used by both the detail-page XP purchase and the
chargen step.

`SorcererBasicsForm` validates the chained foreign keys itself, restricting
choices to the fellowship's favoured attributes and paths, so the view no longer
deletes errors and trusts raw `form.data`.

`MageSpheresForm` declares `resonance` as a required `CharField`. Resonance is
typed free text that `add_resonance` resolves; the model's M2M validation was
the only reason errors were being deleted.

`PracticeRatingFormSet` gains `clean()`: the practices sum to Arete, and each
practice's rating is at most half its associated ability dots.

Sorcerer Psychic and Path steps bind the real formsets (`Psychic/Numina
PathRatingFormSet`) instead of `get_form_data`, and their `clean()` enforces a
total of 5.

`ApocalypticFormSelectionForm` builds the dynamic trait fields and validates
4 + 4, the 16-point budget and the overlap rule *before* anything is written.

## Model methods (derived values)

| Method | Owner | Replaces |
|---|---|---|
| `Human.apply_courage_willpower(courage)` → `set_willpower(courage)` | `Human` | direct `willpower =` in Demon and Thrall virtues (D1) |
| `Vampire.apply_virtues(virtue_1, virtue_2, courage)` | `Vampire` | the humanity/path block in `VampireVirtuesView` |
| `Vampire.active_virtue_values(cleaned)` | `Vampire` | conscience/conviction and self-control/instinct selection |
| `Mage.purchase_starting_arete(arete)` | `Mage` | `freebies -= 4` loop (`MageSpheresView`) |
| `Fera.chargen_choice_fields`, `Fera.chargen_help_text`, `Fera.starting_gift_groups()`, `Fera.apply_chargen_choice(field, value)` | each Fera subclass (class attributes) + `Fera` | three 12-way `isinstance` switches and the 139-line context method |
| `Companion.prepare_starting_freebies()` | `Companion` | `CompanionExtrasView.prepare_character` body |
| `Kinfolk.background_violations(ratings)` | `Kinfolk` (default on `Human`) | view `if tribe_name ==` chain and `add_background` chain |

The Fera methods are polymorphic by **declaration**. Each subclass states
`chargen_choice_fields = ("breed", "aspect")`, `chargen_help_text = {...}` and
`gift_group_fields = (("aspect_gifts", "aspect"),)`. The base class turns those
into the form class, the help text and the gift querysets. `apply_chargen_choice`
calls `set_<field>` only when a subclass defines one, and otherwise leaves the
plain field assignment that `form.save(commit=False)` already made. Nuwisha's
"optional role" and Corax's and Nuwisha's fixed gift lists are expressed the same
way (`optional_choice_fields`, `fixed_gift_groups`).

## Services

New operations follow the existing spending services:

```python
@dataclass
class ServiceResult:          # characters/services/result.py
    success: bool
    message: str = ""
    error: str | None = None
    object: Any = None
```

It has the same shape as `XPSpendResult` and `FreebieSpendResult`
(`success`/`message`/`error`). The existing classes are unchanged.

| Service | Signature | Transaction |
|---|---|---|
| `characters/services/rotes.py` | `learn_rote(mage, cleaned_data) -> ServiceResult` | `atomic`; locks the mage row (`select_for_update`); re-reads `rote_points`; creates Effect/Rote; deducts; fails with "Not enough Rote Points" when the locked balance is short |
| `characters/services/mage_chargen.py` | `set_starting_practices(mage, tenet_form, practice_rows) -> ServiceResult` | `atomic`; saves tenets and replaces the mage's `PracticeRating` rows together, or does neither |
| same | `apply_spheres_step(mage, form) -> ServiceResult` | `atomic`; saves the spheres form, adds resonance, calls `purchase_starting_arete` |
| `characters/services/sorcerer_chargen.py` | `set_starting_numina(sorcerer, rows) -> ServiceResult` | `atomic`; creates `PathRating`s, then Willpower 5 and freebies 21 |
| `characters/services/demon_chargen.py` | `apply_apocalyptic_form(demon, low, high) -> ServiceResult` | `atomic`; writes only after the form has validated |
| `game/services.py` | `submit_weekly_xp_request(form) -> WeeklyXPRequest` | one save; the duplicate check runs inside the transaction |
| `FreebieSpendingServiceFactory.locked(character)` / `XPSpendingServiceFactory.locked(character)` | context manager yielding a service bound to a `select_for_update` re-read of the character | `atomic` |

**Locking.** `decide_spending_request` already locks for approval. For
spending, the view enters `Factory.locked(self.object)`, which opens a
transaction, re-reads the character with `select_for_update()` (a no-op on
SQLite, a row lock on PostgreSQL), and hands the service the fresh instance.
Two concurrent spends therefore serialize, and the second sees the first's
deduction. The service classes themselves stay unchanged, so their 69 unit tests
keep driving them with in-memory instances. `spend()` also runs inside
`transaction.atomic()` so that a handler that fails after `_record_spending`
leaves no partial row.

**Result mapping.** Views map `success=True` to `messages.success(result.message)`
(when there is a message) plus `advance()`/redirect, and `success=False` to
`form.add_error(None, result.error)` plus `form_invalid`. Unexpected exceptions
propagate: services catch `ValidationError` and nothing broader.

## Removing validation bypasses

* Delete every `form_invalid` that calls `form_valid`: `MageSpheresView`,
  `MageRoteView` and `SorcererBasicsView`. The forms now validate what the
  views used to paper over.
* No raw `request.POST[...]` / `form.data[...]` where a form exists:
  `MageDetailView` specialties use `SpecialtiesForm`, `SorcererBasicsView`
  uses `cleaned_data`, `MageSpheresView` uses `cleaned_data["resonance"]`, and
  Sorcerer numina use the formsets.
* No mutation before validation: `MageFocusView` no longer saves tenets before
  checking practices, and `DemonApocalypticFormView` no longer clears traits
  before validating.
* `game/views.py` `request.POST["char_type"]`-style reads are a redirect
  selector for Step 5's endpoint split and are not game rules. They stay.

## Read side (game app)

`game/selectors.py`:

* `chronicle_overview(chronicle, user) -> dict`: exactly the context keys
  `ChronicleDetailView` builds today, including the non-staff owner filtering
  (a Step 0 rule that the selector preserves, not changes).
* `annotate_week_scene_counts(weeks, user)`: sets `week.cached_scene_count`
  from one query of visible finished scenes. It sorts their latest post dates
  once and counts each week's window with `bisect`, replacing the per-week
  linear scans.

`straighten_quotes` moves to `game/text.py`. Both `SceneDetailView` and
`SceneChatConsumer` keep a `straighten_quotes` staticmethod alias, because
tests call them.

## Rule-by-rule table

| # | Rule | Current location | Destination / API | Pinned by |
|---|---|---|---|---|
| R1 | Rote create/select ladder (15 checks, exact messages) | `MageDetailView.post`, `MageRoteView.form_valid` | `RoteCreationForm.clean()` | new `characters/tests/forms/mage/test_rote_rules.py` (one case per message) + existing `test_mage*.py` |
| R2 | Rote learning: effect learnable, cost ≤ rote points, deduct, add | `RoteCreationForm.save` (called from views) | `learn_rote(mage, cleaned_data)` service, atomic + lock; `save()` delegates | service unit tests; existing view tests |
| R3 | Rote step advances when rote points reach 0 | `MageRoteView` | stays in view (navigation) | existing |
| R4 | Tenets required (met/per/asc) | `MageFocusView.form_valid` | `MageFocusForm.clean()` | new form tests |
| R5 | Practices sum to Arete; rating ≤ ability dots / 2 | `MageFocusView.form_valid` | `PracticeRatingFormSet.clean()` | new formset tests + characterization |
| R6 | Starting `PracticeRating` rows | `MageFocusView.form_valid` | `set_starting_practices` service (atomic) | service test incl. no partial rows |
| R7 | Arete above 1 costs 4 freebies each, `spent_freebies` entries | `MageSpheresView.form_valid` | `Mage.purchase_starting_arete(arete)` | model test + characterization (freebies and JSON records identical) |
| R8 | Resonance required, typed name | `MageSpheresView.form_invalid` hack | `MageSpheresForm.resonance` `CharField` | form test |
| R9 | Attribute range 1–5; priorities P/S/T over physical/social/mental (+3 base) | `HumanAttributeView.form_valid` | `PriorityRule(base=1, minimum=1, maximum=5)` in `AllocationFormMixin` | `test_allocation_rules.py` + existing attribute view tests |
| R10 | Abilities 0–3; talents/skills/knowledges P/S/T | `HumanAbilityView.form_valid` | `PriorityRule(maximum=3)`; view keeps its optional flash messages | same + existing |
| R11 | Backgrounds total = `background_points` (× multiplier) | `HumanBackgroundsView.form_valid` | `BackgroundRatingFormSet.clean()` | formset test + existing |
| R12 | Kinfolk tribe background limits | `KinfolkBackgroundsView.form_valid`, `Kinfolk.add_background` | `KINFOLK_TRIBE_BACKGROUND_LIMITS` + `Kinfolk.background_violations()` | table-driven test per tribe; existing kinfolk tests |
| R13 | Changeling arts = 3, realms = 5, each ≤ 5 | `ChangelingArtsRealmsView` | two `AllocationRule`s | rule tests + existing |
| R14 | Vampire disciplines = 3, clan only | `VampireDisciplinesView` | `AllocationRule` + clan-only check in form hook | existing vampire tests |
| R15 | Vampire virtues = 7; WP = Courage; Humanity/Path = v1 + v2 | `VampireVirtuesView` | rule + `Vampire.apply_virtues()` | model test + existing |
| R16 | Ghoul disciplines ≤ 2, available only | `GhoulDisciplinesView` | `AllocationRule(comparison="at_most")` + form hook | existing |
| R17 | Demon lores = 3 | `DemonLoresView` | `AllocationRule` | existing |
| R18 | Demon/Thrall virtues = 6; WP = Courage | `DemonVirtuesView`, `ThrallVirtuesView` | rule + `apply_courage_willpower` (D1) | new regression test |
| R19 | Wraith arcanoi = 5, each ≤ 5 | `WraithArcanosView` | `AllocationRule` | existing |
| R20 | Numina = 5; WP 5; freebies 21 | `SorcererPsychicView`, `SorcererPathView` | formset `clean()` + `set_starting_numina` | new + existing sorcerer tests |
| R21 | Apocalyptic form 4/4, ≤ 16, disjoint | `DemonApocalypticFormView` | `ApocalypticFormSelectionForm.clean()` + `apply_apocalyptic_form` | new test proving no mutation on invalid |
| R22 | Fera breed/faction fields, help, setters | `FeraBreedFactionView` | Fera class attributes + `apply_chargen_choice` | existing `test_fera.py` + parametrized per type |
| R23 | Fera starting gift groups | `FeraGiftsView.get_context_data` | `Fera.starting_gift_groups()` | per-type context test |
| R24 | Fera gifts exactly 3 and allowed | `FeraGiftsView.form_valid` | `FeraGiftsForm.clean()` | existing |
| R25 | Companion starting freebies and familiar package | `CompanionExtrasView.prepare_character` | `Companion.prepare_starting_freebies()` | existing Step 3 characterization |
| R26 | Sorcerer fellowship-constrained casting attribute / affinity path | `SorcererBasicsView` bypass | `SorcererBasicsForm.clean_*` | new form tests |
| R27 | Mage detail specialties | `MageDetailView.post` raw POST | `SpecialtiesForm` | new view test (unknown stat rejected) |
| R28 | Weekly XP request duplicate + single save | `WeeklyXPRequestCreateView` | `submit_weekly_xp_request` | new test counting saves |
| R29 | Chronicle overview querysets | `ChronicleDetailView` | `chronicle_overview` selector | existing chronicle tests |
| R30 | Week scene counts | `WeekListView` | `annotate_week_scene_counts` | existing + bisect boundary test |
| R31 | `straighten_quotes` | two copies | `game/text.py` | existing both call sites |

## Defects found: owner decisions

The brief says not to silently "fix" rules. Each defect below is either
**preserved** (with a pinning test) or **fixed** because it is not a game rule
but a crash, bypass or data-integrity problem.

| # | Defect | Action |
|---|---|---|
| D1 | Demon/Thrall virtues assign `willpower = courage` directly, which leaves `temporary_willpower` above permanent. Vampire uses `set_willpower`. | **Fixed** by routing through `set_willpower` (same permanent value; temporary is capped as it is for Vampire). This is a consistency fix, not a rules change |
| D2 | `CompanionExtrasView` keys budgets on `"acoylte"`, `"backup"` and `"ally"`, which are not `companion_type` choices (`companion`, `consor`, `familiar`). A plain "companion" gets no budget. | **Preserved**; owner to decide the intended budget |
| D3 | `Ratkin.set_breed` checks `"rodent"`, but the choice is `"rodens"`, so rodens never get Gnosis 5. `Ratkin.set_aspect` checks `"knife_skull"`, but the choice is `"knife_skulker"`. | **Preserved**; owner to confirm |
| D4 | The base `Fera` has no `set_breed`. The generic branch of `FeraBreedFactionView` would crash for a plain `Fera`. | **Preserved** (declared fields `("breed", "faction")`; plain assignment only, no setter) |
| D5 | Starting Arete bought on the Spheres step writes `spent_freebies` JSON but no `FreebieSpendingRecord`, so an ST cannot review it the way a later Arete freebie purchase is reviewed. | **Preserved**; owner to decide |
| D6 | `SorcererPsychicView` has a no-op check (`if rating > willpower // 2: pass`). | **Preserved** (dropped as dead code; behaviour identical) |
| D7 | Apocalyptic Forms are looked up by `"<demon name>'s Apocalyptic Form"`, so two demons with the same name share one form. | **Preserved**; owner to decide (fixing it needs a data migration) |
| D8 | `MageFocusView` saved tenets and early `PracticeRating` rows before later checks failed. | **Fixed** (validation before mutation; atomic) |
| D9 | `DemonApocalypticFormView` cleared saved traits before validating. | **Fixed** |
| D10 | Sorcerer numina steps return a 500 on non-integer ratings and accept any path pk. | **Fixed** (formset validation; querysets restricted by `numina_type` as the formset already declares) |
| D11 | `SorcererBasicsView` accepted any Attribute or path pk. | **Fixed** (restricted to the fellowship's favoured choices, as the UI offers) |
| D12 | Mage detail specialties accepted arbitrary `stat` keys. | **Fixed** (only `needed_specialties()` fields) |
| D13 | Numeric checks (discipline, lore and virtue totals) have no per-trait upper bound beyond the model validators. | **Preserved** |

## Test strategy

1. **Characterization first.** Before each slice, add view-level tests that pin
   the current observable behaviour: persisted fields, `spent_freebies`
   entries, error text, flash messages, redirect target and `creation_status`.
   Run them against the unchanged code, then keep them green through the move.
   The Step 3 suites (`test_shared_*`) already cover the language, specialty,
   ability, extras and freebie steps.
2. **Unit tests without views.** `characters/tests/rules/test_allocation.py`
   covers the pure rule objects (no database). Form tests in
   `characters/tests/forms/` cover `clean()` messages, and service tests in
   `characters/tests/services/` cover atomicity (inject a failure and assert no
   rows remain).
3. **Regression tests for each fixed defect** (D1, D8–D12), written failing
   first.
4. **Bypass guard.** An AST test (`characters/tests/test_view_rules_guard.py`)
   fails if any `form_invalid` under `characters/views` calls `form_valid`.

## PR slicing (implemented here as ordered commits in one PR)

1. Rules package, allocation forms and mixin, core attribute, ability and
   background steps (R9–R11).
2. Rote validation and service; Mage focus, spheres and specialties
   (R1–R8, R27).
3. Gameline allocation steps: Changeling, Vampire, Ghoul, Demon, Thrall, Wraith
   (R13–R19), plus derived-stat model methods (D1).
4. Sorcerer basics and numina; Demon Apocalyptic Form (R20, R21, R26).
5. Kinfolk tribe table (R12); Companion budgets (R25).
6. Fera polymorphism (R22–R24).
7. Game app: selectors, weekly XP single save, `straighten_quotes`, locked
   spending factories (R28–R31).
8. The bypass guard test and the implementation record.

Each slice is independently revertible. Slices 1 and 3 share only the mixin
from slice 1.
