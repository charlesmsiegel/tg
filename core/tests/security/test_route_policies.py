"""Every project URL and DictView branch has a reviewed policy declaration."""

import importlib

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, SimpleTestCase
from django.urls import get_resolver

from characters.models.core import CharacterModel, Group
from core.access_policy import PROJECT_PREFIXES, authorize_route, route_policy
from core.model_registry import get_registry
from core.models import CharacterTemplate
from core.route_policy_manifest import POLICIES, VIEW_POLICIES
from items.models.core import ItemModel
from locations.models.core import LocationModel
from scripts.inventory_authorization_routes import walk


class RoutePolicyTests(SimpleTestCase):
    def test_every_project_route_and_router_target_has_one_policy(self):
        names = {
            row[2]
            for row in walk(get_resolver().url_patterns)
            if row[2].startswith(PROJECT_PREFIXES)
        }
        registered = {
            action.view_path: action.policy
            for app in ("items", "locations")
            for entry in get_registry(app)
            for action in entry.actions.values()
        }
        self.assertFalse(registered.keys() & VIEW_POLICIES.keys(), "Policy has two sources")
        declared = VIEW_POLICIES | registered
        self.assertEqual(names, declared.keys())
        self.assertEqual(
            sum(len(group) for group in POLICIES.values()) + len(registered), len(names)
        )
        for name, policy in declared.items():
            module, class_name = name.rsplit(".", 1)
            target = getattr(importlib.import_module(module), class_name)
            self.assertEqual(route_policy(target), policy, name)

    def test_unknown_route_has_no_implicit_fallback(self):
        class NewUnreviewedView:
            pass

        self.assertIsNone(route_policy(NewUnreviewedView))
        request = RequestFactory().get("/new/")
        request.user = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            authorize_route(request, NewUnreviewedView)

    def test_public_reference_views_do_not_accept_mutating_methods(self):
        auth_forms = {
            "accounts.views.SignUp",
            "accounts.views.CustomLoginView",
            "accounts.views.CustomPasswordResetView",
        }
        registered_reads = {
            action.view_path
            for app in ("items", "locations")
            for entry in get_registry(app)
            for action in entry.actions.values()
            if action.policy == "PUBLIC_READ"
        }
        for name in (POLICIES["PUBLIC_READ"] | registered_reads) - auth_forms:
            module, class_name = name.rsplit(".", 1)
            view = getattr(importlib.import_module(module), class_name)
            self.assertFalse(
                any(hasattr(view, method) for method in ("post", "put", "patch", "delete")),
                f"{name} needs a write policy",
            )

    def test_player_object_routers_check_before_handoff(self):
        for name in POLICIES["ROUTER"]:
            module, class_name = name.rsplit(".", 1)
            view = getattr(importlib.import_module(module), class_name)
            model = getattr(view, "model_class", None)
            if isinstance(model, type) and issubclass(
                model, (CharacterModel, Group, ItemModel, LocationModel, CharacterTemplate)
            ):
                self.assertTrue(
                    view.protected_object or view.chargen_router,
                    f"{name} must authorize before handing off to a target",
                )
