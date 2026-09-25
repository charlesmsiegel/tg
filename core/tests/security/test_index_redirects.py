from django.contrib.auth import get_user_model
from django.test import TestCase

from game.models import ObjectType


class IndexRedirectSecurityTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("creator")

    def test_unknown_selection_does_not_create_type(self):
        self.client.force_login(self.user)
        for url, field in (
            ("/characters/index/", "char_type"),
            ("/items/index/", "item_type"),
            ("/locations/index/", "loc_type"),
        ):
            with self.subTest(url=url):
                before = ObjectType.objects.count()
                response = self.client.post(
                    url, {"action": "create", field: "client_supplied_type"}
                )
                self.assertIn(response.status_code, {400, 404})
                self.assertEqual(ObjectType.objects.count(), before)

    def test_known_type_redirects_without_writing(self):
        ObjectType.objects.create(name="weapon", type="obj", gameline="wod")
        self.client.force_login(self.user)
        before = ObjectType.objects.count()
        response = self.client.post(
            "/items/index/", {"action": "create", "item_type": "weapon"}
        )
        self.assertRedirects(response, "/items/create/weapon/", fetch_redirect_response=False)
        self.assertEqual(ObjectType.objects.count(), before)

    def test_unsupported_gameline_is_controlled_404(self):
        ObjectType.objects.create(name="lost_type", type="obj", gameline="mtr")
        self.client.force_login(self.user)
        response = self.client.post(
            "/items/index/", {"action": "create", "item_type": "lost_type"}
        )
        self.assertEqual(response.status_code, 404)
