# Chargen Step Registry Design

## Goal and scope

Make one ordered workflow definition authoritative for character creation routing,
freebie positions, progress, form fragments, skipping, and back navigation. The
user explicitly requested implementation as well as the design; that supersedes
the source brief's historical design-only restriction. Existing game-rule form
validation stays in its current views. Generic step-class consolidation, rules
extraction, and htmx remain separate projects.

## Source audit

The current checkout includes authorization hardening and Chantry improvements.
The requested legacy repository skills have been consolidated into
`.claude/skills/tg-standards/`; consult its models, views, templates, testing,
permissions and domain references together with `CLAUDE.md`. The authorization
implementation takes precedence over stale permission examples in those references.

Confirmed by runtime inventory: 21 routers and 231 slots, including the misspelled
`CopanionCharacterCreationView`. Preserve its import name. Fera's twelve concrete
subtypes share the Fera router. Character types with detail-only routes do not
acquire a wizard just because they inherit from a wizard-enabled model.

Confirmed: routing dictionaries, model freebie constants, QuerySet map and numeric
template branches duplicate the same information. Werewolf, Fomor, Wraith and
Demon QuerySet positions disagree with their actual freebie views. Fera now has
an explicit freebie position of 8, so the reported inherited-5 defect is stale.
Human progress is still isolated to its seven wrappers. Vampire's specialties
branch is at 10 instead of 13; Garou only has its first three form branches.
Demon, Thrall and DtFHuman lack chargen shells. Human's old nonexistent template
reference has already been replaced, but its shell still compares string status
to integers. Mage Chantry and Specialties have already moved to 20 and 21;
Mentor, Contacts and Retainers remain missing. The pre-migration HEAD has 335 creation_status comparisons in chargen shells
and 93 view increments; the audit's 330/~92 counts are slightly stale. Mage, Companion and Sorcerer still hand-code background skip order.
The common skip handlers now mutate on POST, not GET; preserve that security fix.

## Architecture and alternatives

Use a small `characters/chargen/` package: immutable Step and Workflow records,
declarations grouped by gameline, pure skip predicates, and a transition service.
Keep view import paths as strings until a router needs its mapping. Models can
therefore read metadata without importing views during Django app loading.

Rejected model-local definitions: they couple models to forms/views and invite
inheritance of the wrong workflow for detail-only subtypes. Rejected a third-party
wizard framework: its session persistence and form lifecycle would duplicate the
existing database workflow and require rewriting game rules.

A Step has a stable key, label, view import path, fragment template, optional
`skip_if(character)` predicate and optional skip effect (default language).
`key == 'freebies'` identifies the single freebie step. Workflow positions are
one-based and derive from tuple order. Shared step fragments and common ordered
prefixes compose workflows; view bindings remain explicit where class names
differ. No declaration imports model or view classes eagerly.

`get_workflow(type)` returns the exact registered workflow, including explicit
Fera aliases. Unknown/detail-only types return None. Detail-only freebie positions live in an explicit metadata table to preserve existing eligibility without inventing workflows. Workflow derives
`view_mapping`, `freebie_step`, `step(position)`, and progress labels. A descriptor
preserves both `Mage.freebie_step` and `mage.freebie_step` access. The QuerySet
builds an OR of `polymorphic_ctype__app_label='characters'`, concrete model name
and the corresponding workflow freebie position, with an empty-result seed.

## Rendering and routing

Keep router classes and route-policy identities. Replace literal mappings with a
registry-derived mapping descriptor. Every routed step uses a common mixin for
registry context and a common shell including `step.template`; gameline shells
extend that shell. Retain existing form partials, widgets, validation scripts and
formset management where available. Supply actual generic form fragments for
previously blank steps and missing Demon shells. Fragments contain no outer form
or base-page extension, so a later htmx project can render them directly.

Progress displays every registered step. The shell includes the selected form,
its media and validation errors; unavailable steps show a Continue action.
Freebies awaiting ST approval show a waiting message, not a spend form.

## Authorization and transitions

Reuse Step 0's `CHARGEN_STEP` policy and `authorize_route`; do not duplicate a
permission field in every Step. Middleware and DictView remain the outer gates.
The common step mixin also invokes the same policy before skip handling, including
direct `as_view()` calls. GET/HEAD never advance or create English/background rows.

`advance(character, *, user)` authorizes editable Un/Rev state before mutation,
advances once, then evaluates consecutive pure skip conditions in registry order.
Only transition execution applies a skip effect such as adding English. Freebies
skip only when approved and exhausted; languages skip without the Language merit;
linked backgrounds skip without incomplete ratings. Sorcerer Psychic/Path/Ritual
conditions derive from sorcerer_type. Existing terminal specialty handlers submit
the character; they are never automatically skipped. Empty/out-of-range workflows
raise rather than silently wrapping. Successful multi-record background creation
stays on the same step until its final incomplete rating is completed.

Back navigation retains the owner-only, editable-state, freebie-approval lock and
row lock. It locates the preceding applicable registered step without applying
skip effects. It must not bounce immediately forward through an inapplicable step.
Transitions do not attempt to rewrite all existing form transactions or solve
general duplicate form submission; that remains a known inherited limitation.

## Persistence and deploy

Retain integer creation_status. The pre-change router snapshot is the golden
contract: every view keeps its original position, including mid-creation Un and
Rev characters. No schema or data migration is needed. Fixing which form renders
does not change saved positions. Future reorderings require an explicit migration
mapping old positions to stable step keys and then to new positions; never reorder
the tuple and regenerate the golden fixture without migrating in-progress rows.
Invalid historical positions fall back to existing detail routing and are not
silently repaired. Rollback leaves all persisted positions understandable.

## Rollout and visible changes

Implement foundation plus Vampire pilot, then Core, Werewolf, Mage, Wraith,
Changeling and Demon integrations as independently reviewable batches. All batches
are implemented in this worktree; they can be split into PRs by the plan boundaries.
Missing late forms begin working, all gamelines gain progress, default language
and empty backgrounds skip consistently after successful POST, and freebie queues
match the real view positions. No positions or game-rule allocations change.
Old completed-stat ladders are replaced by a focused current-step form; the full
character sheet remains available on the existing detail routes.

## Verification and extension model

Pin all 231 view slots before edits. Test exact route/registry coverage, aliases,
freebie-view parity, template loading and owner GETs for every step. Test each
fragment with its real view context, including formsets and widget media. Test
unauthorized GET/POST immutability, denied direct view calls, skip chains,
unapproved zero freebies, Sorcerer branches, background completion, Back, and
terminal submission. Audit orphan classes without adding new workflow positions. The unreferenced
FeraFetishView and WerewolfFetishView placeholders were removed; neither had a
form class, route, caller or tests.

Theory: a persisted position identifies one ordered task, independent of which
view renders or validates it. Step metadata describes navigation; existing views
own game rules. A new task adds a declaration and fragment, with an explicit data
migration if it changes existing positions. Reused: Django forms, templates,
polymorphic queries and authorization. Cost: linear scans of at most 21 steps;
skip predicates may query related ratings. Watch: custom Mage/Sorcerer formsets
and spending services have lifecycles beyond a one-submit-per-step form.

## Complete example bindings

The runtime declarations compose shared task tuples in `characters/chargen/definitions.py`.
These expanded examples show every persisted position; paths below are exact.

### human

| Position | Key / label | View | Fragment |
|---|---|---|---|
| 1 | attributes / Attributes | `characters.views.core.human.HumanAttributeChargenView` | `characters/core/attribute_block/form.html` |
| 2 | abilities / Abilities | `characters.views.core.human.HumanAbilityChargenView` | `characters/core/chargen/abilities.html` |
| 3 | backgrounds / Backgrounds | `characters.views.core.human.HumanBackgroundsChargenView` | `characters/core/background_block/form.html` |
| 4 | biography / Biography | `characters.views.core.human.HumanBiographicalInformationChargenView` | `characters/core/chargen/form.html` |
| 5 | freebies / Freebies | `characters.views.core.human.HumanFreebiesChargenView` | `characters/core/chargen/freebies.html` |
| 6 | languages / Languages | `characters.views.core.human.HumanLanguagesChargenView` | `characters/core/human/human_language_block_form.html` |
| 7 | specialties / Specialties | `characters.views.core.human.HumanSpecialtiesChargenView` | `characters/core/chargen/specialties.html` |

### vampire

| Position | Key / label | View | Fragment |
|---|---|---|---|
| 1 | attributes / Attributes | `characters.views.vampire.vampire_chargen.VampireAttributeView` | `characters/core/attribute_block/form.html` |
| 2 | abilities / Abilities | `characters.views.vampire.vampire_chargen.VampireAbilityView` | `characters/vampire/vtmhuman/ability_block_form.html` |
| 3 | backgrounds / Backgrounds | `characters.views.vampire.vampire_chargen.VampireBackgroundsView` | `characters/core/background_block/form.html` |
| 4 | disciplines / Disciplines | `characters.views.vampire.vampire_chargen.VampireDisciplinesView` | `characters/vampire/vampire/steps/disciplines.html` |
| 5 | virtues / Virtues | `characters.views.vampire.vampire_chargen.VampireVirtuesView` | `characters/vampire/vampire/steps/virtues.html` |
| 6 | biography / Biography | `characters.views.vampire.vampire_chargen.VampireExtrasView` | `characters/core/chargen/form.html` |
| 7 | freebies / Freebies | `characters.views.vampire.vampire_chargen.VampireFreebiesView` | `characters/core/chargen/freebies.html` |
| 8 | languages / Languages | `characters.views.vampire.vampire_chargen.VampireLanguagesView` | `characters/core/human/human_language_block_form.html` |
| 9 | allies / Allies | `characters.views.vampire.vampire_chargen.VampireAlliesView` | `characters/core/chargen/form.html` |
| 10 | mentor / Mentor | `characters.views.vampire.vampire_chargen.VampireMentorView` | `characters/core/chargen/form.html` |
| 11 | contacts / Contacts | `characters.views.vampire.vampire_chargen.VampireContactsView` | `characters/core/chargen/form.html` |
| 12 | retainers / Retainers | `characters.views.vampire.vampire_chargen.VampireRetainersView` | `characters/core/chargen/form.html` |
| 13 | specialties / Specialties | `characters.views.vampire.vampire_chargen.VampireSpecialtiesView` | `characters/core/chargen/specialties.html` |

### mage

| Position | Key / label | View | Fragment |
|---|---|---|---|
| 1 | attributes / Attributes | `characters.views.mage.mage.MageAttributeView` | `characters/core/attribute_block/form.html` |
| 2 | abilities / Abilities | `characters.views.mage.mage.MageAbilityView` | `characters/mage/mtahuman/ability_block_form.html` |
| 3 | backgrounds / Backgrounds | `characters.views.mage.mage.MageBackgroundsView` | `characters/core/background_block/form.html` |
| 4 | spheres / Spheres | `characters.views.mage.mage.MageSpheresView` | `characters/mage/mage/mage_powers_block_form.html` |
| 5 | focus / Focus | `characters.views.mage.mage.MageFocusView` | `characters/mage/mage/mage_focus_block_form.html` |
| 6 | biography / Biography | `characters.views.mage.mage.MageExtrasView` | `characters/core/chargen/form.html` |
| 7 | freebies / Freebies | `characters.views.mage.mage.MageFreebiesView` | `characters/core/chargen/freebies.html` |
| 8 | languages / Languages | `characters.views.mage.mage.MageLanguagesView` | `characters/core/human/human_language_block_form.html` |
| 9 | rote / Rote | `characters.views.mage.mage.MageRoteView` | `characters/mage/mage/mage_rote_form_block.html` |
| 10 | node / Node | `characters.views.mage.mage.MageNodeView` | `locations/mage/node/form_include.html` |
| 11 | library / Library | `characters.views.mage.mage.MageLibraryView` | `locations/mage/library/form_include.html` |
| 12 | familiar / Familiar | `characters.views.mage.mage.MageFamiliarView` | `characters/mage/mage/familiar_form.html` |
| 13 | wonder / Wonder | `characters.views.mage.mage.MageWonderView` | `items/mage/wonder/form_include.html` |
| 14 | enhancement / Enhancement | `characters.views.mage.mage.MageEnhancementView` | `characters/mage/mage/mage_enhancements_form.html` |
| 15 | sanctum / Sanctum | `characters.views.mage.mage.MageSanctumView` | `locations/mage/sanctum/form_include.html` |
| 16 | allies / Allies | `characters.views.mage.mage.MageAlliesView` | `characters/core/chargen/form.html` |
| 17 | mentor / Mentor | `characters.views.mage.mage.MageMentorView` | `characters/core/chargen/form.html` |
| 18 | contacts / Contacts | `characters.views.mage.mage.MageContactsView` | `characters/core/chargen/form.html` |
| 19 | retainers / Retainers | `characters.views.mage.mage.MageRetainersView` | `characters/core/chargen/form.html` |
| 20 | chantry / Chantry | `characters.views.mage.mage.MageChantryView` | `locations/mage/chantry/select_or_create_form.html` |
| 21 | specialties / Specialties | `characters.views.mage.mage.MageSpecialtiesView` | `characters/core/chargen/specialties.html` |

## Implementation findings and review record

Owner rendering also exposed inherited blockers: Fera's nested Meta could not
resolve its dynamic fields; Demon forms referenced lore_of_forging and host_name,
which do not exist on the model; Companion Library assumed Mage affiliation fields;
the old Ally partial omitted LinkedNPCForm's required npc_type; Enhancement omitted
new_device_rank and new_device_arete. These were corrected without changing rules.

An independent read-only review found three migration regressions, each reproduced
with a failing test and fixed: duplicate Sorcerer final-freebie advancement, missing
auxiliary ritual inputs, and lost completion predicates for Wraith Passions/Fetters.
The review accepted preserved positions, detail-only freebie metadata and removal
of the unrouted Fetish placeholders. General duplicate-submit protection remains
outside this migration; tests run on SQLite, so production row-lock behavior is
not a new guarantee. No browser automation or full-project test run is claimed.
