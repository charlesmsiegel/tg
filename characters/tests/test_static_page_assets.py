"""Rendered page configuration remains data when JavaScript is served statically."""

import json
from html.parser import HTMLParser
from types import SimpleNamespace

from django import forms
from django.template.loader import render_to_string
from django.test import SimpleTestCase


class ScriptParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.scripts = []
        self.current = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.current = {"attrs": dict(attrs), "body": ""}
            self.scripts.append(self.current)

    def handle_data(self, data):
        if self.current is not None:
            self.current["body"] += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.current = None


class StaticPageConfigurationTests(SimpleTestCase):
    def test_chargen_templates_do_not_display_developer_comments(self):
        from django.contrib.auth.models import AnonymousUser

        for template in (
            "core/form.html",
            "characters/core/ability_block/validation.html",
            "characters/core/background_block/form.html",
        ):
            with self.subTest(template=template):
                html = render_to_string(
                    template,
                    {
                        "form": forms.formset_factory(forms.Form, extra=0)(),
                        "request": SimpleNamespace(user=AnonymousUser()),
                    },
                )
                self.assertNotIn("{#", html)
                self.assertNotIn("#}", html)

    def test_registered_vampire_virtues_loads_static_validator(self):
        from characters.chargen import get_workflow

        step = next(step for step in get_workflow("vampire").steps if step.key == "virtues")
        scripts = ScriptParser(render_to_string(step.template)).scripts
        self.assertEqual(len(scripts), 1)
        self.assertTrue(scripts[0]["attrs"]["src"].endswith("characters/js/vampire-virtues.js"))
        self.assertEqual(scripts[0]["body"], "")

    def test_ability_validation_requires_all_targets(self):
        template = "characters/core/ability_block/validation.html"
        for context in (
            {},
            {"primary": 13, "secondary": 9},
            {"primary": 13, "secondary": 9, "tertiary": 0},
        ):
            with self.subTest(context=context):
                self.assertNotIn("<script", render_to_string(template, context))
        html = render_to_string(template, {"primary": 13, "secondary": 9, "tertiary": 5})
        self.assertIn('data-primary="13"', html)
        self.assertIn('data-secondary="9"', html)
        self.assertIn('data-tertiary="5"', html)
        scripts = ScriptParser(html).scripts
        self.assertEqual(len(scripts), 1)
        self.assertTrue(scripts[0]["attrs"]["src"].endswith("characters/js/ability-validation.js"))
        self.assertEqual(scripts[0]["body"], "")

    def test_background_multiplier_json_is_inert_and_round_trips(self):
        # Even a future string-valued map cannot escape the inert JSON element.
        multipliers = {"1": 2, "unexpected": "</script><script>alert('x')</script>"}
        html = render_to_string(
            "characters/core/background_block/form.html",
            {
                "form": forms.formset_factory(forms.Form, extra=0)(),
                "object": SimpleNamespace(background_points=5),
                "background_multipliers_json": json.dumps(multipliers),
            },
        )
        data = next(
            script
            for script in ScriptParser(html).scripts
            if script["attrs"].get("id") == "background-multipliers"
        )
        self.assertEqual(data["attrs"]["type"], "application/json")
        self.assertEqual(json.loads(json.loads(data["body"])), multipliers)
        self.assertNotIn("<script>alert", html)
        self.assertIn('data-budget="5"', html)

    def test_sorcerer_type_is_escaped_data(self):
        value = '"</script><script>alert("x")</script>'
        html = render_to_string(
            "characters/mage/sorcerer/sorcerer_freebies_form.html",
            {"object": SimpleNamespace(sorcerer_type=value)},
        )
        script = next(
            script
            for script in ScriptParser(html).scripts
            if script["attrs"].get("id") == "sorcerer-freebies-script"
        )
        self.assertEqual(script["attrs"]["data-sorcerer-type"], value)
        self.assertEqual(script["body"], "")
        self.assertNotIn("<script>alert", html)

    def test_group_membership_is_boolean_data(self):
        for is_member in (True, False):
            with self.subTest(is_member=is_member):
                html = render_to_string(
                    "characters/mage/mage/mage_xp_form.html",
                    {"object": SimpleNamespace(is_group_member=is_member)},
                )
                script = next(
                    script
                    for script in ScriptParser(html).scripts
                    if script["attrs"].get("id") == "mage-xp-script"
                )
                self.assertEqual(script["attrs"]["data-is-group-member"], str(is_member).lower())
                self.assertEqual(script["body"], "")
