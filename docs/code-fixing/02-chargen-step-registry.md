# Task: Design a single source of truth for character-creation steps in `tg` (Step 2)

You are designing, **not implementing**, a registry that defines each character type's creation wizard ("chargen") steps in exactly one place. The repository is `charlesmsiegel/tg`: Django 5.2 with django-polymorphic 4.1, a World of Darkness manager with 8 gamelines and about 30 character types. The registry is the keystone of the view refactor: Steps 3 (generic step views), 4 (rules out of views) and 10 (htmx chargen) all build on it. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/model-standards/SKILL.md`, `.claude/skills/tg-domain/SKILL.md` (it explains chargen, freebies, XP and the gameline terms), `.claude/skills/tg-testing/SKILL.md` and `.claude/skills/tg-permissions/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/` and follow their format. Read the Step 0 authorization design (`*-authorization-hardening-design.md`) if it exists; your registry must fit its permission mechanism. Write:
  - `docs/superpowers/specs/2026-09-25-chargen-step-registry-design.md`
  - `docs/superpowers/plans/2026-09-25-chargen-step-registry.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed.
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## How chargen works today

- **Routing.** `/characters/<pk>/` is `GenericCharacterDetailView(DictView)` (`characters/views/core/__init__.py:138`, `DictView` at `core/views/generic.py:43-75`).
  - It dispatches on the object's polymorphic `type` to a per-type router, e.g. `MageCharacterCreationView` (`characters/views/mage/mage.py:1095-1121`).
  - That router is a `HumanCharacterCreationView` subclass (`characters/views/core/human.py:653-668`, `key_property = "creation_status"`). While `status == "Un"` it dispatches on the integer `creation_status` to a step view; otherwise it falls back to the detail view.
  - Each router only overrides a literal `view_mapping = {1: ..., 2: ...}` dict. **Confirmed.**
  - Reported: 21 routers with 231 step slots (Mage 21, Sorcerer 18, Demon 15, MtAHuman/Companion/Wraith 14, Vampire 13, Garou 12, Fera 11, Fomor 10, Changeling/Thrall/Ghoul 9, the gameline humans and Kinfolk 8, Human/Drone 7).
- **Step numbers are duplicated in four places:**
  1. `view_mapping` positions.
  2. Model `freebie_step` class attributes, e.g. `characters/models/vampire/vampire.py:~23`.
  3. A hard-coded `freebie_step_map` in a Character QuerySet method (`characters/models/core/character.py:~78-113`), commented "This must match the freebie_step class attributes defined in each character type". **Confirmed.**
  4. Template ladders like `{% if object.creation_status == 17 %}{% include ... %}{% endif %}` in each type's `chargen.html`. Reported: 330 such checks (mage 32, sorcerer 31, companion 27, wraith 25, mtahuman 25, fera 24, …).
- **They have drifted apart:**
  - **Mage (Confirmed).** The views put Mentor at 17, Contacts at 18, Retainers at 19, Chantry at 20 and Specialties at 21. `characters/templates/characters/mage/mage/chargen.html:~129-142` renders the Chantry form at 17 and Specialties at 18, and has nothing for 19–21.
  - **Vampire (Reported).** The template renders Specialties at step 10 and has no blocks for 11–13 (`vampire_chargen.py:~350-364` vs `vampire/vampire/chargen.html:~256`).
  - **Garou (Reported).** `werewolf/garou/chargen.html` has blocks only for steps 1–3 of 12.
  - **`freebie_step` disagreements (Reported).**

    | Type | `view_mapping` | `freebie_step_map` |
    |---|---|---|
    | Werewolf | 7 | 5 |
    | Fomor | 6 | 5 |
    | Wraith | 9 | 7 |
    | Demon | 8 | 7 |

    Fera inherits 5 but the map says 8.
  - The code admits it: `characters/views/core/chargen_back.py:~45` and `human.py:~612-613` ("a mismatch silently miscolors the progress bar").
- **The progress bar.** `ChargenProgressMixin` (`characters/views/core/chargen_mixins.py`) is used only by the 7 `Human*ChargenView` classes (`human.py:625-650`), so no gameline shows it. **Confirmed.**
- **Step advancement happens by side effect:**
  - Reported: about 92 `creation_status += 1` mutations spread across views.
  - Some steps skip themselves on GET inside `dispatch`, e.g. `HumanFreebiesView.dispatch` (`human.py:518-524`, **Confirmed**), `HumanLanguagesView.dispatch` and `GenericBackgroundView.dispatch` (`characters/views/core/generic_background.py:~87-95`).
  - Reported: hand-rolled "skip the following background steps" loops in `mage.py:~947-972`, `companion.py:~456-479` and `sorcerer.py:~597-620`, each of which re-encodes the `view_mapping` order.
- **Back navigation** lives in `characters/views/core/chargen_back.py`; read it.
- **Missing templates.** Several step views reference templates that don't exist, e.g. `characters/human/human/chargen.html` (see the comment at `human.py:~457-462`) and the Demon, Thrall and DtFHuman `chargen.html` files (Reported).
- Supernatural types reuse mortal steps across modules: Mage builds on MtAHuman, Garou/Fera/Kinfolk on WtAHuman, and Wraith on WtOHuman.

## What the design must deliver

1. **A registry data model.** For example, an ordered list of `Step(key, view, template, label, skip_if, required_permission, is_freebie_step, …)` per character type.
   - Decide where it lives: the model class, the gameline package, or a central module.
   - Decide how shared prefixes compose: MtAHuman steps plus Mage-specific steps, WtAHuman plus Garou, and so on. Use composition, not copying.
   - Show the complete registry for 2–3 real types, including Mage and Vampire.
2. **What is derived from the registry:**
   - the router mapping;
   - the freebie step, replacing both the model attributes and `freebie_step_map`. Show how the QuerySet filter that uses the map is expressed;
   - the progress bar for every type;
   - back navigation;
   - template selection. `chargen.html` includes `step.template` from context, so the `creation_status == N` ladders are deleted and each step becomes a standalone partial. Step 10 (htmx) depends on those partials;
   - one `advance(character)` operation that evaluates skip conditions, replacing the `dispatch` self-skips and the hand-rolled loops. It must never mutate state before authorization (see Step 0).
3. **A persistence decision:** keep an integer `creation_status` or move to step keys. Justify it against existing data: characters mid-chargen (`status="Un"`) whose integer would point at a different step if the order changes. Include any data migration and how in-progress characters are handled on deploy.
4. **Parity and safety tests:**
   - for every type, each step's template exists and renders for the owner;
   - the registry-derived freebie step matches the step that holds the freebies view;
   - there are no orphan step views;
   - golden tests pinning the current step order before migrating, so any reorder is deliberate.
5. **A migration plan:** one pilot gameline first (Vampire is suggested: 13 steps with known drift), then one PR per gameline.
   - List the user-visible behaviour changes. Fixing drift changes which form appears at some steps, and some steps that currently render nothing will start working.
   - Decide what to do about types whose step templates don't exist yet.
6. **Interaction with authorization.** Say whether each step declares its own required permission or whether the router enforces one gate, consistent with the Step 0 design.

## Constraints and scope

- Design only. Don't modify application code.
- In scope: the registry, routing, advancement, the freebie step, the progress bar, back navigation, and template selection for steps.
- Out of scope, owned by other steps:
  - merging per-gameline copies of step view classes such as Languages and Specialties (Step 3; your design should make that easy);
  - moving game rules out of `form_valid` (Step 4);
  - htmx/Alpine (Step 10). Do make step partials fragment-renderable.
- Prefer no new third-party dependencies (e.g. django-formtools) unless you justify them against a small in-house registry.
