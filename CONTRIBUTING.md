# Contributing

This page is for anyone proposing a change to Tellurium Games, human or agent. It covers
setting up, the rules a change must follow, and how a pull request is reviewed. Coding agents
should also read [`AGENTS.md`](AGENTS.md).

## Set up

Follow [Installation](docs/getting-started/installation.md) and
[Local development](docs/getting-started/local-development.md). Then install the git hooks:

```bash
pre-commit install
```

The hooks run black and ruff (and a few file hygiene checks) on every commit. The versions
they use are pinned in [`.pre-commit-config.yaml`](.pre-commit-config.yaml); see
[Code style](docs/development/code-style.md).

## Before you write code

- Read the README and `docs/` of the app you are changing, and the architecture page for the
  area ([`docs/README.md`](docs/README.md) lists them).
- Read the [`tg-standards`](.claude/skills/tg-standards/SKILL.md) rules for the kind of change
  you are making. They are short, and each names the test that enforces it.
- For a new model, character type, item or location type, reference data, view or schema
  change, follow the matching [guide](docs/README.md#guides).

## Making the change

- **Keep it focused.** One concern per pull request; split unrelated fixes out.
- **Schema changes** reach existing databases only through a guarded migration in
  [`tg_schema/`](tg_schema/README.md). Never commit migration files for the local apps. See
  [Changing the schema](docs/guides/changing-the-schema.md).
- **Every new route** needs exactly one access policy; the route-policy tests fail otherwise.
  See [Authorization](docs/architecture/authorization.md).
- **Templates** use the Spread design system; the template policy test rejects inline styles.
  See [Front end](docs/architecture/frontend.md).
- **Tests** go next to the code they cover, in `<app>/tests/`, mirroring the source path. Add a
  test for each behaviour and a denial test for each new route. Change a guard file (query
  ceilings, template policy, route policies, field baselines) only on purpose, and say why in
  the commit. See [Testing](docs/development/testing.md).
- **Documentation** changes with the code: update the app docs, the guides and the reference
  pages your change affects in the same pull request.

## Commits

- Imperative subject line, under about 70 characters ("Lock the character when a spending
  request is decided").
- A body that explains why the change is needed and anything a reviewer would not see from
  the diff.
- Keep the branch history linear: rebase on `main` or cherry-pick; do not merge `main` into
  a feature branch.

## Before opening a pull request

```bash
python manage.py check
python manage.py test --parallel 4
pre-commit run --all-files
```

The full suite must pass, including the browser tests if you touched front-end behaviour
(set `TG_BROWSER_BINARY`; see [Testing](docs/development/testing.md)). Open the pull request
only when the branch is complete.

In the description, say what changed and why, list any behaviour change, schema change or
new setting, and say how you tested it.

## Review

Pull requests get automated reviews (the Claude review workflow in
[`.github/workflows/`](.github/workflows/), and Codex when requested). Treat each finding as a
bug report: fix it, or reply with why it does not apply. A maintainer merges; the project uses
rebase merges, so every commit on the branch lands on `main`.

## Reporting bugs and security issues

Open bugs and feature requests as [GitHub Issues](https://github.com/charlesmsiegel/tg/issues).
Do not report security problems in public issues; follow [`SECURITY.md`](SECURITY.md).
