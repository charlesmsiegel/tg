# Generic chargen consolidation audit

Baseline: `c14f2bad`, after rebasing on main. Reproduce the current inventory with
`python scripts/inventory_chargen_views.py --output docs/superpowers/specs/generic-chargen-inventory-after.json`.
The before/after JSON files include exact and literal-normalized AST groups, bases,
configuration and own methods. Shape similarity requires semantic review. Counts
below cover view-class bodies, including configuration adapters and hooks, not
whole application source or an assertion that every remaining method is duplicate.

| Family | Classes before/after | Classes defining methods before/after | Class lines before/after |
|---|---:|---:|---:|
| AbilityView | 21/21 | 6/2 | 466/195 |
| CreateView | 79/79 | 17/17 | 1339/940 |
| DetailView | 100/100 | 25/25 | 829/830 |
| ExtrasView | 20/21 | 18/4 | 851/475 |
| FettersView | 1/1 | 1/1 | 67/16 |
| FreebiesView | 21/21 | 3/1 | 427/176 |
| LanguagesView | 21/21 | 11/1 | 459/84 |
| PassionsView | 1/1 | 1/1 | 70/17 |
| SpecialtiesView | 21/21 | 11/3 | 422/137 |
| TemplateSelectView | 6/7 | 6/1 | 264/70 |
| TemplateSelectionForm | 6/6 | 6/0 | 102/18 |
| UpdateView | 96/96 | 36/11 | 2734/1162 |

The shared FreebieSpendingView, PointAllocationView, CharacterFormStepView,
ScopedEditFormMixin and moved form/field modules sit outside some family suffixes;
the table must not be read as a net source-line reduction. Extras and template
view counts include their new shared base. The remaining Wraith ability method
is feedback only; the remaining Companion/Sorcerer specialty methods are rule
hooks. Passion/Fetter methods only translate form fields into model calls.

## Findings from the original brief

* Languages: 21 classes, 11 implementations including Human. WtA/CtD/MtA share
  behavior but differ in object queries and local variable names, not just literal
  templates. Companion used nonexistent num_languages and zero-based fields;
  Companion/Sorcerer omitted English. All three failures are reproduced and fixed.
* Specialties: 21 classes, 11 own implementations. Sorcerer did retain a companion
  variable. Preserve its rituals exclusion and four-dot path rule and Companion's
  broad ability scan; default classes use the model's needed_specialties method.
* Extras: 20 classes, 18 own implementations, rather than 18 total classes.
  Copied Awakened/mage wording is confirmed and replaced outside actual Mage
  biography. Preserve Changeling additional fields/date widgets, Vampire/Ghoul
  history wording, Companion grants/budgets and Wraith death validation/messages.
* Template selection: six form/view copies confirmed. All filter public approved
  templates by configured gameline and type. Shared code retains all six imports
  and routes and the pre-registry position-zero entry. The six shell templates
  remain because their style differences are harmless configuration.
* CRUD: 30 duplicated selectors consolidated; 24 long declarations (1,640 lines)
  composed into reviewed allowlist groups and shared constants. Original ordered
  fields are pinned by a baseline fixture. The duplicate Mage time is confirmed.
  Unrestricted model-field introspection was rejected to preserve security.
* Abilities: MtA manually expanded the same three primary pools. Its model groups
  also contain secondary abilities, so the generic calculation intersects form
  fields. Demon/DtF/Thrall share the algorithm; Wraith keeps feedback messages.
* Freebies: 21 adapters with three own implementations, including Human, confirmed.
  Companion used handwritten spending; Sorcerer duplicated validation and invoked
  form_valid from form_invalid. Shared orchestration resolves actual form choices,
  rejects invalid forms and advances only after successful final spending.
* Passions/Fetters: the same bound-check/add/complete lifecycle, with distinct
  model calls and context keys, confirmed. Dark-passion semantics remain unchanged.
* Details: 14 character details lacked the common base. They now inherit filtered
  scenes and status actions. Reference detail classes remain outside that hierarchy.
* Base templates: HumanAbility's Wraith shell was confirmed and corrected. The
  missing HumanFreebies template report is stale; Step 2 had already fixed it.
* Bespoke rules: virtues, arts/realms, apocalyptic form, paths/rituals,
  spheres/focus/rotes and breed/faction remain bespoke. Linked background creation
  remains with existing GenericBackgroundView and its specialized subclasses.
* Inheritance depth: the historical 17-class estimate is not used as a target.
  Central authorization in ChargenStepMixin remains authoritative. Removed
  per-copy gates do not introduce new policy identities or workflow slots.

## New defects pinned during characterization

* Sorcerer path specialty keys lacked Statistic rows and crashed SpecialtiesForm.
* Anonymous template GET checked object ownership before login in four copies;
  all six copies accepted template writes for locked position-zero characters.
* Companion extras advanced before setting freebies, incorrectly skipping spending
  when the old approved balance was zero.
* Retiring an already-deceased Mage raised model validation errors; common status
  handling correctly leaves it deceased.
* Vampire CRUD listed nonexistent current_willpower; its full form could not render.
* Vampire/Ghoul/Revenant update views omitted direct-view edit gates.
* Chained freebie choice IDs and category labels disagreed with service inputs.
  The adapter now converts validated IDs, background prefixes, virtue descriptors,
  Sorcerer path/ritual inputs and Mage rote/resonance inputs.

## Deliberately preserved boundaries

Companion's existing form/service cost conventions differ for Advantages
and Charms, and some Mage-derived choices are unsupported for Companion/Sorcerer.
Vampire out-of-clan discipline cost configuration also remains an existing rules
issue. This refactor preserves the services' existing rule decisions; it does not
invent prices or complete unsupported categories. Human ModelChoiceField inputs
use numeric IDs while chained background choices use bg_/br_ prefixes; both are
accepted in their validated form contracts. General concurrent/replayed POST
protection remains Step 2's inherited limitation.


## Independent review

Review found two concrete spending defects at the new adapter boundary, both fixed:
Companion Advantage requests for lower/same/unsupported ratings could create
refunds or charge for unapplied changes; the service now validates a supported
increase and checks the model operation before recording/deducting. Mage Arete
choices contain a level string, not a Practice; the shared adapter uses the
service's plain increment contract. Actual-view regression tests failed before
both fixes and passed afterward; the reviewer independently reran both inputs.
No remaining critical or important findings. Human/Drone/Fomor/Spirit sheets do
not render XP-approval buttons, so preserving their existing lack of that handler
is intentional; their common status actions and scene context are wired.


Final status-action characterization also pinned the existing model transition
map: forbidden death transitions now hide their buttons and ignore forged POSTs
without model validation exceptions. Mage's existing action-level 403 checks run
before common mutation handling. A stale Step 0 test expected the language skip
to stop at WtA Human position 7; an isolated archive of unmodified c14f2bad reproduced
its 8-versus-7 failure. Its expectation now reflects Step 2 skipping the empty
Allies step as well, and also asserts English was added.

## Final verification

The final relevant suite ran 1,953 tests in four independent database batches:
489, 488, 488 and 488. All passed, with four existing skips. Coverage includes
character views, forms and spending services; registry, workflow and transitions;
and core security, permissions and mixins. The batches used an in-memory SQLite
test database and Django's MD5 test password hasher.

Django system checks passed. All 55 changed/new Python files compiled, passed
Black's formatting check, and passed Ruff checks for unused/duplicate imports,
undefined names and import order (F401, F811, F821, F822, F823, I001).
`git diff --check` passed. No migrations or dependency changes are required.

Including new shared modules, production forms/views/services and core mixins
remove 2,680 net lines (2,062 added, 4,742 removed). This excludes tests,
documentation and the inventory script.
