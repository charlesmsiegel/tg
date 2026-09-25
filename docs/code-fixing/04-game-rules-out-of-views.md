# Task: Design moving game rules out of views in `tg` (Step 4)

You are designing, **not implementing**, the relocation of game rules (point distributions, freebie and XP costs and spending, validation, derived stats, state transitions) out of Django views and into forms, services and model methods. The repository is `charlesmsiegel/tg`: Django 5.2 with django-polymorphic 4.1, a World of Darkness character manager. After this step, views only orchestrate: bind the form, call a service, respond. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and these skills: `.claude/skills/model-standards/SKILL.md`, `.claude/skills/tg-domain/SKILL.md` (rules vocabulary: freebies, XP, Arete, Spheres, virtues, etc.) and `.claude/skills/tg-testing/SKILL.md`.
- Read `docs/superpowers/specs/` and `docs/superpowers/plans/`. Read the designs for Step 0 (authorization), Step 2 (chargen step registry) and Step 3 (generic chargen steps) if they exist. Write:
  - `docs/superpowers/specs/2026-09-25-game-rules-out-of-views-design.md`
  - `docs/superpowers/plans/2026-09-25-game-rules-out-of-views.md`
- Study the existing service layer first:
  - `characters/services/xp_spending/` and `characters/services/freebie_spending/` (a `base.py` plus one module per gameline, about 7,000 lines, with result objects that have `success`, `message` and `error`);
  - `core/services/approval.py` and `core/services/chronicle_data.py`;
  - `core/xp_utils.py`.
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed.
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## Rules currently embedded in views

**Mage** (`characters/views/mage/mage.py`)
- Module-level XP-cost helpers at `:10-34` (Reported). They duplicate the XP service's cost logic.
- `MageDetailView.post` (`:268-437`, 170 lines) contains a Rote validation ladder of about 15 `if not rote_form.cleaned_data[...]` checks. **Confirmed.**
  - That ladder is duplicated in `MageRoteView.form_valid` (`~:896-974`, Reported).
  - It belongs in `RoteCreationForm.clean()`.
- `MageFocusView.form_valid` (`~:695-738`, Reported): practices must sum to Arete, 2 ability dots per practice dot, and it creates `PracticeRating` rows directly.
- `MageSpheresView.form_valid` (`~:768-787`, Reported): `freebies -= 4` per Arete dot, and appends to `spent_freebies`.

**Validation bypass** (Reported). `form_invalid` calls `form_valid` in `mage.py:~795`, `mage.py:~893`, `companion.py:~499`, `sorcerer.py:~642` and `sorcerer.py:~87`, so invalid input can be saved.

**Hand-rolled freebie math** (Reported). `CompanionFreebiesView.form_valid` (`mage/companion.py:~351-482`) does `freebies -= cost` in 8 branches, with identical if/else branches around `~440-447`, even though `CompanionFreebieSpendingService` exists.

**Distribution checks in views** (Reported):
- attributes: `characters/views/core/human.py:~161-201`;
- abilities: `human.py:~227-247`;
- backgrounds: `characters/views/core/backgrounds.py:~27-46`;
- Changeling arts = 3, realms = 5: `changeling/changeling.py:~352-428`.

**Merit/flaw cost rules written twice** (Reported): 3×|Δ| XP and the −7 flaw cap, in `human.py:~289-328` and `human.py:~415-445`.

**Tribe restrictions keyed on name strings** (Reported): `werewolf/kinfolk.py:~263-372`, e.g. `if tribe_name == "Bone Gnawers"`.

**Derived stats** (Reported). Vampire (`vampire/vampire_chargen.py:~245-256`) computes humanity/path and uses `set_willpower()`, while Demon (`demon/demon_chargen.py:~331`) assigns `willpower` directly.

**Type dispatch in views** (Reported). `werewolf/fera.py` has 48 `isinstance` calls across 5 twelve-way switches. `FeraBreedFactionView.form_valid` (`~:270-317`) is one; `FeraGiftsView.get_context_data` (`~:366-504`, 139 lines) is another. These belong in polymorphic model methods.

**Game app** (`game/views.py`, Reported)
- `ChronicleDetailView.get_context_data` builds about 15 querysets (`~:78-181`); these could move to a selector.
- `WeekListView` counts scenes per week in Python (`~:551-565`).
- `WeeklyXPRequestCreateView.form_valid` saves twice (`~:684-685`).
- `XPSpendingRequestApproveView` (`~:932-965`) marks requests approved without calling the spending service.
- `straighten_quotes` is defined at `game/views.py:~347-386`, and another definition exists at `game/consumers.py:220` (**Confirmed**). Consolidate them into one utility.

**Client-side copies of rules.**
- `characters/core/attribute_block/form.html` has a 232-line validator, and `core/ability_block/validation.html` and `core/background_block/form.html` have their own.
- Recent commits ("align client-side chargen validation with server rules") show these drift and have to be re-synced by hand.

## What the design must deliver

1. **A placement taxonomy** with clear criteria:
   - input validation → `Form.clean()`;
   - state-changing operations (spend, approve, advance) → a service returning a result object;
   - derived values → model methods or properties;
   - read-side aggregation → selectors or QuerySet methods.
2. **A rule-by-rule table:** current location, destination, API signature, and the tests that pin current behaviour. Mark any current behaviour you believe is a rules bug, and don't silently "fix" game rules; list them for the owner.
3. **Cost and limit data.** Say where cost tables and per-gameline limits live so that the server, the forms and any client-side hints read one source. Step 10 will pass limits to the browser as data attributes; design the data source to allow that.
4. **Service conventions:** transaction boundaries, locking (e.g. `select_for_update` for spend and approve), result and error types, and how views map results to messages and redirects. Stay consistent with the existing spending services, or propose a justified change.
5. **Remove validation bypasses.** No `form_invalid → form_valid` calls, no raw `request.POST[...]` where a form exists, and no view-side mutation before validation.
6. **A test strategy:** unit tests for forms and services independent of views, and characterization tests captured before moving each rule.
7. **PR slicing:** a sensible order. Suggestions: consolidate the Rote validation; route Companion freebies through the service; distribution checks; merit/flaw costs; Fera polymorphism; game-app selectors.

## Constraints and scope

- Design only. Don't modify application code.
- Keep game-rule behaviour identical unless you explicitly flag something as a bug for the owner to decide.
- Out of scope:
  - consolidating duplicate view classes (Step 3); you may assume it is done or state your assumptions;
  - splitting multi-action POST handlers into separate endpoints (Step 5), though your services should make those endpoints thin;
  - permission policy (Step 0).
