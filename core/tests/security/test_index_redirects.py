"""Choosing a type to create is a GET to one typed endpoint (Step 5).

The selection is resolved only through seeded ObjectType rows and the
item/location registries; nothing is created and no route name is trusted.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from game.models import ObjectType


def url(kind, action="create"):
    return reverse("core:object_type_redirect", kwargs={"kind": kind, "action": action})


class ObjectTypeRedirectTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("creator")

    def test_unknown_selection_does_not_create_type(self):
        self.client.force_login(self.user)
        for kind, field in (
            ("character", "char_type"),
            ("group", "group_type"),
            ("item", "item_type"),
            ("location", "loc_type"),
        ):
            with self.subTest(kind=kind):
                before = ObjectType.objects.count()
                response = self.client.get(url(kind), {field: "client_supplied_type"})
                self.assertEqual(response.status_code, 404)
                self.assertEqual(ObjectType.objects.count(), before)

    def test_known_type_redirects_without_writing(self):
        ObjectType.objects.create(name="weapon", type="obj", gameline="wod")
        self.client.force_login(self.user)
        before = ObjectType.objects.count()
        response = self.client.get(url("item"), {"item_type": "weapon"})
        self.assertRedirects(response, "/items/create/weapon/", fetch_redirect_response=False)
        self.assertEqual(ObjectType.objects.count(), before)

    def test_every_configured_character_gameline_resolves_or_is_a_controlled_404(self):
        self.client.force_login(self.user)
        valid = {code for code, _ in ObjectType._meta.get_field("gameline").choices}
        for code in settings.GAMELINES:
            if code not in valid:
                continue
            with self.subTest(gameline=code):
                ObjectType.objects.create(name=f"probe_{code}", type="char", gameline=code)
                response = self.client.get(
                    url("character"), {"char_type": f"probe_{code}", "gameline": code}
                )
                self.assertIn(response.status_code, {302, 404})

    def test_known_character_type_redirects(self):
        ObjectType.objects.create(name="mage", type="char", gameline="mta")
        self.client.force_login(self.user)
        response = self.client.get(url("character"), {"char_type": "mage", "gameline": "mta"})
        self.assertRedirects(
            response, reverse("characters:mage:create:mage"), fetch_redirect_response=False
        )

    def test_unsupported_gameline_is_controlled_404(self):
        ObjectType.objects.create(name="lost_type", type="obj", gameline="mtr")
        self.client.force_login(self.user)
        response = self.client.get(url("item"), {"item_type": "lost_type"})
        self.assertEqual(response.status_code, 404)

    def test_unknown_kind_or_action_is_404(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(url("spell")).status_code, 404)
        self.assertEqual(self.client.get(url("item", "delete")).status_code, 404)

    def test_anonymous_create_requires_login(self):
        # AuthErrorHandlerMiddleware turns the login redirect into the
        # project's 401 for unauthenticated access.
        ObjectType.objects.create(name="weapon", type="obj", gameline="wod")
        response = self.client.get(url("item"), {"item_type": "weapon"})
        self.assertEqual(response.status_code, 401)

    def test_anonymous_list_navigation_is_public(self):
        ObjectType.objects.create(name="weapon", type="obj", gameline="wod")
        response = self.client.get(url("item", "list"), {"item_type": "weapon"})
        self.assertIn(response.status_code, {302, 404})

    def test_post_is_rejected(self):
        self.client.force_login(self.user)
        for target in (url("item"), "/characters/index/", "/items/index/", "/locations/index/"):
            with self.subTest(target=target):
                response = self.client.post(target, {"action": "create", "item_type": "weapon"})
                self.assertEqual(response.status_code, 405)
