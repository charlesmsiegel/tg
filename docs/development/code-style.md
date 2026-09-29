# Code style

This page lists the formatting and lint tools the repository uses and how they are
configured, the naming and module conventions the code follows, and how commit messages
are written. It is for anyone about to change code here, human or agent. Template and
CSS conventions are in [Front end](../architecture/frontend.md).

## Tools at a glance

| Tool | Version | Configured in | Enforced by |
|------|---------|---------------|-------------|
| black | hook pinned to `25.12.0`; `requirements.txt` asks for `black>=25.1.0` | `[tool.black]` in [`pyproject.toml`](../../pyproject.toml) | pre-commit |
| ruff | `0.3.4` (hook `v0.3.4`, `requirements.txt` `ruff==0.3.4`) | `[tool.ruff]` and `[tool.ruff.lint]` in `pyproject.toml` | pre-commit (`ruff --fix`) |
| pre-commit | `3.7.0` | [`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) | your local git hook |
| djlint | `1.36.4` | not configured | nothing: installed by `requirements.txt` but not in pre-commit |

No CI workflow runs formatters, linters or tests: the two GitHub workflows in
`.github/workflows/` run Claude code review. Run the checks yourself before you commit.

## Python version

Target Python 3.10. `pyproject.toml` sets `target-version` to `py310` for black and
ruff, the black hook runs under `python3.10`, and
[`requirements.txt`](../../requirements.txt) notes that environments should use 3.10.
You may use 3.10 syntax such as `X | Y` in `isinstance` checks and `match`, but nothing
newer.

## black

```toml
[tool.black]
line-length = 100
target-version = ['py310']
```

`exclude` skips `.conda`, `.git`, `.vscode`, `migrations` and `__pycache__` directories,
so generated migration files are never reformatted. Run it on the whole tree with
`black .`, or let the pre-commit hook run it on staged files.

## ruff

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["E501", "B008"]

[tool.ruff.lint.per-file-ignores]
"populate_db/**" = ["E402"]
```

| Rule set | What it covers |
|----------|----------------|
| `E`, `W` | pycodestyle errors and warnings. `E501` (line length) is ignored because black owns line length. |
| `F` | Pyflakes: unused imports and variables, undefined names. |
| `I` | Import sorting (isort rules). **ruff is the only import sorter**; do not add isort or another tool. The hook's `--fix` sorts imports for you. |
| `B` | flake8-bugbear. `B008` (function calls in argument defaults) is ignored. |
| `C4` | flake8-comprehensions. |
| `UP` | pyupgrade, towards Python 3.10 syntax. |

`populate_db/**` may import mid-file (`E402`) because each import of another data
script runs that script, so the position of the import is the load order (see
[Seed data](../getting-started/seed-data.md#scripts-that-import-other-scripts)). Other
intentional exceptions are marked inline with `# noqa: <code>`, for example the star
imports in `tg/settings/development.py` and `production.py` (`F403`, `F405`) and the
routing import in `tg/asgi.py` that must follow `get_asgi_application()` (`E402`).

The same directories as black are excluded. Run `ruff check .` to lint and
`ruff check --fix .` to apply safe fixes.

[`pyproject.toml`](../../pyproject.toml) is tracked in git even though `.gitignore`
lists it; git ignores only untracked files, so your edits to it show up as normal
changes.

## pre-commit

```bash
pre-commit install          # once per clone: installs the git hook
pre-commit run --all-files  # run every hook over the whole tree
```

[`.pre-commit-config.yaml`](../../.pre-commit-config.yaml) runs, in order:

1. From `pre-commit-hooks` `v4.5.0`: `trailing-whitespace`, `end-of-file-fixer`,
   `check-yaml`, `check-added-large-files`, `check-merge-conflict`.
2. `black` `25.12.0` (with `language_version: python3.10`, so pre-commit needs a
   `python3.10` interpreter on `PATH` to build the hook environment).
3. `ruff` `v0.3.4` with `--fix`.

When a hook modifies files the commit stops; review the changes, stage them and commit
again.

## Templates

djlint is installed but has no configuration and no hook, so template formatting is not
checked automatically. What is checked is the template policy in
[`core/tests/test_template_policy.py`](../../core/tests/test_template_policy.py): no new
inline `style="..."` attributes, no new `<style>` blocks and a maximum `{% extends %}`
depth. See [Testing](testing.md#guard-tests) and [Front end](../architecture/frontend.md).

## Conventions in the code

These are the patterns the code follows; match them in new code.

### Layout by gameline

`characters`, `items` and `locations` split models, forms, views, URLs, templates and
tests into one subpackage per gameline, plus `core` for shared bases:

```text
characters/models/<gameline>/<model>.py
characters/forms/<gameline>/<model>.py
characters/views/<gameline>/<model>.py        (+ <model>_chargen.py for creation workflows)
characters/urls/<gameline>/...
characters/templates/characters/<gameline>/<model>/detail.html, form.html, list.html
characters/tests/<models|forms|views>/<gameline>/test_<model>.py
```

Gameline directory names are `core`, `vampire`, `werewolf`, `mage`, `wraith`,
`changeling`, `demon`, `mummy` and `hunter`. Not every app has every gameline in every
layer.

### Modules and names

- One main model per module; the module is the model's name in lower case
  (`characters/models/vampire/clan.py` holds `VampireClan`,
  `characters/models/werewolf/garou.py` holds `Werewolf`). Multi-word names are
  sometimes joined (`battlescar.py`, `renownincident.py`, `wtahuman.py`) and sometimes
  snake_case (`spirit_character.py`, `merit_flaw_block.py`); follow the neighbouring
  files.
- Test modules are `test_<module>.py` in the mirrored test directory.
- Classes are `CamelCase`, functions and variables `snake_case`, module-level constants
  `UPPER_CASE`.
- Loggers are module-level: `logger = logging.getLogger(__name__)`. Loggers under the
  project apps are routed by the logging configuration (see the
  [Settings reference](../reference/settings.md#logging)).

### Shared values

- Gameline codes and names come from `settings.GAMELINES` and `settings.GAMELINE_CHOICES`
  ([Configuration](../getting-started/configuration.md#project-specific-settings)), never
  hard-coded lists.
- Status and other choice values come from [`core/constants.py`](../../core/constants.py)
  (`CharacterStatus`, `ImageStatus`, `XPApprovalStatus`, `GameLine`, `HeadingChoices`,
  `ThemeChoices`, `ObjectTypeChoices`, `AbilityFields`).
- View mixins are imported from `core.mixins`. See [Adding a view](../guides/adding-a-view.md).
- Use `get_object_or_404()` in views, and `select_related()` / `prefetch_related()` for
  anything a template iterates; the query budgets in
  [`core/tests/test_query_budgets.py`](../../core/tests/test_query_budgets.py) catch
  regressions on the main pages.

### Comments and docstrings

Module and class docstrings say what the code is for and, where a rule is not obvious,
why it exists (see `tg_schema/schema.py` or `core/tests/test_query_budgets.py`). Write
comments about the reason for the code, not a restatement of it.

## Commit messages

The history follows one style:

- **Subject**: one line stating the change or the behaviour that results, in plain
  English, sentence case, no trailing period and no type prefix (`feat:`, `fix:`).
  Imperative or descriptive present tense are both used:
  - `Make ruff the only import sorter`
  - `Never cache a request with a query string`
  - `One scene read status per user and scene`
  - `Anonymous visitors share one cached copy of a page`
- **Body**: after a blank line, wrapped at about 80 columns, explaining **why**: the bug
  or risk the change addresses, what was wrong before, and anything a reviewer needs to
  trust it (tests added, rules pinned). A pure formatting commit says so
  (`Formatting only.`).
- When a change touches a guard test's ceiling, allowlist or baseline, the body gives the
  reason.
- Trailers such as `Co-Authored-By:` go at the end, after a blank line.

Example from the history:

```text
tg_schema 0008 skips a table whose columns were renamed

Like the other migrations, it no longer fails migrate if a later release
renames the table or one of the columns it reads.
```

Commit on a branch, not directly on `main`.

## See also

- [Testing](testing.md)
- [Front end](../architecture/frontend.md)
- [Adding a view](../guides/adding-a-view.md)
- [Seed data](../getting-started/seed-data.md)
- [`CONTRIBUTING.md`](../../CONTRIBUTING.md)
