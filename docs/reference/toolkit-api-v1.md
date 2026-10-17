# Native TG API v1 — first increment of toolkit issue #195

This is an initial authenticated JSON interface, **not completion of #195** and not a
Rust `Store` implementation. Install `requirements.txt`; DRF supplies JSON read views,
serializers and pagination. Django 5.2 is the supported framework version. No database
schema, token table, migration or CORS setting is added.

## Authentication and CSRF

Use the existing Django session login flow at `/accounts/login/`: GET the form to obtain
the CSRF cookie, then POST credentials and its CSRF token with a cookie-aware client.
Keep the resulting `sessionid` cookie private. This increment adds no JSON login/logout,
JWT, bearer token, password handling or cross-origin access. Existing site logout applies.

`GET /api/v1/session/` requires an authenticated session and returns
`{"user":{"id":123,"username":"name"},"csrf_token":"..."}`. Retain its cookies and send
`X-CSRFToken: <csrf_token>` on every JSON POST. Both mutation routes run normal Django
CSRF middleware (not `csrf_exempt`). Use HTTPS in production; session cookie security
continues to come from the existing production settings. Do not put cookies in URLs.

## Routes

| Method and path | Result / authority |
|---|---|
| GET `/api/v1/session/` | Current user ID/name and CSRF token; login required |
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
object/scope checks. Anonymous calls are 401. Hidden and missing read objects return the
same 404. Partial viewers and observers receive no private sheets from these routes,
even if a public card is available through the ordinary site. A visible object that
cannot be edited returns 403. Validation errors are 400; unsupported methods are 405.
Some middleware denials/CSRF errors remain standard TG text/HTML, so clients must check
HTTP status and Content-Type before parsing JSON. Successful reads/writes use
`Cache-Control: private, no-store`; no public API cache is introduced.

Mutation bodies require `Content-Type: application/json` and a JSON object. Unknown fields
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
