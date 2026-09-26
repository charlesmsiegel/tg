# Item and location registry design

The current request authorizes both planning and implementation, superseding the
design-only instruction in `docs/code-fixing/07-items-locations-registry.md`.

## Intent and architecture

Each model has one declaration describing its gameline, slug, menu label, form
fields or form class, templates, ordering, action policies and custom views.
Declarations generate ordinary Django CRUD classes and URL patterns. Model class
identity selects the polymorphic detail view; `type` is presentation/legacy data,
never a dispatch key. Keep custom creation workflows as explicit overrides.

Use a small shared registry in `core/model_registry.py`, separate declarations in
`items/registry.py` and `locations/registry.py`, and lazy view construction so model
imports never depend on URL loading. Existing view import paths remain compatibility
exports. This permits migration one gameline at a time without changing consumers.

Rejected alternatives: extending `create_reference_views` would import its reference
data caching and login-only write assumptions into private player objects. Runtime
discovery from legacy view classes would preserve the duplication as the source of
truth. Use Django's standard generic views and the existing authorization evaluator.

## Authorization

Every action explicitly declares a Step 0 policy. Missing or unknown declarations
fail during registry construction. Generated views enforce the evaluator even when
called directly without middleware. Custom overrides receive the same wrapper.
Reference Material and Medium use public reads/staff writes; player objects use
public cards and visibility-filtered lists, authenticated creation, and object-scoped
editing. Creation assigns the authenticated owner. Do not introduce a second
permission algorithm or cache private responses.

## Compatibility and URLs

Capture every existing fully qualified URL name, path and callback before changing
code. The generated set must be a superset, including duplicate names with different
arguments (Mage location list aliases), chantry/freehold direct creation and wizard
routes, and AJAX. Preserve path spelling (`meleeweapon`, `realm`, etc.) through
per-action path overrides. Convert integer IDs to `<int:pk>`; malformed IDs become
resolver 404s. No valid old path requires a redirect. Import errors must propagate.

A registry URL mixin supplies model detail/update/create URLs. Preserve canonical
detail routing through the generic dispatcher where existing models use it, including
Chantry's creation-state router. Material and Medium are reference models outside
the ItemModel inheritance tree and retain their direct routes.

## Views and escape hatches

Weapon demonstrates generated views with six shared editable fields. Wonder uses
WonderForm and a custom resonance detail context. City uses generated CRUD and
field-widget/help metadata. Chantry retains its wizard, forms, detail context, list
context, direct creation and update handlers. Freehold likewise retains its wizard.
Any action can supply a custom class by import path; generation wraps it with the
declared policy and supplies its metadata. Preserve specialized form/context logic
instead of attempting to encode imperative workflows in the registry.

Template selection tries the declared existing template before a shared action
fallback. Template visual deduplication and character views remain out of scope.

## Menus and data

Index forms and item/location create/list redirects derive their choices from the
registry. Character navigation continues using ObjectType. Legacy ObjectType rows
for items and locations are no longer routing authority; no data deletion is needed.
Keep legacy names scoped by gameline, rejecting ambiguous unscoped selections.
The colliding `type` attributes are Python class attributes, not persisted fields;
dispatch by class fixes collisions without rewriting objects or seed data.

## Verification and reuse

Test URL-name/path parity, explicit policies, duplicate declarations, concrete model
coverage, menus without seeded rows, class-based dispatch for both collisions, single
object handoff, malformed/missing IDs, public reference reads, private projections,
owner assignment and unauthorized writes. Generate per-entry CRUD smoke cases and
run existing item/location/security and wizard tests, followed by the full suite.

Reference character models can later use the same machinery with explicit public
read/staff write policies. That migration is separate.

## Theory

The registry describes routable model types; it does not describe workflow state or
replace authorization. A new mundane model adds one declaration; a new multistep
workflow adds an explicit custom action. URL aliases describe historical compatibility
and never become a second model identity.


## Verified audit against this checkout

| Reported finding | Verified result |
|---|---|
| Item view classes | 113; 101 satisfy the original boilerplate heuristic |
| Location view classes | 156; 124 satisfy that heuristic; includes ChantryObjectMixin |
| Identical inline field pairs | 43 of 63 create/update pairs; 103 field-list literals |
| Named leaf routes | 112 items + 147 locations; repeated include mounts yield 268 runtime routes |
| Untyped PK declarations | 106 (the Step 0 middleware already rejected malformed IDs) |
| No-op app_name declarations | Already removed; zero remain |
| Unused reference factory | Confirmed; retained for future reference-only use |
| Existing URLMethodsMixin adoption | Only Resonance, Derangement and Archetype |
| Type collisions | Confirmed; exact-model dispatch replaces ambiguous strings |
| Material/Medium missing from polymorphic dispatch | Not a defect: separate reference tables, outside ItemModel |
| Dead index type lists and redirect chains | Already removed/replaced by Step 0/Step 1 |
| Rebuilt dispatch mapping and duplicate fetch | Confirmed; registry caches mapping and hands off the loaded object |
| Messages without MessageMixin | Nine current location classes; generated wrappers supply messaging |
| Ownership only assigned in three classes | Three direct assignments, but seven creators already call prepare_created_object |
| Missing read permissions | Step 0 already enforces policies through middleware; registry also enforces direct calls |

`type` is not a persisted model field. Seed scripts already use `wraith_artifact`,
`wraith_relic` and `demon_relic`, while historical routes use `artifact`/`relic`.
The registry preserves both identities and maps between them. ObjectType IDs and
Chronicle.allowed_objects links are untouched. Material, Medium and RealityZone
are explicitly registered reference models; there are 60 polymorphic models plus
these three references. RealityZone's old object-permission mixin made its declared
public detail policy return 404; the generated public-reference view fixes that.
Its related-location panel now uses VIEW_FULL checks so the public reference page
cannot reveal private locations or their ranks.

The missing historical project skills were consolidated into the main checkout's
`.claude/skills/tg-standards/SKILL.md`; its model/view/URL/permission/testing references
were used alongside the Step 0 design and current source.

## Four concrete declarations

The executable declarations are in `items/registry.py` and `locations/registry.py`.
Every entry declares all four actions; no policy defaults are inferred.

| Entry | Editable fields/form | Read/write policies | Overrides and compatibility |
|---|---|---|---|
| Weapon | name, description, difficulty, damage, damage_type, conceal | OBJECT_DETAIL / OBJECT_LIST / OBJECT_CREATE / OBJECT_WRITE | core/weapon templates; canonical `/items/<pk>/`; typed direct weapon route remains |
| Wonder | items.forms.mage.wonder.WonderForm | OBJECT_DETAIL / OBJECT_LIST / OBJECT_CREATE / OBJECT_WRITE | resonance detail context; create hook constructs the chosen subtype before ownership preparation |
| City | name, description, contained_within, gauntlet, shroud, dimension_barrier, population, mood, theme, media, politicians, characters | OBJECT_DETAIL / OBJECT_LIST / OBJECT_CREATE / OBJECT_WRITE | existing widget placeholders/help text; duplicate description field removed |
| Chantry | existing direct-form field list and specialized wizard forms | OBJECT_DETAIL / OBJECT_LIST / OBJECT_CREATE / OBJECT_ST_WRITE | four custom CRUD handlers; wizard basics remains primary create; direct creation stays separate; canonical detail enters ChantryCreationView |

`ActionSpec` stores the historical public view import path, an explicit policy,
optional private custom-class import path, action-specific options, form widget/help
metadata and historical `(name, path)` aliases. `ModelSpec` groups those actions
with shared fields/form, templates, model URL names, slug, gameline and menu label.
`registry.view(model, action)` returns a cached wrapped Django class;
`registry.urls(group, action)` emits typed paths; `registry.selection_url` maps
canonical menu keys to preserved aliases. Model URL methods use RegistryURLMixin,
a small sibling to URLMethodsMixin because canonical detail URLs can route through
polymorphic workflow dispatch rather than the model's direct detail endpoint.

For a future entry, public view paths may point into the registry module itself;
the factory exports those classes without a handwritten view module.

Existing Python view modules are intentionally retained as compatibility exports
and homes for custom hooks. Ordinary CRUD classes and hand-written CRUD path calls
are removed. Deleting these import modules outright would break callers and policy
inventory tooling; they contain no duplicate model definitions.

## Exact custom action classes retained

Private classes contain only custom behavior; the exported public classes wrap them
with registry metadata and authorization. The following list excludes unchanged
wizard adapters, which are listed separately below.

- `items.views.core.item._ItemCreateView` (create)
- `items.views.core.item._ItemUpdateView` (update)
- `items.views.mage.artifact._ArtifactDetailView` (detail)
- `items.views.mage.charm._CharmDetailView` (detail)
- `items.views.mage.grimoire._GrimoireDetailView` (detail)
- `items.views.mage.periapt._PeriaptDetailView` (detail)
- `items.views.mage.talisman._TalismanDetailView` (detail)
- `items.views.mage.wonder._WonderDetailView` (detail)
- `items.views.mage.wonder._WonderCreateView` (create)
- `items.views.vampire._VampireArtifactCreateView` (create)
- `items.views.vampire._VampireArtifactUpdateView` (update)
- `locations.views.changeling.freehold._FreeholdDetailView` (detail)
- `locations.views.changeling.freehold._FreeholdCreateView` (create)
- `locations.views.changeling.freehold._FreeholdUpdateView` (update)
- `locations.views.core.location._LocationCreateView` (create)
- `locations.views.core.location._LocationUpdateView` (update)
- `locations.views.mage.chantry._ChantryDetailView` (detail)
- `locations.views.mage.chantry._ChantryListView` (list)
- `locations.views.mage.chantry._ChantryCreateView` (create)
- `locations.views.mage.chantry._ChantryUpdateView` (update)
- `locations.views.mage.demesne._DemesneCreateView` (create)
- `locations.views.mage.library._LibraryCreateView` (create)
- `locations.views.mage.node._NodeDetailView` (detail)
- `locations.views.mage.node._NodeCreateView` (create)
- `locations.views.mage.paradox_realm._ParadoxRealmDetailView` (detail)
- `locations.views.mage.paradox_realm._ParadoxRealmCreateView` (create)
- `locations.views.mage.paradox_realm._ParadoxRealmUpdateView` (update)
- `locations.views.mage.sanctum._SanctumCreateView` (create)
- `locations.views.vampire._HavenDetailView` (detail)
- `locations.views.mage.reality_zone._RealityZoneDetailView` (detail)

All freehold wizard classes in `locations/views/changeling/creation.py` remain:
FreeholdBasicsView, FreeholdFeaturesView, FreeholdPowersView, FreeholdDetailsView,
FreeholdCreationView. Chantry wizard/helper classes remain: ChantryBasicsView,
ChantryObjectMixin, ChantryPointsView, ChantryIntegratedEffectsView, ChantryNodeView,
ChantryLibrarysView, ChantryAlliesView, ChantrySanctumView, ChantryCreationView and
LoadExamplesView. The two index views and generic detail adapters remain hand-written.

## Implementation-specific safeguards

- All 268 baseline routes retain both names and valid paths. Added base item/location
  list endpoints complete CRUD coverage; integer converters reject malformed IDs.
- Authorization declarations for generated views were removed from the legacy
  manifest. The inventory test now checks the disjoint union of legacy policies and
  registry policies, including router branches; missing/duplicate declarations fail.
- Registries reject duplicate models, canonical keys, per-action route names and paths.
- The global registry caches detail mappings. Generated detail views reuse the resolved
  instance through permission checks and rendering; polymorphic loading still needs
  a base query plus its concrete-model query. Custom workflow steps may make their own
  state-specific queries.
- Existing model URL spellings are preserved. Selection redirects prefer matching
  canonical aliases (notably Tremere Chantry) and otherwise use the explicit model URL.
- Menus are independent of seeded rows, preserve Mage-only selection for ordinary
  users, and restrict staff-only reference creations. Characters retain ObjectType routing.
- No schema/data migration or bulk rewrite is required. Character views and the old
  reference factory are not migrated.

## Practical limits

The generated smoke matrix exercises authorized form rendering and unauthorized writes
for every entry, with successful POST regressions for Weapon, Wonder and Node plus
existing wizard tests. It does not synthesize valid POST payloads for every specialist
form. The suite retains existing custom-form tests. No production database or browser
session was used; template fallback rendering is exercised in Django tests.
