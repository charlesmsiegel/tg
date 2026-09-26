"""Declarative CRUD for items and locations; policies and workflows stay explicit."""

from dataclasses import dataclass, field
from functools import cached_property, lru_cache
from importlib import import_module

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.urls import path, reverse
from django.utils.module_loading import import_string
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.access_policy import authorize_route
from core.mixins import (
    MessageMixin,
    PermissionContextMixin,
    VisibilityFilterMixin,
    prepare_created_object,
)
from core.route_policy_manifest import POLICIES


@dataclass(frozen=True)
class ActionSpec:
    view_path: str
    policy: str
    custom: str | None = None
    options: dict = field(default_factory=dict)
    # (legacy URL name, path relative to this action's include)
    routes: tuple = ()
    form_updates: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ModelSpec:
    model_label: str
    slug: str
    group: str
    gameline: str
    actions: dict
    fields: tuple = ()
    form_class: str | None = None
    templates: dict = field(default_factory=dict)
    label: str = ""
    model_urls: dict = field(default_factory=dict)
    dispatch_view: str | None = None

    @property
    def model(self):
        return apps.get_model(self.model_label)

    @property
    def name(self):
        """Compatibility with ObjectType in index templates."""
        return self.slug

    @property
    def menu_label(self):
        return self.label or self.model._meta.verbose_name.title()


class RegistryViewMixin(PermissionContextMixin):
    """Enforce declared policy before custom logic, even outside URL middleware."""

    registry_action = None
    registry_spec = None
    registry_subject = None
    registry_form_updates = None

    def dispatch(self, request, *args, **kwargs):
        if self.registry_subject is None and self.registry_action in {"detail", "update"}:
            try:
                self.registry_subject = self.get_object()
            except self.model.DoesNotExist as exc:
                raise Http404("Object not found") from exc
        denial = authorize_route(request, type(self), args, kwargs, subject=self.registry_subject)
        if denial is not None:
            return denial
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.registry_subject is not None:
            return self.registry_subject
        if queryset is None:
            return super().get_object()
        return super().get_object(queryset)

    def get_template_names(self):
        names = list(super().get_template_names())
        action = "form" if self.registry_action in {"create", "update"} else self.registry_action
        return names + [f"core/registry/{action}.html"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for name, changes in (self.registry_form_updates or {}).items():
            if name in form.fields:
                form.fields[name].widget.attrs.update(changes.get("attrs", {}))
                if "help_text" in changes:
                    form.fields[name].help_text = changes["help_text"]
        return form

    def form_valid(self, form):
        if self.registry_action == "create":
            prepare_created_object(form, self.request)
        return super().form_valid(form)


class ModelRegistry:
    def __init__(self, app, entries):
        self.app = app
        self.entries = tuple(entries)
        self._models = {}
        self._views = {}
        keys = set()
        route_names = set()
        route_paths = set()
        for entry in self.entries:
            if set(entry.actions) != {"detail", "list", "create", "update"}:
                raise ImproperlyConfigured(f"Declare all four actions: {entry.model_label}")
            key = (entry.gameline, entry.slug)
            if entry.model_label in self._models or key in keys:
                raise ImproperlyConfigured(f"Duplicate registry entry: {entry.model_label}")
            self._models[entry.model_label] = entry
            keys.add(key)
            for action, spec in entry.actions.items():
                if action not in {"detail", "list", "create", "update"}:
                    raise ImproperlyConfigured(f"Unknown registry action: {action}")
                if not spec.policy or spec.policy not in POLICIES:
                    raise ImproperlyConfigured(
                        f"Missing/unknown policy: {entry.model_label}.{action}"
                    )
                for name, route in spec.routes:
                    name_key = (entry.group, action, name)
                    path_key = (entry.group, action, route.replace("<pk>", "<int:pk>"))
                    if name_key in route_names or path_key in route_paths:
                        raise ImproperlyConfigured(f"Duplicate registry route: {name_key}")
                    route_names.add(name_key)
                    route_paths.add(path_key)

    def __iter__(self):
        return iter(self.entries)

    def entry(self, model):
        label = model if isinstance(model, str) else model._meta.label
        try:
            return self._models[label]
        except KeyError as exc:
            raise ImproperlyConfigured(f"Unregistered model: {label}") from exc

    def _build_view(self, entry, action, custom=None):
        spec = entry.actions[action]
        module, name = spec.view_path.rsplit(".", 1)
        attrs = dict(spec.options)
        attrs.update(
            __module__=module,
            model=entry.model,
            access_policy=spec.policy,
            registry_spec=entry,
            registry_action=action,
            registry_form_updates=spec.form_updates,
        )
        if action in entry.templates:
            attrs.setdefault("template_name", entry.templates[action])
        form_path = attrs.get("form_class", entry.form_class)
        if action in {"create", "update"}:
            verb = "created" if action == "create" else "updated"
            label = entry.model._meta.verbose_name
            attrs.setdefault("success_message", f"{label.title()} '{{name}}' {verb} successfully!")
            attrs.setdefault(
                "error_message", f"Failed to {action} {label}. Please correct the errors below."
            )
            if form_path:
                attrs["form_class"] = import_string(form_path)
                attrs.pop("fields", None)
            elif custom is None:
                attrs.setdefault("fields", list(entry.fields))
        elif isinstance(attrs.get("form_class"), str):
            attrs["form_class"] = import_string(attrs["form_class"])
        if action == "list":
            attrs.setdefault("ordering", ["name"])
        bases = [RegistryViewMixin]
        base = (
            custom
            or {"detail": DetailView, "list": ListView, "create": CreateView, "update": UpdateView}[
                action
            ]
        )
        if action in {"create", "update"} and not issubclass(base, MessageMixin):
            bases.append(MessageMixin)
        # Public reference lists retain their declared policy; private object
        # querysets use the same visibility rules as handwritten list views.
        if (
            action == "list"
            and spec.policy == "OBJECT_LIST"
            and not issubclass(base, VisibilityFilterMixin)
        ):
            bases.append(VisibilityFilterMixin)
        bases.append(base)
        view = type(name, tuple(bases), attrs)
        self._views[(entry.model_label, action)] = view
        # New entries can use their registry module as the public view module.
        # Existing compatibility exports remain authoritative when already loaded.
        import_module(module).__dict__.setdefault(name, view)
        return view

    def view(self, model, action):
        entry = self.entry(model)
        key = (entry.model_label, action)
        if key not in self._views:
            spec = entry.actions[action]
            import_module(spec.view_path.rsplit(".", 1)[0])
            if key not in self._views:
                custom = import_string(spec.custom) if spec.custom else None
                self._build_view(entry, action, custom)
        return self._views[key]

    def detail_view(self, model):
        entry = self.entry(model)
        return (
            import_string(entry.dispatch_view)
            if entry.dispatch_view
            else self.view(model, "detail")
        )

    @cached_property
    def detail_views(self):
        base = apps.get_model(self.app, "ItemModel" if self.app == "items" else "LocationModel")
        return {
            entry.model: self.detail_view(entry.model)
            for entry in self
            if issubclass(entry.model, base)
        }

    def urls(self, group, action):
        return [
            path(
                route.replace("<pk>", "<int:pk>"),
                self.view(entry.model, action).as_view(),
                name=name,
            )
            for entry in self
            if entry.group == group and action in entry.actions
            for name, route in entry.actions[action].routes
        ]

    def url(self, model, action, pk=None):
        entry = self.entry(model)
        name = entry.model_urls[action]
        return reverse(name, kwargs={"pk": pk} if action in {"detail", "update"} else None)

    def resolve(self, type_name, gameline=None):
        matches = [
            entry
            for entry in self
            if entry.slug == type_name and (gameline is None or entry.gameline == gameline)
        ]
        if len(matches) != 1:
            raise Http404("Unknown or ambiguous object type")
        return matches[0]

    def selection_url(self, entry, action):
        """Prefer a matching legacy alias for a menu selection when one exists."""
        if any(name == entry.slug for name, _ in entry.actions[action].routes):
            namespace = self.app + (f":{entry.group}" if entry.group != "core" else "")
            return reverse(f"{namespace}:{action}:{entry.slug}")
        return self.url(entry.model, action)

    def menu(self, user):
        if not user or not user.is_authenticated:
            return []
        all_games = user.is_staff or user.is_superuser or user.profile.is_st()
        return sorted(
            (
                entry
                for entry in self
                if "create" in entry.actions
                and (all_games or entry.gameline == "mta")
                and (
                    entry.actions["create"].policy != "STAFF_WRITE"
                    or user.is_staff
                    or user.is_superuser
                )
            ),
            key=lambda entry: (entry.gameline, entry.menu_label),
        )


@lru_cache(maxsize=2)
def get_registry(app):
    if app not in {"items", "locations"}:
        raise ImproperlyConfigured(f"Unsupported registry: {app}")
    return import_module(f"{app}.registry").registry
