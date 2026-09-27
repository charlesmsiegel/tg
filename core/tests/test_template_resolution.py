"""Specific-then-shared template lookup (core.template_resolution)."""

from django.core.exceptions import ImproperlyConfigured
from django.template.loader import select_template
from django.test import SimpleTestCase, override_settings
from django.views.generic import TemplateView

from core.mixins import SharedTemplateMixin
from core.template_resolution import shared_template_names

LOCMEM_TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        "shared/page.html": "shared {% block body %}default{% endblock %}",
                        "specific/override.html": (
                            '{% extends "shared/page.html" %}{% block body %}custom{% endblock %}'
                        ),
                    },
                )
            ]
        },
    }
]


class SharedPage(SharedTemplateMixin, TemplateView):
    template_name = "specific/page.html"
    shared_template_name = "shared/page.html"


class SharedTemplateNamesTest(SimpleTestCase):
    def test_specific_names_come_first_then_shared(self):
        self.assertEqual(
            shared_template_names(["a.html", "b.html"], "shared.html", "last.html"),
            ["a.html", "b.html", "shared.html", "last.html"],
        )

    def test_duplicates_and_empty_names_are_dropped(self):
        self.assertEqual(
            shared_template_names(["a.html", "shared.html"], "shared.html", None, ""),
            ["a.html", "shared.html"],
        )

    def test_mixin_appends_the_shared_template(self):
        self.assertEqual(
            SharedPage().get_template_names(), ["specific/page.html", "shared/page.html"]
        )

    def test_mixin_without_template_name_uses_the_shared_template(self):
        view = type("OnlyShared", (SharedPage,), {"template_name": None})()
        self.assertEqual(view.get_template_names(), ["shared/page.html"])

    def test_mixin_without_any_template_is_still_misconfigured(self):
        view = type(
            "Nothing", (SharedPage,), {"template_name": None, "shared_template_name": None}
        )()
        with self.assertRaises(ImproperlyConfigured):
            view.get_template_names()


@override_settings(TEMPLATES=LOCMEM_TEMPLATES)
class SharedTemplateOverrideTest(SimpleTestCase):
    def test_missing_specific_template_falls_back_to_shared(self):
        template = select_template(SharedPage().get_template_names())
        self.assertEqual(template.render({}), "shared default")

    def test_specific_template_overrides_by_extending_the_shared_one(self):
        view = type("Override", (SharedPage,), {"template_name": "specific/override.html"})()
        template = select_template(view.get_template_names())
        self.assertEqual(template.render({}), "shared custom")
