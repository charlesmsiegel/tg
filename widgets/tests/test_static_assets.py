"""Contracts for static loading and inert, safely encoded widget configuration."""

import json
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command
from django.template import Context, Engine, Template
from django.test import SimpleTestCase, override_settings

from widgets import (
    ChainedSelect,
    ConditionalFieldsMixin,
    CreateOrSelectWidget,
    OptionMetadataSelect,
    PointPoolInput,
    PointPoolSelect,
)


class Scripts(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.scripts = []
        self.current = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.current = [dict(attrs), ""]
            self.scripts.append(self.current)

    def handle_data(self, data):
        if self.current is not None:
            self.current[1] += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.current = None


class StaticWidgetTests(SimpleTestCase):
    def test_independent_renders_and_combined_media(self):
        for widget_class, asset in [
            (ChainedSelect, "chained"),
            (CreateOrSelectWidget, "create_or_select"),
            (OptionMetadataSelect, "metadata_select"),
            (PointPoolInput, "point_pool"),
            (PointPoolSelect, "point_pool"),
        ]:
            with self.subTest(widget=widget_class):
                first, second = widget_class(), widget_class()
                path = f"widgets/{asset}.js"
                self.assertIn(path, str(first.media))
                self.assertEqual(str(first.media), str(second.media))
                self.assertEqual(str(first.media + second.media).count(path), 1)
                self.assertIsNotNone(finders.find(path))
                for widget in (first, second):
                    self.assertEqual(Scripts(widget.render("field", None)).scripts, [])

    def test_configuration_cannot_escape_script_or_attributes(self):
        hostile = '</script><script>alert("x")</script>&< >'
        for widget in [
            ChainedSelect(chain_name=hostile, choices_tree={"value": hostile}),
            PointPoolInput(pool_name=hostile, is_root=True, pool_config={"value": hostile}),
            PointPoolSelect(pool_name=hostile, is_root=True, pool_config={"value": hostile}),
        ]:
            with self.subTest(widget=type(widget)):
                scripts = Scripts(widget.render("field", None)).scripts
                self.assertEqual(len(scripts), 1)
                attrs, body = scripts[0]
                self.assertEqual(attrs["type"], "application/json")
                self.assertEqual(json.loads(body), {"value": hostile})
                self.assertIn(hostile, attrs.values())

    def test_conditional_media_and_safe_rules(self):
        class Form(ConditionalFieldsMixin, forms.Form):
            choice = forms.CharField(widget=ChainedSelect)
            conditional_fields = {"detail": {"visible_when": {"choice": {"value_is": "</script>"}}}}

        for form in (Form(), Form()):
            media = str(form.media)
            self.assertIn("widgets/conditional.js", media)
            self.assertIn("widgets/chained.js", media)
            scripts = Scripts(form.conditional_js()).scripts
            self.assertEqual(len(scripts), 1)
            self.assertEqual(json.loads(scripts[0][1])["rules"], form.conditional_fields)

    def test_page_media_includes_empty_formset_and_deduplicates(self):
        class Form(forms.Form):
            choice = forms.CharField(widget=ChainedSelect)

        formset = forms.formset_factory(Form, extra=0)()
        template = Template("{% load widget_media %}{% page_media %}")
        html = template.render(
            Context({"form": Form(), "other_form": Form(), "rows_context": {"formset": formset}})
        )
        self.assertEqual(html.count("widgets/chained.js"), 1)
        self.assertEqual(html.count("widgets/formset_manager.js"), 1)

    def test_included_tag_media_is_scoped_to_each_render(self):
        engine = Engine(
            libraries={
                "widget_media": "widgets.templatetags.widget_media",
                "formset_tags": "widgets.templatetags.formset_tags",
            },
            loaders=[
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        "fragment": "{% load formset_tags %}{% formset_script %}",
                    },
                )
            ],
        )
        template = engine.from_string(
            '{% load widget_media %}{% if include %}{% include "fragment" %}'
            '{% include "fragment" %}{% endif %}{% page_media %}'
        )
        context = Context({"include": True})
        self.assertEqual(template.render(context).count("widgets/formset_manager.js"), 1)
        self.assertEqual(template.render(context).count("widgets/formset_manager.js"), 1)
        context["include"] = False
        self.assertEqual(template.render(context), "")


class ManifestCollectionTests(SimpleTestCase):
    def test_all_application_scripts_receive_content_hashes(self):
        with tempfile.TemporaryDirectory(prefix="tg-static-test-") as output:
            with override_settings(
                STATIC_ROOT=output,
                STORAGES={
                    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                    "staticfiles": {
                        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
                    },
                },
            ):
                call_command("collectstatic", interactive=False, verbosity=0)
                for app in (
                    "accounts",
                    "characters",
                    "core",
                    "game",
                    "items",
                    "locations",
                    "widgets",
                ):
                    static_dir = Path(settings.BASE_DIR) / app / "static"
                    for script in static_dir.rglob("*.js"):
                        name = script.relative_to(static_dir).as_posix()
                        hashed = staticfiles_storage.stored_name(name)
                        self.assertNotEqual(name, hashed)
                        self.assertTrue((Path(output) / hashed).is_file())


class InlineScriptInventoryTests(SimpleTestCase):
    def test_no_executable_inline_scripts_outside_scene_chat(self):
        allowlist = {"game/templates/game/scene/detail.html"}
        found = set()
        for app in ("accounts", "characters", "core", "game", "items", "locations", "widgets"):
            for path in (Path(settings.BASE_DIR) / app / "templates").rglob("*.html"):
                scripts = Scripts(path.read_text(encoding="utf-8")).scripts
                if any(
                    "src" not in attrs and attrs.get("type") != "application/json"
                    for attrs, _ in scripts
                ):
                    found.add(path.relative_to(settings.BASE_DIR).as_posix())
        self.assertEqual(found, allowlist)
