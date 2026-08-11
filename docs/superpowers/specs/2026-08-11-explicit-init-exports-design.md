# Explicit Package Exports in Python Initializers

## Goal

Make intentional package-level imports explicit in every Python `__init__.py` file and
remove the repository-wide Ruff `F401` exemption for initializers. Preserve existing
runtime behavior and package APIs.

## Scope

- Review every `__init__.py` file in the repository.
- Add or complete `__all__` where imports intentionally re-export modules, classes,
  functions, constants, or other names.
- Keep empty package markers and documentation-only initializers unchanged.
- Keep imports that are consumed by executable initializer logic unchanged.
- Use a narrow `# noqa: F401` only when an import exists solely for registration or
  another import-time side effect and is not part of the public API.
- Remove the `"__init__.py" = ["F401"]` entry from Ruff's per-file ignores.

## Public API Preservation

For a re-exporting initializer, `__all__` will contain the names intentionally made
available from that package. Existing `__all__` declarations will be retained and
checked against their imports. No imported object will be renamed or moved.

Initializers that define runtime values such as Django `urls`, `urlpatterns`, or
settings will not expose their implementation imports merely to satisfy Ruff. Imports
already referenced by executable code are not unused and need no export declaration.

## Side-Effect Imports

Some service packages import modules to register implementations with a factory. If
the imported names are also supported package-level API, they belong in `__all__`.
Otherwise, the import will receive a local `# noqa: F401` with a concise explanation.
The repository-wide suppression will not be replaced with another broad suppression.

## Verification

1. Run Ruff with `F401` enabled and confirm no initializer violations remain.
2. Compile the affected Python files to catch syntax errors.
3. Run Django's system check to catch import and application-registration failures.
4. Run the relevant test suite, expanding to the full suite when practical.
5. Inspect the final diff to confirm only intentional initializers, Ruff configuration,
   and task documentation changed.

## Non-Goals

- Refactoring package layouts or resolving unrelated import cycles.
- Changing which Django models, views, forms, or services are implemented.
- Editing empty marker files solely for consistency.
- Modifying unrelated untracked documentation or database metadata.
