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
