"""Public-card admission is independent of partial/private read roles."""

import re
from types import SimpleNamespace
from unittest.mock import patch

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from characters.models.changeling.chimera import Chimera
from characters.models.core import Ability, Attribute, Group, Human
from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from core.constants import ImageStatus
from core.models import CharacterTemplate, Observer
from core.permissions import Permission, PermissionManager
from core.views.public_object import PublicObjectDetailView, can_view_public_object
from game.models import Chronicle, Gameline, STRelationship
from items.models.core import Weapon
from locations.models.core import City


@override_settings(DEBUG=False)
class PublicObjectVisibilityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_user_model()
        cls.owner = users.objects.create_user("card_owner")
        cls.reader = users.objects.create_user("card_chronicle_reader")
        cls.stranger = users.objects.create_user("card_stranger")
        cls.observer = users.objects.create_user("card_observer")
        cls.head = users.objects.create_user("card_head")
        cls.game_st = users.objects.create_user("card_game_st")
        cls.other_line_st = users.objects.create_user("card_other_line_st")
        cls.other_chronicle_st = users.objects.create_user("card_other_chronicle_st")
        cls.staff = users.objects.create_user("card_staff", is_staff=True)
        cls.chronicle = Chronicle.objects.create(name="Card chronicle", head_st=cls.head)
        cls.chronicle.game_storytellers.add(cls.game_st)
        other_chronicle = Chronicle.objects.create(name="Other card chronicle")
        line = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(
            user=cls.other_line_st, chronicle=cls.chronicle, gameline=line
        )
        STRelationship.objects.create(
            user=cls.other_chronicle_st, chronicle=other_chronicle, gameline=line
        )
        Human.objects.create(name="Reader's character", owner=cls.reader, chronicle=cls.chronicle)
        attribute = Attribute.objects.create(name="Card attribute", property_name="card_attribute")
        ability = Ability.objects.create(name="Card ability", property_name="card_ability")
        effect = Effect.objects.create(name="Supporting effect")
        cls.objects = []
        for model in (Weapon, City, Human, Group, Effect, Rote, Chimera, CharacterTemplate):
            extra = {}
            if model is Rote:
                extra = {"effect": effect, "attribute": attribute, "ability": ability}
            elif model is CharacterTemplate:
                extra = {"character_type": "human"}
            obj = model.objects.create(
                name=f"Visibility {model.__name__}",
                owner=cls.owner,
                chronicle=cls.chronicle,
                status="App",
                public_info="CARD ONLY TEXT",
                description="PRIVATE DESCRIPTION",
                st_notes="PRIVATE ST NOTES",
                **extra,
            )
            # A stored approved image path needs no upload or storage write.
            model.objects.filter(pk=obj.pk).update(
                image="images/card-approved.jpg", image_status=ImageStatus.APPROVED
            )
            obj.refresh_from_db()
            Observer.objects.create(content_object=obj, user=cls.observer, granted_by=cls.owner)
            cls.objects.append(obj)

    def login_as(self, user):
        self.client.logout()
        if user is not None:
            self.client.force_login(user)

    def routes_for(self, obj):
        if isinstance(obj, CharacterTemplate):
            return [reverse("core:character_template_detail", args=[obj.pk])]
        routes = [obj.get_absolute_url()]
        if isinstance(obj, Weapon):
            routes.extend(reverse(name, args=[obj.pk]) for name in ("items:item", "items:weapon"))
        elif isinstance(obj, City):
            routes.extend(
                reverse(name, args=[obj.pk]) for name in ("locations:location", "locations:city")
            )
        return list(dict.fromkeys(routes))

    def set_visibility(self, obj, visibility):
        # Also models legacy/unknown persisted values without relaxing validation.
        type(obj).objects.filter(pk=obj.pk).update(visibility=visibility)
        obj.visibility = visibility

    def assert_card(self, response, obj, method):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/public_object_detail.html")
        self.assertNotIn("object", response.context)
        self.assertEqual(
            set(response.context["public_object"]), {"name", "public_info", "image_url"}
        )
        if method == "get":
            self.assertContains(response, obj.name)
            self.assertContains(response, "CARD ONLY TEXT")
            self.assertContains(response, "card-approved.jpg")
            self.assertNotContains(response, "PRIVATE DESCRIPTION")
            self.assertNotContains(response, "PRIVATE ST NOTES")

    def assert_denied(self, response, obj):
        self.assertEqual(response.status_code, 404)
        self.assertNotIn("public_object", response.context)
        for text in (
            obj.name,
            "CARD ONLY TEXT",
            "PRIVATE DESCRIPTION",
            "PRIVATE ST NOTES",
            "card-approved.jpg",
        ):
            self.assertNotContains(response, text, status_code=404)

    def test_nonfull_visibility_matrix_on_generic_and_typed_get_and_head(self):
        audiences = (
            (None, False),
            (self.stranger, False),
            (self.reader, True),
            (self.observer, False),
            (self.other_chronicle_st, False),
        )
        for obj in self.objects:
            for visibility in ("PUB", "PRI", "CHR"):
                self.set_visibility(obj, visibility)
                for user, chronicle_reader in audiences:
                    self.login_as(user)
                    expected = visibility == "PUB" or (visibility == "CHR" and chronicle_reader)
                    for route in self.routes_for(obj):
                        for method in ("get", "head"):
                            with self.subTest(
                                model=type(obj).__name__,
                                visibility=visibility,
                                user=user,
                                route=route,
                                method=method,
                            ):
                                response = getattr(self.client, method)(route)
                                if expected:
                                    self.assert_card(response, obj, method)
                                else:
                                    self.assert_denied(response, obj)

    def test_full_viewers_keep_detail_access_for_every_visibility(self):
        for obj in self.objects:
            for visibility in ("PUB", "PRI", "CHR", "CUS", "BAD"):
                self.set_visibility(obj, visibility)
                for user in (self.owner, self.head, self.game_st, self.other_line_st, self.staff):
                    self.login_as(user)
                    for route in self.routes_for(obj):
                        for method in ("get", "head"):
                            with self.subTest(
                                model=type(obj).__name__,
                                visibility=visibility,
                                user=user,
                                route=route,
                                method=method,
                            ):
                                response = getattr(self.client, method)(route)
                                self.assertEqual(response.status_code, 200)
                                self.assertNotIn("public_object", response.context)

    def test_partial_read_roles_do_not_admit_private_cards(self):
        for user in (self.reader, self.observer):
            request = RequestFactory().get("/")
            request.user = user
            for obj in self.objects:
                self.assertTrue(
                    PermissionManager.user_has_permission(
                        user, obj, Permission.VIEW_PARTIAL, request=request
                    )
                )
                self.assertFalse(
                    PermissionManager.user_has_permission(
                        user, obj, Permission.VIEW_FULL, request=request
                    )
                )
                self.login_as(user)
                self.assert_denied(self.client.get(self.routes_for(obj)[0]), obj)

    def test_chronicle_only_without_a_chronicle_is_hidden(self):
        obj = self.objects[0]
        type(obj).objects.filter(pk=obj.pk).update(visibility="CHR", chronicle=None)
        for user in (None, self.reader, self.observer):
            self.login_as(user)
            for route in self.routes_for(obj):
                self.assert_denied(self.client.get(route), obj)

    def test_chronicle_only_projection_without_chronicle_attribute_fails_closed(self):
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        obj = SimpleNamespace(visibility="CHR")
        with self.assertRaisesMessage(Http404, "Object not found"):
            PublicObjectDetailView.as_view(resolved_object=obj)(request)

    def test_all_player_models_deny_chronicle_only_projection_without_a_chronicle(self):
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        player_roots = (Human, Group, Effect, Rote, Chimera, CharacterTemplate, Weapon, City)
        # Include the wider inheritance roots, not just the eight fixture types.
        player_roots = tuple(model._meta.get_field("chronicle").model for model in player_roots)
        models = [model for model in apps.get_models() if issubclass(model, player_roots)]
        self.assertIn(Rote, models)
        self.assertIn(CharacterTemplate, models)
        for model in models:
            with self.subTest(model=model._meta.label):
                obj = model(visibility="CHR")
                self.assertIsNone(obj.chronicle_id)
                self.assertFalse(can_view_public_object(request, obj))
                with self.assertRaisesMessage(Http404, "Object not found"):
                    PublicObjectDetailView.as_view(resolved_object=obj)(request)

    def test_public_routes_check_full_access_once_before_the_independent_projection_guard(self):
        obj = self.objects[0]
        self.set_visibility(obj, "PUB")
        self.login_as(self.stranger)
        for route in self.routes_for(obj):
            for method in ("get", "head"):
                with self.subTest(route=route, method=method):
                    with patch.object(
                        PermissionManager,
                        "user_has_permission",
                        wraps=PermissionManager.user_has_permission,
                    ) as permission_check:
                        response = getattr(self.client, method)(route)
                    self.assert_card(response, obj, method)
                    full_checks = [
                        call
                        for call in permission_check.call_args_list
                        if call.args[2] == Permission.VIEW_FULL
                    ]
                    self.assertEqual(len(full_checks), 2)

    def test_legacy_custom_and_unknown_values_fail_closed_for_nonfull_viewers(self):
        obj = self.objects[0]
        for visibility in ("CUS", "BAD", ""):
            self.set_visibility(obj, visibility)
            for user in (None, self.reader, self.observer, self.stranger):
                self.login_as(user)
                for route in self.routes_for(obj):
                    for method in ("get", "head"):
                        with self.subTest(
                            visibility=visibility, user=user, route=route, method=method
                        ):
                            self.assert_denied(getattr(self.client, method)(route), obj)

    def test_hidden_and_missing_details_have_the_same_response(self):
        obj = self.objects[0]
        for user in (None, self.reader, self.stranger):
            self.login_as(user)
            for name in ("items:weapon", "items:item"):
                for method in ("get", "head"):
                    hidden = getattr(self.client, method)(reverse(name, args=[obj.pk]))
                    missing = getattr(self.client, method)(reverse(name, args=[999999]))
                    self.assertEqual(hidden.status_code, missing.status_code)
                    self.assertEqual(hidden.status_code, 404)
                    self.assertEqual(hidden["Content-Type"], missing["Content-Type"])

                    # The authenticated shell masks its CSRF token on every render.
                    def normalize(body):
                        return re.sub(
                            rb'(name="csrfmiddlewaretoken" value=")[^"]+', rb"\1TOKEN", body
                        )

                    self.assertEqual(normalize(hidden.content), normalize(missing.content))

    def test_public_projection_itself_denies_hidden_objects(self):
        obj = self.objects[0]
        for resolved in (None, obj):
            for method in ("get", "head"):
                request = getattr(RequestFactory(), method)("/")
                request.user = AnonymousUser()
                with self.subTest(resolved=resolved is not None, method=method):
                    with self.assertRaisesMessage(Http404, "Object not found"):
                        PublicObjectDetailView.as_view(
                            model_class=Weapon, resolved_object=resolved
                        )(request, pk=obj.pk)

    def test_template_collection_flag_does_not_replace_detail_visibility(self):
        template = next(obj for obj in self.objects if isinstance(obj, CharacterTemplate))
        CharacterTemplate.objects.filter(pk=template.pk).update(visibility="PUB", is_public=False)
        for method in ("get", "head"):
            response = getattr(self.client, method)(self.routes_for(template)[0])
            self.assert_card(response, template, method)
        collection = self.client.get(reverse("core:character_template_list"))
        self.assertNotContains(collection, template.name)
