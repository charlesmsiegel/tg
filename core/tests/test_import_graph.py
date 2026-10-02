"""Guard: every import sits at module scope and the module import graph has no cycles.

A function-level import hides a dependency and usually papers over a circular
import. The project breaks cycles structurally instead (string model references,
reverse accessors, ``apps.get_model`` at call time, or a service that imports both
sides); see ``docs/development/code-style.md``. The only exceptions are the signal
registrations in ``AppConfig.ready()``, which Django requires because the receivers
import models.
"""

import ast
from pathlib import Path

from django.test import SimpleTestCase

ROOT = Path(__file__).resolve().parents[2]
PACKAGES = ("accounts", "characters", "core", "game", "items", "locations", "widgets", "tg")
SKIP_DIRS = {"migrations", "__pycache__"}

# Imports that Django's app loading makes necessary: (file, function, module).
ALLOWED_FUNCTION_IMPORTS = {
    ("accounts/apps.py", "ready", "accounts.signals"),
    ("game/apps.py", "ready", "game.signals"),
}


def project_modules():
    """{dotted module name: path} for every module of the project packages."""
    modules = {}
    for package in PACKAGES:
        for path in (ROOT / package).rglob("*.py"):
            if SKIP_DIRS & set(path.relative_to(ROOT).parts):
                continue
            parts = list(path.relative_to(ROOT).with_suffix("").parts)
            if parts[-1] == "__init__":
                parts.pop()
            modules[".".join(parts)] = path
    return modules


def resolve(name, modules):
    """The project module a dotted name refers to, or None (longest prefix wins)."""
    parts = name.split(".")
    for i in range(len(parts), 0, -1):
        candidate = ".".join(parts[:i])
        if candidate in modules:
            return candidate
    return None


class ImportPlacementTests(SimpleTestCase):
    def test_imports_sit_at_module_scope(self):
        offenders = []

        def visit(node, scope, relative):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Import | ast.ImportFrom):
                    if scope is None:
                        continue
                    imported = {alias.name for alias in child.names}
                    if isinstance(child, ast.ImportFrom):
                        imported = {child.module or ""}
                    if any(
                        (relative, scope.name, name) in ALLOWED_FUNCTION_IMPORTS
                        for name in imported
                    ):
                        continue
                    offenders.append(f"{relative}:{child.lineno} {ast.unparse(child)}")
                elif isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
                    visit(child, child, relative)
                else:
                    visit(child, scope, relative)

        for path in sorted(project_modules().values()):
            tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
            visit(tree, None, str(path.relative_to(ROOT)))
        self.assertEqual(
            offenders, [], "Imports inside functions or classes:\n" + "\n".join(offenders)
        )


class ImportGraphTests(SimpleTestCase):
    def test_module_level_imports_are_acyclic(self):
        modules = project_modules()
        edges = {module: set() for module in modules}
        for module, path in modules.items():
            tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
            is_package = path.name == "__init__.py"
            for node in tree.body:
                if isinstance(node, ast.Import):
                    targets = [resolve(alias.name, modules) for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if node.level:
                        base = module if is_package else module.rsplit(".", 1)[0]
                        base = ".".join(base.split(".")[: len(base.split(".")) - node.level + 1])
                        full = f"{base}.{node.module}" if node.module else base
                    else:
                        full = node.module or ""
                    targets = [
                        (
                            f"{full}.{alias.name}"
                            if f"{full}.{alias.name}" in modules
                            else resolve(full, modules)
                        )
                        for alias in node.names
                    ]
                else:
                    continue
                edges[module].update(t for t in targets if t and t != module)

        # Tarjan's strongly connected components, iterative so a deep import chain
        # cannot overflow the stack; any component of two or more modules is a cycle.
        index, low, stack, on_stack, cycles = {}, {}, [], set(), []

        def strong(root):
            work = [(root, iter(sorted(edges[root])))]
            index[root] = low[root] = len(index)
            stack.append(root)
            on_stack.add(root)
            while work:
                node, children = work[-1]
                for child in children:
                    if child not in index:
                        index[child] = low[child] = len(index)
                        stack.append(child)
                        on_stack.add(child)
                        work.append((child, iter(sorted(edges[child]))))
                        break
                    if child in on_stack:
                        low[node] = min(low[node], index[child])
                else:
                    work.pop()
                    if work:
                        parent = work[-1][0]
                        low[parent] = min(low[parent], low[node])
                    if low[node] == index[node]:
                        component = []
                        while True:
                            member = stack.pop()
                            on_stack.discard(member)
                            component.append(member)
                            if member == node:
                                break
                        if len(component) > 1:
                            cycles.append(sorted(component))

        for module in sorted(modules):
            if module not in index:
                strong(module)
        self.assertEqual(
            cycles, [], "Import cycles between modules:\n" + "\n".join(map(str, cycles))
        )
