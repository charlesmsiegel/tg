# Action endpoints: implementation plan (Step 5)

Design: `docs/superpowers/specs/2026-09-25-action-endpoints-design.md`.

Each task is one commit on the step branch, in this order. Before every
commit, run `python manage.py test core game characters accounts` (or the
narrower apps listed) and `ruff check` on the touched files. A task is done
when its tests pass and its old handler is gone.

## Task 0: Baseline

- Record the failing tests at the base commit (`python manage.py test
  --parallel 8`), so later failures can be told apart from pre-existing ones.
- Write the probe test for D8 (generic router 403 for an approved Vampire,
  Demon, etc.) and keep it as a pinned `expectedFailure`-free assertion of
  the **current** status (403), with a comment naming Step 2 as the owner.

## Task 1: Base class and approval endpoints (A1, A2)

Files:
- `core/actions.py` (new): `ActionFailed`, `ObjectActionView` as designed.
- `core/access_policy.py`: `ACTION` family (405 for non-POST, 401 for
  anonymous).
- `game/spending_approval.py`: look up the record by `pk` and character
  first, then check visibility (404) and approver rights (403), then raise
  `SpendingAlreadyDecided` if it is not `Pending`.
- `characters/views/core/actions.py` (new): `XPRequestDecisionView` and the
  subclasses `XPRequestApproveView` / `XPRequestRejectView`.
- `characters/urls/core/detail.py`: two routes, placed **before**
  `<pk>/`.
- `core/route_policy_manifest.py`: `"ACTION"` frozenset with the two classes.
- `characters/templates/characters/mage/mage/mage_xp_form.html`: history
  moved out of the spend form; per-row forms for `Pending` only.
- Delete `ApprovalMixin`, `XPApprovalMixin` and their imports and bases in
  the 25 detail views; delete the approval block of `MageDetailView.post`.
- Tests: `core/tests/test_actions.py` (base class, using a tiny test-only
  action on `Human`), `characters/tests/views/test_xp_decision_actions.py`
  (matrix, GET 405, double submit, cross-character 404, self-approval).
  Remove the `ApprovalMixin` tests in `core/tests/mixins/test_mixins.py` and
  move any unique assertions into the new file.

Verify: `python manage.py test core characters.tests.views game.tests.views`.

## Task 2: Retire and decease (A3, A4)

- `characters/services/status.py` (new): `change_character_status`.
- `characters/views/core/actions.py`: `CharacterRetireView` (owner or scoped
  editor) and `CharacterDeceaseView` (scoped editor), both `lock = True`.
- URLs `characters:retire` and `characters:decease`; manifest entries.
- `buttons.html`: one form per button, each with its own `action`.
- Delete `CharacterDetailView.post` and the retire/decease block of
  `MageDetailView.post`.
- Tests: `characters/tests/views/test_status_actions.py` (the matrix, GET
  405, invalid transition message, one action per request) and the
  every-type walk over `GenericCharacterDetailView.view_mapping`.
- Update the existing tests that POST `retire`/`decease` to detail URLs
  (`characters/tests/models/core/test_character.py`, the per-gameline model
  tests, `test_public_detail_authorization.py`).

## Task 3: Mage sheet (A5, A6)

- `characters/services/specialties.py`: `record_specialties`.
- `characters/services/mage_xp.py`: `spend_mage_xp`.
- `characters/views/core/actions.py`: `CharacterSpecialtiesView` (`model =
  Human`, `EDIT_FULL`).
- `characters/views/mage/actions.py` (new): `MageXPSpendView`
  (`host_view_class = MageDetailView`; `is_valid` also binds and validates
  `RoteCreationForm` for the Rote category; `form_invalid` passes both forms
  to the host).
- `MageDetailView.get_context_data`: use `setdefault` for `rote_form` so a
  bound form from the action survives. Delete `post`, `learn_rote` and
  `add_specialties`.
- URLs `characters:add_specialties` and `characters:mage:spend_xp`; manifest.
- Templates: the Mage spend form and specialties form get their `action`s;
  remove the three dead Vampire-family specialties blocks.
- Tests: move the Mage view tests that post `spend_xp`/`specialties` to
  the new URLs; add a matrix for both endpoints; add an unknown-stat
  specialty test (D12 from Step 4, kept green); add the re-render-with-errors
  test for an invalid rote.

## Task 4: Scene (G1–G3)

- `game/actions.py` (new): `SceneActionView` base (`model = Scene`,
  `can_see = can_view_scene`, finished → 403 except for close),
  `SceneCloseView`, `SceneAddCharacterView` (`AddCharForm`), `ScenePostView`
  (`PostForm`).
- URLs under `game:`; manifest.
- `game/scene/detail.html`: three `action`s.
- Delete `SceneDetailView.post` (keep the `straighten_quotes` alias).
- Tests: `game/tests/views/test_scene_actions.py`; update
  `test_relationship_security.py`, `test_views.py` and
  `test_private_visibility.py` scene POSTs to the new URLs. The
  cross-chronicle add changes from 403 to a form error with no write.

## Task 5: Journal (G4, G5)

- `game/actions.py`: `JournalEntryCreateView`, `JournalResponseView`
  (`APPROVE` on the character; entry scoped to the journal).
- URLs; manifest; `game/journal/detail.html` actions.
- Delete `JournalDetailView.post`.
- Tests: the matrix, a draft-owner self-response regression (D5, failing
  first), PRG (D6), an entry of another journal → 404.

## Task 6: Chronicle (G6, G7, N4)

- `game/actions.py`: `ChronicleStoryCreateView`, `ChronicleSceneCreateView`
  (`host_view_class = ChronicleDetailView`).
- The chronicle's creation forms point at the typed endpoint from Task 7.
  Task 7 therefore lands the endpoint first, or this task adds it.
- Delete `ChronicleDetailView.post` and `_get_create_redirect_url`.
- Tests: the matrix for story and scene creation, the wrong-gameline ST 403,
  the invalid form re-rendered with its errors (D10).

## Task 7: Index navigation (N1–N3)

- `core/views/object_type_redirect.py` (new): `ObjectTypeRedirectView`, GET
  only, `PUBLIC_READ` in the manifest, `create` requires login.
- `core/urls.py`: `types/<str:kind>/<str:action>/`.
- Five templates switch to `method="get"`.
- Delete the three index `post` methods.
- Tests: move `core/tests/security/test_index_redirects.py` to the new
  endpoint (every gameline code, unknown → 404, anonymous create → login,
  POST → 405).

## Task 8: Guard and record

- `core/tests/test_action_guard.py`: the AST scan and the DetailView `post`
  walk. Show that they fail at the base commit.
- Add the implementation record to the design doc: measured line counts,
  deviations, and pre-existing failures.
