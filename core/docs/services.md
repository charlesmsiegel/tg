# Core services

This page describes the service layer in [`core/services/`](../services/) and the XP
helpers in [`core/xp_utils.py`](../xp_utils.py): what each function does, which checks
it makes itself and which it leaves to the caller. It is for anyone changing approval
flows, chronicle pages or XP awards. For the end-to-end flows across apps see
[XP and approvals](../../docs/architecture/xp-and-approvals.md).

A service holds the business rule and the database writes; the view (or action endpoint)
that calls it loads the request data, authorizes the route and turns the result into a
response. Import services from the package:

```python
from core.services import ApprovalService, ChronicleDataService
```

## `ApprovalService`

[`core/services/approval.py`](../services/approval.py) owns the status workflow of
approvable objects: submit, return for revisions, approve, and image approval. The
`accounts` views `ObjectSubmissionView`, `ObjectRevisionView`, `ObjectApprovalView` and
`ImageApprovalView` call it; the `{% tl_object_actions %}` tag renders the matching
buttons (see [templates and static files](templates-and-static.md#object-actions)).

### Model type keys

Callers name the object with a model type string and a primary key.

| Map | Keys |
|-----|------|
| `OBJECT_MODEL_MAP` | `character` (`Character`), `group` (`Group`), `chimera` (`Chimera`), `effect` (`Effect`), `location` (`LocationModel`), `item` (`ItemModel`), `rote` (`Rote`), `template` (`CharacterTemplate`) |
| `IMAGE_MODEL_MAP` | `character`, `location`, `item` |

An unknown key raises `ValueError`; a missing object raises `Http404`.

### Status transitions

The statuses are the `CharacterStatus` codes (see
[models](models.md#constants)). The service allows these transitions:

| From | To | Method | Who |
|------|----|--------|-----|
| `Un`, `Rev` | `Sub` | `transition_object(type, pk, user, "Sub")` | A user with `EDIT_FULL` (the owner of a draft, or a scoped editor) |
| `Sub` | `Rev` | `transition_object(type, pk, user, "Rev")` | A user with `APPROVE` |
| `Sub` | `App` | `approve_object(type, pk, approver)` | A user with `APPROVE` |

Retiring and marking deceased are character actions in the `characters` app, not part of
this service.

#### `transition_object(model_type, object_id, user, target_status)`

Runs in a transaction and locks the row (`select_for_update`). In order:

1. `target_status` must be `"Sub"` or `"Rev"` (else `ValueError`).
2. The user must have `VIEW_FULL`, else `PermissionDenied`. A user who cannot see the
   object learns nothing about its state.
3. For `"Sub"`: the status must be `Un` or `Rev` (else `ValidationError`), and the user
   must have `EDIT_FULL` (else `PermissionDenied`). If the model defines
   `submission_errors()`, a non-empty list is raised as a `ValidationError`.
4. For `"Rev"`: the status must be `Sub` (else `ValidationError`), and the user must have
   `APPROVE` (else `PermissionDenied`). If the model defines `on_returned_for_revision()`,
   it is called and the field names it returns are saved along with `status`.
5. Saves `status` (with `update_fields`) and returns the object.

The two hooks are opt-in per model. `locations.models.mage.chantry.Chantry` uses both:
`submission_errors()` lists unfinished creation steps and unspent points, and
`on_returned_for_revision()` resets `creation_status` to 1 so the owner re-enters the
creation wizard.

```python
class Chantry(LocationModel):
    def submission_errors(self):
        """Reasons this chantry cannot be submitted yet; empty when it can."""
        ...

    def on_returned_for_revision(self):
        self.creation_status = 1
        return ["creation_status"]
```

#### `approve_object(model_type, object_id, approver=None)`

Runs in a transaction and locks the row. Raises `PermissionDenied` unless `approver` is
given and has `APPROVE` on the object, and `ValidationError` unless the status is `Sub`.
Sets `status="App"` and, for characters, calls `update_pooled_backgrounds()` on every
group the character belongs to. Returns `(object, message)`.

### Images

`approve_image(model_type, object_id)` sets `image_status="app"` and saves. It makes no
permission check: the caller must authorize first. `accounts.views.ImageApprovalView`
does so with `verify_st_for_chronicle` (a storyteller for the object's chronicle and
gameline). `parse_image_id(raw_id)` turns a form value such as `"image-123"` into
`"123"`.

### Permission checks inside the service

The service calls `PermissionManager.user_has_permission` without a `request`, so each
check queries the database rather than the per-request cache. The route policy for the
calling views (`ACCOUNT`) only requires a signed-in user; the object rule is here and, for
approvals, also in `verify_st_for_chronicle`.

## `ChronicleDataService`

[`core/services/chronicle_data.py`](../services/chronicle_data.py) groups a chronicle's
characters, locations, items, setting elements and scenes into gameline tabs for the
chronicle page. `game.selectors` calls it. All methods are class methods and return an
`OrderedDict` keyed by gameline code.

- The tab order is `GAMELINE_ORDER`: the keys of `settings.GAMELINES` except `orp`.
- The `wod` key is always first and labelled "All"; it holds everything.
- Other tabs appear only when they have content. Their label is the part of the
  gameline name before the colon ("Vampire: the Masquerade" becomes "Vampire"), from
  `get_display_name(code)`.

| Method | Grouping | Entry keys |
|--------|----------|------------|
| `group_by_gameline(queryset, gameline_attr="gameline")` | Filters the queryset per gameline in SQL (one `exists()` per tab) | `name`, `items` |
| `group_characters_by_gameline(queryset)` | Evaluates once (through `characters.models.core.character.attach_first_groups`) and filters in Python on the class attribute `gameline`; `wod` characters appear in every tab | `name`, `characters` |
| `group_locations_by_gameline(queryset)` | Evaluates once; only root locations (`parent is None`); `wod` locations in every tab | `name`, `locations` |
| `group_items_by_gameline(queryset)` | Evaluates once; `wod` items in every tab | `name`, `items` |
| `group_scenes_by_gameline(queryset)` | Filters the `gameline` field in SQL | `name`, `scenes`, `scenes_by_month` |
| `group_scenes_by_month(queryset)` | `[(datetime(year, month, 1), [scenes])]` by `date_of_scene`, in the queryset's order; scenes without a date go under 1900-01 | |

The Python-side methods group by the model class attribute, not a database column,
because `gameline` on characters, items and locations is a class attribute of each
polymorphic subclass.

## XP helpers

[`core/xp_utils.py`](../xp_utils.py):

### `award_xp_atomically(parent_model, parent_pk, character_xp_map)`

Awards XP for a `Story` or `Scene` exactly once. Inside one transaction it locks the
parent row, raises `ValidationError` (code `xp_already_given`) if `parent.xp_given` is
already true, then for each character with a positive amount locks and re-reads the
character, adds to `xp` and saves only that field, and finally sets
`parent.xp_given = True`. It returns the number of characters that received XP.
`game.models.Story.award_xp` and `game.models.Scene.award_xp` call it.

```python
from core.xp_utils import award_xp_atomically

count = award_xp_atomically(Scene, scene.pk, {char_a: 1, char_b: 0})
```

The parent model must have an `xp_given` boolean field. The lock order (parent, then each
character) is what makes a double submit or two storytellers awarding at once safe: the
second caller sees `xp_given` and fails.

### `calculate_story_xp(xp_categories)`

Returns `duration` plus one point each for true `success`, `danger`, `growth` and `drama`
keys.

## See also

- [XP and approvals](../../docs/architecture/xp-and-approvals.md)
- [Permissions and policies](permissions-and-policies.md)
- [Views: action endpoints](views.md#action-endpoints)
- [accounts app](../../accounts/README.md)
- [game app](../../game/README.md)
