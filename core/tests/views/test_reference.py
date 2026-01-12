"""Tests for reference view factory module."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.test import RequestFactory, TestCase
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.mage import Sphere
from core.mixins import MessageMixin
from core.views.generic import CachedDetailView, CachedListView
from core.views.reference import ReferenceViewSet, create_reference_views

User = get_user_model()


class CreateReferenceViewsTest(TestCase):
    """Test create_reference_views() factory function."""

    def test_creates_four_views(self):
        """Test that factory generates all four view types."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name", "property_name"],
        )
        self.assertIn("detail", views)
        self.assertIn("list", views)
        self.assertIn("create", views)
        self.assertIn("update", views)

    def test_views_have_correct_model(self):
        """Test that all generated views have correct model attribute."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name", "property_name"],
        )
        self.assertEqual(views["detail"].model, Sphere)
        self.assertEqual(views["list"].model, Sphere)
        self.assertEqual(views["create"].model, Sphere)
        self.assertEqual(views["update"].model, Sphere)

    def test_template_paths_generated_correctly(self):
        """Test that template paths are auto-generated from app_prefix and model."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertEqual(
            views["detail"].template_name, "characters/mage/sphere/detail.html"
        )
        self.assertEqual(
            views["list"].template_name, "characters/mage/sphere/list.html"
        )
        self.assertEqual(
            views["create"].template_name, "characters/mage/sphere/form.html"
        )
        self.assertEqual(
            views["update"].template_name, "characters/mage/sphere/form.html"
        )

    def test_custom_template_override(self):
        """Test that custom templates override auto-generated paths."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
            detail_template="custom/detail.html",
            list_template="custom/list.html",
            form_template="custom/form.html",
        )
        self.assertEqual(views["detail"].template_name, "custom/detail.html")
        self.assertEqual(views["list"].template_name, "custom/list.html")
        self.assertEqual(views["create"].template_name, "custom/form.html")
        self.assertEqual(views["update"].template_name, "custom/form.html")

    def test_custom_model_name_affects_path(self):
        """Test that model_name parameter affects template paths."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
            model_name="custom_sphere",
        )
        self.assertEqual(
            views["detail"].template_name, "characters/mage/custom_sphere/detail.html"
        )

    def test_cached_true_uses_cached_views(self):
        """Test that cached=True uses CachedDetailView/CachedListView."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
            cached=True,
        )
        self.assertTrue(issubclass(views["detail"], CachedDetailView))
        self.assertTrue(issubclass(views["list"], CachedListView))

    def test_cached_false_uses_regular_views(self):
        """Test that cached=False uses regular DetailView/ListView."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
            cached=False,
        )
        self.assertTrue(issubclass(views["detail"], DetailView))
        self.assertTrue(issubclass(views["list"], ListView))
        # Should NOT be cached views
        self.assertFalse(issubclass(views["detail"], CachedDetailView))
        self.assertFalse(issubclass(views["list"], CachedListView))

    def test_create_view_has_login_required_mixin(self):
        """Test that CreateView includes LoginRequiredMixin for security."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertTrue(issubclass(views["create"], LoginRequiredMixin))

    def test_update_view_has_login_required_mixin(self):
        """Test that UpdateView includes LoginRequiredMixin for security."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertTrue(issubclass(views["update"], LoginRequiredMixin))

    def test_create_view_has_message_mixin(self):
        """Test that CreateView includes MessageMixin."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertTrue(issubclass(views["create"], MessageMixin))

    def test_update_view_has_message_mixin(self):
        """Test that UpdateView includes MessageMixin."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertTrue(issubclass(views["update"], MessageMixin))

    def test_create_view_is_createview(self):
        """Test that create view is a CreateView subclass."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertTrue(issubclass(views["create"], CreateView))

    def test_update_view_is_updateview(self):
        """Test that update view is an UpdateView subclass."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertTrue(issubclass(views["update"], UpdateView))

    def test_list_view_has_correct_ordering(self):
        """Test that ListView has correct default ordering."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertEqual(views["list"].ordering, ["name"])

    def test_custom_ordering(self):
        """Test that custom ordering is applied to ListView."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
            ordering=["property_name", "-name"],
        )
        self.assertEqual(views["list"].ordering, ["property_name", "-name"])

    def test_create_view_has_correct_fields(self):
        """Test that CreateView has correct fields list."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name", "property_name"],
        )
        self.assertEqual(views["create"].fields, ["name", "property_name"])

    def test_update_view_has_correct_fields(self):
        """Test that UpdateView has correct fields list."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name", "property_name"],
        )
        self.assertEqual(views["update"].fields, ["name", "property_name"])

    def test_success_message_capitalized(self):
        """Test that success messages have capitalized verbose_name."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertEqual(views["create"].success_message, "Sphere created successfully.")
        self.assertEqual(views["update"].success_message, "Sphere updated successfully.")

    def test_error_messages_use_verbose_name(self):
        """Test that error messages use model verbose_name."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertEqual(
            views["create"].error_message, "There was an error creating the Sphere."
        )
        self.assertEqual(
            views["update"].error_message, "There was an error updating the Sphere."
        )

    def test_extra_context_applied_to_all_views(self):
        """Test that extra_context is applied to all view types."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
            extra_context={"custom_key": "custom_value"},
        )
        self.assertEqual(
            views["detail"].extra_context, {"custom_key": "custom_value"}
        )
        self.assertEqual(views["list"].extra_context, {"custom_key": "custom_value"})
        self.assertEqual(
            views["create"].extra_context, {"custom_key": "custom_value"}
        )
        self.assertEqual(
            views["update"].extra_context, {"custom_key": "custom_value"}
        )

    def test_view_class_names_generated_correctly(self):
        """Test that generated view classes have correct names."""
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
        )
        self.assertEqual(views["detail"].__name__, "SphereDetailView")
        self.assertEqual(views["list"].__name__, "SphereListView")
        self.assertEqual(views["create"].__name__, "SphereCreateView")
        self.assertEqual(views["update"].__name__, "SphereUpdateView")


class ReferenceViewSetTest(TestCase):
    """Test ReferenceViewSet metaclass."""

    def test_viewset_generates_views(self):
        """Test that ReferenceViewSet metaclass generates all views."""

        class SphereViews(ReferenceViewSet):
            model = Sphere
            app_prefix = "characters/mage"
            fields = ["name", "property_name"]

        self.assertTrue(hasattr(SphereViews, "detail_view"))
        self.assertTrue(hasattr(SphereViews, "list_view"))
        self.assertTrue(hasattr(SphereViews, "create_view"))
        self.assertTrue(hasattr(SphereViews, "update_view"))

    def test_viewset_views_have_correct_model(self):
        """Test that viewset-generated views have correct model."""

        class SphereViews(ReferenceViewSet):
            model = Sphere
            app_prefix = "characters/mage"
            fields = ["name", "property_name"]

        self.assertEqual(SphereViews.detail_view.model, Sphere)
        self.assertEqual(SphereViews.list_view.model, Sphere)
        self.assertEqual(SphereViews.create_view.model, Sphere)
        self.assertEqual(SphereViews.update_view.model, Sphere)

    def test_viewset_with_custom_ordering(self):
        """Test that custom ordering is respected in viewset."""

        class SphereViews(ReferenceViewSet):
            model = Sphere
            app_prefix = "characters/mage"
            fields = ["name"]
            ordering = ["property_name", "-name"]

        self.assertEqual(
            SphereViews.list_view.ordering, ["property_name", "-name"]
        )

    def test_viewset_with_cached_false(self):
        """Test that cached=False works in viewset."""

        class SphereViews(ReferenceViewSet):
            model = Sphere
            app_prefix = "characters/mage"
            fields = ["name"]
            cached = False

        self.assertFalse(issubclass(SphereViews.detail_view, CachedDetailView))
        self.assertFalse(issubclass(SphereViews.list_view, CachedListView))

    def test_incomplete_viewset_without_model_skips_generation(self):
        """Test that incomplete viewset without model doesn't generate views."""

        class IncompleteViews(ReferenceViewSet):
            pass  # No model defined

        # Should not have views attached
        self.assertFalse(hasattr(IncompleteViews, "detail_view"))

    def test_viewset_missing_app_prefix_raises_error(self):
        """Test that missing app_prefix raises ValueError."""
        with self.assertRaises(ValueError) as cm:

            class BadViews(ReferenceViewSet):
                model = Sphere
                # Missing app_prefix
                fields = ["name"]

        self.assertIn("app_prefix", str(cm.exception))

    def test_viewset_missing_fields_raises_error(self):
        """Test that missing fields raises ValueError."""
        with self.assertRaises(ValueError) as cm:

            class BadViews(ReferenceViewSet):
                model = Sphere
                app_prefix = "characters/mage"
                # Missing fields

        self.assertIn("fields", str(cm.exception))

    def test_viewset_empty_fields_raises_error(self):
        """Test that empty fields list raises ValueError."""
        with self.assertRaises(ValueError) as cm:

            class BadViews(ReferenceViewSet):
                model = Sphere
                app_prefix = "characters/mage"
                fields = []  # Empty

        self.assertIn("fields", str(cm.exception))


class ReferenceViewIntegrationTest(TestCase):
    """Integration tests for generated reference views.

    Note: These tests verify view behavior without full database setup.
    They test the LoginRequiredMixin redirect behavior using AnonymousUser.
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_create_view_redirects_anonymous_user(self):
        """Test that create view redirects unauthenticated users."""
        from django.contrib.auth.models import AnonymousUser

        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name", "property_name"],
        )

        request = self.factory.get("/create/sphere/")
        request.user = AnonymousUser()

        view = views["create"].as_view()
        response = view(request)

        # Should redirect to login (302)
        self.assertEqual(response.status_code, 302)

    def test_update_view_redirects_anonymous_user(self):
        """Test that update view redirects unauthenticated users."""
        from django.contrib.auth.models import AnonymousUser

        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name", "property_name"],
        )

        request = self.factory.get("/update/sphere/1/")
        request.user = AnonymousUser()

        view = views["update"].as_view()
        response = view(request, pk=1)

        # Should redirect to login (302)
        self.assertEqual(response.status_code, 302)

    def test_detail_view_allows_anonymous_access(self):
        """Test that detail view is accessible without authentication.

        Note: This tests view inheritance, not actual rendering.
        DetailView for reference data should be public per CLAUDE.md.
        """
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
            cached=False,
        )
        # Verify detail view does NOT have LoginRequiredMixin
        self.assertFalse(issubclass(views["detail"], LoginRequiredMixin))

    def test_list_view_allows_anonymous_access(self):
        """Test that list view is accessible without authentication.

        Note: This tests view inheritance, not actual rendering.
        ListView for reference data should be public per CLAUDE.md.
        """
        views = create_reference_views(
            model=Sphere,
            app_prefix="characters/mage",
            fields=["name"],
            cached=False,
        )
        # Verify list view does NOT have LoginRequiredMixin
        self.assertFalse(issubclass(views["list"], LoginRequiredMixin))
