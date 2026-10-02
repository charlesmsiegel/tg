# Code style

Formatting, linting and import rules, and the Python conventions the codebase follows.
The tools are configured in [`pyproject.toml`](../../../../pyproject.toml) and
[`.pre-commit-config.yaml`](../../../../.pre-commit-config.yaml); the developer guide is
[docs/development/code-style.md](../../../../docs/development/code-style.md).

## Tools

| Tool | Version | Role |
|------|---------|------|
| black | `rev: 25.12.0` in pre-commit (`black>=25.1.0` in `requirements.txt`) | Formatting, `line-length = 100`, `target-version = py310` |
| ruff | `v0.3.4` (`ruff==0.3.4`) | Lint rules `E`, `W`, `F`, `I`, `B`, `C4`, `UP`; `--fix` in pre-commit |
| pre-commit | `3.7.0` | Runs the hooks below on commit |

Pre-commit also runs `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`,
`check-added-large-files` and `check-merge-conflict`.

```bash
pre-commit install           # once per clone
pre-commit run --all-files   # before pushing
ruff check .                 # lint only
black --check .              # formatting only
```

## Rules

- **Ruff is the only import sorter** (the `I` rules). Do not add isort, or reorder imports
  by hand against it. Order: standard library, third party, then project apps (`accounts`,
  `characters`, `core`, `game`, `items`, `locations`, `widgets`, ...), each block
  alphabetical.
- **Keep ruff clean repo-wide.** The application code has no ruff findings; a change adds
  none. Do not add `# noqa` without a rule code and a reason.
- `E501` is ignored (black handles length) and so is `B008`. `populate_db/**` may use
  `E402` because each data script imports others mid-file on purpose to set load order.
- black and ruff both exclude directories named `migrations`, which includes
  `tg_schema/migrations/`. Format those files by hand in the same style.
- Settings modules use star imports with `# noqa: F403, F401` / `F405`; nowhere else.

## Python conventions

- Target Python 3.10+ syntax (`X | None`, `match` is allowed, `list[str]`); ruff's `UP`
  rules rewrite older forms.
- Module docstrings say what the module is for; class and function docstrings state
  contracts, not history. No commented-out code.
- Every import is at module top; no imports inside functions or methods. The
  module-level import graph is acyclic, and a change that needs a cycle restructures
  instead: name a related model by string (`"game.Chronicle"`), use the reverse accessor
  (`self.rote_set`, `self.model.group_set.through`) or the field's `related_model`, look a
  model up with `django.apps.apps.get_model()` at call time, or move the rule into a service
  that imports both sides. The only imports inside a function are the signal registrations
  in `AppConfig.ready()`, which Django requires, and optional-dependency guards such as
  `debug_toolbar` and Playwright.
- Use `logging.getLogger(__name__)`; the per-app loggers are configured in
  `tg/settings/base.py`. No `print()` in application code; management commands write to
  `self.stdout` / `self.stderr`.
- Constants in `UPPER_CASE` at module level; choices from `core.constants` or settings.
- `f`-strings for formatting, except `str.format` templates such as
  `success_message = "Clan '{name}' created"` that `MessageMixin` fills later.

## Checklist

- [ ] `pre-commit run --all-files` passes.
- [ ] `ruff check .` clean; no new blanket `noqa`.
- [ ] Imports sorted by ruff; none inside a function (except `AppConfig.ready()` signal
  registration and optional-dependency guards).
- [ ] `tg_schema` migrations formatted by hand to black style.

## See also

- [docs/development/code-style.md](../../../../docs/development/code-style.md)
- [`pyproject.toml`](../../../../pyproject.toml), [`.pre-commit-config.yaml`](../../../../.pre-commit-config.yaml)
- [testing.md](testing.md)
