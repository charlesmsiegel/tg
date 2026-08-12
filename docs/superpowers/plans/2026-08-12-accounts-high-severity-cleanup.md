# Accounts High-Severity Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the remaining accounts high-severity health records by fixing multipart password-reset email behavior, correcting detector false positives, and extracting profile-dashboard responsibilities without changing user-visible behavior.

**Architecture:** `accounts.context_processors` remains the HTTP/cache adapter while a new `ProfileDashboard` owns dashboard queries and notification aggregation. Existing `Profile` query methods remain compatibility adapters during this campaign. Canonical detector fixes live in `coding-skills` and are reinstalled before generated health pages are rebuilt.

**Tech Stack:** Python 3.14 test runner for skills, project Python/Django 5.2 virtualenv, Django `TestCase`, locmem email backend, Ruff, code-overview.

## Global Constraints

- Pause before every commit containing application, detector, test-refactor, or generated-report changes; show the diff and fresh verification evidence.
- Documentation-only spec and plan commits do not require a pause.
- Use TDD for every behavior or detector change and record the intended RED failure.
- Preserve the existing 60-second notification cache and fail-soft context-processor contract.
- Keep existing `Profile` public methods as forwarding adapters.
- Do not hand-edit generated HTML.

---

### Task 1: Send safe multipart password-reset email

**Files:**
- Modify: `accounts/views.py`
- Modify: `accounts/urls.py`
- Modify: `accounts/templates/registration/password_reset_email.html`
- Create: `accounts/tests/views/test_password_reset.py`

**Interfaces:**
- Produces: `CustomPasswordResetView(PasswordResetView)` with `email_template_name = "registration/password_reset_email.txt"` and `html_email_template_name = "registration/password_reset_email.html"`.
- Preserves: the public `/accounts/password_reset/` URL and global `password_reset` route name from Django auth URLs.

- [ ] **Step 1: Write the failing end-to-end email test**

Create an active user whose username is `<b>Unsafe Name</b>`, post its email to `reverse("password_reset")`, and assert:

```python
message = mail.outbox[0]
assert message.body.startswith("Password Reset Request")
assert "<b>Unsafe Name</b>" in message.body
assert message.alternatives[0].mimetype == "text/html"
assert "&lt;b&gt;Unsafe Name&lt;/b&gt;" in message.alternatives[0].content
assert "/accounts/reset/" in message.body
assert "/accounts/reset/" in message.alternatives[0].content
```

The production change that makes this pass is configuring the Django view to render separate text and HTML templates and enabling escaping in the HTML template.

- [ ] **Step 2: Verify RED**

Run:

```powershell
& .\.venv\Scripts\python.exe manage.py test accounts.tests.views.test_password_reset --keepdb --verbosity 2
```

Expected: failure because the stock view sends the `.html` template as the text body and attaches no HTML alternative.

- [ ] **Step 3: Implement the minimal multipart view**

Subclass `PasswordResetView` in `accounts/views.py`, set the two template attributes, and add `password_reset/` to `accounts.urls` before the remaining account patterns. Remove `{% autoescape off %}` and `{% endautoescape %}` only from the HTML template.

- [ ] **Step 4: Verify GREEN and affected behavior**

Run the new test, all accounts view tests, `manage.py check`, and focused Ruff over the four changed files.

- [ ] **Step 5: Pause before commit**

Show the exact diff and verification results. Commit only after approval:

```bash
git commit -m "fix: send escaped multipart password reset email"
```

---

### Task 2: Correct high-severity detector false positives

**Files in `C:\Users\charl\github\coding-skills`:**
- Modify: `skills/python-code-doctor/scripts/find_mutation_hazards.py`
- Modify: `skills/python-code-doctor/scripts/find_dead_code.py`
- Modify: `skills/django-code-doctor/scripts/find_django_security.py`
- Modify: focused tests under `tests/python_code_doctor/` and `tests/django_code_doctor/`

**Interfaces:**
- Produces: Django declarative configuration is not a mutable-state defect; intentional `AppConfig.ready()` registration imports and `# noqa: F401` imports are not unused; autoescape-off in `.txt` templates is not an HTML security finding.
- Preserves: ordinary mutable class attributes, unused imports, and HTML autoescape blocks remain detectable.

- [ ] **Step 1: Add paired RED fixtures**

For every correction, pair a clean Django case with a defect that must remain:

```python
class PostOnlyView(View):
    http_method_names = ["post"]       # clean Django configuration

class Bag:
    values = []                         # still a mutable-state finding
```

Also cover `ModelForm.Meta.fields`, `import accounts.signals  # noqa: F401` inside `ready()`, an ordinary unused import, `.txt` autoescape off, and `.html` autoescape off.

- [ ] **Step 2: Verify RED**

Run only the new tests and confirm each clean fixture is incorrectly reported while each control is reported.

- [ ] **Step 3: Implement narrow context-aware rules**

Use AST ancestry/base names for Django declarations rather than filename ignores. Honor exact F401 suppression and registration-import context without globally disabling unused-import reporting. Gate autoescape security findings to HTML-like template suffixes.

- [ ] **Step 4: Verify affected skill suites**

Run:

```powershell
& C:\Python314\python.exe -m pytest tests/python_code_doctor tests/django_code_doctor -q
& C:\Python314\python.exe -m ruff check skills/python-code-doctor skills/django-code-doctor tests/python_code_doctor tests/django_code_doctor
```

Then run `bash ./install.sh --codex`, hash-compare both installed payloads with canonical source, and rerun the installed detectors against `tg`.

- [ ] **Step 5: Pause before commit**

Show detector count changes and the diff. Commit only after approval:

```bash
git commit -m "fix: recognize Django declarative configuration"
```

---

### Task 3: Extract notification aggregation from the context processor

**Files:**
- Create: `accounts/dashboard.py`
- Modify: `accounts/context_processors.py`
- Modify: `accounts/tests/context_processors/test_context_processors.py`
- Create: `accounts/tests/test_dashboard.py`

**Interfaces:**
- Produces: `ProfileDashboard(profile)` and `ProfileDashboard.notification_context() -> dict[str, object]`.
- Context contract: `{"notification_count": int, "notification_breakdown": dict[str, int]}`.
- `notification_count(request)` continues to own authentication, cache key `notification_count_<user id>`, cache duration `60`, logging, and fail-soft fallback.

- [ ] **Step 1: Add characterization tests**

Add a mixed player/ST scenario asserting exact labels and total, a cache-hit test proving aggregation is not called twice, and direct dashboard tests for positive-count inclusion and zero-count omission.

- [ ] **Step 2: Verify RED for the new interface**

The direct `ProfileDashboard` tests must fail because the class does not exist.

- [ ] **Step 3: Implement aggregation helpers**

Use a small `_add_count(breakdown, label, value)` helper and separate player/ST methods. Do not change labels, query methods, or exception behavior in this task.

- [ ] **Step 4: Verify behavior and complexity**

Run both dashboard/context-processor modules, all accounts tests, Ruff, and the complexity detector focused on `accounts/context_processors.py`.

- [ ] **Step 5: Pause before commit**

Show exact output and commit only after approval:

```bash
git commit -m "refactor: extract profile notification dashboard"
```

---

### Task 4: Move profile dashboard queries behind one selector

**Files:**
- Modify: `accounts/dashboard.py`
- Modify: `accounts/models.py`
- Modify: `accounts/tests/models/test_models.py`
- Modify: `accounts/tests/test_dashboard.py`

**Interfaces:**
- Produces: `Profile.dashboard -> ProfileDashboard` and dashboard methods corresponding to all existing profile page selectors.
- Private helpers: `_owned(model)`, `_pending_approval(model)`, and `_pending_image(model)` implement the three model-family query recipes once.
- Existing methods such as `Profile.my_characters()` and `Profile.character_images_to_approve()` remain public forwarding adapters.

- [ ] **Step 1: Add direct-selector and compatibility tests**

For characters, items, and locations, assert direct dashboard methods and legacy Profile methods return identical primary-key sets. Retain the existing zero-query template cache tests for approval relations.

- [ ] **Step 2: Verify RED**

Direct selector calls fail until the dashboard interface exists.

- [ ] **Step 3: Move query construction and add forwarders**

Move dashboard-only query logic without changing queryset ordering, `select_related`, `prefetch_related`, `distinct`, or return container type. Keep validation, authorization, `__str__`, and URL behavior on `Profile`.

- [ ] **Step 4: Verify models, context processors, and query counts**

Run accounts model/context/dashboard tests, then the complete accounts suite, `manage.py check`, Ruff, and the duplicate/low-cohesion detectors.

- [ ] **Step 5: Pause before commit**

Show the compatibility proof and commit only after approval:

```bash
git commit -m "refactor: centralize profile dashboard queries"
```

---

### Task 5: Consolidate repeated authorization tests

**Files:**
- Modify: `accounts/tests/views/test_profile_actions.py`
- Modify: `accounts/tests/views/test_views.py`

**Interfaces:**
- Produces no production interface.
- Preserves distinct coverage for invalid object types, nonexistent objects, profile owner access, other-user denial, staff access, and unauthenticated access.

- [ ] **Step 1: Record the existing focused test baseline**

Run the two modules before editing and record the test count.

- [ ] **Step 2: Parameterize equivalent cases**

Use `subTest()` for invalid/nonexistent route cases and a small shared setup mixin for profile owner/staff fixtures. Keep separate test methods where access semantics differ.

- [ ] **Step 3: Verify test count and behavior**

Run both modules and all accounts tests. Run the duplicate detector and confirm only the intended test clusters disappear.

- [ ] **Step 4: Pause before commit**

Show the test-only diff and commit only after approval:

```bash
git commit -m "test: consolidate account authorization cases"
```

---

### Task 6: Regenerate affected health artifacts

**Files:**
- Regenerate: `accounts/docs/health.html`
- Regenerate: `accounts/docs/summary.html`
- Regenerate: `docs/health.html`
- Regenerate: `docs/summary.html`
- Navigation injection may mechanically update existing generated HTML navigation blocks.

**Interfaces:**
- Consumes: final installed doctor outputs and `docs/code-overview.json`.
- Produces: internally consistent package and repository health/summary pages.

- [ ] **Step 1: Run doctors once at repository scope**

Use an isolated snapshot without `.conda` and generated docs as analyzer input, then merge code-doctor, Python, and Django outputs.

- [ ] **Step 2: Rebuild only count-dependent pages**

Regenerate accounts and repository health pages, then their summaries. Run navigation injection and `--check` until it reports zero updates.

- [ ] **Step 3: Verify metadata**

Extract `code-health-meta` and report before/after high, total, candidate, category, and score values. Confirm no finding from the six addressed groups remains high unless supported by a concrete failing behavior.

- [ ] **Step 4: Final test and review gates**

Run all accounts tests, Django check, focused application Ruff, both affected skill suites, skill Ruff, installed-payload hashes, and an independent review of all code ranges.

- [ ] **Step 5: Pause before commit**

Show generated diffs and verification results. Commit only after approval:

```bash
git commit -m "docs: refresh account health after cleanup"
```
