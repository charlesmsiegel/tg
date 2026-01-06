"""
Tests for the widgets app point pool functionality.
"""

from django import forms
from django.test import TestCase
from widgets import (
    DistributionPoolMixin,
    PointPoolInput,
    PointPoolMixin,
    PointPoolSelect,
    SimplePoolMixin,
)


class TestPointPoolInput(TestCase):
    """Tests for PointPoolInput widget."""

    def test_widget_attributes(self):
        """Test widget adds correct data attributes."""
        widget = PointPoolInput(
            pool_name="test_pool",
            pool_group="test_group",
        )
        attrs = widget.build_attrs({})
        self.assertEqual(attrs["data-point-pool"], "true")
        self.assertEqual(attrs["data-pool-name"], "test_pool")
        self.assertEqual(attrs["data-pool-group"], "test_group")

    def test_widget_css_class(self):
        """Test widget adds CSS class."""
        widget = PointPoolInput()
        attrs = widget.build_attrs({})
        self.assertIn("point-pool-input", attrs["class"])

    def test_widget_render_includes_script(self):
        """Test widget renders JavaScript."""
        PointPoolInput.reset_js_rendered()
        widget = PointPoolInput(
            pool_name="test",
            is_root=True,
            pool_config={"mode": "simple", "total_budget": 10},
        )
        html = widget.render("test_field", "5")
        self.assertIn("data-point-pool-js", html)
        self.assertIn("PointPoolManager", html)

    def test_widget_render_config(self):
        """Test widget embeds config for root position."""
        PointPoolInput.reset_js_rendered()
        config = {"mode": "simple", "total_budget": 10, "min_value": 0, "max_value": 5}
        widget = PointPoolInput(
            pool_name="test",
            is_root=True,
            pool_config=config,
        )
        html = widget.render("test_field", "3")
        self.assertIn("data-pool-config", html)
        self.assertIn('"total_budget": 10', html)

    def test_widget_js_rendered_once(self):
        """Test JavaScript is only rendered once."""
        PointPoolInput.reset_js_rendered()
        widget1 = PointPoolInput(pool_name="test1", is_root=True, pool_config={})
        widget2 = PointPoolInput(pool_name="test2", is_root=True, pool_config={})

        html1 = widget1.render("field1", "")
        html2 = widget2.render("field2", "")

        # JS should be in first render only
        self.assertIn("data-point-pool-js", html1)
        self.assertNotIn("data-point-pool-js", html2)


class TestPointPoolSelect(TestCase):
    """Tests for PointPoolSelect widget."""

    def test_widget_attributes(self):
        """Test widget adds correct data attributes."""
        widget = PointPoolSelect(
            pool_name="test_pool",
            pool_group="test_group",
            choices=[(0, "0"), (1, "1"), (2, "2")],
        )
        attrs = widget.build_attrs({})
        self.assertEqual(attrs["data-point-pool"], "true")
        self.assertEqual(attrs["data-pool-name"], "test_pool")
        self.assertEqual(attrs["data-pool-group"], "test_group")

    def test_widget_css_class(self):
        """Test widget adds CSS class."""
        widget = PointPoolSelect(choices=[(0, "0")])
        attrs = widget.build_attrs({})
        self.assertIn("point-pool-select", attrs["class"])

    def test_widget_render_includes_script(self):
        """Test widget renders JavaScript."""
        PointPoolInput.reset_js_rendered()  # Both share the flag
        widget = PointPoolSelect(
            pool_name="test",
            is_root=True,
            pool_config={"mode": "simple"},
            choices=[(0, "0"), (1, "1")],
        )
        html = widget.render("test_field", "1")
        self.assertIn("data-point-pool-js", html)


class TestSimplePoolMixin(TestCase):
    """Tests for SimplePoolMixin form mixin."""

    def test_simple_pool_form_valid(self):
        """Test form with valid simple pool allocation."""

        class TestForm(SimplePoolMixin, forms.Form):
            simple_pool_name = "backgrounds"
            simple_pool_budget = 7
            simple_pool_min = 0
            simple_pool_max = 5
            pool_fields = ["allies", "contacts", "resources"]

            allies = forms.IntegerField(min_value=0, max_value=5)
            contacts = forms.IntegerField(min_value=0, max_value=5)
            resources = forms.IntegerField(min_value=0, max_value=5)

        form = TestForm(data={"allies": 3, "contacts": 2, "resources": 2})
        self.assertTrue(form.is_valid())

    def test_simple_pool_form_over_budget(self):
        """Test form rejects allocation over budget."""

        class TestForm(SimplePoolMixin, forms.Form):
            simple_pool_name = "backgrounds"
            simple_pool_budget = 7
            simple_pool_min = 0
            simple_pool_max = 5
            pool_fields = ["allies", "contacts", "resources"]

            allies = forms.IntegerField(min_value=0, max_value=5)
            contacts = forms.IntegerField(min_value=0, max_value=5)
            resources = forms.IntegerField(min_value=0, max_value=5)

        form = TestForm(data={"allies": 5, "contacts": 5, "resources": 5})
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("exceeds", form.errors["__all__"][0].lower())

    def test_simple_pool_form_under_budget(self):
        """Test form rejects allocation under budget."""

        class TestForm(SimplePoolMixin, forms.Form):
            simple_pool_name = "backgrounds"
            simple_pool_budget = 7
            simple_pool_min = 0
            simple_pool_max = 5
            pool_fields = ["allies", "contacts", "resources"]

            allies = forms.IntegerField(min_value=0, max_value=5)
            contacts = forms.IntegerField(min_value=0, max_value=5)
            resources = forms.IntegerField(min_value=0, max_value=5)

        form = TestForm(data={"allies": 1, "contacts": 1, "resources": 1})
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("exactly", form.errors["__all__"][0].lower())

    def test_simple_pool_form_invalid_range(self):
        """Test form rejects values outside range."""

        class TestForm(SimplePoolMixin, forms.Form):
            simple_pool_name = "test"
            simple_pool_budget = 10
            simple_pool_min = 1
            simple_pool_max = 5
            pool_fields = ["field1", "field2"]

            field1 = forms.IntegerField(min_value=1, max_value=5)
            field2 = forms.IntegerField(min_value=1, max_value=5)

        form = TestForm(data={"field1": 6, "field2": 4})
        self.assertFalse(form.is_valid())
        self.assertIn("field1", form.errors)


class TestDistributionPoolMixin(TestCase):
    """Tests for DistributionPoolMixin form mixin."""

    def test_distribution_form_valid_primary_secondary_tertiary(self):
        """Test form with valid distribution allocation."""

        class TestForm(DistributionPoolMixin, forms.Form):
            distribution_pool_name = "attributes"
            distribution_groups = {
                "physical": ["strength", "dexterity", "stamina"],
                "social": ["charisma", "manipulation", "appearance"],
                "mental": ["perception", "intelligence", "wits"],
            }
            distribution_targets = [6, 8, 10]  # 3+3=6, 3+5=8, 3+7=10
            distribution_min = 1
            distribution_max = 5

            # Physical (primary = 10 total, 7 dots added to base 3)
            strength = forms.IntegerField(min_value=1, max_value=5)
            dexterity = forms.IntegerField(min_value=1, max_value=5)
            stamina = forms.IntegerField(min_value=1, max_value=5)
            # Social (secondary = 8 total, 5 dots added to base 3)
            charisma = forms.IntegerField(min_value=1, max_value=5)
            manipulation = forms.IntegerField(min_value=1, max_value=5)
            appearance = forms.IntegerField(min_value=1, max_value=5)
            # Mental (tertiary = 6 total, 3 dots added to base 3)
            perception = forms.IntegerField(min_value=1, max_value=5)
            intelligence = forms.IntegerField(min_value=1, max_value=5)
            wits = forms.IntegerField(min_value=1, max_value=5)

        # Physical=10 (4+3+3), Social=8 (3+3+2), Mental=6 (2+2+2)
        form = TestForm(
            data={
                "strength": 4,
                "dexterity": 3,
                "stamina": 3,
                "charisma": 3,
                "manipulation": 3,
                "appearance": 2,
                "perception": 2,
                "intelligence": 2,
                "wits": 2,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_distribution_form_any_permutation_valid(self):
        """Test that any permutation of targets is valid."""

        class TestForm(DistributionPoolMixin, forms.Form):
            distribution_pool_name = "attributes"
            distribution_groups = {
                "physical": ["str", "dex", "sta"],
                "social": ["cha", "man", "app"],
                "mental": ["per", "int", "wit"],
            }
            distribution_targets = [6, 8, 10]
            distribution_min = 1
            distribution_max = 5

            str = forms.IntegerField(min_value=1, max_value=5)
            dex = forms.IntegerField(min_value=1, max_value=5)
            sta = forms.IntegerField(min_value=1, max_value=5)
            cha = forms.IntegerField(min_value=1, max_value=5)
            man = forms.IntegerField(min_value=1, max_value=5)
            app = forms.IntegerField(min_value=1, max_value=5)
            per = forms.IntegerField(min_value=1, max_value=5)
            int = forms.IntegerField(min_value=1, max_value=5)
            wit = forms.IntegerField(min_value=1, max_value=5)

        # Mental=10, Physical=8, Social=6 (different permutation)
        form = TestForm(
            data={
                "str": 3,
                "dex": 3,
                "sta": 2,
                "cha": 2,
                "man": 2,
                "app": 2,
                "per": 4,
                "int": 3,
                "wit": 3,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_distribution_form_invalid_distribution(self):
        """Test form rejects invalid distribution."""

        class TestForm(DistributionPoolMixin, forms.Form):
            distribution_pool_name = "attributes"
            distribution_groups = {
                "physical": ["str", "dex", "sta"],
                "social": ["cha", "man", "app"],
                "mental": ["per", "int", "wit"],
            }
            distribution_targets = [6, 8, 10]
            distribution_min = 1
            distribution_max = 5

            str = forms.IntegerField(min_value=1, max_value=5)
            dex = forms.IntegerField(min_value=1, max_value=5)
            sta = forms.IntegerField(min_value=1, max_value=5)
            cha = forms.IntegerField(min_value=1, max_value=5)
            man = forms.IntegerField(min_value=1, max_value=5)
            app = forms.IntegerField(min_value=1, max_value=5)
            per = forms.IntegerField(min_value=1, max_value=5)
            int = forms.IntegerField(min_value=1, max_value=5)
            wit = forms.IntegerField(min_value=1, max_value=5)

        # All groups = 8 (invalid, not 6/8/10)
        form = TestForm(
            data={
                "str": 3,
                "dex": 3,
                "sta": 2,
                "cha": 3,
                "man": 3,
                "app": 2,
                "per": 3,
                "int": 3,
                "wit": 2,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("distribution", form.errors["__all__"][0].lower())

    def test_distribution_form_auto_pool_fields(self):
        """Test pool_fields is automatically generated from groups."""

        class TestForm(DistributionPoolMixin, forms.Form):
            distribution_pool_name = "test"
            distribution_groups = {
                "group1": ["a", "b"],
                "group2": ["c", "d"],
            }
            distribution_targets = [4, 6]
            distribution_min = 1
            distribution_max = 5

            a = forms.IntegerField(min_value=1, max_value=5)
            b = forms.IntegerField(min_value=1, max_value=5)
            c = forms.IntegerField(min_value=1, max_value=5)
            d = forms.IntegerField(min_value=1, max_value=5)

        form = TestForm()
        pool_fields = form.pool_fields
        self.assertIn("a", pool_fields)
        self.assertIn("b", pool_fields)
        self.assertIn("c", pool_fields)
        self.assertIn("d", pool_fields)


class TestPointPoolMixin(TestCase):
    """Tests for base PointPoolMixin."""

    def test_mixin_configures_widgets(self):
        """Test mixin sets up point pool widgets on fields."""

        class TestForm(PointPoolMixin, forms.Form):
            pool_config = {
                "mode": "simple",
                "pool_name": "test",
                "total_budget": 10,
                "min_value": 0,
                "max_value": 5,
            }
            pool_fields = ["field1", "field2"]

            field1 = forms.IntegerField(min_value=0, max_value=5)
            field2 = forms.IntegerField(min_value=0, max_value=5)

        PointPoolInput.reset_js_rendered()
        form = TestForm()

        # Check widgets were configured
        self.assertIsInstance(form.fields["field1"].widget, PointPoolInput)
        self.assertIsInstance(form.fields["field2"].widget, PointPoolInput)

        # Check pool_name is set
        self.assertEqual(form.fields["field1"].widget.pool_name, "test")
        self.assertEqual(form.fields["field2"].widget.pool_name, "test")

    def test_mixin_with_choice_fields(self):
        """Test mixin uses PointPoolSelect for choice fields."""

        class TestForm(PointPoolMixin, forms.Form):
            pool_config = {
                "mode": "simple",
                "pool_name": "test",
                "total_budget": 5,
            }
            pool_fields = ["rating"]

            rating = forms.ChoiceField(
                choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
            )

        PointPoolInput.reset_js_rendered()
        form = TestForm()

        self.assertIsInstance(form.fields["rating"].widget, PointPoolSelect)

    def test_mixin_distribution_mode_sets_groups(self):
        """Test distribution mode sets pool_group on widgets."""

        class TestForm(PointPoolMixin, forms.Form):
            pool_config = {
                "mode": "distribution",
                "pool_name": "attrs",
                "groups": {
                    "physical": ["str", "dex"],
                    "mental": ["int", "wit"],
                },
                "targets": [4, 6],
            }
            pool_fields = ["str", "dex", "int", "wit"]

            str = forms.IntegerField(min_value=1, max_value=5)
            dex = forms.IntegerField(min_value=1, max_value=5)
            int = forms.IntegerField(min_value=1, max_value=5)
            wit = forms.IntegerField(min_value=1, max_value=5)

        PointPoolInput.reset_js_rendered()
        form = TestForm()

        self.assertEqual(form.fields["str"].widget.pool_group, "physical")
        self.assertEqual(form.fields["dex"].widget.pool_group, "physical")
        self.assertEqual(form.fields["int"].widget.pool_group, "mental")
        self.assertEqual(form.fields["wit"].widget.pool_group, "mental")


class TestWidgetsPointPoolImports(TestCase):
    """Tests that point pool components export correctly."""

    def test_all_exports_available(self):
        """Test all expected point pool exports are available."""
        from widgets import (
            DistributionPoolMixin,
            PointPoolInput,
            PointPoolMixin,
            PointPoolSelect,
            SimplePoolMixin,
        )

        # Verify imports work
        self.assertIsNotNone(PointPoolInput)
        self.assertIsNotNone(PointPoolSelect)
        self.assertIsNotNone(PointPoolMixin)
        self.assertIsNotNone(SimplePoolMixin)
        self.assertIsNotNone(DistributionPoolMixin)
