# Native TG API v1 — first increment of toolkit issue #195

This is an initial authenticated JSON interface, **not completion of #195** and not a
Rust `Store` implementation. Install `requirements.txt`; DRF supplies JSON read views,
serializers and pagination. Django 5.2 is the supported framework version. No database
schema, token table, migration or CORS setting is added.

## Authentication and CSRF

The native HTML flow at `/accounts/login/` remains available. The initial backend
increment for toolkit #198 also provides a JSON response facade over that same native
login form, session rotation and shared throttle. It adds no JWT, refresh token,
credential table, cross-origin exemption or browser authorization bridge.

1. GET `/api/v1/auth/csrf/` using a cookie-aware HTTPS client. Anonymous response:
   `{"authenticated":false,"csrf_token":"..."}` plus the CSRF cookie.
2. POST `/api/v1/auth/login/` with **application/x-www-form-urlencoded** body containing
   `username` and `password`, retaining cookies and supplying `X-CSRFToken` (or one
   `csrfmiddlewaretoken` form field). Native HTTPS Origin/Referer checks apply. JSON,
   multipart and other content types return 415; duplicate/unknown form fields return
   400. Do not send `next` or arbitrary user/profile fields.
3. Successful login returns 200 session discovery JSON and a rotated session/CSRF
   cookie. Retain both cookies and use the returned fresh token on subsequent writes.
   Invalid, missing or inactive credentials return identical 400
   `{"error":"invalid_credentials"}`. Shared native login account/IP throttling returns
   429 `{"error":"too_many_attempts"}` even for correct credentials after the limit.
4. POST `/api/v1/auth/logout/` with valid CSRF to flush the server session, returning
   204. GET never logs out. Anonymous repeated logout also requires CSRF. An offline
   local disconnect cannot promise server-side revocation.

Authenticated discovery (`auth/csrf/`, login success and existing `GET /api/v1/session/`)
returns `authenticated`, fresh `csrf_token`, `user: {id, username}`, `profile: {theme,
preferred_heading, is_st}` (null if missing), and `session: {browser_close,
cookie_age_seconds}`. Profile projection excludes email, Discord, lines/veils and all
other private fields. `is_st` is the native advisory chronicle ST summary, not a grant:
game storytellers are read-only; staff status alone does not set it. Every object route
still checks live native permissions.

`cookie_age_seconds` is configured session cookie lifetime policy, **not remaining TTL**.
Redis eviction, logout, password changes or account deactivation may revoke earlier;
GET does not promise sliding refresh. `browser_close` tells native clients not to
persist that credential across app restarts. No exact expiry or refresh endpoint is
claimed. Expired sessions yield anonymous discovery and 401 on `/api/v1/session/`.

All facade responses use private/no-store caching. CSRF and some middleware errors
remain native text/HTML, so inspect status and Content-Type before parsing JSON. The
HTML and API login share the same fixed-window account/IP quota and cache-outage
behavior; this facade adds no second password-check route outside those controls.
Native sign-up/reset remain on the site. No CAPTCHA/MFA provider is configured in
repository source; an operator's external challenge may require a future browser flow.

Keep passwords/session cookies out of URLs, logs, React state stores, SQLite and
ordinary config files. A native Rust transport should hold cookies and CSRF in its own
origin-bound client and persist session secrets only in an OS keyring; unavailable
keyring means memory-only or explicit failure, never plaintext fallback. Use HTTPS,
certificate validation and fixed-origin redirects. Rust client/keyring/login UI,
connection profiles, scoped capability display and offline queueing are separate
increments; #198 and #196 are not complete with this backend facade.

## Routes

| Method and path | Result / authority |
|---|---|
| GET `/api/v1/session/` | Projected own session/profile and CSRF token; login required |
| GET `/api/v1/chronicles/` | Readable chronicles, IDs and names |
| GET `/api/v1/chronicles/{id}/` | Native settings, head ST, game ST IDs and assigned ST/gameline IDs |
| GET `/api/v1/chronicles/{id}/allowed-objects/` | Native object-type rows (`id`, `name`, `type`, `gameline`) |
| GET `/api/v1/chronicles/{id}/characters/` | Full-view character summaries in a readable chronicle |
| GET `/api/v1/characters/{id}/` | Explicit partial native field projection; full-view permission required |
| POST `/api/v1/characters/{id}/update/` | Descriptive edits only, `EDIT_LIMITED` permission; returns `{"id":123}` |
| POST `/api/v1/chronicles/create/` | Staff/admin only, same no-existing-scope rule as the site create page; returns ID with HTTP 201 |

Collections use DRF page-number pagination: `?page=2&page_size=50` (default 50, max 100).
Responses have `count`, `next`, `previous`, `results`. Chronology is stable by primary key.
Status/gameline/owner filters are deferred; only pagination parameters are supported.

Every route has a manifest policy. Reads use `LOGIN` plus `readable_chronicles` or
`PermissionManager` full-view filtering; writes use `ACTION`/`OBJECT_CREATE` plus existing
object/scope checks. Anonymous calls to authenticated data routes are 401. Hidden and missing read objects return the
same 404. Partial viewers and observers receive no private sheets from these routes,
even if a public card is available through the ordinary site. A visible object that
cannot be edited returns 403. Validation errors are 400; unsupported methods are 405.
Some middleware denials/CSRF errors remain standard TG text/HTML, so clients must check
HTTP status and Content-Type before parsing JSON. Successful reads/writes use
`Cache-Control: private, no-store`; no public API cache is introduced.

The character/chronicle mutation bodies below require `Content-Type: application/json` and a JSON object. Unknown fields
fail the whole request. Descriptive update keys are `notes`, `description`, `public_info`,
`history`, `goals`, all optional strings (empty string allowed; null/numbers/objects are
rejected). `history` and `goals` require a Human subclass. Non-submitted draft owners and
scoped storytellers can use their existing `EDIT_LIMITED` permission; status restrictions
still apply. Name, ownership, chronicle, type, status, visibility, image, XP, freebies,
traits, Focus and all mechanics are deliberately unwritable through this increment,
including for staff. It cannot bypass creation, approval or spending services.

Chronicle creation accepts only `name`, `theme`, `mood`, `year`, `headings`; model validation
runs and `head_st` is bound to the current staff user. Arbitrary owners, storytellers,
allowed types or toolkit module selections cannot be supplied. Existing site configuration
remains available afterwards. No character-creation shortcut is exposed.

## Explicit mappings and fidelity boundary

All IDs are native integer database IDs, not toolkit UUIDs. `type` is the concrete TG
polymorphic discriminator and `gameline` is the TG code. Summaries have ID, type, gameline,
name, owner ID, chronicle ID and status. Character details also expose concept, notes,
description, public information, visibility, NPC flag and XP.

Character detail always includes `projection: "tg-character-v1"`, `complete: false`.
It **must not be used as a lossless archive** or echoed into an unrestricted update.
The allowlists in `core/api/projections.py` are the exact response contract:

- Human subclasses: nine Attributes and the nineteen common Human Abilities, nature and
  demeanor as Archetype IDs, permanent/temporary Willpower, native health string/count,
  history/goals, background rows and merit/flaw rows. Backgrounds retain row IDs, definition
  IDs, independent ratings, named notes, URL, completion and pooling flags; repeated
  backgrounds are never flattened. Merit/flaw rows retain row/definition IDs and ratings.
- Mage subclasses: Arete, nine Sphere columns, essence, affiliation/faction/subfaction IDs,
  affinity Sphere ID, Quintessence/Paradox, three tenet IDs and additional tenet IDs,
  instrument ID/name pairs, and practice through-row ID/definition ID/rating. This preserves
  TG's actual tenet/practice model; toolkit paradigm/practice arrays are not fabricated.
- Other gameline subtype powers, extra Mage Abilities, specialties, languages, rotes,
  resonance, quiet, media, sourcebooks and other unlisted fields are not projected yet.
  They remain untouched on descriptive updates; polymorphic instances are loaded and locked
  before saving, and permissions are checked again on the locked object with
  request permission caches invalidated. No subclass is downcast into a new Human row.

TG chronicles have native allowed-object rows, not toolkit `active_modules`, per-module
bounds, disabled-trait settings or module UUIDs. Those fields are not invented. Toolkit
archive `traits`, `extras`, `metadata`, identity and module fields are rejected on writes.
A future adapter must explicitly translate IDs, trait definitions, repeated backgrounds,
Archetype references, Focus/tenets, health and approvals, and refuse unmapped data.

## Remaining #195 work

Native client credential lifecycle and optional future token mechanisms; complete per-gameline serializers; stable toolkit
ID/trait/module adapter; chronicle settings writes; character creation via proper chargen
services, deletion and approval actions; templates and trait definitions; items/locations;
XP/freebie requests and approvals; general list filters; scene mutations and WebSocket
integration remain future increments. Read-only scenes/journals are covered below.
Dedicated POST action paths deliberately follow TG's current route standards instead of adding PATCH/DELETE to detail views. Any later REST method expansion
needs an explicit policy design and denial tests; it is not implied by this version.

Tests: `python manage.py test core.tests.api`, followed by route-policy/action/import guards
and `python manage.py test` for the complete suite.

## Read-only scenes and journals — initial #204 increment

These additional session-authenticated routes expose native TG reads, not a Rust transport
or WebSocket client. They require a session even when the ordinary site permits anonymous
public-scene reading. They accept GET/HEAD only (plus authenticated OPTIONS metadata).

| Path under `/api/v1/` | Response |
|---|---|
| `scenes/` | Visible scene metadata, paginated |
| `scenes/{id}/` | One visible scene's metadata |
| `scenes/{id}/posts/` | Paginated stored transcript, stable ascending post ID |
| `journals/` | Full-readable journal identifiers, paginated |
| `journals/{id}/` | Journal ID and underlying character ID |
| `journals/{id}/entries/` | Paginated entry text and timestamps |
| `characters/{id}/journal/` | Existing full-readable journal for the character; never creates one |

Scene metadata includes only ID, name, chronicle ID, gameline, visibility, played/in-game
dates and finished state. A public scene remains accessible outside a readable chronicle;
its chronicle ID is a reference, not permission to read that chronicle's other data.
Transcript rows expose only ID, scene ID, stored display name, message and creation time.
They do not expand private character names/sheets, owner IDs, location records, author
character IDs or arbitrary stored roll JSON. Stored text already includes native rendered
roll messages; structured dice integration is deferred. Scene/journal detail projections
are marked `complete:false` and are not archives.

Journal metadata exposes only journal ID and character ID. Entries expose ID, journal ID,
message, in-game date and creation time. They are ordered by descending entry date, then
creation time and ID for stable ties. Actual native private-record and full-character
permissions apply: owners and chronicle storytellers (including game/read-only and
other-gameline storytellers) can read; ordinary chronicle players and partial-only
observers cannot. Retirement/death does not remove the owner's native full-read access.
Staff/superusers retain their existing read rights. No new edit or approval power is granted.

Scene visibility follows `filter_scenes`/`can_view_scene`: PUBLIC, CHRONICLE and PARTICIPANTS
keep their native audiences. Same-chronicle membership does not grant a nonparticipant
access to a participants-only scene. Detail and nested reads recheck current visibility,
cast membership, journal-to-character links and character permissions after lookup; the
API does not cache role grants or treat an earlier read as a permission lease. Lists filter
before counting/pagination. Hidden and missing valid IDs have the same JSON 404 response.

New collection routes support `page` and `page_size` (50 default, capped at100); scene and
journal lists additionally support `chronicle_id`. Values must be single positive native
integer strings (maximum signed64-bit), and duplicate or unsupported query keys fail400.
Unknown/hidden chronicle filters yield an empty authorized list rather than disclosing
chronicle existence. Out-of-range pages return404. Native path IDs outside the valid range
return404. No `include` flag can request additional private columns.

The original minimal scene and entry collection projections omit both `Scene.st_message`
and `JournalEntry.st_message`, including for staff. TG's journal field is an owner-visible
ST response, not an ST-private note; the scene field is an `@storyteller` request. The
explicit entry-detail route below now exposes the owner-visible response under native
journal permissions. No separate ST-private note model is invented.

GETs never invoke `message_processing`, execute stored commands, add entries/posts,
award XP, spend points, close scenes or update `UserSceneReadStatus`. The HTML scene
view's read-marker behavior is not reused. Scene participation, general journal editing,
true ST-private notes, WebSockets, XP/dice workflows and Rust UI/transport integration
remain separate work. Keep #204 open for those phases.

## Bounded journal actions — next #204 increment

These routes preserve native `JournalEntryCreateView` owner-only and
`JournalResponseView` full-read + `Permission.APPROVE` authority. They do not grant staff
or STs an owner override for adding prose. Native journal append permits its owner in
all character statuses, including submitted, deceased and retired; it does not use the
character descriptive-edit permission. Native status/role rules remain authoritative.
Ordinary/partial viewers cannot read or write a journal even for a public character.

| Method and path under `/api/v1/` | Contract |
|---|---|
| POST `journals/{id}/entries/append/` | Owner-only JSON `{date:"YYYY-MM-DD",message:"..."}`; 201 new entry |
| GET `journals/{id}/entries/{entry_id}/` | Native full-readable entry, including owner-visible `st_message` |
| POST `journals/{id}/entries/{entry_id}/response/` | Scoped native approver JSON `{st_message:"..."}`; 200 first response only |

All three return the explicit entry fields `id`, `journal_id`, `message`, `date`,
`datetime_created`, `st_message`. New entries have an empty response. The response is
visible to the native journal audience (owner, permitted STs, staff), not an ST-only
secret. Response text `Read` retains TG's existing acknowledgement convention. No author
identity is accepted or invented: the character/journal is bound by the authorized URL.
Existing collection and authentication projections remain unchanged.

Only the listed fields and string scalars are accepted. Unknown or duplicate JSON keys,
malformed objects, invalid Unicode, invalid/ambiguous dates and empty text fail400 with
`{"errors":{"field":[{"message":"...","code":"..."}]}}`. Native form whitespace
stripping applies, and dates become aware midnight using TG's current timezone. Each
text/date value is limited to10,000 characters and the request to65,536 bytes. Non-JSON
media types fail415. Neither timestamps, parent links, author/owner fields nor player
prose can be supplied through the response action.

Prose append deliberately bypasses `Journal.add_post`/`message_processing`: **no dice or
resource command executes**. Native reserved substrings `/roll`, `/rolls`, `/extended`,
`/stat`, `#WP`, `#Q`/`#P` with signed digit amounts, and signed damage tags ending in
`B`, `L`, `A` are rejected with `unsupported_command`, even embedded in prose or after
whitespace; case variants are rejected too. Other prose/URLs/markup are stored as text.
Use the native site for journal commands. ST responses follow their native literal-text
semantics; command-looking response text is stored without processing.

Responses are first-answer-only. An existing response, including `Read`, returns409
`already_answered`; the service performs a conditional empty-response update and never
replaces player prose or an existing answer. On supported SQLite deployments, simultaneous read-to-write upgrades can conflict even
with row-lock requests. Known SQLite busy/locked failures roll back and return409
`write_conflict`; refresh before another explicit request. Either request may lose, and
both may conflict without a partial write. Unrelated database errors are not disguised
as edit conflicts. No general entry editing, response
replacement, clearing or deletion is implemented. There is no new revision field/schema.
Append creates independent records; it is non-idempotent. After a timeout clients must
check/reconcile the journal instead of automatically replaying a write; this API does
not promise an offline queue or deduplication.

Writes require a session and ordinary CSRF/Origin checks. Dedicated POST action policies
reject other methods. Hidden/missing/cross-journal targets receive identical404 before
payload validation; an authorized reader lacking the action gets403. Canonical journal,
character, actor, chronicle and current relevant ST relation rows are locked/reloaded,
permission caches invalidated and native policy checked again before writes. Entry
responses also lock/check their exact journal parent. Entry detail repeats native
journal/private-entry visibility after lookup. Responses use private/no-store; native
middleware denials may remain text/HTML. No native HTML actions or auth behavior changed.

## Exact concrete Human read profile and public catalogs

These additive authenticated GET/HEAD endpoints preserve all earlier v1 contracts:

| Path under `/api/v1/` | Contract |
|---|---|
| `character-profiles/human-v1/` | Static `tg-human-v1` exposed-field manifest, native bounds, redactions and read-only capabilities |
| `catalogs/human-v1/{kind}/` | Public reference facts, paginated with `page`/`page_size` (default50, maximum100) |
| `characters/{id}/human-profile/` | Exact concrete `Human`, native full-view audience, bounded exposed profile and fingerprint |

Kinds are `archetypes`, `backgrounds`, `merits-flaws`, `specialties`, `languages`,
`derangements`, and `books`. Definition IDs are opaque decimal strings; names are not
identities. Each catalog has a fixed field allowlist. Native public-list route policies
and querysets remain authoritative; changing a route to a nonpublic policy or a different
model fails closed. Background is a public `Statistic` definition without ownership or
visibility fields. Inherited private reference metadata, descriptions, ST notes and reverse
known-by/owner relationships are never expanded. Merit/flaw ratings preserve signed native
values, with bounded `allowed_types` (`id`, `name`, `type`, `gameline`). The manifest lists
both scalar and nested catalog fields.

The character profile preserves native nullable scalars, nine attributes, nineteen
abilities, willpower/temporary willpower, damage string and native wound penalty, workflow
flags, age/date, XP/freebies totals, and six independent relation collections. Background
and merit/flaw rating rows retain their own IDs, nullable definition IDs, ratings and
explicit row metadata; repeated backgrounds remain separate even with identical names or
notes. Specialty/language/derangement IDs and book-reference row IDs, nullable book IDs
and page numbers remain distinct. All native primary/foreign keys are decimal strings,
including values beyond JavaScript's exact integer range. Keep identity scoped to the
configured server origin, resource kind and native ID; these are not toolkit UUIDs.

Full native character authorization occurs before subtype diagnostics. Authorized Mage,
gameline-specific Human or other concrete subclasses receive422 `unsupported_type`;
unauthorized or missing targets receive identical404 JSON. Fixed redactions apply even to
staff: `st_notes`, image storage/moderation fields, legacy `spent_freebies`, separate
freebie/XP ledgers and reverse/group data. `complete:false` and all write/CAS capabilities
false are intentional: this is an exact **exposed read profile**, not every Human field,
a portable archive, a Rust `Character`, or a `Store` implementation. Native bounds (for
example attributes/abilities0..10 and signed merit/flaw ratings) are preserved without
clamping to local WodBase rules. Totals do not reconstruct their audit histories.

Each relation and nested catalog expansion is capped at500 rows. An oversized profile
fails422 `profile_limit` instead of silently truncating. Unknown/duplicate query keys and
invalid pagination fail400; native IDs must be positive signed64-bit decimal values.
Other methods fail405; no writes, imports, relation changes or rule execution are offered.

A read transaction compares two canonical exposed projections, including relation rows,
with an active actor reload, fresh target and invalidated permission caches. Observed
scalar/relation changes fail409 `snapshot_changed`; revoked access remains404, including
before type/size diagnostics. `snapshot_token` is a keyed fingerprint of only the exposed
payload, actor, request origin and deployment prefix. It is stable for unchanged exposed
data; hidden-field changes do not affect it. It is not a database revision, catalog-wide
snapshot, CAS token, authentication credential or permission lease. Separate catalog/page
requests are independent reads. Clients must refresh after409 and reauthorize every read.
Responses are private/no-store. Native HTML views and existing authentication are unchanged.
