"""Report dead-code candidates: URL names, views, templates, template tags, symbols.

Run: python scripts/find_dead_code.py [--section NAME]... [--format md|tsv] > dead-code.md
Sections: urls, views, templates, tags, symbols (default: all); --section repeats.
The script is read-only; no database connection is required (the default
database is pointed at in-memory SQLite before anything could open it).
Every row is a candidate for review, not a verdict: reflection, string-built
names and third-party conventions can hide real uses. The symbols section is
an explicit name-occurrence heuristic.
"""

# Django must initialize before model imports in this standalone script.
# ruff: noqa: E402

import argparse
import ast
import importlib
import inspect
import os
import re
import sys
from collections import Counter, defaultdict
from functools import cache
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")

import django

django.setup()

from django.apps import AppConfig, apps
from django.conf import settings
from django.db import connections, models
from django.db.migrations import Migration
from django.template import Library
from django.template.backends.django import get_installed_libraries
from django.urls import NoReverseMatch, URLResolver, get_resolver, resolve, reverse
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.base import TemplateResponseMixin

from characters.forms.core.character_creation import CharacterCreationForm
from core.create_redirects import APP_NAMES
from core.views.generic import DictView
from scripts.inventory_authorization_routes import descendants

# Never touch a real database: the scan needs none. Fail loudly rather than
# misconfigure a non-SQLite connection if the settings ever change.
if not connections["default"].settings_dict["ENGINE"].endswith("sqlite3"):
    sys.exit("find_dead_code.py expects the default database to use SQLite")
connections["default"].settings_dict["NAME"] = ":memory:"

LOCAL_CONFIGS = [c for c in apps.get_app_configs() if Path(c.path).resolve().is_relative_to(ROOT)]
LOCAL_APPS = tuple(sorted({c.name.split(".")[0] for c in LOCAL_CONFIGS}))
PROJECT_PKGS = (*LOCAL_APPS, "tg")
SKIP_DIRS = {
    "node_modules",
    "__pycache__",
    "docs",
    "logs",
    "collected_static",
    "staticfiles",
    "venv",
    "scripts",
}  # scripts/ holds tooling like this file, not app code
TEXT_EXTS = {".py", ".html", ".js", ".txt", ".xml"}
URL_FUNCS = {"reverse", "reverse_lazy", "redirect", "resolve_url"}
TEMPLATE_FUNCS = {
    "render",
    "render_to_string",
    "get_template",
    "select_template",
    "TemplateResponse",
}
ERROR_TEMPLATES = {"400.html", "403.html", "403_csrf.html", "404.html", "500.html"}
QUOTED = re.compile(r"""(['"])([^'"\s{}%]{1,200})\1""")
IDENT = re.compile(r"[A-Za-z_]\w*")
LOAD_RE = re.compile(r"\{%\s*load\s+(.+?)\s*%\}")
INCLUDE_RE = re.compile(r"\{%\s*(include|extends)\s+(.+?)\s*%\}")
URL_TAG_RE = re.compile(r"\{%\s*url\s+(\S+)")
DECORATOR_SKIP = re.compile(r"register|receiver|shared_task|\.task\b")
CALL_CTX = {**dict.fromkeys(URL_FUNCS, "url"), **dict.fromkeys(TEMPLATE_FUNCS, "template")}
NOT_URL_GETTERS = {"get_success_url", "get_gameline_for_url"}
SEED_METHODS = {"create", "get_or_create", "update_or_create"}
# Actions the index views pass to core.create_redirects.resolve_object_type_url:
# characters/views/core/__init__.py asks only for "create"; items and locations
# ask for "create" or "list".
INDEX_ACTIONS = {"char": {"create"}, "obj": {"create", "list"}, "loc": {"create", "list"}}
# The character index only offers types its forms list: CharacterCreationForm drops
# EXCLUDED_TYPES, and GroupCreationForm offers these (local list in group_creation.py).
GROUP_FORM_TYPES = {"cabal", "pack", "motley", "group", "coterie", "circle", "conclave"}
CHAR_NOT_OFFERED = set(CharacterCreationForm.EXCLUDED_TYPES) - GROUP_FORM_TYPES
OBJECT_TYPE_STATUS = "dynamic: object-type index (resolve_object_type_url)"
PAGE_KINDS = [(CreateView, "create"), (UpdateView, "update"), (DeleteView, "delete")]
PAGE_KINDS += [(ListView, "list"), (DetailView, "detail"), (FormView, "form")]
PAGE_KINDS += [(TemplateView, "template")]
TAG_HEADERS = ("Library", "Kind", "Name", "Defined at", "Template files using")
TAG_HEADERS += ("Python refs (non-test)", "Python refs (tests)", "Status")


def is_test_path(rel):
    parts = rel.split("/")
    name = parts[-1]
    return (
        "tests" in parts
        or name.startswith("test_")
        or name in {"tests.py", "conftest.py"}
        or name.endswith("_tests.py")
    )


def module_top(obj):
    return (getattr(obj, "__module__", "") or "").split(".")[0]


def call_name(node):
    func = node.func
    return func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)


class Src:
    """One scanned text file plus (for Python) its AST-derived index."""

    def __init__(self, rel, text):
        self.rel, self.text = rel, text
        self.test = is_test_path(rel)
        self.migration = "/migrations/" in f"/{rel}"
        self.top = rel.split("/")[0]
        self.literals, self.code_idents, self.str_idents = set(), set(), set()
        self.computed, self.defs, self.object_types = [], [], []
        self.template_text = text  # for .py: only non-docstring string constants
        if rel.endswith(".py"):
            self.template_text = ""
            self._index_python()
        else:
            self.literals = {m.group(2) for m in QUOTED.finditer(text)}
            self.str_idents = set(IDENT.findall(text))

    def _index_python(self):
        try:
            tree = ast.parse(self.text)
        except SyntaxError as exc:
            print(f"warning: cannot parse {self.rel}: {exc}", file=sys.stderr)
            return
        skip = set()  # docstrings, __all__ entries and path(name=...) declarations
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                skip.add(id(node.value))
            elif isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets
            ):
                skip.update(id(n) for n in ast.walk(node.value))
            elif isinstance(node, ast.Call) and call_name(node) in {"path", "re_path"}:
                skip.update(id(k.value) for k in node.keywords if k.arg == "name")
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and (seed := object_type_seed(node)):
                self.object_types.append((*seed, node.lineno))
            if isinstance(node, ast.Name):
                self.code_idents.add(node.id)
            elif isinstance(node, ast.Attribute):
                self.code_idents.add(node.attr)
            elif (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and id(node) not in skip
            ):
                self.literals.add(node.value)
                if "{%" in node.value or "{{" in node.value:
                    self.template_text += node.value + "\n"
                self.literals.update(m.group(2) for m in QUOTED.finditer(node.value))
                self.str_idents.update(IDENT.findall(node.value))
        find_computed(tree, self.computed, None)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
                decorators = " ".join(ast.unparse(d) for d in node.decorator_list)
                kind = "class" if isinstance(node, ast.ClassDef) else "function"
                self.defs.append((node.name, kind, node.lineno, decorators))


def object_type_seed(call):
    """(name, category, gameline) from a literal ObjectType.objects.get_or_create(...) call."""
    func = call.func
    if not (isinstance(func, ast.Attribute) and func.attr in SEED_METHODS):
        return None
    if ast.unparse(func.value) != "ObjectType.objects":
        return None
    fields = {k.arg: k.value for k in call.keywords if k.arg}
    defaults = fields.get("defaults")
    if isinstance(defaults, ast.Dict):
        fields.update(
            {
                getattr(k, "value", None): v
                for k, v in zip(defaults.keys, defaults.values, strict=True)
            }
        )
    try:
        return tuple(ast.literal_eval(fields[f]) for f in ("name", "type", "gameline"))
    except (KeyError, ValueError):
        return None


def str_parts(node):
    """Flatten a string-building expression into literal parts; None marks a placeholder."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.JoinedStr):
        return [v.value if isinstance(v, ast.Constant) else None for v in node.values]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = str_parts(node.left), str_parts(node.right)
        if left is None and right is None:
            return None
        return (left or [None]) + (right or [None])
    fmt, pattern = None, None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        fmt, pattern = node.left, r"%(?:\(\w+\))?[sdrf]"
    elif isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "format":
        fmt, pattern = node.func.value, r"\{[^{}]*\}"
    if isinstance(fmt, ast.Constant) and isinstance(fmt.value, str):
        pieces = re.split(pattern, fmt.value)
        return [x for piece in pieces for x in (piece, None)][:-1]
    return None


def find_computed(node, out, ctx):
    """Record string-building expressions (and variable reverse() args) for manual review."""
    parts = str_parts(node) if isinstance(node, ast.JoinedStr | ast.BinOp | ast.Call) else None
    if parts and None in parts and any(parts):
        literal = "".join(p for p in parts if p)
        kind = ctx
        if kind is None and re.search(r"\.(html|txt)\b", literal):
            kind = "template"
        elif kind is None and re.fullmatch(r"[a-z_]+:[\w:-]*", parts[0] or ""):
            kind = "url"
        if kind:
            out.append((kind, node.lineno, parts, ast.unparse(node)))
        return
    if ctx == "url" and isinstance(node, ast.Name | ast.Attribute | ast.Subscript):
        out.append(("url", node.lineno, [None], ast.unparse(node)))
    if isinstance(node, ast.Call):
        name = call_name(node)
        arg_ctx = CALL_CTX.get(name)
        for index, child in enumerate(node.args):
            # redirect() often takes a model object first, so only a string-building
            # first arg counts there; render()'s name is its second arg.
            builds_string = isinstance(child, ast.JoinedStr | ast.BinOp | ast.Call)
            wanted = (
                index == 0 and arg_ctx == "url" and (name != "redirect" or builds_string)
            ) or (arg_ctx == "template" and index == (1 if name == "render" else 0))
            find_computed(child, out, arg_ctx if wanted else None)
        for child in [node.func, *node.keywords]:
            find_computed(
                child, out, "template" if getattr(child, "arg", "") == "template_name" else None
            )
        return
    if isinstance(node, ast.Assign) and any(
        getattr(t, "id", "") == "template_name" for t in node.targets
    ):
        return find_computed(node.value, out, "template")
    for child in ast.iter_child_nodes(node):
        find_computed(child, out, None)


def pattern_regex(parts, wildcard):
    return re.compile("".join(re.escape(p) if p is not None else wildcard for p in parts) + r"\Z")


def load_sources():
    sources = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for filename in sorted(filenames):
            path = Path(dirpath, filename)
            if path.suffix in TEXT_EXTS:
                rel = path.relative_to(ROOT).as_posix()
                sources.append(Src(rel, path.read_text(encoding="utf-8", errors="replace")))
    return sources


SOURCES = []


def scanned():
    """Non-test, non-migration sources: what counts as live application code."""
    return [s for s in SOURCES if not s.test and not s.migration]


def literal_files(test):
    index = defaultdict(set)
    for src in SOURCES:
        if src.test == test and not src.migration:
            for literal in src.literals:
                index[literal].add(src.rel)
    return index


def computed_items(kind):
    """(file:line, expression, regex, anchored) for string-built names of this kind."""
    wildcard = r"[\w:-]*" if kind == "url" else r".*"
    items = [
        (f"{s.rel}:{line}", expr, pattern_regex(parts, wildcard), bool(parts[0]))
        for s in scanned()
        for k, line, parts, expr in s.computed
        if k == kind
    ]
    for src in scanned():  # template-side expressions
        if src.rel.endswith(".py"):
            continue
        regex = URL_TAG_RE if kind == "url" else INCLUDE_RE
        for match in regex.finditer(src.text):
            expr = (
                match.group(1 if kind == "url" else 2).split(" with ")[0].split(" only")[0].strip()
            )
            if re.fullmatch(r"""(['"])[^'"]*\1""", expr):
                continue
            prefix = re.match(r"""(['"])([^'"]*)\1""", expr)
            parts = [prefix.group(2), None] if prefix else [None]
            line = src.text.count("\n", 0, match.start()) + 1
            items.append((f"{src.rel}:{line}", expr, pattern_regex(parts, wildcard), bool(prefix)))
    return items


def summarize(total, counts, extra=""):
    return total + "; " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())) + extra


def review_table(title, computed, used_for):
    rows = {
        (where, expr, "yes" if anchored else "no (too broad)")
        for where, expr, _, anchored in computed
    }
    return title, ("Location", "Expression", used_for), rows


def iter_patterns(patterns, ns=(), prefix=""):
    for pattern in patterns:
        route = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver):
            inner = (*ns, pattern.namespace) if pattern.namespace else ns
            yield from iter_patterns(pattern.url_patterns, inner, route)
        else:
            yield (":".join((*ns, pattern.name)) if pattern.name else None), route, pattern


def view_of(callback):
    return getattr(callback, "view_class", None) or inspect.unwrap(callback)


def qualname(obj):
    return f"{obj.__module__}.{obj.__qualname__}"


@cache
def routed_views():
    routed = set()
    for _, _, pattern in iter_patterns(get_resolver().url_patterns):
        view = view_of(pattern.callback)
        routed.add(view)
        if isinstance(view, type):
            routed.update(target for _, target, _ in descendants(view) if target)
    return routed


def url_name_of(getter):
    """Resolve what a URL getter returns back to its URL name (None if it cannot run)."""
    try:
        return resolve(urlsplit(getter()).path).view_name
    except Exception:  # needs DB/arguments: fall back to literals
        return None


@cache
def absolute_url_name(model):
    return url_name_of(getattr(model(pk=1), "get_absolute_url", lambda: None))


def model_url_names():
    """Evaluate every model get_*_url() method on unsaved instances (or the class)."""
    names = set()
    for model in apps.get_models():
        if module_top(model) not in LOCAL_APPS:
            continue
        instance = None
        for attr in dir(model):
            if not re.fullmatch(r"get_\w*url", attr) or attr in NOT_URL_GETTERS:
                continue
            bound = getattr(model, attr)
            try:
                if not inspect.ismethod(bound) and instance is None:
                    instance = model(pk=1)
                target = bound if inspect.ismethod(bound) else getattr(instance, attr)
            except Exception:  # model cannot be instantiated bare
                continue
            names.add(url_name_of(target))
    return names - {None}


def object_type_routes():
    """Route names resolve_object_type_url() builds for statically seeded ObjectType rows.

    Rows: (route name, category, gameline, type, action, seeded at, requested, problem).
    """
    seeds = {}  # prefer the populate_db seed over app-code get_or_create calls
    for src in sorted(scanned(), key=lambda s: s.top != "populate_db"):
        for name, category, gameline, line in src.object_types:
            seeds.setdefault((name, category, gameline), f"{src.rel}:{line}")
    url_names = {name for name, _, _ in iter_patterns(get_resolver().url_patterns) if name}
    per_name = Counter((category, name) for name, category, _ in seeds)
    rows = []
    for (name, category, gameline), where in sorted(seeds.items()):
        config = settings.GAMELINES.get(gameline)
        namespace = "" if gameline == "wod" else f"{(config or {}).get('app_name')}:"
        for action in ("create", "list"):
            route_name = f"{APP_NAMES.get(category)}:{namespace}{action}:{name}"
            problem = ""
            if category not in APP_NAMES or config is None:
                problem = "unsupported category/gameline"
            else:
                try:
                    reverse(route_name)
                except NoReverseMatch:
                    exists = route_name in url_names
                    problem = "route needs URL arguments" if exists else "no such URL name"
            if per_name[(category, name)] > 1:
                problem += "; name seeded in several gamelines (404 unless gameline is posted)"
            requested = action in INDEX_ACTIONS.get(category, ()) and not (
                category == "char" and name in CHAR_NOT_OFFERED
            )
            requested = "yes" if requested else "no"
            rows.append((route_name, category, gameline, name, action, where, requested, problem))
    return rows


def classify_dead_route(view, name, route):
    """(a) alias detail, (b) JSON/AJAX, (c) unlinked page view, (d) other."""
    try:
        source = inspect.getsource(view)
    except (OSError, TypeError):
        source = ""
    if re.search(r"ajax|json|load_", f"{name} {route}", re.I) or "JsonResponse" in source:
        return "(b) JSON/AJAX endpoint"
    if not isinstance(view, type):
        return "(d) other (function view)"
    model = getattr(view, "model", None)
    if issubclass(view, DetailView) and isinstance(model, type):
        target = absolute_url_name(model)
        if target and target != name:
            return f"(a) alias: {model.__name__}.get_absolute_url() -> {target}"
    for base, kind in PAGE_KINDS:
        if issubclass(view, base):
            return f"(c) {kind} page with no link"
    return "(d) other (DictView router)" if issubclass(view, DictView) else "(d) other"


def section_urls():
    nontest, test = literal_files(False), literal_files(True)
    referenced = set(nontest) | model_url_names()
    for literal in nontest:
        if literal.startswith("/") and "//" not in literal:
            try:
                referenced.add(resolve(urlsplit(literal).path).view_name)
            except Exception:  # not a routable path
                pass
    computed = computed_items("url")
    type_routes = object_type_routes()
    via_index = {r[0] for r in type_routes if r[6] == "yes" and not r[7].startswith(("no ", "uns"))}
    rows, counts, dead_kinds = [], defaultdict(int), Counter()
    seen = set()
    routes = defaultdict(set)  # a dead name may share its path with a live one
    for name, route, _ in iter_patterns(get_resolver().url_patterns):
        if name in referenced:
            routes[route].add(name)
    for name, route, pattern in iter_patterns(get_resolver().url_patterns):
        view = view_of(pattern.callback)
        if not name or name in seen or module_top(view) not in LOCAL_APPS:
            continue
        seen.add(name)
        if name in referenced:
            counts["referenced"] += 1
            continue
        kind = "-"
        if name in via_index:
            status = OBJECT_TYPE_STATUS
        elif any(anchored and rx.match(name) for _, _, rx, anchored in computed):
            status = "dynamic (manual review)" + ("; tests reference it" if name in test else "")
        elif routes[route]:
            status = "path also reversed as " + ", ".join(sorted(routes[route]))
        else:
            status = "tests only" if name in test else "dead"
            kind = classify_dead_route(view, name, route)
            dead_kinds[f"{status} {kind[:3]}"] += 1
        counts[status.split(" as ")[0].split(";")[0]] += 1
        rows.append((name, route, qualname(view), status, kind))
    review = review_table("Computed URL names - manual review", computed, "Marks names dynamic")
    broken = [r for r in type_routes if r[7] and r[6] == "yes"]
    unrequested = [r[:6] + r[7:] for r in type_routes if r[7] and r[6] == "no"]
    extra = f"; {len(review[2])} computed; dead/tests-only by kind: " + ", ".join(
        f"{k}: {v}" for k, v in sorted(dead_kinds.items())
    )
    extra += f"; seeded object-type routes failing: {len(broken)} requested by an index view"
    extra += f" (live 404s), {len(unrequested)} never requested"
    headers = ("URL name", "Route", "View", "Status", "Dead-route kind")
    broken_headers = ("Computed route name", "Category", "Gameline", "Type", "Action")
    broken_headers += ("Seeded at", "Problem")
    return summarize(f"{len(seen)} project URL names", counts, extra), [
        ("Unreferenced URL names", headers, rows),
        (
            "Seeded object types: index-requested route fails (live 404)",
            broken_headers,
            [r[:6] + r[7:] for r in broken],
        ),
        ("Seeded object types: unresolvable but never requested", broken_headers, unrequested),
        review,
    ]


def project_views():
    stack, found = [View], set()
    while stack:
        for sub in stack.pop().__subclasses__():
            if sub not in found:
                found.add(sub)
                stack.append(sub)
    views = {}
    for cls in found:
        if module_top(cls) in LOCAL_APPS and not is_test_path(
            cls.__module__.replace(".", "/") + ".py"
        ):
            try:
                path, line = inspect.getsourcefile(cls), inspect.getsourcelines(cls)[1]
            except (OSError, TypeError):  # built with type(): no source of its own
                continue
            views[cls] = f"{Path(path).resolve().relative_to(ROOT).as_posix()}:{line}"
    return views


def import_project_modules():
    failures = []
    for src in scanned():
        if src.rel.endswith(".py") and src.top in LOCAL_APPS:
            module = src.rel[:-3].replace("/", ".").removesuffix(".__init__")
            try:
                importlib.import_module(module)
            except Exception as exc:  # report and keep scanning
                failures.append(f"{module}: {type(exc).__name__}")
    if failures:
        print(f"warning: {len(failures)} modules failed to import: {failures[:5]}", file=sys.stderr)


def code_ident_files(test=False, include_strings=False):
    index = defaultdict(set)
    for src in SOURCES:
        if src.test == test:
            for name in src.code_idents | (src.str_idents if include_strings else set()):
                index[name].add(src.rel)
    return index


@cache
def unrouted_views():
    """(rows, counts) for project view classes that no URL or router reaches."""
    views, routed = project_views(), routed_views()
    idents = code_ident_files()
    orphan_routers = {}  # targets reachable only through an unrouted DictView
    for cls in views:
        if cls not in routed:
            for _, target, _ in descendants(cls):
                orphan_routers.setdefault(target, cls.__name__)
    rows, counts = [], defaultdict(int)
    for cls, where in views.items():
        if cls in routed:
            counts["routed"] += 1
            continue
        if any(cls in r.__mro__[1:] for r in routed if isinstance(r, type)):
            counts["base of routed"] += 1
            continue
        others = sorted(idents.get(cls.__name__, set()) - {where.split(":")[0]})
        if any(cls in v.__mro__[1:] for v in views):
            status = "base of unrouted views only"
        elif cls in orphan_routers:
            status = f"dead: only mapped by unrouted {orphan_routers[cls]}"
        elif others:
            status = f"referenced in code (review): {', '.join(others[:2])}"
        else:
            status = "dead"
        counts[status.split(":")[0]] += 1
        rows.append((cls, where, status))
    return rows, counts


def section_views():
    rows, counts = unrouted_views()
    table = [(qualname(cls), where, status) for cls, where, status in rows]
    summary = summarize(f"{sum(counts.values())} project view classes", counts)
    return summary, [("Unrouted view classes", ("View", "Defined at", "Status"), table)]


def view_template_names(view):
    if not (isinstance(view, type) and issubclass(view, TemplateResponseMixin)):
        return []
    try:
        instance = view()
        instance.request, instance.args, instance.kwargs, instance.object = None, (), {}, None
        model = getattr(view, "model", None)
        is_model = isinstance(model, type) and issubclass(model, models.Model)
        instance.object_list = model._default_manager.none() if is_model else []
        return list(instance.get_template_names())
    except Exception:  # needs request/object state: rely on literals
        return []


def template_dirs(local):
    configs = (
        LOCAL_CONFIGS if local else [c for c in apps.get_app_configs() if c not in LOCAL_CONFIGS]
    )
    dirs = [Path(c.path, "templates") for c in configs]
    if local:
        dirs += [Path(d) for engine in settings.TEMPLATES for d in engine.get("DIRS", [])]
    else:
        dirs.append(Path(django.__file__).parent / "forms" / "templates")
    return [d for d in dirs if d.is_dir()]


def template_names(local):
    names = {}
    for base in template_dirs(local):
        for path in sorted(base.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                names.setdefault(
                    path.relative_to(base).as_posix(),
                    path.resolve().relative_to(ROOT).as_posix()
                    if path.resolve().is_relative_to(ROOT)
                    else str(path),
                )
    return names


def section_templates():
    templates, framework = template_names(True), set(template_names(False)) | ERROR_TEMPLATES
    nontest, test = literal_files(False), literal_files(True)
    runtime = {name for view in routed_views() for name in view_template_names(view)}
    computed = computed_items("template")
    dead_view_templates = {}  # template -> first unrouted view by name (stable output)
    for cls, where, status in sorted(unrouted_views()[0], key=lambda row: row[0].__name__):
        if status.startswith("dead"):
            for name in view_template_names(cls):
                dead_view_templates.setdefault(name, (cls.__name__, where.split(":")[0]))
    status_of, users_of = {}, {}
    for name, rel in templates.items():
        users = nontest.get(name, set()) - {rel}
        if name in runtime or name in framework:
            continue
        users_of[name] = users
        if users:
            continue
        if any(anchored and rx.match(name) for _, _, rx, anchored in computed):
            status_of[name] = "possibly dynamic"
        else:
            status_of[name] = "tests only" if name in test else "dead"
    changed = True
    while changed:  # propagate through templates/views that are themselves dead
        changed = False
        dead_files = {templates[n] for n, st in status_of.items() if st != "possibly dynamic"}
        for name, users in users_of.items():
            if name in status_of or not users:
                continue
            view_name, view_file = dead_view_templates.get(name, (None, None))
            if users <= dead_files:
                status_of[name] = "only referenced by dead templates"
            elif view_name and users <= dead_files | {view_file}:
                status_of[name] = f"only used by unrouted {view_name}"
            else:
                continue
            changed = True
    rows = [(name, templates[name], status) for name, status in status_of.items()]
    counts = Counter(
        re.sub(r"unrouted \w+", "unrouted view", status) for status in status_of.values()
    )
    counts["referenced"] = len(templates) - len(rows)
    review = review_table(
        "Computed template names - manual review", computed, "Marks possibly dynamic"
    )
    summary = summarize(
        f"{len(templates)} project templates", counts, f"; {len(review[2])} computed"
    )
    return summary, [("Unreferenced templates", ("Template", "File", "Status"), rows), review]


def loads_by_file(test):
    loads = defaultdict(set)
    for src in SOURCES:
        if src.test != test or src.migration or not src.rel.endswith((".html", ".txt", ".py")):
            continue
        for match in LOAD_RE.finditer(src.template_text):
            tokens = match.group(1).split()
            loads[src.rel].update(tokens[-1:] if "from" in tokens else tokens)
    return loads


def section_tags():
    builtins = {
        b for engine in settings.TEMPLATES for b in engine.get("OPTIONS", {}).get("builtins", [])
    }
    loads, test_loads = loads_by_file(False), loads_by_file(True)
    texts = {s.rel: s.template_text for s in SOURCES}
    lib_rows, tag_rows = [], []
    for lib, module_path in sorted(get_installed_libraries().items()):
        if module_path.split(".")[0] not in LOCAL_APPS:
            continue
        module = importlib.import_module(module_path)
        # Django itself loads a library through its module-level ``register``.
        register = getattr(module, "register", None)
        if not isinstance(register, Library):
            lib_rows.append((lib, module_path, 0, 0, "no `register` Library (review)"))
            continue
        users = (
            sorted(f for f, libs in loads.items() if lib in libs)
            if module_path not in builtins
            else list(texts)
        )
        test_users = sorted(f for f, libs in test_loads.items() if lib in libs)
        status = "loaded" if users else ("tests only" if test_users else "never loaded")
        lib_rows.append((lib, module_path, len(users), len(test_users), status))
        for kind, registry in (("tag", register.tags), ("filter", register.filters)):
            for name, func in sorted(registry.items()):
                func = inspect.unwrap(func)
                where = f"{module_path.replace('.', '/')}.py:{func.__code__.co_firstlineno}"
                usage = re.compile(
                    (r"\{%-?\s*" if kind == "tag" else r"\|\s*") + re.escape(name) + r"\b"
                )
                used = sum(1 for f in users if usage.search(texts.get(f, "")))
                py = [
                    s
                    for s in SOURCES
                    if s.rel.endswith(".py")
                    and module_path in s.text
                    and func.__name__ in s.code_idents
                    and s.rel != module_path.replace(".", "/") + ".py"
                ]
                py_nontest, py_test = sum(not s.test for s in py), sum(s.test for s in py)
                tag_status = (
                    "used" if used else ("unused (library never loaded)" if not users else "unused")
                )
                tag_rows.append((lib, kind, name, where, used, py_nontest, py_test, tag_status))
    unused_libs = sum(r[-1] != "loaded" for r in lib_rows)
    unused_tags = [r for r in tag_rows if r[-1] != "used"]
    summary = (
        f"{len(lib_rows)} project tag libraries, {unused_libs} not loaded by non-test code; "
        f"{len(tag_rows)} tags/filters, {len(unused_tags)} unused in templates"
    )
    lib_headers = ("Library", "Module", "Loaded in (files)", "Loaded in tests", "Status")
    return summary, [
        ("Tag libraries", lib_headers, lib_rows),
        ("Unused tags and filters", TAG_HEADERS, unused_tags),
    ]


def symbol_kind(module_name, name, kind):
    obj = getattr(sys.modules.get(module_name), name, None)
    if not isinstance(obj, type):
        return kind
    if issubclass(obj, View | AppConfig | Migration) or name == "Command":
        return None  # views: see the views section; framework-discovered classes
    return "model" if issubclass(obj, models.Model) else "class"


def section_symbols():
    # Migrations and populate_db count as references, never as definitions.
    refs = code_ident_files(include_strings=True)
    test_refs = code_ident_files(test=True, include_strings=True)
    rows = []
    for src in scanned():
        if not src.rel.endswith(".py") or src.top not in PROJECT_PKGS:
            continue
        module = src.rel[:-3].replace("/", ".").removesuffix(".__init__")
        for name, kind, line, decorators in src.defs:
            if name.startswith("__") or DECORATOR_SKIP.search(decorators):
                continue
            kind = symbol_kind(module, name, kind)
            if kind is None or refs.get(name):
                continue
            status = "only referenced from tests" if test_refs.get(name) else "unreferenced"
            rows.append((status, f"{module}.{name}", kind, f"{src.rel}:{line}"))
    headers = ("Symbol", "Kind", "Defined at")
    summary = summarize(
        "HEURISTIC (name occurrence only; same-named attributes elsewhere hide dead code)",
        Counter(row[0] for row in rows),
    )
    return summary, [
        (
            "Unreferenced symbols (heuristic)",
            headers,
            [r[1:] for r in rows if r[0] == "unreferenced"],
        ),
        (
            "Only referenced from tests (heuristic)",
            headers,
            [r[1:] for r in rows if r[0] != "unreferenced"],
        ),
    ]


SECTIONS = {
    "urls": section_urls,
    "views": section_views,
    "templates": section_templates,
    "tags": section_tags,
    "symbols": section_symbols,
}


def emit(section, summary, tables, fmt):
    print(f"## {section}\n\n**Summary:** {summary}\n" if fmt == "md" else f"# {section}\t{summary}")
    for title, headers, rows in tables:
        rows = sorted(rows, key=lambda r: tuple(str(v) for v in r))
        if fmt == "tsv":
            print("\t".join(("section", "table", *headers)))
            for row in rows:
                print("\t".join((section, title, *(str(v).replace("\t", " ") for v in row))))
            continue
        print(f"### {title} ({len(rows)})\n\n| " + " | ".join(headers) + " |")
        print("|" + "---|" * len(headers))
        for row in rows:
            print("| " + " | ".join(str(v).replace("|", "\\|") for v in row) + " |")
        print()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sections = sorted(SECTIONS)
    parser.add_argument("--section", choices=sections, action="append", help="repeatable")
    parser.add_argument("--format", choices=("md", "tsv"), default="md")
    args = parser.parse_args()
    SOURCES.extend(load_sources())
    import_project_modules()  # unrouted views/symbols must be loaded to be found
    if args.format == "md":
        print("# Dead code report\n\nCandidates only; see each section's summary and statuses.\n")
    for section in args.section or SECTIONS:
        summary, tables = SECTIONS[section]()
        emit(section, summary, tables, args.format)


if __name__ == "__main__":
    main()
