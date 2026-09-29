# game

The `game` app models how a chronicle is played: chronicles and their storytellers,
stories, scenes with their posts and live chat, dice commands, character journals, and
the experience (XP) and freebie records that storytellers review. This page is the entry
point for developers and agents working in the app; the pages under [`docs/`](docs/) are
the detailed reference.

## Main concepts

- **Chronicle**: a campaign. It has a head storyteller (`head_st`), view-only game
  storytellers, and per-gameline storytellers recorded as `STRelationship` rows.
  Characters, items, locations and scenes belong to a chronicle.
- **Scene**: a play session inside a chronicle, with a cast of characters, a location, a
  gameline and a visibility (`CHRONICLE`, `PARTICIPANTS`, `PUBLIC`). Players post as
  their characters; posts can spend points and roll dice. An open scene updates live
  over a WebSocket.
- **Story**: a named arc in a chronicle. `Story.award_xp` gives a one-off story XP award
  and marks it given (no page calls it; see [XP](docs/xp.md#story-xp)).
- **Week**: a weekly XP period. Closing a scene enrolls its characters in the week that
  ends on the next Sunday; players then file a `WeeklyXPRequest`.
- **XP and freebie records**: `XPSpendingRequest` (a pending or decided XP spend),
  `FreebieSpendingRecord` (freebie points spent at character creation) and
  `StoryXPRequest`.
- **Journal**: one per character, created automatically; the owner writes dated entries
  and a storyteller can answer each one.

Terms such as ST, gameline, freebies and botch are defined in the
[glossary](../docs/reference/glossary.md).

## Key modules

| Path | Responsibility |
|------|----------------|
| [`models.py`](models.py) | All models, the scene querysets and managers, and the dice-command parser (`process_message`, `roll_record`, `roll_result`) |
| [`views.py`](views.py) | Page views: chronicle, scene, story, week, journal, XP and freebie records, setting elements |
| [`actions.py`](actions.py) | POST-only action views: close a scene, add a character, post, journal entry and response, create a story or scene from a chronicle |
| [`forms.py`](forms.py) | Scene, post, journal, chronicle, story, weekly XP, XP spend and freebie forms; chronicle object-creation forms |
| [`urls.py`](urls.py) | URL patterns under `/game/` in the `game` namespace |
| [`security.py`](security.py) | Read audiences: `readable_chronicles`, `staffed_chronicles`, `filter_scenes`, `can_view_scene`, `filter_private_records`, `can_read_private_record` |
| [`selectors.py`](selectors.py) | Read-side aggregation: the chronicle page, week scene counts, post windows, author roles, read markers |
| [`scene_chat.py`](scene_chat.py) | The single posting path (`can_post`, `create_post`) and `broadcast` of scene events |
| [`consumers.py`](consumers.py) | `SceneChatConsumer`, the WebSocket consumer for live scenes |
| [`routing.py`](routing.py) | WebSocket URL patterns (`ws/scene/<id>/`) |
| [`rolls.py`](rolls.py) | Turns a post's stored roll data into the roll strip shown in the transcript |
| [`xp_spend.py`](xp_spend.py) | The Spend XP page's preview and spend, through the character's XP service |
| [`spending_approval.py`](spending_approval.py) | `can_approve_spending`, `require_spending_approver`, `decide_spending_request` |
| [`text.py`](text.py) | `straighten_quotes`: typographic quotes to ASCII in posts |
| [`signals.py`](signals.py) | Creates a `Journal` for every new character |
| [`admin.py`](admin.py) | Django admin registrations for every model |
| [`management/commands/`](management/commands/) | `migrate_jsonfield_to_models` |
| [`templates/game/`](templates/game/) | Spread pages and partials for everything above |
| [`static/game/js/`](static/game/js/) | `scene-chat.js`, `week-detail.js`, `xp-spend.js` |
| [`tests/`](tests/) | Model, view, action, form, consumer, browser and URL tests |

`game/migrations/` contains no migration files; schema changes for older databases are
applied by the `tg_schema` app (see
[schema migrations](../docs/architecture/schema-migrations.md)).

## How it connects to other apps

- **characters, items, locations**: characters join scenes (`Scene.characters`), weeks
  (`Week.characters`) and own journals and XP records. Scenes point at a
  `locations.LocationModel`. The Spend XP and approval code calls the character XP and
  freebie services in `characters/services/`.
- **core**: permissions come from `core.permissions.PermissionManager`; route access
  is declared in [`core/route_policy_manifest.py`](../core/route_policy_manifest.py)
  (`GAME` for pages, `ACTION` for `actions.py`) and enforced by
  `core.middleware.authorization.AuthorizationMiddleware`, which also hides private game
  records and unreadable scenes and chronicles with a `404`. Action views extend
  `core.actions.ObjectActionView`. `core.xp_utils` awards scene and story XP.
- **accounts**: the profile dashboard reads this app's models and `security.py`
  audiences; the profile's scene XP, weekly XP and mark-read actions live in `accounts`.
- **tg**: [`tg/asgi.py`](../tg/asgi.py) routes WebSocket connections to
  `game.routing.websocket_urlpatterns`; `CHANNEL_LAYERS` in the settings selects the
  channel layer.

## Documentation

| Page | Contents |
|------|----------|
| [docs/models.md](docs/models.md) | Every model: fields, relations, methods and invariants |
| [docs/scenes.md](docs/scenes.md) | Scene lifecycle, posting, dice commands, roll strips, read markers |
| [docs/websockets.md](docs/websockets.md) | The live scene protocol, consumer, events and client script |
| [docs/xp.md](docs/xp.md) | Scene, story and weekly XP awards; XP spending and freebie records |
| [docs/access-and-selectors.md](docs/access-and-selectors.md) | `security.py` audiences and `selectors.py` read helpers |
| [docs/views-and-urls.md](docs/views-and-urls.md) | Every URL, view and permission |
| [docs/forms.md](docs/forms.md) | Every form |
| [docs/templates.md](docs/templates.md) | Templates, partials and scripts |
| [docs/admin.md](docs/admin.md) | Django admin configuration |
| [docs/management-commands.md](docs/management-commands.md) | `migrate_jsonfield_to_models` |

## Tests

Tests live in [`tests/`](tests/) and run with `python manage.py test game`. See
[testing](../docs/development/testing.md) for the runner and conventions.

| Path | Covers |
|------|--------|
| `tests/models/test_models.py` | Every model, querysets, `get_next_sunday`, indexes |
| `tests/views/test_views.py` | Page views, dice-command processing, list query counts |
| `tests/views/test_game_actions.py` | The action views in `actions.py` |
| `tests/views/test_xp_spend.py` | The Spend XP page, chaining, preview and spend |
| `tests/views/test_approval_security.py`, `test_private_visibility.py`, `test_relationship_security.py` | Approval scope, private records, ST relationship rules |
| `tests/views/test_story_chronicle.py`, `test_spread_pages.py` | Stories in chronicles; chronicle tabs, current week, week navigation |
| `tests/forms/test_forms.py` | Scene, post, story, journal and weekly XP forms |
| `tests/integration/test_integration.py` | `XPSpendingRequest` and `FreebieSpendingRecord` behaviour, the XP spending system, indexes and edge cases |
| `tests/test_scene_chat.py`, `test_scene_rolls.py`, `test_scene_unread.py` | Posting path and post windows; roll parsing and strips; read markers and the unread divider |
| `tests/consumers/` | `SceneChatConsumer` authorization, posting, sync, events, live rolls and read markers |
| `tests/browser/test_scene_chat.py` | Real-browser live chat through Daphne and Playwright; skipped when Playwright or Chromium is missing |
| `tests/urls/test_url_patterns.py` | URL names and paths |
| `tests/test_rules_out_of_views.py`, `tests/templates/` | Extracted helpers; scene template structure |

## See also

- [Scenes and real-time architecture](../docs/architecture/scenes-and-realtime.md)
- [XP and approvals](../docs/architecture/xp-and-approvals.md)
- [Authorization](../docs/architecture/authorization.md)
- [accounts app](../accounts/README.md)
- [characters app](../characters/README.md)
