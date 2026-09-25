from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from items.models.core.weapon import Weapon


class WeaponAuthorizationTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("weapon_owner")
        self.other = users.objects.create_user("weapon_other")
        self.weapon = Weapon.objects.create(
            name="Private sword", owner=self.owner, st_notes="SECRET"
        )

    def test_anonymous_update_is_denied(self):
        url = reverse("items:update:weapon", kwargs={"pk": self.weapon.pk})
        self.assertIn(self.client.get(url).status_code, {401, 403, 404})
        self.assertIn(self.client.post(url, {"name": "Changed"}).status_code, {401, 403, 404})
        self.weapon.refresh_from_db()
        self.assertEqual(self.weapon.name, "Private sword")

    def test_other_player_cannot_update(self):
        self.client.force_login(self.other)
        url = reverse("items:update:weapon", kwargs={"pk": self.weapon.pk})
        self.assertIn(self.client.get(url).status_code, {403, 404})

    def test_player_create_records_owner(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("items:create:weapon"),
            {"name": "Owned sword", "description": "A sword", "difficulty": 6,
             "damage": 4, "damage_type": "L", "conceal": "P"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Weapon.objects.get(name="Owned sword").owner, self.owner)

    def test_anonymous_gets_only_public_detail(self):
        response = self.client.get(reverse("items:weapon", kwargs={"pk": self.weapon.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Private sword")
        self.assertNotContains(response, "SECRET")

    def test_anonymous_index_uses_public_fields_only(self):
        Weapon.objects.create(
            name="Public sword", owner=self.owner, visibility="PUB",
            st_notes="ANOTHER SECRET",
        )
        response = self.client.get("/items/index/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Private sword")
        self.assertContains(response, "Public sword")
        self.assertNotContains(response, "SECRET")
        self.assertNotContains(response, self.owner.username)
