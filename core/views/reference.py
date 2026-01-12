"""
Reference Model View Factory

This module provides a factory function to generate standard CRUD views
for reference models (Clan, Tribe, Sphere, Archetype, etc.).

The typical reference model has 4 views with nearly identical structure:
- DetailView: Display a single object
- ListView: Display all objects
- CreateView: Create a new object
- UpdateView: Edit an existing object

The create_reference_views() factory reduces ~30 lines per model to ~5 lines.

Example usage:
    # In characters/views/mage/sphere.py
    from core.views.reference import create_reference_views
    from characters.models.mage import Sphere

    views = create_reference_views(
        model=Sphere,
        app_prefix="characters/mage",
        fields=["name", "property_name"],
    )

    SphereDetailView = views["detail"]
    SphereListView = views["list"]
    SphereCreateView = views["create"]
    SphereUpdateView = views["update"]

Or using class-based configuration:
    from core.views.reference import ReferenceViewSet

    class SphereViews(ReferenceViewSet):
        model = Sphere
        app_prefix = "characters/mage"
        fields = ["name", "property_name"]

    # Access views via class attributes
    SphereDetailView = SphereViews.detail_view
    SphereListView = SphereViews.list_view
    SphereCreateView = SphereViews.create_view
    SphereUpdateView = SphereViews.update_view
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import MessageMixin
from core.views.generic import CachedDetailView, CachedListView


def create_reference_views(
    model,
    app_prefix,
    fields,
    model_name=None,
    ordering=None,
    cached=True,
    detail_template=None,
    list_template=None,
    form_template=None,
    extra_context=None,
):
    """
    Create standard CRUD views for a reference model.

    Args:
        model: The Django model class
        app_prefix: Template path prefix (e.g., "characters/mage")
        fields: List of field names for create/update forms
        model_name: Override for model name in templates (default: model.__name__.lower())
        ordering: List ordering field(s) (default: ["name"])
        cached: Whether to cache detail/list views (default: True)
        detail_template: Override detail template path
        list_template: Override list template path
        form_template: Override form template path
        extra_context: Extra context to add to all views

    Returns:
        Dict with keys: 'detail', 'list', 'create', 'update'
    """
    name = model_name or model.__name__.lower()
    ordering = ordering or ["name"]
    verbose_name = model._meta.verbose_name

    # Build template paths
    base_path = f"{app_prefix}/{name}"
    detail_tpl = detail_template or f"{base_path}/detail.html"
    list_tpl = list_template or f"{base_path}/list.html"
    form_tpl = form_template or f"{base_path}/form.html"

    # Build extra context
    context = extra_context or {}

    # Select base classes based on caching preference
    detail_base = CachedDetailView if cached else DetailView
    list_base = CachedListView if cached else ListView

    # Create DetailView
    detail_attrs = {
        "model": model,
        "template_name": detail_tpl,
    }
    if context:
        detail_attrs["extra_context"] = context

    detail_class = type(f"{model.__name__}DetailView", (detail_base,), detail_attrs)

    # Create ListView
    list_attrs = {
        "model": model,
        "template_name": list_tpl,
        "ordering": ordering,
    }
    if context:
        list_attrs["extra_context"] = context

    list_class = type(f"{model.__name__}ListView", (list_base,), list_attrs)

    # Create CreateView with LoginRequiredMixin for security
    create_attrs = {
        "model": model,
        "fields": fields,
        "template_name": form_tpl,
        "success_message": f"{verbose_name.capitalize()} created successfully.",
        "error_message": f"There was an error creating the {verbose_name}.",
    }
    if context:
        create_attrs["extra_context"] = context

    create_class = type(
        f"{model.__name__}CreateView",
        (LoginRequiredMixin, MessageMixin, CreateView),
        create_attrs,
    )

    # Create UpdateView with LoginRequiredMixin for security
    update_attrs = {
        "model": model,
        "fields": fields,
        "template_name": form_tpl,
        "success_message": f"{verbose_name.capitalize()} updated successfully.",
        "error_message": f"There was an error updating the {verbose_name}.",
    }
    if context:
        update_attrs["extra_context"] = context

    update_class = type(
        f"{model.__name__}UpdateView",
        (LoginRequiredMixin, MessageMixin, UpdateView),
        update_attrs,
    )

    return {
        "detail": detail_class,
        "list": list_class,
        "create": create_class,
        "update": update_class,
    }


class ReferenceViewSetMeta(type):
    """Metaclass that auto-generates view classes from ReferenceViewSet attributes."""

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Skip processing for the base class
        if name == "ReferenceViewSet":
            return cls

        # Validate required attributes
        if not hasattr(cls, "model") or cls.model is None:
            return cls  # Allow incomplete subclasses

        # Validate app_prefix is set
        app_prefix = getattr(cls, "app_prefix", "")
        if not app_prefix:
            raise ValueError(
                f"{name} must define 'app_prefix' (e.g., 'characters/mage')"
            )

        # Validate fields is set and non-empty
        fields = getattr(cls, "fields", [])
        if not fields:
            raise ValueError(
                f"{name} must define 'fields' list for create/update forms"
            )

        # Generate views
        views = create_reference_views(
            model=cls.model,
            app_prefix=app_prefix,
            fields=fields,
            model_name=getattr(cls, "model_name", None),
            ordering=getattr(cls, "ordering", None),
            cached=getattr(cls, "cached", True),
            detail_template=getattr(cls, "detail_template", None),
            list_template=getattr(cls, "list_template", None),
            form_template=getattr(cls, "form_template", None),
            extra_context=getattr(cls, "extra_context", None),
        )

        # Attach views as class attributes
        cls.detail_view = views["detail"]
        cls.list_view = views["list"]
        cls.create_view = views["create"]
        cls.update_view = views["update"]

        return cls


class ReferenceViewSet(metaclass=ReferenceViewSetMeta):
    """
    Base class for generating standard CRUD views for reference models.

    Subclass this and set the required attributes to auto-generate views.

    Required attributes:
        model: The Django model class
        app_prefix: Template path prefix (e.g., "characters/mage")
        fields: List of field names for create/update forms

    Optional attributes:
        model_name: Override for model name in templates
        ordering: List ordering field(s) (default: ["name"])
        cached: Whether to cache detail/list views (default: True)
        detail_template: Override detail template path
        list_template: Override list template path
        form_template: Override form template path
        extra_context: Extra context to add to all views

    Example:
        class SphereViews(ReferenceViewSet):
            model = Sphere
            app_prefix = "characters/mage"
            fields = ["name", "property_name"]

        # Use in urls.py:
        path("spheres/", SphereViews.list_view.as_view(), name="list:sphere"),
        path("sphere/<int:pk>/", SphereViews.detail_view.as_view(), name="sphere"),
        path("create/sphere/", SphereViews.create_view.as_view(), name="create:sphere"),
        path("update/sphere/<int:pk>/", SphereViews.update_view.as_view(), name="update:sphere"),
    """

    model = None
    app_prefix = ""
    fields = []
    model_name = None
    ordering = None
    cached = True
    detail_template = None
    list_template = None
    form_template = None
    extra_context = None
