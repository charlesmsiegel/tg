"""
Tests for the ConditionalFieldsMixin.
"""

import json

from django import forms
from django.test import TestCase

from widgets import ChainedChoiceField, ChainedSelectMixin, ConditionalFieldsMixin


class TestConditionalFieldsMixin(TestCase):
    """Tests for ConditionalFieldsMixin."""

    def test_basic_form_with_rules(self):
        """Test form with conditional visibility rules."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[('a', 'A'), ('b', 'B')])
            detail = forms.CharField(required=False)

            conditional_fields = {
                'detail': {
                    'visible_when': {'category': {'value_is': 'a'}},
                },
            }

        form = TestForm()
        rules = form.get_conditional_rules()

        self.assertIn('detail', rules)
        self.assertEqual(
            rules['detail']['visible_when']['category']['value_is'], 'a'
        )

    def test_conditional_js_output(self):
        """Test conditional_js() generates correct JavaScript."""
        ConditionalFieldsMixin.reset_js_rendered()

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[('a', 'A'), ('b', 'B')])
            detail = forms.CharField(required=False)

            conditional_fields = {
                'detail': {
                    'visible_when': {'category': {'value_is': 'a'}},
                },
            }

        form = TestForm()
        js = form.conditional_js()

        # Should include JavaScript manager
        self.assertIn('ConditionalFieldsManager', js)
        self.assertIn('data-conditional-fields-js', js)

        # Should include rules as JSON
        self.assertIn('data-conditional-rules', js)
        self.assertIn('"detail"', js)

    def test_conditional_js_rendered_once(self):
        """Test JavaScript is only rendered once per request."""
        ConditionalFieldsMixin.reset_js_rendered()

        class TestForm(ConditionalFieldsMixin, forms.Form):
            field1 = forms.CharField()
            conditional_fields = {'field1': {'visible_when': {}}}

        form1 = TestForm()
        form2 = TestForm()

        js1 = form1.conditional_js()
        js2 = form2.conditional_js()

        # First should have JS manager
        self.assertIn('data-conditional-fields-js', js1)
        # Second should not (already rendered)
        self.assertNotIn('data-conditional-fields-js', js2)
        # But both should have rules
        self.assertIn('data-conditional-rules', js1)
        self.assertIn('data-conditional-rules', js2)

    def test_conditional_context(self):
        """Test conditional context variables are included."""
        ConditionalFieldsMixin.reset_js_rendered()

        class TestForm(ConditionalFieldsMixin, forms.Form):
            pooled = forms.BooleanField(required=False)

            conditional_fields = {
                'pooled': {
                    'visible_when': {
                        '_context': {'is_group_member': True},
                    },
                },
            }

        form = TestForm(conditional_context={'is_group_member': True})
        js = form.conditional_js()

        # Context should be in the JSON
        self.assertIn('is_group_member', js)
        self.assertIn('true', js.lower())

    def test_get_conditional_context_override(self):
        """Test overriding get_conditional_context."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            pooled = forms.BooleanField(required=False)

            conditional_fields = {
                'pooled': {
                    'visible_when': {'_context': {'custom_var': True}},
                },
            }

            def get_conditional_context(self):
                return {'custom_var': True, 'another_var': False}

        form = TestForm()
        context = form.get_conditional_context()

        self.assertEqual(context['custom_var'], True)
        self.assertEqual(context['another_var'], False)

    def test_wrap_field(self):
        """Test wrap_field method generates correct HTML."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            detail = forms.CharField(required=False)

            conditional_fields = {
                'detail': {
                    'initially_hidden': True,
                },
            }

        form = TestForm()
        html = form.wrap_field('detail')

        self.assertIn('id="detail_wrap"', html)
        self.assertIn('d-none', html)  # Initially hidden

    def test_wrap_field_with_label(self):
        """Test wrap_field with label prefix."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            pooled = forms.BooleanField(required=False)

            conditional_fields = {
                'pooled': {'initially_hidden': True},
            }

        form = TestForm()
        html = form.wrap_field('pooled', 'Pooled?')

        self.assertIn('Pooled?', html)
        self.assertIn('id="pooled_wrap"', html)

    def test_wrap_field_initially_visible(self):
        """Test wrap_field when initially_hidden is False."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            detail = forms.CharField(required=False)

            conditional_fields = {
                'detail': {
                    'initially_hidden': False,
                },
            }

        form = TestForm()
        html = form.wrap_field('detail')

        self.assertIn('id="detail_wrap"', html)
        self.assertNotIn('d-none', html)  # Not hidden

    def test_empty_rules(self):
        """Test form with no conditional rules."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            field1 = forms.CharField()

        form = TestForm()
        js = form.conditional_js()

        # Should return empty string
        self.assertEqual(js, '')


class TestConditionalFieldsWithChainedSelect(TestCase):
    """Tests for ConditionalFieldsMixin combined with ChainedSelectMixin."""

    def test_combined_mixins(self):
        """Test ConditionalFieldsMixin works with ChainedSelectMixin."""

        class TestForm(ConditionalFieldsMixin, ChainedSelectMixin, forms.Form):
            category = ChainedChoiceField(
                choices=[('bg', 'Background'), ('mf', 'Merit/Flaw')]
            )
            example = ChainedChoiceField(
                parent_field='category',
                choices_map={
                    'bg': [('bg1', 'Allies', {'poolable': 'true'})],
                    'mf': [('mf1', 'Acute Sense')],
                },
            )
            value = forms.ChoiceField(required=False, choices=[])
            pooled = forms.BooleanField(required=False)

            conditional_fields = {
                'value': {
                    'visible_when': {'category': {'value_is': 'mf'}},
                },
                'pooled': {
                    'visible_when': {
                        'category': {'value_is': 'bg'},
                        'example': {'metadata_is': {'poolable': 'true'}},
                    },
                },
            }

        form = TestForm()

        # ChainedSelectMixin should configure chains
        self.assertIsNotNone(form.fields['category']._chain_name)

        # ConditionalFieldsMixin should have rules
        rules = form.get_conditional_rules()
        self.assertIn('pooled', rules)
        self.assertEqual(
            rules['pooled']['visible_when']['example']['metadata_is'],
            {'poolable': 'true'}
        )

    def test_combined_js_output(self):
        """Test combined form generates all necessary JavaScript."""
        ConditionalFieldsMixin.reset_js_rendered()

        class TestForm(ConditionalFieldsMixin, ChainedSelectMixin, forms.Form):
            category = ChainedChoiceField(
                choices=[('bg', 'Background'), ('mf', 'Merit/Flaw')]
            )
            example = ChainedChoiceField(
                parent_field='category',
                choices_map={
                    'bg': [('bg1', 'Allies')],
                    'mf': [('mf1', 'Acute Sense')],
                },
            )
            pooled = forms.BooleanField(required=False)

            conditional_fields = {
                'pooled': {
                    'visible_when': {'category': {'value_is': 'bg'}},
                },
            }

        form = TestForm()

        # Should have conditional JS
        conditional_js = form.conditional_js()
        self.assertIn('ConditionalFieldsManager', conditional_js)

        # ChainedSelect widget should render its JS (reset it first)
        from widgets.widgets.chained import ChainedSelect
        ChainedSelect.reset_js_rendered()

        category_html = str(form['category'])
        self.assertIn('ChainedSelectManager', category_html)


class TestConditionalFieldsRuleTypes(TestCase):
    """Tests for different rule types in conditional fields."""

    def test_value_in_rule(self):
        """Test value_in rule type."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C')])
            detail = forms.CharField(required=False)

            conditional_fields = {
                'detail': {
                    'hidden_when': {'category': {'value_in': ['a', 'b']}},
                },
            }

        form = TestForm()
        rules = form.get_conditional_rules()

        self.assertEqual(
            rules['detail']['hidden_when']['category']['value_in'],
            ['a', 'b']
        )

    def test_value_not_in_rule(self):
        """Test value_not_in rule type."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[('a', 'A'), ('b', 'B'), ('c', 'C')])
            detail = forms.CharField(required=False)

            conditional_fields = {
                'detail': {
                    'visible_when': {'category': {'value_not_in': ['a']}},
                },
            }

        form = TestForm()
        rules = form.get_conditional_rules()

        self.assertEqual(
            rules['detail']['visible_when']['category']['value_not_in'],
            ['a']
        )

    def test_metadata_truthy_rule(self):
        """Test metadata_truthy rule type."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            example = forms.ChoiceField(choices=[])
            pooled = forms.BooleanField(required=False)

            conditional_fields = {
                'pooled': {
                    'visible_when': {'example': {'metadata_truthy': 'poolable'}},
                },
            }

        form = TestForm()
        rules = form.get_conditional_rules()

        self.assertEqual(
            rules['pooled']['visible_when']['example']['metadata_truthy'],
            'poolable'
        )

    def test_multiple_conditions(self):
        """Test multiple conditions in visible_when."""

        class TestForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[])
            example = forms.ChoiceField(choices=[])
            pooled = forms.BooleanField(required=False)

            conditional_fields = {
                'pooled': {
                    'visible_when': {
                        'category': {'value_is': 'bg'},
                        'example': {'metadata_is': {'poolable': 'true'}},
                        '_context': {'is_group_member': True},
                    },
                },
            }

        form = TestForm(conditional_context={'is_group_member': True})
        rules = form.get_conditional_rules()
        context = form.get_conditional_context()

        # Should have all three conditions
        visible_when = rules['pooled']['visible_when']
        self.assertIn('category', visible_when)
        self.assertIn('example', visible_when)
        self.assertIn('_context', visible_when)

        # Context should be passed through
        self.assertTrue(context['is_group_member'])


class TestImports(TestCase):
    """Tests for module exports."""

    def test_conditional_fields_mixin_export(self):
        """Test ConditionalFieldsMixin is exported from widgets package."""
        from widgets import ConditionalFieldsMixin

        self.assertIsNotNone(ConditionalFieldsMixin)
