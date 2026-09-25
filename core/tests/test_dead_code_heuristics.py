"""Unit tests for the pure heuristics in scripts/dead_code_heuristics.py.

Only the heuristics module is imported: find_dead_code.py re-points the default
database when imported, so it is exercised in a subprocess instead
(core/tests/test_find_dead_code_script.py).
"""

import ast
import os
import subprocess
import sys
from pathlib import Path

from django.http import JsonResponse
from django.test import SimpleTestCase
from django.views import View
from django.views.generic import CreateView, DetailView

from scripts.dead_code_heuristics import (
    classify_dead_route,
    find_computed,
    object_type_seed,
    pattern_regex,
    str_parts,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
URL_WILDCARD = r"[\w:-]*"


def expr(source):
    return ast.parse(source, mode="eval").body


def computed(source):
    out = []
    find_computed(ast.parse(source), out, None)
    return out


class StrPartsTest(SimpleTestCase):
    def test_plain_string_is_one_literal_part(self):
        self.assertEqual(str_parts(expr('"shop:item_list"')), ["shop:item_list"])

    def test_f_string_placeholders_become_none(self):
        self.assertEqual(str_parts(expr('f"shop:{kind}_detail"')), ["shop:", None, "_detail"])

    def test_percent_formatting(self):
        self.assertEqual(str_parts(expr('"shop/%s.html" % kind')), ["shop/", None, ".html"])
        self.assertEqual(
            str_parts(expr('"shop/%(kind)s/%d.html" % values')),
            ["shop/", None, "/", None, ".html"],
        )

    def test_percent_i_and_x_are_placeholders(self):
        self.assertEqual(str_parts(expr('"shop/%i.html" % kind')), ["shop/", None, ".html"])
        self.assertEqual(str_parts(expr('"shop/%x.html" % kind')), ["shop/", None, ".html"])

    def test_percent_percent_is_a_literal_percent_not_a_placeholder(self):
        self.assertEqual(str_parts(expr('"50%% done" % ()')), ["50% done"])
        self.assertEqual(
            str_parts(expr('"100%% off: %s" % kind')),
            ["100% off: ", None, ""],
        )

    def test_str_format(self):
        self.assertEqual(str_parts(expr('"shop:{}_list".format(kind)')), ["shop:", None, "_list"])
        self.assertEqual(
            str_parts(expr('"shop/{kind}.html".format(kind=k)')), ["shop/", None, ".html"]
        )

    def test_concatenation(self):
        self.assertEqual(str_parts(expr('"shop:" + kind')), ["shop:", None])
        self.assertEqual(str_parts(expr('kind + "_detail"')), [None, "_detail"])
        self.assertEqual(str_parts(expr('"shop/" + kind + ".html"')), ["shop/", None, ".html"])

    def test_expressions_without_literals_are_not_strings(self):
        self.assertIsNone(str_parts(expr("first + second")))
        self.assertIsNone(str_parts(expr("kind")))
        self.assertIsNone(str_parts(expr("build_name(kind)")))
        self.assertIsNone(str_parts(expr("fmt % kind")))


class FindComputedTest(SimpleTestCase):
    def test_literal_reverse_is_ignored(self):
        self.assertEqual(computed('reverse("shop:item_list")'), [])

    def test_reverse_of_a_variable_is_recorded(self):
        self.assertEqual(computed("reverse(target)"), [("url", 1, [None], "target")])
        self.assertEqual(
            computed("reverse_lazy(self.success_name)"),
            [("url", 1, [None], "self.success_name")],
        )

    def test_redirect_to_an_object_is_ignored(self):
        self.assertEqual(computed("redirect(item)"), [])
        self.assertEqual(computed("redirect(item.get_absolute_url())"), [])

    def test_redirect_to_a_built_name_is_recorded(self):
        self.assertEqual(
            computed('redirect(f"shop:{kind}_detail", pk=1)'),
            [("url", 1, ["shop:", None, "_detail"], "f'shop:{kind}_detail'")],
        )

    def test_template_name_keyword_is_a_template(self):
        self.assertEqual(
            computed('show(template_name="shop/" + kind + ".html")'),
            [("template", 1, ["shop/", None, ".html"], "'shop/' + kind + '.html'")],
        )

    def test_template_name_assignment_is_a_template(self):
        source = 'class ItemView:\n    template_name = "shop/%s/detail.txt" % kind\n'
        self.assertEqual(
            computed(source),
            [("template", 2, ["shop/", None, "/detail.txt"], "'shop/%s/detail.txt' % kind")],
        )

    def test_render_takes_its_template_from_the_second_argument(self):
        self.assertEqual(
            computed('render(request, f"shop/{kind}.html")'),
            [("template", 1, ["shop/", None, ".html"], "f'shop/{kind}.html'")],
        )

    def test_viewname_keyword_counts_only_for_url_functions(self):
        self.assertEqual(computed("reverse(viewname=target)"), [("url", 1, [None], "target")])
        self.assertEqual(computed("audit(viewname=target)"), [])

    def test_unanchored_builds_are_classified_by_their_literal(self):
        self.assertEqual(
            computed('name = f"shop:{kind}_list"'),
            [("url", 1, ["shop:", None, "_list"], "f'shop:{kind}_list'")],
        )
        self.assertEqual(computed('label = f"{first}:{second}"'), [])


class ObjectTypeSeedTest(SimpleTestCase):
    def test_keyword_fields(self):
        call = expr('ObjectType.objects.get_or_create(name="vampire", type="char", gameline="vtm")')
        self.assertEqual(object_type_seed(call), ("vampire", "char", "vtm"))

    def test_defaults_dict_fields(self):
        call = expr(
            'ObjectType.objects.update_or_create(name="node", '
            'defaults={"type": "loc", "gameline": "mta"})'
        )
        self.assertEqual(object_type_seed(call), ("node", "loc", "mta"))

    def test_non_literal_or_incomplete_calls_are_skipped(self):
        for source in (
            'ObjectType.objects.get_or_create(name=kind, type="char", gameline="vtm")',
            'ObjectType.objects.get_or_create(name="vampire", type="char")',
            'ObjectType.objects.filter(name="vampire", type="char", gameline="vtm")',
            'Clan.objects.create(name="vampire", type="char", gameline="vtm")',
        ):
            with self.subTest(source=source):
                self.assertIsNone(object_type_seed(expr(source)))


class PatternRegexTest(SimpleTestCase):
    def test_placeholders_match_the_wildcard_and_literals_are_escaped(self):
        regex = pattern_regex(["shop:", None, "_detail"], URL_WILDCARD)
        self.assertTrue(regex.match("shop:item_detail"))
        self.assertIsNone(regex.match("shop:item_detail_extra"))
        self.assertIsNone(regex.match("other:item_detail"))

        template = pattern_regex(["shop/", None, ".html"], r".*")
        self.assertTrue(template.match("shop/items/list.html"))
        self.assertIsNone(template.match("shop/items/listXhtml"))


class Item:
    """Stands in for a model: classify_dead_route only needs a class."""


class ItemDetail(DetailView):
    model = Item


class ItemCreate(CreateView):
    model = Item


class ItemData(View):
    def get(self, request):
        return JsonResponse({})


class Router(View):
    pass


class RoutedChild(Router):
    pass


def plain_view(request):
    return None


class ClassifyDeadRouteTest(SimpleTestCase):
    def test_json_and_ajax_endpoints(self):
        self.assertEqual(
            classify_dead_route(Router, "shop:ajax:load_items", "shop/ajax/"),
            "(b) JSON/AJAX endpoint",
        )
        self.assertEqual(
            classify_dead_route(ItemData, "shop:item_data", "shop/data/"),
            "(b) JSON/AJAX endpoint",
        )

    def test_function_view(self):
        self.assertEqual(
            classify_dead_route(plain_view, "shop:plain", "shop/plain/"),
            "(d) other (function view)",
        )

    def test_alias_detail_route(self):
        self.assertEqual(
            classify_dead_route(
                ItemDetail,
                "shop:item_alias",
                "shop/alias/<pk>/",
                alias_target=lambda m: "shop:item",
            ),
            "(a) alias: Item.get_absolute_url() -> shop:item",
        )

    def test_canonical_detail_route_is_an_unlinked_page(self):
        self.assertEqual(
            classify_dead_route(
                ItemDetail, "shop:item", "shop/<pk>/", alias_target=lambda m: "shop:item"
            ),
            "(c) detail page with no link",
        )
        self.assertEqual(
            classify_dead_route(ItemDetail, "shop:item", "shop/<pk>/"),
            "(c) detail page with no link",
        )

    def test_page_kinds(self):
        self.assertEqual(
            classify_dead_route(ItemCreate, "shop:create", "shop/create/"),
            "(c) create page with no link",
        )

    def test_routers_are_named_only_when_their_base_is_given(self):
        self.assertEqual(
            classify_dead_route(RoutedChild, "shop:router", "shop/r/", router_bases=(Router,)),
            "(d) other (DictView router)",
        )
        self.assertEqual(classify_dead_route(RoutedChild, "shop:router", "shop/r/"), "(d) other")


class HeuristicsImportTest(SimpleTestCase):
    def test_import_does_not_configure_django(self):
        env = {k: v for k, v in os.environ.items() if k != "DJANGO_SETTINGS_MODULE"}
        code = (
            "import django.apps, django.conf, scripts.dead_code_heuristics; "
            "print(django.apps.apps.ready, django.conf.settings.configured)"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "False False")
