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

JSON login/logout and JWT/token lifecycle; complete per-gameline serializers; stable toolkit
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

Both `Scene.st_message` and `JournalEntry.st_message` are omitted server-side, including
for staff. TG's journal `st_message` is actually an owner-visible ST response, not a
private ST-only note, and the scene field is an `@storyteller` request. This schema does
not provide a separate ST-private note model. The omission is intentional; this API does
not invent a private-note feature or rely on client filtering. A future explicitly named
owner-visible response or private-note API needs its own documented field policy.

GETs never invoke `message_processing`, execute stored commands, add journal entries or
posts, award XP, spend points, close scenes or update `UserSceneReadStatus`. The HTML scene
view's read-marker behavior is not reused. Journal writes are deferred because native
`Journal.add_post` processes commands and can change character state; any future write
must have explicit services, allowlists, CSRF, locks and fresh permission checks. Scene
participation, journal editing, true ST-private notes, WebSockets, XP/dice workflows and
Rust UI/transport integration remain separate work. Keep #204 open for those phases.
