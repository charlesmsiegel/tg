# game forms

This page documents every form in [`game/forms.py`](../forms.py): what it binds to, the
extra constructor arguments it needs, how it narrows its choices and how it saves. Read
it before changing a scene, journal, chronicle, story or XP form, or before reusing one
from another app.

Most forms take their context as keyword arguments that the constructor pops before
calling Django's `Form.__init__` (for example `scene=`, `user=`, `character=`). Views
pass them from `get_form_kwargs`; `game.actions` views pass them from
`ObjectActionView.get_form_kwargs`. Templates render fields through Spread includes
(`core/tl/field.html`, `game/tl/fields.html`), so widget CSS classes set here matter
only where noted.

## Scene forms

### SceneCreationForm

Plain `Form` behind NEW SCENE on the chronicle page (`ChronicleDetailView` renders it,
`actions.ChronicleSceneCreateView` saves it).

- Constructor: `SceneCreationForm(data=None, *, chronicle, user=None)`.
- Fields: `name`, `location` (locations of `chronicle`, by name), `date_of_scene`,
  `gameline` (`core.constants.GameLine.CHOICES`, initial `wod`).
- Gameline narrowing: head ST, staff and superusers keep every gameline. For anyone
  else the choices are limited to the gamelines of their `STRelationship` rows in the
  chronicle, mapped from `Gameline.name` to a code through `GAMELINE_NAME_TO_CODE`; when
  `wod` is not among them the first allowed code becomes the initial value. A user with
  no relationship keeps the full list, and the action's `can_manage_scope` check then
  refuses the save.
- No `save()`: the action calls `Chronicle.add_scene(name, location, date_of_scene=...,
  gameline=...)`.

### SceneForm

`ModelForm` on `Scene` for `SceneCreateView` and `SceneUpdateView`.

- Constructor: `SceneForm(data=None, *, chronicle=None, instance=None)`.
- Fields: `name`, `location`, `date_of_scene` (date input), `gameline`, `visibility`,
  `finished`, `xp_given`.
- `location` is limited to the given chronicle's locations, or the instance's
  chronicle's when editing; with neither, every location is offered.
- `visibility` is optional; `clean_visibility` turns an empty value into
  `Scene.Visibility.CHRONICLE`.

The form has no `chronicle` field. `SceneCreateView` sets `instance.chronicle` from the
URL; without `chronicle_pk` the scene is saved with no chronicle.

### AddCharForm

Used by `actions.SceneAddCharacterView`, and by `SceneDetailView` and the WebSocket
consumer to list the characters a viewer can add.

- Constructor: `AddCharForm(data=None, *, user, scene)`.
- Field: `character_to_add`, a `ModelChoiceField` over the characters of the scene's
  chronicle that are not in the scene yet. Unless the user can manage the scene's scope
  (`PermissionManager.can_manage_scope(user, scene.chronicle, scene.gameline)`), only
  the user's own characters are offered.

### PostForm

The post composer, used by `actions.ScenePostView` and the WebSocket consumer.

- Constructor: `PostForm(data=None, *, user, scene)`.
- Fields: `character` (optional), `display_name` (optional, up to 100 characters),
  `message`.
- `character_queryset` (an attribute, also the `character` field's queryset): the
  user's characters in the scene's chronicle that are already in the scene.
- `clean()` rejects an empty or whitespace-only message and requires `character` when
  the user has more than one character in the scene.
- No `save()`: `game.scene_chat.create_post(scene, form)` posts it (see
  [scenes](scenes.md#posting)).

## Chronicle forms

### ChronicleForm

`ModelForm` on `Chronicle` for `ChronicleCreateView` and `ChronicleUpdateView`. Fields:
`name`, `head_st`, `theme`, `mood`, `year`, `headings`. Game storytellers, setting
elements and allowed object types are edited in the Django admin.

### Chronicle object-creation forms

`ChronicleCharacterCreationForm`, `ChronicleLocationCreationForm` and
`ChronicleItemCreationForm` share `ChronicleObjectCreationFormBase`
(`widgets.ChainedSelectMixin` + `Form`). The chronicle page renders them as GET forms
that submit to `core:object_type_redirect`, which forwards to the chosen type's creation
page; they are never saved.

- Constructor: `(data=None, *, chronicle, user)`.
- Fields: `gameline` and a chained type field (`char_type`, `loc_type` or
  `item_type`), both `widgets.ChainedChoiceField`. Because all three forms share one
  page, `_setup_chains` gives each its own chain name and field ids
  (`chronicle_<char|loc|obj>`).
- Choices come from `ObjectType` rows of the form's `object_type_code` (`char`, `loc`,
  `obj`), via `_build_choices(chronicle, user, excluded_types)`:

  | Caller | Gamelines offered | Types offered |
  |--------|-------------------|---------------|
  | Head ST, staff, superuser | Every gameline with an `ObjectType` | Every type |
  | User with `STRelationship` rows in the chronicle | Those gamelines | Every type |
  | Anyone else | Gamelines that have an ST in the chronicle | The chronicle's `allowed_objects` of that kind |

- The character form excludes group types and trait or reference types listed in
  `ChronicleCharacterCreationForm.EXCLUDED_TYPES`.
- Labels come from `_format_label`: `<line>_human` becomes "Human (<Gameline>)",
  `spirit_character` becomes "Spirit", other names are title-cased.

The template hides a form whose `gameline` choices are empty.

## Story forms

- `StoryForm`: `ModelForm` on `Story` with `name` only, for NEW STORY on the chronicle
  page; `actions.ChronicleStoryCreateView` sets the chronicle.
- `StoryEditForm(StoryForm)`: adds `chronicle`, for the staff-only standalone pages.
  The constructor requires `user=`; the chronicle choices are
  `staffed_chronicles(user)` by name, with "Unassigned" as the empty label.
- `StoryXPRequestForm`: `ModelForm` on `StoryXPRequest` with `story`, `success`,
  `danger`, `growth`, `drama`, `duration`. Takes `character=` (or reads it from the
  instance) and limits `story` to the character's chronicle's stories plus stories with
  no chronicle. `save()` sets `instance.character` from the constructor argument.

## Journal forms

- `JournalEntryForm`: `date` and `message`. Constructor: `JournalEntryForm(data=None,
  *, instance)` where `instance` is the `Journal`. `save()` returns
  `instance.add_post(date, message)`, which applies point tags and dice commands and
  returns `None` for a malformed command.
- `STResponseForm`: `st_message`. Constructor: `STResponseForm(data=None, *, entry,
  prefix=...)`; the journal page prefixes each with `entry-<pk>`. `save()` writes
  `entry.st_message`.

## XP forms

### WeeklyXPRequestForm

`ModelForm` on `WeeklyXPRequest`, used on the profile (`accounts` views) and on the
`game` weekly request pages.

- Constructor: `WeeklyXPRequestForm(data=None, *, character=None, week=None,
  instance=None)`.
- Fields: `finishing`, `learning`, `rp`, `focus`, `standingout`, and the four scene
  fields. With a `week`, each scene field offers `week.finished_scenes()` that
  `character` played in. `finishing` and the scene fields are optional.
- `clean()` raises "Must include scene for any XP claimed" when a claimed criterion has
  no scene.
- `player_save(commit=True)`: sets `finishing=True`, `week` and `character` on the
  instance and saves it when `commit`.
- `submit()`: files the player's request once through `player_save`; returns `None`
  when the character already has a request for the week, including when a concurrent
  submit wins the `(week, character)` unique constraint. Both create views call it.
- `st_save()`: passes the cleaned criteria and scenes to `WeeklyXPRequest.approve`,
  which awards the XP. It raises `ValueError` if the request is already approved.

Templates render it through `game/tl/fields.html` with `skip="finishing"` or the
profile's `accounts/includes/xp_weekly_rows.html`.

### XP spend forms

The Spend XP page (`XPSpendingRequestCreateView`) uses `XPSpendForm` or
`MageXPSpendForm`, chosen by `xp_spend_form_class(character)` (`MageXPSpendForm` for a
`characters.models.mage.mage.Mage`). Each combines `XPSpendFormMixin` with the
character's own XP form, `characters.forms.core.xp.XPForm` or
`characters.forms.mage.xp.MageXPForm`, which knows the traits the character may raise.

`XPSpendFormMixin`:

- Constructor: `(data=None, *, character, ...)`. It reads the current `category` and
  `example` from the data (or `initial`) before the base form builds its choices, so
  only the chosen trait type's traits, and the chosen merit's ratings, are built.
- Replaces the chained fields with plain `ChoiceField`s: `category` ("Trait type",
  limited to `XP_SPEND_TRAIT_TYPES`), `example` ("Trait") and `value` ("Rating").
  Drops `pooled`, `image_field` and `resonance`; relabels `note` for new backgrounds.
- `_forget_stale_choices()`: a submitted trait or rating that is not on offer for the
  chosen type is removed from the bound data, so changing the trait type does not
  leave an invalid choice behind.
- `has_traits`: false for `Willpower` and `Arete` (`XP_SPEND_SINGLE_TRAITS`), which
  have no trait list.
- `enable_htmx(url)`: adds `hx-get`, `hx-trigger="change delay:200ms"`,
  `hx-target="#xp-spend-fields"`, `hx-swap`, `hx-sync` and
  `hx-include="#xp-spend-fields"` to the three selects, so the CSRF token is never sent
  on these GETs.
- `quiet()`: clears errors for a preview of an unfinished selection.
- `clean_example()` requires a trait for types that have one; `clean_value()` requires
  a rating for `MeritFlaw`.

`game.xp_spend.spend_arguments(cleaned_data)` turns the cleaned data into the service's
`spend(category, example, value, note)` arguments. See [XP](xp.md#the-spend-xp-page).

### Other record forms

| Form | Model | Fields | Used by |
|------|-------|--------|---------|
| `XPSpendingRequestCorrectionForm` | `XPSpendingRequest` | `trait_name`, `trait_type`, `trait_value` (never `cost`) | `XPSpendingRequestUpdateView` |
| `XPSpendingRequestApprovalForm` | `XPSpendingRequest` | `approved` as a select of `XPApprovalStatus.CHOICES` | The decision form on the request's detail page. It offers `Pending` too, but `XPSpendingRequestApproveView` answers `400` to anything but `Approved` or `Denied`. |
| `FreebieSpendingRecordForm` | `FreebieSpendingRecord` | `trait_name`, `trait_type`, `trait_value`, `cost` (0 or more) | `FreebieSpendingRecordCreateView`, which files the record through `game.freebie_records.file_freebie_record` (the cost is deducted from the pool); takes `character=` |
| `FreebieSpendingRecordCorrectionForm` | `FreebieSpendingRecord` | `trait_name`, `trait_type`, `trait_value` (never `cost`) | `FreebieSpendingRecordUpdateView` |

## See also

- [game views and URLs](views-and-urls.md)
- [Scenes](scenes.md)
- [XP](xp.md)
- [accounts forms](../../accounts/docs/forms.md)
- [widgets app](../../widgets/README.md) (chained selects)
