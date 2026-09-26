"""Guards for code deleted by the Step 1 dead-code removal.

Design: docs/superpowers/specs/2026-09-25-dead-code-removal-design.md. Each rollout PR adds
one ``SimpleTestCase`` subclass named after its PR ID (``D2DependencyRemovedTest``, ...) that
mixes in ``RemovalAssertions``. A guard fails while the dead code exists and keeps it from
coming back. Guards need no database, so every class is a ``SimpleTestCase``.
"""

import importlib
import importlib.util
import re
from pathlib import Path

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import SimpleTestCase
from django.urls import NoReverseMatch, get_resolver, resolve, reverse

REPO_ROOT = Path(settings.BASE_DIR)


class RemovalAssertions:
    """Assertions shared by every removal guard in this module."""

    def assertRequirementRemoved(self, distribution):
        names = set()
        for line in (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                names.add(re.split(r"[\s<>=!~;\[]", line, maxsplit=1)[0].lower())
        self.assertNotIn(distribution.lower(), names)

    def assertModuleRemoved(self, dotted_path):
        try:
            spec = importlib.util.find_spec(dotted_path)
        except ModuleNotFoundError:  # a parent package is gone too
            spec = None
        self.assertIsNone(spec, f"{dotted_path} still exists")

    def assertAttributesRemoved(self, module_path, *names):
        module = importlib.import_module(module_path)
        for name in names:
            with self.subTest(name=f"{module_path}.{name}"):
                self.assertFalse(hasattr(module, name), f"{module_path}.{name} still exists")
                self.assertNotIn(name, getattr(module, "__all__", ()))

    def assertUrlNamesRemoved(self, *names):
        for name in names:
            with self.subTest(name=name), self.assertRaises(NoReverseMatch):
                reverse(name)

    def assertUrlNamespaceRemoved(self, namespace):
        *parents, leaf = namespace.split(":")
        resolver = get_resolver()
        for parent in parents:
            resolver = resolver.namespace_dict[parent][1]
        self.assertNotIn(leaf, resolver.namespace_dict, f"{namespace} is still mounted")

    def assertTemplatesRemoved(self, *names):
        for name in names:
            with self.subTest(name=name), self.assertRaises(TemplateDoesNotExist):
                get_template(name)


class D2DependencyRemovedTest(RemovalAssertions, SimpleTestCase):
    """D2: django-smart-selects is not a dependency."""

    def test_django_smart_selects_not_in_requirements(self):
        self.assertRequirementRemoved("django-smart-selects")


class D3ChainedSelectRemovedTest(RemovalAssertions, SimpleTestCase):
    """D3: the deprecated chained_select app and its widgets-side copies are gone."""

    def test_chained_select_app_removed(self):
        self.assertNotIn("chained_select", settings.INSTALLED_APPS)
        self.assertModuleRemoved("chained_select")

    def test_widgets_copies_removed(self):
        self.assertAttributesRemoved("widgets", "ChainedSelectAjaxView", "make_ajax_view")
        self.assertAttributesRemoved("widgets", "ChainedSelectMultiple")
        self.assertAttributesRemoved("widgets.views", "ChainedSelectAjaxView", "make_ajax_view")
        self.assertAttributesRemoved("widgets.widgets", "ChainedSelectMultiple")
        self.assertAttributesRemoved("widgets.widgets.chained", "ChainedSelectMultiple")

    def test_live_widget_endpoint_kept(self):
        self.assertEqual(reverse("__chained_select_ajax__"), "/__chained_select__/")


class D4AjaxEndpointsRemovedTest(RemovalAssertions, SimpleTestCase):
    """D4: the unused AJAX endpoints, their views, templates and bases are gone."""

    def test_freebie_population_views_removed(self):
        for module_path, name in [
            ("characters.views.core.human", "HumanFreebieFormPopulationView"),
            ("characters.views.werewolf.garou", "WerewolfFreebieFormPopulationView"),
            ("characters.views.demon.demon_chargen", "DemonFreebieFormPopulationView"),
            ("characters.views.demon.dtfhuman_chargen", "DtFHumanFreebieFormPopulationView"),
            ("characters.views.demon.thrall_chargen", "ThrallFreebieFormPopulationView"),
            ("characters.views.demon", "DemonFreebieFormPopulationView"),
            ("characters.views.demon", "DtFHumanFreebieFormPopulationView"),
            ("characters.views.demon", "ThrallFreebieFormPopulationView"),
        ]:
            self.assertAttributesRemoved(module_path, name)

    def test_dropdown_templates_removed(self):
        self.assertTemplatesRemoved(
            "characters/core/human/load_examples_dropdown_list.html",
            "characters/core/human/load_values_dropdown_list.html",
            "characters/mage/mage/load_faction_dropdown_list.html",
            "characters/mage/mage/load_mf_rating_dropdown_list.html",
            "characters/mage/mage/load_subfaction_dropdown_list.html",
            "characters/mage/sorcerer/load_affinity_dropdown_list.html",
            "characters/mage/sorcerer/load_attribute_dropdown_list.html",
        )

    REMOVED_AJAX_URL_NAMES = (
        "characters:ajax:load_examples",
        "characters:ajax:load_values",
        "characters:mage:ajax:load_mf_ratings",
        "characters:mage:ajax:load_xp_examples",
        "characters:mage:ajax:get_abilities",
        "characters:mage:ajax:load_companion_examples",
        "characters:mage:ajax:load_advantage_values",
        "characters:mage:ajax:load_sorcerer_examples",
        "characters:mage:ajax:get_practice_abilities",
        "characters:mage:ajax:load_attributes",
        "characters:mage:ajax:load_affinities",
    )
    REMOVED_AJAX_VIEWS = (
        "characters.views.core.human.LoadExamplesView",
        "characters.views.core.human.LoadValuesView",
        "characters.views.mage.mage.LoadMFRatingsView",
        "characters.views.mage.mage.LoadXPExamplesView",
        "characters.views.mage.mage.GetAbilitiesView",
        "characters.views.mage.companion.LoadExamplesView",
        "characters.views.mage.companion.LoadCompanionValuesView",
        "characters.views.mage.sorcerer.LoadExamplesView",
        "characters.views.mage.sorcerer.GetPracticeAbilitiesView",
        "characters.views.mage.sorcerer.LoadAttributesView",
        "characters.views.mage.sorcerer.LoadAffinitiesView",
    )

    def test_ajax_url_names_removed(self):
        self.assertUrlNamesRemoved(*self.REMOVED_AJAX_URL_NAMES)
        self.assertUrlNamespaceRemoved("characters:ajax")
        self.assertUrlNamespaceRemoved("characters:mage:ajax")
        self.assertModuleRemoved("characters.urls.core.ajax")
        self.assertModuleRemoved("characters.urls.mage.ajax")

    def test_ajax_views_removed(self):
        from core.route_policy_manifest import VIEW_POLICIES

        for dotted in self.REMOVED_AJAX_VIEWS:
            module_path, name = dotted.rsplit(".", 1)
            self.assertAttributesRemoved(module_path, name)
            self.assertNotIn(dotted, VIEW_POLICIES)
        self.assertAttributesRemoved(
            "characters.views.mage",
            "LoadCompanionValuesView",
            "GetAbilitiesView",
            "LoadMFRatingsView",
            "GetPracticeAbilitiesView",
            "LoadAffinitiesView",
            "LoadAttributesView",
        )

    def test_chantry_ajax_endpoint_kept_until_c5(self):
        # resolve() a path and never spell the URL name, so find_dead_code.py still reports
        # the route as dead until chantry PR C5 deletes it together with this test.
        from locations.views.mage.chantry import LoadExamplesView

        match = resolve("/locations/mage/ajax/load_chantry_examples/")
        self.assertIs(match.func.view_class, LoadExamplesView)

    def test_empty_gameline_ajax_modules_removed(self):
        for namespace in (
            "characters:changeling:ajax",
            "characters:vampire:ajax",
            "characters:werewolf:ajax",
            "characters:wraith:ajax",
            "locations:vampire:ajax",
        ):
            app, gameline, _ = namespace.split(":")
            self.assertModuleRemoved(f"{app}.urls.{gameline}.ajax")
            self.assertUrlNamespaceRemoved(namespace)

    def test_every_gameline_urlconf_still_mounted(self):
        # characters/urls/__init__.py and locations/urls/__init__.py swallow ImportError,
        # so a dangling "from . import ajax" would silently drop a whole gameline.
        from core.constants import GameLine

        for app in ("characters", "locations"):
            mounted = get_resolver().namespace_dict[app][1].namespace_dict
            for _url_path, module_name, namespace in GameLine.URL_PATTERNS:
                with self.subTest(app=app, gameline=module_name):
                    module = importlib.import_module(f"{app}.urls.{module_name}")
                    self.assertTrue(hasattr(module, "urls"))
                    self.assertIn(namespace, mounted)

    def test_object_ajax_policy_removed(self):
        from core.route_policy_manifest import POLICIES

        self.assertNotIn("OBJECT_AJAX", POLICIES)
        for relative in (
            "core/access_policy.py",
            "scripts/build_route_policy_manifest.py",
            "scripts/inventory_authorization_routes.py",
        ):
            with self.subTest(file=relative):
                source = (REPO_ROOT / relative).read_text(encoding="utf-8")
                self.assertNotIn("OBJECT_AJAX", source)

    def test_ajax_view_bases_removed(self):
        self.assertAttributesRemoved(
            "core.mixins",
            "AjaxLoginRequiredMixin",
            "DropdownOptionsView",
            "SimpleValuesView",
            "JsonListView",
        )
        # dropdown_options_response stays until chantry PR C5 removes its last caller.
        self.assertAttributesRemoved("core.ajax", "simple_values_response")


class D5RemovedTests(SimpleTestCase):
    """Unit D5: dead template tag libraries, tags, filters and templates stay deleted."""

    @staticmethod
    def _module_exists(dotted_path):
        """Return True when ``dotted_path`` can be imported (parents included)."""
        import importlib.util

        try:
            return importlib.util.find_spec(dotted_path) is not None
        except ModuleNotFoundError:
            return False

    def _assert_libraries_removed(self, libraries, modules):
        from django.template.backends.django import get_installed_libraries

        installed = get_installed_libraries()
        for name in libraries:
            with self.subTest(library=name):
                self.assertNotIn(name, installed)
        for dotted_path in modules:
            with self.subTest(module=dotted_path):
                self.assertFalse(self._module_exists(dotted_path))

    def test_never_loaded_libraries_are_gone(self):
        self._assert_libraries_removed(
            ("resonance", "conditional_fields"),
            ("core.templatetags.resonance", "widgets.templatetags.conditional_fields"),
        )

    def test_conditional_mixin_docstring_no_longer_shows_deleted_filter(self):
        from widgets.mixins import conditional

        self.assertNotIn("conditional_wrap", conditional.__doc__)

    def test_kept_step6_library_and_render_post_html_survive(self):
        from django.template.backends.django import get_installed_libraries

        from core.templatetags import sanitize_text

        self.assertIn("permissions", get_installed_libraries())
        self.assertTrue(callable(sanitize_text.render_post_html))

    def test_dots_pool_and_linked_stat_tags_are_gone(self):
        from django.template import TemplateDoesNotExist
        from django.template.loader import get_template

        from core.templatetags import dots

        for name in ("pool", "pool_dots"):
            with self.subTest(filter=name):
                self.assertNotIn(name, dots.register.filters)
        for name in ("pool_rows", "linked_stat", "linked_stat_row"):
            with self.subTest(tag=name):
                self.assertNotIn(name, dots.register.tags)
        for name in (
            "pool",
            "pool_dots",
            "pool_rows",
            "linked_stat_tag",
            "linked_stat_row",
            "_extract_pool_values",
            "_render_pool_rows",
        ):
            with self.subTest(attribute=name):
                self.assertFalse(hasattr(dots, name))
        with self.assertRaises(TemplateDoesNotExist):
            get_template("core/templatetags/linked_stat_row.html")
        for name in ("dots", "boxes", "abs", "lore_name", "linked_dots"):
            with self.subTest(kept_filter=name):
                self.assertIn(name, dots.register.filters)

    def test_unused_single_tags_and_filters_are_gone(self):
        from core.templatetags import json_filters, sanitize_text
        from widgets.templatetags import formset_tags

        cases = (
            (json_filters, json_filters.register.filters, "get_item"),
            (sanitize_text, sanitize_text.register.filters, "badge_text"),
            (formset_tags, formset_tags.register.tags, "formset_remove_btn"),
        )
        for module, registry, name in cases:
            with self.subTest(module=module.__name__, name=name):
                self.assertNotIn(name, registry)
                self.assertFalse(hasattr(module, name))
        self.assertIn("pprint", json_filters.register.filters)
        self.assertIn("formset_add_btn", formset_tags.register.tags)

    def test_item_and_location_tag_libraries_are_gone(self):
        from django.template import TemplateDoesNotExist
        from django.template.loader import get_template

        self._assert_libraries_removed(
            ("item_filters", "location_tags"),
            ("items.templatetags.item_filters", "locations.templatetags.location_tags"),
        )
        with self.assertRaises(TemplateDoesNotExist):
            get_template("locations/location_recursive.html")

    def test_leftover_loads_are_removed_and_templates_compile(self):
        import re
        from pathlib import Path

        from django.conf import settings
        from django.template.loader import get_template

        leftover_loads = (
            ("items/templates/items/index.html", "items/index.html", "item_filters"),
            ("locations/templates/locations/index.html", "locations/index.html", "location_tags"),
            (
                "game/templates/game/chronicle/detail.html",
                "game/chronicle/detail.html",
                "location_tags",
            ),
        )
        base_dir = Path(settings.BASE_DIR)
        for relative_path, template_name, library in leftover_loads:
            with self.subTest(template=template_name, library=library):
                source = (base_dir / relative_path).read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"{%\s*load\b[^%]*\b" + library + r"\b", source))
                get_template(template_name)


class D6RemovedTests(SimpleTestCase):
    """Unit D6: dead mixins, decorators, middleware, cache helpers and utilities stay deleted."""

    @staticmethod
    def _module_exists(dotted_path):
        """Return True when ``dotted_path`` can be imported (parents included)."""
        import importlib.util

        try:
            return importlib.util.find_spec(dotted_path) is not None
        except ModuleNotFoundError:
            return False

    def test_dead_core_mixins_are_gone(self):
        import core.mixins

        for name in (
            "STRequiredMixin",
            "SpendXPPermissionMixin",
            "DeleteMessageMixin",
            "FreebieApprovalMixin",
        ):
            with self.subTest(name=name):
                self.assertFalse(hasattr(core.mixins, name))
        for name in ("SpendFreebiesPermissionMixin", "XPApprovalMixin", "MessageMixin"):
            with self.subTest(kept=name):
                self.assertTrue(hasattr(core.mixins, name))

    def test_character_template_st_mixin_is_gone(self):
        from core.views import character_template

        self.assertFalse(hasattr(character_template, "STRequiredMixin"))

    def test_kept_step6_context_processor_survives(self):
        from core import context_processors

        self.assertTrue(callable(context_processors.permissions))

    def test_decorators_and_cache_middleware_modules_are_gone(self):
        from django.conf import settings

        for dotted_path in ("core.decorators", "core.middleware.cache_middleware"):
            with self.subTest(module=dotted_path):
                self.assertFalse(self._module_exists(dotted_path))
        self.assertNotIn(
            "core.middleware.cache_middleware.PerUserCacheMiddleware", settings.MIDDLEWARE
        )

    def test_dead_cache_helpers_are_gone(self):
        import core.cache

        for name in ("cache_queryset", "get_cached_queryset", "invalidate_cache_on_save"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(core.cache, name))
        self.assertTrue(callable(core.cache.cache_function))
        self.assertTrue(callable(core.cache.get_cached_reference_list))

    def test_linked_stat_aliases_and_widgets_are_gone(self):
        import core.linked_stat
        import core.widgets

        for name in ("MaxCurrentStat", "PermanentTemporaryStat"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(core.linked_stat, name))
        self.assertFalse(self._module_exists("core.widgets.linked_stat"))
        self.assertEqual(core.widgets.__all__, ["AutocompleteTextInput"])
        for name in ("DotsBoxesWidget", "LinkedStatFormField", "LinkedStatWidget", "PoolWidget"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(core.widgets, name))

    def test_dead_utils_and_reexports_are_gone(self):
        import core.utils
        import locations.views.core

        for name in ("fast_selector", "level_name", "tree_sort", "compute_level"):
            with self.subTest(module="core.utils", name=name):
                self.assertFalse(hasattr(core.utils, name))
        for name in ("level_name", "tree_sort"):
            with self.subTest(module="locations.views.core", name=name):
                self.assertFalse(hasattr(locations.views.core, name))
                self.assertNotIn(name, locations.views.core.__all__)

    def test_dead_widgets_leftovers_are_gone(self):
        import widgets
        import widgets.widgets
        from widgets.fields import create_or_select
        from widgets.widgets import filterable, metadata_select

        gone = (
            (widgets, "CreateOrSelectModelChoiceField"),
            (widgets, "get_filterable_list_js"),
            (widgets, "OptionMetadataSelectMultiple"),
            (widgets.widgets, "OptionMetadataSelectMultiple"),
            (create_or_select, "CreateOrSelectModelChoiceField"),
            (filterable, "get_filterable_list_js"),
            (metadata_select, "OptionMetadataSelectMultiple"),
        )
        for module, name in gone:
            with self.subTest(module=module.__name__, name=name):
                self.assertFalse(hasattr(module, name))
                self.assertNotIn(name, getattr(module, "__all__", ()))


class D7RemovedTests(SimpleTestCase):
    """Unit D7: superseded views, forms and templates stay deleted."""

    def assert_names_absent(self, names_by_module):
        for module_path, names in names_by_module.items():
            module = importlib.import_module(module_path)
            for name in names:
                with self.subTest(module=module_path, name=name):
                    self.assertFalse(hasattr(module, name))
                    self.assertNotIn(name, getattr(module, "__all__", ()))

    def assert_modules_absent(self, module_paths):
        for module_path in module_paths:
            with self.subTest(module=module_path):
                self.assertIsNone(importlib.util.find_spec(module_path))

    def assert_templates_absent(self, template_names):
        for template_name in template_names:
            with self.subTest(template=template_name):
                with self.assertRaises(TemplateDoesNotExist):
                    get_template(template_name)

    def test_superseded_character_create_views_removed(self):
        self.assert_names_absent(
            {
                "characters.views.changeling.changeling": ["ChangelingCreateView"],
                "characters.views.changeling.ctdhuman": ["CtDHumanCreateView"],
                "characters.views.changeling": [
                    "ChangelingCharacterListView",
                    "CtDHumanCharacterListView",
                ],
                "characters.views.demon.demon": ["DemonCreateView"],
                "characters.views.demon.dtfhuman": ["DtFHumanCreateView"],
                "characters.views.demon.thrall": ["ThrallCreateView"],
                "characters.views.demon": [
                    "DemonCreateView",
                    "DtFHumanCreateView",
                    "ThrallCreateView",
                ],
                "characters.views.mage.mtahuman": ["MtAHumanCreateView"],
                "characters.views.mage": ["MtAHumanCreateView"],
                "characters.views.vampire.ghoul": ["GhoulCreateView"],
                "characters.views.vampire.vampire": ["VampireCreateView"],
                "characters.views.vampire.vtmhuman": ["VtMHumanCreateView"],
                "characters.views.vampire": [
                    "GhoulCreateView",
                    "VampireCreateView",
                    "VtMHumanCreateView",
                ],
                "characters.views.werewolf.fomor": ["FomorCreateView"],
                "characters.views.werewolf.garou": ["WerewolfCreateView"],
                "characters.views.werewolf.kinfolk": ["KinfolkCreateView"],
                "characters.views.werewolf.wtahuman": ["WtAHumanCreateView"],
                "characters.views.werewolf": [
                    "FomorCreateView",
                    "WerewolfCreateView",
                    "KinfolkCreateView",
                    "WtAHumanCreateView",
                ],
                "characters.views.wraith.wraith": ["WraithCreateView"],
                "characters.views.wraith.wtohuman": ["WtOHumanCreateView"],
                "characters.views.wraith": ["WraithCreateView", "WtOHumanCreateView"],
            }
        )

    def test_update_views_keep_their_field_lists(self):
        from characters.views.changeling import ctdhuman
        from characters.views.vampire import vtmhuman

        self.assertIs(ctdhuman.CtDHumanUpdateView.fields, ctdhuman.CTDHUMAN_FORM_FIELDS)
        self.assertIs(vtmhuman.VtMHumanUpdateView.fields, vtmhuman.VTMHUMAN_FORM_FIELDS)
        self.assertIn("kenning", ctdhuman.CTDHUMAN_FORM_FIELDS)
        self.assertIn("finance", vtmhuman.VTMHUMAN_FORM_FIELDS)

    def test_unrouted_list_views_removed(self):
        self.assert_names_absent(
            {
                "characters.views.core.character": ["CharacterListView"],
                "characters.views.vampire.vampire": ["VampireListView"],
                "characters.views.vampire.ghoul": ["GhoulListView"],
                "characters.views.vampire.revenant": ["RevenantListView"],
                "characters.views.vampire": [
                    "VampireListView",
                    "GhoulListView",
                    "RevenantListView",
                ],
            }
        )
        self.assert_templates_absent(
            [
                "characters/core/character/list.html",
                "characters/vampire/vampire/list.html",
                "characters/vampire/ghoul/list.html",
                "characters/vampire/revenant/list.html",
            ]
        )
