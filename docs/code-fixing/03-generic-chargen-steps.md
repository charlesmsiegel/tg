# Task: Design shared, parameterized chargen step views for `tg` (Step 3)

You are designing, **not implementing**, the consolidation of per-gameline copies of character-creation ("chargen") step views into one parameterized implementation per step type. The repository is `charlesmsiegel/tg`: Django 5.2 with django-polymorphic 4.1, a World of Darkness manager with 8 gamelines. `characters/views/` has about 17,900 lines in 113 files, and the audit estimates 60–70% of the chargen step-view lines are copy-paste plus configuration. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/model-standards/SKILL.md`, `.claude/skills/tg-domain/SKILL.md`, `.claude/skills/tg-testing/SKILL.md` and `.claude/skills/tg-permissions/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/` and follow their format. **Read the Step 0 (authorization) and Step 2 (chargen step registry) designs if they exist** (`*-authorization-hardening-design.md`, `*-chargen-step-registry-design.md`). Your design sits on top of them. Write:
  - `docs/superpowers/specs/2026-09-25-generic-chargen-steps-design.md`
  - `docs/superpowers/plans/2026-09-25-generic-chargen-steps.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed.
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one, ideally by diffing the copies, and say in the doc which ones you confirmed.

## Duplication inventory

**Languages.**
- 21 classes, of which 10 are standalone copies of 45–53 lines each: `werewolf/wtahuman.py:~349`, `changeling/ctdhuman.py:~285`, `mage/mtahuman.py:~636`, `changeling/changeling.py:~517`, `werewolf/fomor.py:~301`, `vampire/vtmhuman.py:~307`, `wraith/wtohuman.py:~407`, `wraith/wraith_chargen.py:~414`, `mage/sorcerer.py:~645` and `mage/companion.py:~502`.
- The base is `HumanLanguagesView` (`characters/views/core/human.py:~527-576`).
- Reported: the wta, ctd and mta copies differ only in `template_name`.
- **Confirmed bug from drift:** `CompanionLanguagesView.form_valid` (`companion.py:~522-535`) reads `cleaned_data.get("num_languages", 1)`, which isn't a form field, and then `language_{i}` from i=0. `HumanLanguageForm` (`core/forms/language.py:20-21`) defines `language_1..N`. So Companion languages are never saved.
- Reported: Companion and Sorcerer never add English.

**Specialties** (Reported).
- 21 classes, 10 standalone copies (e.g. `wtahuman.py:~407-437` vs `human.py:~579-609`).
- `SorcererSpecialtiesView` (`sorcerer.py:~686-739`) is a copy of `CompanionSpecialtiesView` (`companion.py:~543-593`) and still uses a `companion` variable.
- The "needed specialties" rules are hard-coded in the views.

**Extras** (Reported).
- 18 standalone copies of 44–70 lines, each with a near-identical 25-line placeholder `get_form`.
- WtA (`wtahuman.py:~297-340`), VtM (`vtmhuman.py:~255-298`) and CtD (`ctdhuman.py:~233-276`) differ by model, template and one word. All three still say "when and how they Awakened", which was copied from Mage.

**Template select** (Reported).
- 6 copies of about 60 lines of view plus `CharacterTemplateSelectionForm`: `wtahuman.py:~210-271`, `vtmhuman.py:~168-229`, `mtahuman.py:~499-560`, `wtohuman.py:~216-280`, `ctdhuman.py:~147-211` and `demon/dtfhuman_chargen.py:~54-115`.
- The 6 `template_select.html` files differ in 6 lines each: the gameline code and heading class.

**Update / Create views** (Reported).
- 30 identical 13-line `get_form_class` methods returning a `Limited*EditForm` (e.g. `mage.py:~595-607`).
- About 2,600 lines are hand-written field-name lists of more than 20 entries.
- `MageCreateView.FORM_FIELDS` (`mage.py:~442-574`) lists `"time"` twice.

**Abilities** (Reported).
- `HumanAbilityView.form_valid` (`human.py:~227-247`, 21 lines) iterates talents, skills and knowledges.
- `MtAHumanAbilityView.form_valid` (`mtahuman.py:~354-472`, 119 lines) unrolls the same algorithm by hand.
- `DemonAbilityView` (`demon/demon_chargen.py:~74-110`) is identical to `DtFHumanAbilityView` (`dtfhuman_chargen.py:~127-163`).
- `WtOHumanAbilityView` (`wtohuman.py:~292-343`) is the same algorithm plus messages.

**Freebies.**
- 19 thin subclasses of the service-based `HumanFreebiesView`.
- `CompanionFreebiesView` (`companion.py:~346-499`, 132-line `form_valid`) does the math by hand even though `CompanionFreebieSpendingService` exists in `characters/services/freebie_spending/`.
- `SorcererFreebiesView` (`sorcerer.py:~501-642`) uses the service but duplicates validation.
- Moving the rules is Step 4. Here, only make the view layer uniform.

**Wraith Passions vs Fetters** (`wraith_chargen.py:~178-254` vs `~257-332`): about 76 lines each, differing only in names. Reported.

**Detail views** (Reported).
- Werewolf, Fera, Kinfolk, Changeling, CtDHuman, Demon, DtF, Thrall, Earthbound, Hunter and HtR detail views use `(XPApprovalMixin, ViewPermissionMixin, DetailView)` instead of `HumanDetailView`. Drone, Fomor and Spirit use only `(ViewPermissionMixin, DetailView)`.
- They miss `scenes` context and retire/decease handling, yet their templates show retire/decease buttons (`core/character/detail.html` → `display_includes/buttons.html`). On those pages the buttons do nothing.

**Base views pointing at the wrong template:**
- `HumanAbilityView` uses the wraith template (`human.py:~214`). Reported.
- `HumanFreebiesView`'s template doesn't exist (`human.py:~457-462`, comment references #1459). **Confirmed.**

**Genuinely different steps to keep bespoke:** Vampire/Demon virtues, Changeling arts/realms, Demon apocalyptic form, Sorcerer paths/rituals, Mage focus/spheres/rote, Fera breed/faction (Fera's 12-way `isinstance` switches may become polymorphic model methods). Confirm these and note any others you find.

**Inheritance (Reported).**
- MRO chains reach 17 classes, e.g. `KinfolkFreebiesView → WtAHumanFreebiesView → HumanFreebiesView → SpendFreebiesPermissionMixin → …`.
- The problem is inconsistency more than depth. Permissions are inherited by accident, so in one wizard some steps are gated and others aren't. Step 0 fixes the gating; your design must not reintroduce per-copy gating.

## What the design must deliver

1. **An inventory script** that groups step and CRUD view classes by structural similarity (AST or normalized diff). It should report which copies are config-only and which carry real differences. Include its output.
2. **One shared implementation per step type**, configured by class attributes or registry fields (model, form, template, messages, gameline wording):
   - show the class API;
   - list each real variation you preserve, and how: hooks, form subclasses or model methods;
   - show how it plugs into the Step 2 registry.
3. **Generated forms and fields.** Replace hand-written field lists with the form's `Meta` or model introspection. Replace the 30 `get_form_class` copies with one mixin tied to the Step 0 permission model (full vs limited edit).
4. **Detail-view unification.** Every character detail view uses one base with approval and retire/decease wired correctly, or the buttons are removed where the action isn't supported.
5. **Characterization tests before any change.** For each gameline and step type, record the effect of a GET and a representative POST (DB state and redirect) so the refactor provably changes nothing except the listed bug fixes, which get their own failing-then-passing tests.
6. **PR slicing:** one step type per PR across all gamelines (e.g. "Languages: 21 → 1"), ordered by payoff and risk. Estimate the line reduction per PR.

## Constraints and scope

- Design only. Don't modify application code.
- Depends on Step 2 (registry and step templates) and Step 0 (permissions). If those designs don't exist yet, state the assumptions you're making about them.
- Out of scope:
  - moving game rules into forms, services or models (Step 4). Where a copy hand-rolls rules, route it through the shared implementation unchanged and leave a pointer for Step 4;
  - template deduplication outside chargen step partials (Step 8);
  - htmx (Step 10).
