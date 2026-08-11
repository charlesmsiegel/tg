# Explicit Package Exports Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every intentional package re-export explicit and remove the repository-wide Ruff `F401` exemption for `__init__.py` files.

**Architecture:** Treat `__init__.py` files as one of three kinds: package markers, executable framework modules, or public API aggregators. Add `__all__` only to aggregators, delete demonstrably accidental imports from executable URL modules, retain narrowly justified side-effect suppressions, and let Ruff enforce the distinction thereafter.

**Tech Stack:** Python 3.10+, Django 5.1, Ruff, pytest/Django test runner, Python `compileall`.

## Global Constraints

- Preserve existing runtime behavior and intentional package-level APIs.
- Keep empty and documentation-only initializers unchanged.
- Do not expose implementation imports used by Django URL or settings logic.
- Use `# noqa: F401` only for a documented import-time side effect that is not an API export.
- Do not install Ruff or any other dependency without explicit user approval.
- Do not modify the pre-existing untracked documentation or `online_game.sqlite3:Zone.Identifier` metadata file.
- In every new `__all__`, list imported binding names in source-import order; retain the ordering style of an existing `__all__`.

---

### Task 1: Shared packages and accidental URL imports

**Files:**
- Modify: `core/forms/__init__.py`
- Modify: `core/middleware/__init__.py`
- Modify: `core/views/__init__.py`
- Modify: `core/widgets/__init__.py`
- Modify: `characters/urls/changeling/__init__.py`
- Modify: `characters/urls/mage/__init__.py`
- Modify: `characters/urls/vampire/__init__.py`
- Modify: `characters/urls/werewolf/__init__.py`
- Modify: `characters/urls/wraith/__init__.py`
- Modify: `items/urls/mage/__init__.py`
- Modify: `items/urls/mummy/__init__.py`
- Modify: `items/urls/werewolf/__init__.py`
- Modify: `locations/urls/mummy/__init__.py`
- Modify: `locations/urls/werewolf/__init__.py`

**Interfaces:**
- Consumes: Existing imported forms, middleware, views, and widgets.
- Produces: Explicit package APIs for `core.forms`, `core.middleware`, `core.views`, and `core.widgets`; unchanged URL pattern behavior without unused cross-app `views` bindings.

- [ ] **Step 1: Establish the failing lint baseline**

Run, after obtaining approval to install Ruff if `python -m ruff` is unavailable:

```powershell
python -m ruff check core characters/urls items/urls locations/urls --select F401 --config "lint.per-file-ignores = {}"
```

Expected: FAIL with `F401` findings in the four shared aggregator files and the ten URL initializers listed above.

- [ ] **Step 2: Add explicit shared-package exports**

Append literal `__all__` lists containing every imported binding that is intentionally available from each package. For example, `core/forms/__init__.py` becomes:

```python
from .language import HumanLanguageForm

__all__ = ["HumanLanguageForm"]
```

Apply the same literal-list pattern to `UserListMiddleware`, all imported `core.views` names (including the `generic` module), and the five imported `core.widgets` names. Do not export Django or other third-party helper imports.

- [ ] **Step 3: Delete genuinely unused URL imports**

Delete only these ten statements; their bound `views` modules are never referenced by the corresponding `urls` lists:

```python
from characters import views  # five character URL initializers and two item/location werewolf initializers
from items import views       # items/urls/mummy/__init__.py
from locations import views   # locations/urls/mummy/__init__.py
```

Also delete the unused `from characters import views` in `items/urls/mage/__init__.py`. Preserve every `include`, `path`, local URL-module import, `urls` declaration, route, and namespace.

- [ ] **Step 4: Verify the task**

```powershell
python -m ruff check core characters/urls items/urls locations/urls --select F401 --config "lint.per-file-ignores = {}"
python manage.py check
```

Expected: Ruff reports no `F401` in the files modified by this task; Django reports no system-check issues introduced by the changes.

- [ ] **Step 5: Commit**

```powershell
git add core/forms/__init__.py core/middleware/__init__.py core/views/__init__.py core/widgets/__init__.py characters/urls items/urls locations/urls
git commit -m "refactor: make shared package exports explicit"
```

### Task 2: Character form and model exports

**Files:**
- Modify: `characters/forms/__init__.py`
- Modify: `characters/forms/changeling/__init__.py`
- Modify: `characters/forms/core/__init__.py`
- Modify: `characters/forms/mage/__init__.py`
- Modify: `characters/forms/vampire/__init__.py`
- Modify: `characters/forms/werewolf/__init__.py`
- Modify: `characters/forms/wraith/__init__.py`
- Modify: `characters/models/__init__.py`
- Modify: `characters/models/changeling/__init__.py`
- Modify: `characters/models/core/__init__.py`
- Modify: `characters/models/demon/__init__.py`
- Modify: `characters/models/hunter/__init__.py`
- Modify: `characters/models/mage/__init__.py`
- Modify: `characters/models/vampire/__init__.py`
- Modify: `characters/models/werewolf/__init__.py`
- Modify: `characters/models/wraith/__init__.py`
- Audit only: `characters/forms/mummy/__init__.py`
- Audit only: `characters/models/mummy/__init__.py`

**Interfaces:**
- Consumes: Existing character form/model imports and the established package import paths used throughout Django.
- Produces: Literal `__all__` declarations matching every intentional form and model re-export.

- [ ] **Step 1: Demonstrate the character-package failures**

```powershell
python -m ruff check characters/forms characters/models --select F401 --config "lint.per-file-ignores = {}"
```

Expected: FAIL in initializers without `__all__`; existing Mummy declarations remain the reference style.

- [ ] **Step 2: Add form exports**

For every form initializer in the Files list, append a literal `__all__` containing exactly the local names bound by its `from ... import ...` and `from . import ...` statements. The parent package must export its imported modules:

```python
from . import core, mage

__all__ = ["core", "mage"]
```

Preserve all existing import statements and symbol names. Confirm the existing Mummy form list contains all four imported forms and change it only if the audit finds a mismatch.

- [ ] **Step 3: Add model exports**

For every model initializer in the Files list, append a literal `__all__` containing every imported model, rating/helper model, and imported gameline module in source-import order. The top-level `characters.models` list must include its eleven imported gameline/core modules. Confirm the existing Mummy model list matches its four imports and change it only if needed.

- [ ] **Step 4: Verify character form/model imports**

```powershell
python -m ruff check characters/forms characters/models --select F401 --config "lint.per-file-ignores = {}"
python manage.py check
python manage.py test characters.tests.forms characters.tests.models --keepdb
```

Expected: Ruff is clean for both trees, Django imports every model, and the form/model tests pass.

- [ ] **Step 5: Commit**

```powershell
git add characters/forms characters/models
git commit -m "refactor: declare character form and model exports"
```

### Task 3: Character view exports

**Files:**
- Modify: `characters/views/__init__.py`
- Modify: `characters/views/changeling/__init__.py`
- Modify: `characters/views/core/__init__.py`
- Modify: `characters/views/demon/__init__.py`
- Modify: `characters/views/hunter/__init__.py`
- Modify: `characters/views/mage/__init__.py`
- Modify: `characters/views/vampire/__init__.py`
- Modify: `characters/views/werewolf/__init__.py`
- Modify: `characters/views/wraith/__init__.py`
- Audit only: `characters/views/mummy/__init__.py`

**Interfaces:**
- Consumes: Existing class/function/module imports from character view modules.
- Produces: Explicit public view APIs without changing Django view classes or URL resolution.

- [ ] **Step 1: Demonstrate the view-package failures**

```powershell
python -m ruff check characters/views --select F401 --config "lint.per-file-ignores = {}"
```

Expected: FAIL for imported modules and view classes not covered by `__all__`.

- [ ] **Step 2: Add the literal view export lists**

Add `__all__` to each listed initializer. Include every imported local name, including the nine gameline/core modules in `characters/views/__init__.py`, and preserve source-import order. Do not add aliases, wildcard imports, or dynamic `globals()`-based lists. Audit the existing Mummy list against all sixteen imported view classes.

The top-level declaration has this exact module shape:

```python
__all__ = [
    "changeling",
    "core",
    "demon",
    "hunter",
    "mage",
    "mummy",
    "vampire",
    "werewolf",
    "wraith",
]
```

- [ ] **Step 3: Verify character views**

```powershell
python -m ruff check characters/views --select F401 --config "lint.per-file-ignores = {}"
python manage.py check
python manage.py test characters.tests.views --keepdb
```

Expected: Ruff is clean, Django checks succeed, and character view tests pass.

- [ ] **Step 4: Commit**

```powershell
git add characters/views
git commit -m "refactor: declare character view exports"
```

### Task 4: Item package exports

**Files:**
- Modify: `items/forms/__init__.py`
- Modify: `items/forms/core/__init__.py`
- Modify: `items/forms/mage/__init__.py`
- Modify: `items/models/__init__.py`
- Modify: `items/models/core/__init__.py`
- Modify: `items/models/demon/__init__.py`
- Modify: `items/models/hunter/__init__.py`
- Modify: `items/models/mage/__init__.py`
- Modify: `items/models/vampire/__init__.py`
- Modify: `items/models/werewolf/__init__.py`
- Modify: `items/models/wraith/__init__.py`
- Modify: `items/views/__init__.py`
- Modify: `items/views/core/__init__.py`
- Modify: `items/views/demon/__init__.py`
- Modify: `items/views/hunter/__init__.py`
- Modify: `items/views/mage/__init__.py`
- Modify: `items/views/werewolf/__init__.py`
- Audit only: `items/forms/vampire/__init__.py`
- Audit only: `items/models/changeling/__init__.py`
- Audit only: `items/models/mummy/__init__.py`

**Interfaces:**
- Consumes: Existing item form, model, view, and module imports.
- Produces: Explicit `items` subpackage APIs with unchanged object identities and import paths.

- [ ] **Step 1: Demonstrate the item-package failures**

```powershell
python -m ruff check items/forms items/models items/views --select F401 --config "lint.per-file-ignores = {}"
```

Expected: FAIL in initializers lacking complete export declarations.

- [ ] **Step 2: Add item exports**

Append literal `__all__` declarations to every Modify file. Each list contains exactly the bindings introduced by its imports, in import order; parent-package module imports use their local module names. Audit the three existing declarations and alter them only when an imported binding is absent or a non-imported binding is present.

For `items/forms/__init__.py`, the exact declaration is:

```python
__all__ = ["core", "mage", "vampire"]
```

- [ ] **Step 3: Verify item packages**

```powershell
python -m ruff check items/forms items/models items/views --select F401 --config "lint.per-file-ignores = {}"
python manage.py check
python manage.py test items.tests.forms items.tests.models items.tests.views --keepdb
```

Expected: Ruff is clean, Django checks succeed, and item form/model/view tests pass.

- [ ] **Step 4: Commit**

```powershell
git add items/forms items/models items/views
git commit -m "refactor: declare item package exports"
```

### Task 5: Location package exports

**Files:**
- Modify: `locations/forms/__init__.py`
- Modify: `locations/forms/changeling/__init__.py`
- Modify: `locations/forms/core/__init__.py`
- Modify: `locations/forms/mage/__init__.py`
- Modify: `locations/models/__init__.py`
- Modify: `locations/models/changeling/__init__.py`
- Modify: `locations/models/core/__init__.py`
- Modify: `locations/models/hunter/__init__.py`
- Modify: `locations/models/mage/__init__.py`
- Modify: `locations/models/vampire/__init__.py`
- Modify: `locations/models/werewolf/__init__.py`
- Modify: `locations/models/wraith/__init__.py`
- Modify: `locations/views/__init__.py`
- Modify: `locations/views/changeling/__init__.py`
- Modify: `locations/views/core/__init__.py`
- Modify: `locations/views/demon/__init__.py`
- Modify: `locations/views/hunter/__init__.py`
- Modify: `locations/views/mage/__init__.py`
- Modify: `locations/views/werewolf/__init__.py`
- Modify: `locations/views/wraith/__init__.py`
- Audit only: `locations/models/demon/__init__.py`
- Audit only: `locations/models/mummy/__init__.py`

**Interfaces:**
- Consumes: Existing location form, model, view, and module imports.
- Produces: Explicit `locations` subpackage APIs without changing URL configuration or model discovery.

- [ ] **Step 1: Demonstrate the location-package failures**

```powershell
python -m ruff check locations/forms locations/models locations/views --select F401 --config "lint.per-file-ignores = {}"
```

Expected: FAIL in initializers lacking complete export declarations.

- [ ] **Step 2: Add location exports**

Append literal `__all__` declarations to every Modify file. Include exactly the imported local names in source-import order, including module names in parent aggregators. Audit the two existing model declarations and change them only for a demonstrated mismatch.

For `locations/forms/__init__.py`, the exact declaration is:

```python
__all__ = ["core", "mage"]
```

- [ ] **Step 3: Verify location packages**

```powershell
python -m ruff check locations/forms locations/models locations/views --select F401 --config "lint.per-file-ignores = {}"
python manage.py check
python manage.py test locations.tests.forms locations.tests.models locations.tests.views --keepdb
```

Expected: Ruff is clean, Django checks succeed, and location form/model/view tests pass.

- [ ] **Step 4: Commit**

```powershell
git add locations/forms locations/models locations/views
git commit -m "refactor: declare location package exports"
```

### Task 6: Audit side-effect packages and enable the Ruff ratchet

**Files:**
- Modify: `pyproject.toml`
- Audit only: `chained_select/__init__.py`
- Audit only: `characters/managers/__init__.py`
- Audit only: `characters/services/freebie_spending/__init__.py`
- Audit only: `characters/services/xp_spending/__init__.py`
- Audit only: `core/services/__init__.py`
- Audit only: `widgets/__init__.py`
- Audit only: `widgets/fields/__init__.py`
- Audit only: `widgets/mixins/__init__.py`
- Audit only: `widgets/widgets/__init__.py`
- Audit only: `tg/settings/__init__.py`

**Interfaces:**
- Consumes: All explicit export declarations from Tasks 1-5 and Ruff's `F401` rule.
- Produces: Repository-wide enforcement with only the existing narrowly scoped dynamic-settings suppressions.

- [ ] **Step 1: Audit existing exports and side effects**

Confirm each existing literal `__all__` matches its imported public bindings. In the two spending-service packages, retain service imports and their existing export lists because imports also register implementations. In `tg/settings/__init__.py`, retain:

```python
from .production import *  # noqa: F403, F401
from .development import *  # noqa: F403, F401
```

These conditional wildcard imports implement dynamic Django settings loading and are the justified narrow exception.

- [ ] **Step 2: Establish the final red state**

```powershell
python -m ruff check . --select F401 --config "lint.per-file-ignores = {}"
```

Expected before the configuration edit: no source finding outside excluded directories. If a source finding remains, classify it as an API export, used executable import, accidental import, or documented side effect and resolve it according to the approved design before continuing.

- [ ] **Step 3: Remove the blanket exemption**

Delete this entire now-empty table from `pyproject.toml`:

```toml
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # unused imports in __init__.py are OK
```

- [ ] **Step 4: Run final lint and syntax verification**

```powershell
python -m ruff check .
python -m compileall -q accounts chained_select characters core game items locations populate_db tg widgets
```

Expected: both commands exit successfully with no diagnostics.

- [ ] **Step 5: Run Django and test verification**

```powershell
python manage.py check
python manage.py test --keepdb
```

Expected: Django reports no system-check issues and the full test suite passes.

- [ ] **Step 6: Inspect scope and commit the ratchet**

```powershell
git diff --check
git status --short
git diff -- pyproject.toml "**/__init__.py"
git add pyproject.toml
git commit -m "lint: enforce explicit initializer exports"
```

Expected: the diff contains only `pyproject.toml`, intentional initializer edits from Tasks 1-5, and this task's documentation; unrelated pre-existing untracked files remain untouched.
