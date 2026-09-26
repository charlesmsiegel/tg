"""Contracts shared by every declared item and location type."""

import json
from dataclasses import replace
from pathlib import Path

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import Resolver404, get_resolver, resolve

from core.model_registry import ModelRegistry, get_registry
from items.models.core import ItemModel
from locations.models.core import LocationModel
from scripts.inventory_model_routes import inventory


class RegistryContractTests(SimpleTestCase):
    def test_existing_routes_keep_names_and_paths(self):
        baseline = json.loads((Path(__file__).parent / "fixtures/model_routes.json").read_text())
        actual = {(row["name"], row["path"]) for row in inventory(get_resolver().url_patterns)}
        expected = {(row["name"], row["path"].replace("<pk>", "<int:pk>")) for row in baseline}
        self.assertFalse(expected - actual, expected - actual)

    def test_every_concrete_model_is_registered(self):
        for app, base in (("items", ItemModel), ("locations", LocationModel)):
            registry = get_registry(app)
            expected = {m for m in apps.get_app_config(app).get_models() if issubclass(m, base)}
            self.assertFalse(expected - {entry.model for entry in registry})

    def test_every_action_declares_policy(self):
        for app in ("items", "locations"):
            for entry in get_registry(app):
                for action in entry.actions.values():
                    self.assertTrue(action.policy, entry.model_label)

    def test_every_write_view_has_feedback(self):
        for app in ("items", "locations"):
            registry = get_registry(app)
            for entry in registry:
                for action in ("create", "update"):
                    view = registry.view(entry.model, action)
                    self.assertTrue(view.success_message, (entry.model_label, action))
                    self.assertTrue(view.error_message, (entry.model_label, action))

    def test_polymorphic_dispatch_uses_model_identity(self):
        from items.models.demon.relic import Relic
        from items.models.mage.artifact import Artifact
        from items.models.wraith.artifact import WraithArtifact
        from items.models.wraith.relic import WraithRelic

        registry = get_registry("items")
        for model in (Artifact, WraithArtifact, Relic, WraithRelic):
            self.assertIs(registry.detail_view(model).model, model)

    def test_bad_integer_ids_do_not_resolve(self):
        for path in ("/items/nope/", "/locations/nope/", "/items/weapon/nope/"):
            with self.subTest(path=path), self.assertRaises(Resolver404):
                resolve(path)

    def test_missing_or_unknown_policies_are_rejected(self):
        entry = get_registry("items").entry("items.Weapon")
        for policy in (None, "not_a_policy"):
            actions = dict(entry.actions, create=replace(entry.actions["create"], policy=policy))
            with self.assertRaises(ImproperlyConfigured):
                ModelRegistry("items", [replace(entry, actions=actions)])
        with self.assertRaises(ImproperlyConfigured):
            ModelRegistry("items", [replace(entry, actions={})])

    def test_duplicate_models_and_routes_are_rejected(self):
        entry = get_registry("items").entry("items.Weapon")
        with self.assertRaises(ImproperlyConfigured):
            ModelRegistry("items", [entry, entry])
        other = get_registry("items").entry("items.MeleeWeapon")
        for route in (("other_name", "weapon/"), ("weapon", "other_path/")):
            actions = dict(other.actions, create=replace(other.actions["create"], routes=(route,)))
            with self.subTest(route=route), self.assertRaises(ImproperlyConfigured):
                ModelRegistry("items", [entry, replace(other, actions=actions)])

    def test_new_entry_can_export_views_without_a_handwritten_module(self):
        import items.registry as registry_module

        entry = get_registry("items").entry("items.Weapon")
        actions = {
            name: replace(action, view_path=f"items.registry.NewWeapon{name.title()}View")
            for name, action in entry.actions.items()
        }
        registry = ModelRegistry("items", [replace(entry, actions=actions)])
        try:
            for action, spec in actions.items():
                view = registry.view(entry.model, action)
                self.assertIs(
                    getattr(registry_module, spec.view_path.rsplit(".", 1)[1], None), view
                )
        finally:
            for spec in actions.values():
                name = spec.view_path.rsplit(".", 1)[1]
                if hasattr(registry_module, name):
                    delattr(registry_module, name)


class RegistryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = get_user_model().objects.create_user("registry_staff", is_staff=True)
        cls.owner = get_user_model().objects.create_user("registry_owner")
        cls.other = get_user_model().objects.create_user("registry_other")


class RegistryBehaviorTests(RegistryTestCase):
    def test_collision_dispatch_renders_the_correct_concrete_object(self):
        self.client.force_login(self.staff)
        for label in ("items.Artifact", "items.WraithArtifact", "items.Relic", "items.WraithRelic"):
            model = apps.get_model(label)
            obj = model.objects.create(name=label, owner=self.staff)
            response = self.client.get(f"/items/{obj.pk}/")
            self.assertEqual(response.status_code, 200, label)
            self.assertIs(type(response.context["object"]), model)
            self.assertEqual(response.context["object"].pk, obj.pk)

    def test_router_hands_off_the_already_loaded_instance(self):
        from items.models.core import Weapon
        from items.views.core import GenericItemDetailView

        obj = Weapon.objects.create(name="One lookup", owner=self.staff)
        request = RequestFactory().get(f"/items/{obj.pk}/")
        request.user = self.staff
        # Warm content-type caches; count only object table reads, not template queries.
        ItemModel.objects.get(pk=obj.pk)
        with CaptureQueriesContext(connection) as queries:
            response = GenericItemDetailView.as_view()(request, pk=obj.pk)
        self.assertEqual(response.context_data["object"].pk, obj.pk)
        object_reads = [
            q["sql"]
            for q in queries
            if 'FROM "items_itemmodel"' in q["sql"] or 'FROM "items_weapon"' in q["sql"]
        ]
        # Polymorphic loading: one base-table query, one concrete-table query.
        self.assertEqual(len(object_reads), 2, object_reads)

    def test_direct_view_call_still_denies_unauthorized_updates(self):
        from django.core.exceptions import PermissionDenied

        from items.models.core import Weapon

        obj = Weapon.objects.create(name="Protected", owner=self.owner)
        request = RequestFactory().post(obj.get_update_url(), {"name": "Hijacked"})
        request.user = self.other
        with self.assertRaises(PermissionDenied):
            get_registry("items").view(Weapon, "update").as_view()(request, pk=obj.pk)

    def test_missing_specialized_templates_use_shared_fallbacks(self):
        from items.models.core import Weapon

        entry = get_registry("items").entry(Weapon)
        registry = ModelRegistry(
            "items",
            [
                replace(
                    entry, templates={action: "missing-template.html" for action in entry.actions}
                )
            ],
        )
        obj = Weapon.objects.create(name="Fallback weapon", owner=self.staff)
        request = RequestFactory().get("/")
        request.user = self.staff
        for action in ("detail", "list", "create", "update"):
            kwargs = {"pk": obj.pk} if action in {"detail", "update"} else {}
            response = registry.view(Weapon, action).as_view()(request, **kwargs)
            response.render()
            self.assertEqual(response.status_code, 200)
            fallback = "form" if action in {"create", "update"} else action
            self.assertIn(f"core/registry/{fallback}.html", response.template_name)

    def test_wonder_form_creates_an_owned_concrete_subtype(self):
        from items.models.mage import Talisman, Wonder

        self.client.force_login(self.owner)
        response = self.client.post(
            Wonder.get_creation_url(),
            {
                "name": "Registry talisman",
                "description": "Custom form",
                "wonder_type": "talisman",
                "rank": 1,
                "arete": 1,
                "resonance-TOTAL_FORMS": 1,
                "resonance-INITIAL_FORMS": 0,
                "resonance-0-resonance": "Dynamic",
                "resonance-0-rating": 1,
                "effects-TOTAL_FORMS": 0,
                "effects-INITIAL_FORMS": 0,
            },
        )
        self.assertEqual(response.status_code, 302, getattr(response, "context", None))
        self.assertEqual(Talisman.objects.get(name="Registry talisman").owner, self.owner)

    def test_node_custom_create_saves_once_and_redirects(self):
        from characters.models.mage.focus import Practice
        from locations.models.mage import Node

        positive = Practice.objects.create(name="Positive practice")
        negative = Practice.objects.create(name="Negative practice")
        self.client.force_login(self.owner)
        response = self.client.post(
            Node.get_creation_url(),
            {
                "name": "Registry node",
                "description": "Custom form",
                "rank": 1,
                "ratio": 0,
                "size": 0,
                "quintessence_form": "Light",
                "tass_form": "Crystal",
                "gauntlet": 5,
                "shroud": 5,
                "dimension_barrier": 5,
                "resonance-TOTAL_FORMS": 1,
                "resonance-INITIAL_FORMS": 0,
                "resonance-0-resonance": "Dynamic",
                "resonance-0-rating": 1,
                "merit_flaw-TOTAL_FORMS": 0,
                "merit_flaw-INITIAL_FORMS": 0,
                "reality_zone-TOTAL_FORMS": 2,
                "reality_zone-INITIAL_FORMS": 0,
                "reality_zone-0-practice": positive.pk,
                "reality_zone-0-rating": 1,
                "reality_zone-1-practice": negative.pk,
                "reality_zone-1-rating": -1,
            },
        )
        self.assertEqual(
            response.status_code,
            302,
            response.context["form"].errors if response.status_code == 200 else "",
        )
        self.assertEqual(Node.objects.get(name="Registry node").owner, self.owner)

    def test_workflow_router_keeps_public_card(self):
        from locations.models.mage import Chantry

        obj = Chantry.objects.create(
            name="Visible name", description="HIDDEN CHANTRY", owner=self.owner
        )
        for user in (None, self.other):
            if user:
                self.client.force_login(user)
            response = self.client.get(f"/locations/{obj.pk}/")
            self.assertContains(response, "Visible name")
            self.assertNotContains(response, "HIDDEN CHANTRY")

    def test_missing_custom_update_is_404(self):
        self.client.force_login(self.staff)
        response = self.client.get("/locations/mage/update/paradox_realm/999999/")
        self.assertEqual(response.status_code, 404)

    def test_reference_reads_are_public_and_writes_staff_only(self):
        from items.models.core import Material

        obj = Material.objects.create(name="Steel")
        self.assertContains(self.client.get(obj.get_absolute_url()), "Steel")
        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(obj.get_update_url(), {"name": "Gold"}).status_code, 403)
        obj.refresh_from_db()
        self.assertEqual(obj.name, "Steel")

    def test_public_reality_zone_does_not_expose_private_location_stats(self):
        from locations.models.mage import Node, RealityZone

        zone = RealityZone.objects.create(name="Public reference")
        node = Node.objects.create(
            name="PRIVATE NODE LINK", rank=5, owner=self.owner, visibility="PRI", reality_zone=zone
        )
        response = self.client.get(zone.get_absolute_url())
        self.assertContains(response, zone.name)
        self.assertNotContains(response, node.name)
        self.client.force_login(self.owner)
        self.assertContains(self.client.get(zone.get_absolute_url()), node.name)

    def test_create_assigns_owner_and_update_denies_other_user(self):
        from items.models.core import Weapon

        self.client.force_login(self.owner)
        response = self.client.post(
            Weapon.get_creation_url(),
            {
                "name": "Registry sword",
                "description": "Private",
                "difficulty": 6,
                "damage": 3,
                "damage_type": "L",
                "conceal": "T",
            },
        )
        self.assertEqual(response.status_code, 302)
        obj = Weapon.objects.get(name="Registry sword")
        self.assertEqual(obj.owner, self.owner)
        self.client.force_login(self.other)
        response = self.client.post(obj.get_update_url(), {"name": "Hijacked"})
        self.assertEqual(response.status_code, 403)
        obj.refresh_from_db()
        self.assertEqual(obj.name, "Registry sword")

    def test_menus_and_collision_redirects_need_no_database_types(self):
        from core.create_redirects import resolve_object_type_url
        from game.models import ObjectType
        from items.forms.core.item_creation import ItemCreationForm

        self.assertFalse(ObjectType.objects.exists())
        form = ItemCreationForm(user=self.staff)
        self.assertIn(("wraith_artifact", "Artifact"), form.fields["item_type"].choices_map["wto"])
        for name, code, expected in (
            ("wraith_artifact", "wto", "/items/wraith/create/artifact/"),
            ("wraith_relic", "wto", "/items/wraith/create/relic/"),
            ("demon_relic", "dtf", "/items/demon/create/relic/"),
        ):
            self.assertEqual(resolve_object_type_url("obj", name, gameline=code), expected)
        self.assertFalse(ObjectType.objects.exists())


def smoke_case(app, label):
    def test(self):
        registry = get_registry(app)
        entry = registry.entry(label)
        values = {"name": f"Smoke {label}"}
        if issubclass(entry.model, (ItemModel, LocationModel)):
            values.update(owner=self.staff, description="PRIVATE SMOKE DESCRIPTION")
        obj = entry.model.objects.create(**values)
        self.client.force_login(self.staff)
        for action in ("list", "detail", "create", "update"):
            url = registry.url(entry.model, action, obj.pk)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, (label, action, url))
        self.client.force_login(self.other)
        response = self.client.post(
            registry.url(entry.model, "update", obj.pk), {"name": "Hijacked"}
        )
        self.assertIn(response.status_code, {403, 404}, label)
        obj.refresh_from_db()
        self.assertEqual(obj.name, values["name"])
        self.client.logout()
        response = self.client.get(registry.url(entry.model, "detail", obj.pk))
        self.assertEqual(response.status_code, 200, label)
        if "description" in values:
            self.assertNotContains(response, values["description"])
        response = self.client.post(registry.url(entry.model, "create"), {"name": "Unauthorized"})
        self.assertIn(response.status_code, {401, 403}, label)

    return test


class RegistrySmokeTests(RegistryTestCase):
    """Every new declaration automatically gains CRUD/denial smoke coverage."""


for registry_app in ("items", "locations"):
    for registry_entry in get_registry(registry_app):
        setattr(
            RegistrySmokeTests,
            "test_crud_" + registry_entry.model_label.replace(".", "_"),
            smoke_case(registry_app, registry_entry.model_label),
        )
