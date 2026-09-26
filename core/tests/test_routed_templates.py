"""Every routed page's template, and each template it extends or includes, exists.

The scan starts from every project view class that a URL pattern or a DictView
mapping reaches, takes its template names the way Django does, and follows each
constant {% extends %} and {% include %} target. Templates only load their parent
and includes at render time, so compiling the view's own template is not enough.
Names built from variables cannot be followed and are not checked.

KNOWN_MISSING lists the routed pages that return a 500 today because a template was
never written (dead-code design, section 7). Each entry names the template, one
view that reaches it and the step that owns the fix. The test fails when another
template goes missing, and when an allowlisted template exists but its entry stays.
"""

from functools import cache

from django.db import models
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template
from django.template.loader_tags import ExtendsNode, IncludeNode
from django.test import SimpleTestCase
from django.urls import URLResolver, get_resolver
from django.views.generic.base import TemplateResponseMixin

from core.access_policy import PROJECT_PREFIXES, route_name
from scripts.inventory_authorization_routes import descendants

KNOWN_MISSING = {
    "characters/core/character/chargen.html": (
        "characters.views.werewolf.drone.DroneBasicsView",
        "Step 2",
    ),
    "characters/demon/ritual/form.html": (
        "characters.views.demon.ritual.RitualUpdateView",
        "Step 7",
    ),
    "characters/demon/ritual/list.html": (
        "characters.views.demon.ritual.RitualListView",
        "Step 7",
    ),
    "characters/wraith/wraith/form.html": (
        "characters.views.wraith.wraith.WraithUpdateView",
        "Step 7",
    ),
}

# Routed template views that return their own response and never render the
# template name Django would derive for them.
NON_RENDERING_VIEWS = {
    "core.views.character_template.CharacterTemplateExportView": "returns a JSON download",
}


def iter_routed_views(patterns):
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            yield from iter_routed_views(pattern.url_patterns)
            continue
        view = getattr(pattern.callback, "view_class", None)
        if view is None:  # the one project function view is a JSON endpoint
            continue
        yield view
        yield from (target for _, target, _ in descendants(view) if target is not None)


def routed_project_views():
    views = set(iter_routed_views(get_resolver().url_patterns))
    return {view for view in views if route_name(view).startswith(PROJECT_PREFIXES)}


def view_template_names(view):
    """The names Django would try for this view, without a request or an object."""
    if not issubclass(view, TemplateResponseMixin) or route_name(view) in NON_RENDERING_VIEWS:
        return []
    instance = view()
    instance.request, instance.args, instance.kwargs, instance.object = None, (), {}, None
    model = getattr(view, "model", None)
    is_model = isinstance(model, type) and issubclass(model, models.Model)
    instance.object_list = model._default_manager.none() if is_model else []
    return list(instance.get_template_names())


def constant_name(expression):
    """A quoted template name with no filters, else None."""
    return expression.var if not expression.filters and isinstance(expression.var, str) else None


@cache
def referenced_templates(name):
    """Constant extends/include targets of one template; raises if it cannot load."""
    nodelist = get_template(name).template.nodelist
    targets = {constant_name(node.parent_name) for node in nodelist.get_nodes_by_type(ExtendsNode)}
    targets |= {constant_name(node.template) for node in nodelist.get_nodes_by_type(IncludeNode)}
    return tuple(sorted(targets - {None}))


def scan_templates(root, missing, broken):
    seen, stack = set(), [root]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        try:
            stack.extend(referenced_templates(name))
        except TemplateDoesNotExist:
            missing.add(name)
        except TemplateSyntaxError as exc:
            broken[name] = str(exc).splitlines()[0]


def first_loadable(names):
    """The name select_template() would use: the first that exists, else the first name."""
    for name in names:
        try:
            get_template(name)
        except TemplateDoesNotExist:
            continue
        except TemplateSyntaxError:
            pass  # it exists; scan_templates reports the error
        return name
    return names[0]


def missing_routed_templates():
    """({missing template: {views reaching it}}, {broken template: first error line})."""
    missing_by_template, broken = {}, {}
    for view in routed_project_views():
        names = view_template_names(view)
        if not names:
            continue
        missing = set()
        scan_templates(first_loadable(names), missing, broken)
        for name in missing:
            missing_by_template.setdefault(name, set()).add(route_name(view))
    return missing_by_template, broken


class RoutedTemplatesTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.missing, cls.broken = missing_routed_templates()

    def test_routed_templates_compile(self):
        self.assertEqual(self.broken, {})

    def test_no_new_missing_templates(self):
        new = {t: sorted(views) for t, views in self.missing.items() if t not in KNOWN_MISSING}
        self.assertEqual(
            new, {}, "Routed pages whose template is missing: write it, or add to KNOWN_MISSING"
        )

    def test_known_missing_templates_are_still_missing(self):
        written = sorted(set(KNOWN_MISSING) - set(self.missing))
        self.assertEqual(
            written,
            [],
            "These templates are no longer missing from routed pages: remove them from KNOWN_MISSING",
        )

    def test_known_missing_entries_name_a_view_that_reaches_them(self):
        for template, (view, _step) in KNOWN_MISSING.items():
            with self.subTest(template=template):
                self.assertIn(view, self.missing.get(template, {view}))

    def test_non_rendering_views_are_still_routed(self):
        routed = {route_name(view) for view in routed_project_views()}
        self.assertEqual(set(NON_RENDERING_VIEWS) - routed, set())
