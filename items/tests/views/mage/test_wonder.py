"""Tests for wonder views."""

from characters.models.mage.resonance import Resonance
from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from items.models.mage import Wonder, WonderResonanceRating


class TestWonderDetailViewQueryOptimization(TestCase):
    """Test that WonderDetailView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.wonder = Wonder.objects.create(name="Test Wonder", rank=3)
        for i in range(5):
            resonance = Resonance.objects.create(name=f"Resonance {i}")
            WonderResonanceRating.objects.create(
                wonder=self.wonder, resonance=resonance, rating=i + 1
            )

    def test_detail_view_query_count_is_bounded(self):
        """Test that detail view query count doesn't scale with number of resonances."""
        self.client.login(username="testuser", password="password")

        with CaptureQueriesContext(connection) as context:
            response = self.client.get(f"/items/mage/wonder/{self.wonder.pk}/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # With select_related on resonance, queries should be bounded
        # regardless of number of resonance ratings
        self.assertLessEqual(
            query_count,
            15,
            f"Too many queries ({query_count}). Detail view may have N+1 issue.",
        )

    def test_resonance_is_in_context(self):
        """Test that resonance ratings are included in context."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/items/mage/wonder/{self.wonder.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("resonance", response.context)
        self.assertEqual(response.context["resonance"].count(), 5)


class TestWonderCreateView(TestCase):
    """Test WonderCreateView functionality."""

    def test_create_view_has_get_success_url_method(self):
        """Test that WonderCreateView has explicit get_success_url method."""
        from items.views.mage.wonder import WonderCreateView

        self.assertTrue(
            hasattr(WonderCreateView, "get_success_url"),
            "WonderCreateView should have get_success_url method",
        )
        # Verify it's defined on the class itself, not inherited
        self.assertIn(
            "get_success_url",
            WonderCreateView.__dict__,
            "get_success_url should be explicitly defined on WonderCreateView",
        )


class TestWonderUpdateView(TestCase):
    """Test WonderUpdateView functionality."""

    def test_update_view_has_get_success_url_method(self):
        """Test that WonderUpdateView has explicit get_success_url method."""
        from items.views.mage.wonder import WonderUpdateView

        self.assertTrue(
            hasattr(WonderUpdateView, "get_success_url"),
            "WonderUpdateView should have get_success_url method",
        )
        # Verify it's defined on the class itself, not inherited
        self.assertIn(
            "get_success_url",
            WonderUpdateView.__dict__,
            "get_success_url should be explicitly defined on WonderUpdateView",
        )


class TestWonderFormTemplateStaticJS(TestCase):
    """Test that wonder form template includes static JavaScript file."""

    def test_form_include_loads_static_wonder_form_js(self):
        """Wonder form_include.html loads wonder-form.js from static files."""
        from django.template import loader

        template = loader.get_template("items/mage/wonder/form_include.html")

        # Verify the template source contains the static file reference
        template_source = template.template.source
        self.assertIn("js/wonder-form.js", template_source)
        self.assertIn("{% static", template_source)

    def test_form_include_does_not_contain_inline_script(self):
        """Wonder form_include.html does not contain large inline scripts."""
        from django.template import loader

        template = loader.get_template("items/mage/wonder/form_include.html")
        template_source = template.template.source

        # The template should not have inline function definitions
        self.assertNotIn("function toggleEffectFields", template_source)
        self.assertNotIn("function addForm", template_source)
        self.assertNotIn("function resetEffectsFormset", template_source)
