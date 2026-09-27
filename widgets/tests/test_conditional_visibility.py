"""Server-side evaluation of ConditionalFieldsMixin rules.

The cases mirror widgets/static/widgets/conditional.js; the browser test in
characters.tests.browser checks both evaluators agree on the same inputs.
"""

from django import forms
from django.test import SimpleTestCase

from widgets import ChainedChoiceField, ChainedSelectMixin, ConditionalFieldsMixin

RULES = {
    "example": {"hidden_when": {"category": {"value_in": ["-----", "Willpower"]}}},
    "value": {"visible_when": {"category": {"value_is": "MeritFlaw"}}},
    "note": {"visible_when": {"category": {"value_not_in": ["-----", "Willpower"]}}},
    "pooled": {
        "visible_when": {
            "category": {"value_is": "Background"},
            "example": {"metadata_truthy": "poolable"},
            "_context": {"is_group_member": True},
        }
    },
    "flag_text": {"visible_when": {"flag": {"checked_is": True}}},
    "kind_text": {"visible_when": {"example": {"metadata_is": {"kind": "a"}}}},
    "ghost": {"visible_when": {"missing": {"value_is": "x"}}},
    "always": {},
}


class Form(ConditionalFieldsMixin, ChainedSelectMixin, forms.Form):
    category = forms.ChoiceField(
        choices=[("-----", "-----"), ("Willpower", "W"), ("MeritFlaw", "M"), ("Background", "B")]
    )
    example = ChainedChoiceField(
        parent_field="category",
        required=False,
        choices_map={
            "Background": [
                ("bg_1", "Allies", {"poolable": "true", "kind": "a"}),
                ("bg_2", "Fame", {"poolable": "false"}),
            ]
        },
    )
    value = forms.CharField(required=False)
    note = forms.CharField(required=False)
    pooled = forms.BooleanField(required=False)
    flag = forms.BooleanField(required=False)
    flag_text = forms.CharField(required=False)
    kind_text = forms.CharField(required=False)
    ghost = forms.CharField(required=False)
    always = forms.CharField(required=False)

    conditional_fields = RULES


def visible(values, group_member=False):
    form = Form(conditional_context={"is_group_member": group_member})
    return {name for name, shown in form.field_visibility(values).items() if shown}


class FieldVisibilityTests(SimpleTestCase):
    def test_hidden_when_any_condition_holds(self):
        self.assertNotIn("example", visible({"category": "Willpower"}))
        self.assertIn("example", visible({"category": "Background"}))

    def test_value_is_and_value_not_in(self):
        self.assertIn("value", visible({"category": "MeritFlaw"}))
        self.assertNotIn("value", visible({"category": "Background"}))
        self.assertIn("note", visible({"category": "Background"}))
        self.assertNotIn("note", visible({"category": "-----"}))

    def test_visible_when_needs_every_condition_including_context(self):
        values = {"category": "Background", "example": "bg_1"}
        self.assertNotIn("pooled", visible(values))
        self.assertIn("pooled", visible(values, group_member=True))
        self.assertNotIn("pooled", visible({**values, "example": "bg_2"}, group_member=True))

    def test_metadata_comes_from_the_childs_choices_for_its_parent(self):
        self.assertIn("kind_text", visible({"category": "Background", "example": "bg_1"}))
        self.assertNotIn("kind_text", visible({"category": "Background", "example": "bg_2"}))
        # A value that is not an option for the parent has no metadata.
        self.assertNotIn("kind_text", visible({"category": "MeritFlaw", "example": "bg_1"}))

    def test_checked_is_uses_the_checkbox_state(self):
        self.assertIn("flag_text", visible({"flag": True}))
        self.assertNotIn("flag_text", visible({"flag": False}))

    def test_missing_source_field_fails_its_condition_and_empty_rules_show(self):
        self.assertNotIn("ghost", visible({"missing": "x"}))
        self.assertIn("always", visible({}))

    def test_current_values_read_bound_data_and_unbound_first_option(self):
        unbound = Form()
        self.assertEqual(unbound.current_values()["category"], "-----")
        bound = Form(data={"category": "Background", "example": "bg_1", "flag": "on"})
        values = bound.current_values()
        self.assertEqual(
            (values["category"], values["flag"], values["pooled"]), ("Background", True, False)
        )
        self.assertEqual(Form(data={"category": "MeritFlaw"}).visibility["value"], True)

    def test_htmx_mode_drops_the_browser_interpreter(self):
        form = Form()
        self.assertIn("widgets/conditional.js", str(form.media))
        self.assertNotEqual(form.conditional_js(), "")
        form.enable_htmx_chains("/characters/1/")
        self.assertNotIn("widgets/conditional.js", str(form.media))
        self.assertEqual(form.conditional_js(), "")


class HtmxChainTests(SimpleTestCase):
    def test_chain_follows_parent_links_from_a_plain_root(self):
        self.assertEqual(Form().chain_for("example"), ["category", "example"])
        self.assertEqual(Form().chain_for("category"), ["category", "example"])

    def test_root_requests_child_options_without_the_csrf_token(self):
        form = Form()
        form.enable_htmx_chains("/characters/1/")
        html = str(form["category"])
        self.assertIn('hx-get="/characters/1/"', html)
        self.assertIn('hx-target="#id_example"', html)
        self.assertIn('hx-include="#id_category, #id_example"', html)
        self.assertNotIn("hx-get", str(form["example"]))
        self.assertNotIn("data-chain-tree", html + str(form["example"]))

    def test_bound_form_fills_child_options_from_submitted_parent(self):
        form = Form(data={"category": "Background"})
        form.enable_htmx_chains("/characters/1/")
        self.assertIn('<option value="bg_1">Allies</option>', str(form["example"]))
