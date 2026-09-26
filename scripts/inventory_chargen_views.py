"""Compare own-method ASTs without importing Django or treating similarity as proof.

Run from any directory: python scripts/inventory_chargen_views.py [--output PATH].
Exact groups discard docstrings only. Shape groups additionally erase literal
values, so gameline wording/configuration differences remain visible for review.
Inherited-only adapters are reported separately from implementations.
"""

import argparse
import ast
import copy
import hashlib
import json
from collections import defaultdict
from pathlib import Path


class Normalize(ast.NodeTransformer):
    def __init__(self, literals=False):
        self.literals = literals

    def visit_FunctionDef(self, node):
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)
        return self.generic_visit(node)

    def visit_Constant(self, node):
        if self.literals:
            return ast.Constant(value=type(node.value).__name__)
        return node


def fingerprint(methods, *, literals=False):
    tree = ast.Module(body=copy.deepcopy(methods), type_ignores=[])
    normalized = ast.dump(Normalize(literals).visit(tree), include_attributes=False)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def inventory(root):
    classes = []
    groups = {kind: defaultdict(list) for kind in ("exact", "shape")}
    suffixes = (
        "LanguagesView",
        "SpecialtiesView",
        "ExtrasView",
        "AbilityView",
        "FreebiesView",
        "TemplateSelectView",
        "PassionsView",
        "FettersView",
        "CreateView",
        "UpdateView",
        "DetailView",
        "TemplateSelectionForm",
    )
    for path in sorted((root / "characters/views").rglob("*.py")):
        for node in ast.parse(path.read_text(encoding="utf-8")).body:
            if not isinstance(node, ast.ClassDef) or not node.name.endswith(suffixes):
                continue
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            class_path = (
                f"{path.relative_to(root).with_suffix('').as_posix().replace('/', '.')}.{node.name}"
            )
            entry = {
                "class": class_path,
                "family": next(s for s in suffixes if node.name.endswith(s)),
                "bases": [ast.unparse(base) for base in node.bases],
                "lines": node.end_lineno - node.lineno + 1,
                "methods": [n.name for n in methods],
                "configuration": [
                    ast.unparse(n) for n in node.body if isinstance(n, (ast.Assign, ast.AnnAssign))
                ],
                "configuration_only": not methods,
            }
            for kind in groups:
                entry[kind] = fingerprint(methods, literals=kind == "shape") if methods else None
                if methods:
                    groups[kind][entry[kind]].append(class_path)
            classes.append(entry)
    families = {}
    for family in sorted({entry["family"] for entry in classes}):
        entries = [entry for entry in classes if entry["family"] == family]
        families[family] = {
            "classes": len(entries),
            "own_implementations": sum(not e["configuration_only"] for e in entries),
            "lines": sum(e["lines"] for e in entries),
        }
    return {
        "note": "Own-method comparison only; shape groups ignore literal values and require semantic review.",
        "families": families,
        "duplicate_groups": {
            kind: [v for _, v in sorted(group.items()) if len(v) > 1]
            for kind, group in groups.items()
        },
        "classes": classes,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(inventory(Path(__file__).resolve().parents[1]), indent=2) + "\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")
