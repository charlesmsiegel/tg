"""Pure heuristics behind scripts/find_dead_code.py.

Importing this module has no side effects: it does not configure Django, open a
database or import project code. Everything here works on AST nodes, strings and
classes passed in, so the tests can import it directly.
"""

import ast
import inspect
import re

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

URL_FUNCS = {"reverse", "reverse_lazy", "redirect", "resolve_url"}
TEMPLATE_FUNCS = {
    "render",
    "render_to_string",
    "get_template",
    "select_template",
    "TemplateResponse",
}
CALL_CTX = {**dict.fromkeys(URL_FUNCS, "url"), **dict.fromkeys(TEMPLATE_FUNCS, "template")}
SEED_METHODS = {"create", "get_or_create", "update_or_create"}
PAGE_KINDS = [(CreateView, "create"), (UpdateView, "update"), (DeleteView, "delete")]
PAGE_KINDS += [(ListView, "list"), (DetailView, "detail"), (FormView, "form")]
PAGE_KINDS += [(TemplateView, "template")]
# %(name)s / %s / %d / %r / %f / %i / %x are placeholders; %% is a literal percent.
_PERCENT_RE = re.compile(r"%%|%(?:\(\w+\))?[sdrifx]")


def call_name(node):
    func = node.func
    return func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)


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


def _percent_format_parts(text):
    """Split a %-format string into literal/placeholder parts; %% is a literal percent."""
    parts, literal, pos = [], "", 0
    for match in _PERCENT_RE.finditer(text):
        literal += text[pos : match.start()]
        if match.group() == "%%":
            literal += "%"
        else:
            parts.append(literal)
            parts.append(None)
            literal = ""
        pos = match.end()
    parts.append(literal + text[pos:])
    return parts


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
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        fmt = node.left
        if isinstance(fmt, ast.Constant) and isinstance(fmt.value, str):
            return _percent_format_parts(fmt.value)
        return None
    if isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "format":
        fmt = node.func.value
        if isinstance(fmt, ast.Constant) and isinstance(fmt.value, str):
            pieces = re.split(r"\{[^{}]*\}", fmt.value)
            return [x for piece in pieces for x in (piece, None)][:-1]
        return None
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
    if ctx == "url" and (
        isinstance(node, ast.Name | ast.Attribute | ast.Subscript)
        # A nested reverse() or a model get_*url() is resolved elsewhere.
        or (
            isinstance(node, ast.Call)
            and call_name(node) not in CALL_CTX
            and not re.fullmatch(r"get_\w*url", call_name(node) or "")
        )
    ):
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
        find_computed(node.func, out, None)
        for keyword in node.keywords:
            if keyword.arg == "template_name":
                kw_ctx = "template"
            elif keyword.arg == "viewname" and arg_ctx == "url":
                kw_ctx = "url"
            else:
                kw_ctx = None
            find_computed(keyword.value, out, kw_ctx)
        return
    if isinstance(node, ast.Assign) and any(
        getattr(t, "id", "") == "template_name" for t in node.targets
    ):
        return find_computed(node.value, out, "template")
    for child in ast.iter_child_nodes(node):
        find_computed(child, out, None)


def pattern_regex(parts, wildcard):
    return re.compile("".join(re.escape(p) if p is not None else wildcard for p in parts) + r"\Z")


def classify_dead_route(view, name, route, *, alias_target=lambda model: None, router_bases=()):
    """(a) alias detail, (b) JSON/AJAX, (c) unlinked page view, (d) other.

    alias_target(model) returns the URL name that model's get_absolute_url() resolves
    to, or None. router_bases are the classes whose subclasses count as routers
    (find_dead_code.py passes DictView).
    """
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
        target = alias_target(model)
        if target and target != name:
            return f"(a) alias: {model.__name__}.get_absolute_url() -> {target}"
    for base, kind in PAGE_KINDS:
        if issubclass(view, base):
            return f"(c) {kind} page with no link"
    if router_bases and issubclass(view, tuple(router_bases)):
        return "(d) other (DictView router)"
    return "(d) other"
