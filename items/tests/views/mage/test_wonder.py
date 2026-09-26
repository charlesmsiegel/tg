"""Tests for wonder views."""

from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext

from characters.models.mage.resonance import Resonance
from items.models.mage import Wonder, WonderResonanceRating


class TestWonderDetailViewQueryOptimization(TestCase):
    """Test that WonderDetailView uses optimized queries."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.wonder = Wonder.objects.create(name="Test Wonder", rank=3, owner=self.user)
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
        for i in range(5, 10):
            resonance = Resonance.objects.create(name=f"Resonance {i}")
            WonderResonanceRating.objects.create(wonder=self.wonder, resonance=resonance, rating=1)
        with CaptureQueriesContext(connection) as expanded:
            self.client.get(f"/items/mage/wonder/{self.wonder.pk}/")
        self.assertLessEqual(len(expanded.captured_queries), query_count + 2)

    def test_resonance_is_in_context(self):
        """Test that resonance ratings are included in context."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/items/mage/wonder/{self.wonder.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("resonance", response.context)
        self.assertEqual(response.context["resonance"].count(), 5)


class TestWonderCreateView(TestCase):
    """Test WonderCreateView functionality."""

    def test_create_view_redirects_to_saved_object(self):
        from items.models.mage.wonder import Wonder
        from items.views.mage.wonder import WonderCreateView

        obj = Wonder.objects.create(name="Saved Wonder")
        view = WonderCreateView()
        view.object = obj
        self.assertEqual(view.get_success_url(), obj.get_absolute_url())


class TestWonderUpdateView(TestCase):
    """Test WonderUpdateView functionality."""

    def test_update_view_redirects_to_saved_object(self):
        from items.models.mage.wonder import Wonder
        from items.views.mage.wonder import WonderUpdateView

        obj = Wonder.objects.create(name="Saved Wonder")
        view = WonderUpdateView()
        view.object = obj
        self.assertEqual(view.get_success_url(), obj.get_absolute_url())


class TestWonderFormTemplateJS(TestCase):
    """Test that wonder form template includes required JavaScript functionality."""

    def test_form_include_has_toggle_effect_fields(self):
        """The form loads the static asset containing its effect-field toggle."""
        from pathlib import Path

        from django.contrib.staticfiles import finders
        from django.template import loader

        template = loader.get_template("items/mage/wonder/form_include.html")
        template_source = template.template.source

        self.assertIn("{% static 'items/js/wonder-form.js' %}", template_source)
        script = Path(finders.find("items/js/wonder-form.js")).read_text(encoding="utf-8")
        self.assertIn("function toggleEffectFields", script)

    def test_form_include_has_init_wonder_form(self):
        """The static asset initializes the form when the DOM is ready."""
        from pathlib import Path

        from django.contrib.staticfiles import finders

        script = Path(finders.find("items/js/wonder-form.js")).read_text(encoding="utf-8")
        self.assertIn("function initWonderForm", script)
        self.assertIn("document.addEventListener('DOMContentLoaded', initWonderForm)", script)
