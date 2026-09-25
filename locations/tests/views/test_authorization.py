from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from game.models import Chronicle, Gameline, STRelationship
from locations.models.core.city import City


class CityAuthorizationTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("city_owner")
        self.other = users.objects.create_user("city_other")
        self.head = users.objects.create_user("city_head")
        self.st = users.objects.create_user("city_st")
        self.wrong_st = users.objects.create_user("city_wrong_st")
        self.staff = users.objects.create_user("city_staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="City chronicle", head_st=self.head)
        wod = Gameline.objects.create(name="World of Darkness")
        vtm = Gameline.objects.create(name="Vampire: the Masquerade")
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=wod)
        STRelationship.objects.create(
            user=self.wrong_st, chronicle=self.chronicle, gameline=vtm
        )
        self.city = City.objects.create(
            name="Draft city", owner=self.owner, chronicle=self.chronicle,
            status="Un", st_notes="PRIVATE ST NOTES",
        )

    def test_public_card_hides_private_fields(self):
        response = self.client.get(reverse("locations:location", args=[self.city.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft city")
        self.assertNotContains(response, "PRIVATE ST NOTES")

    def test_private_city_is_unlisted_but_public_city_is_discoverable(self):
        City.objects.create(name="Public city", visibility="PUB")
        response = self.client.get("/locations/index/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Draft city")
        self.assertContains(response, "Public city")

    def test_owner_can_edit_only_before_submission(self):
        url = reverse("locations:update:city", args=[self.city.pk])
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.city.status = "Sub"
        self.city.save(update_fields=["status"])
        self.assertEqual(self.client.get(url).status_code, 403)

    def test_other_player_and_wrong_gameline_st_cannot_edit(self):
        url = reverse("locations:update:city", args=[self.city.pk])
        for user in (self.other, self.wrong_st):
            self.client.force_login(user)
            self.assertEqual(self.client.get(url).status_code, 403)

    def test_matching_st_head_and_staff_can_edit_shared_city(self):
        self.city.owner = None
        self.city.save(update_fields=["owner"])
        url = reverse("locations:update:city", args=[self.city.pk])
        for user in (self.st, self.head, self.staff):
            self.client.force_login(user)
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_character_possession_does_not_grant_edit_of_ownerless_city(self):
        character = Human.objects.create(
            name="Resident", owner=self.owner, chronicle=self.chronicle
        )
        self.city.owner = None
        self.city.owned_by = character
        self.city.save(update_fields=["owner", "owned_by"])
        self.client.force_login(self.owner)
        self.assertEqual(
            self.client.get(reverse("locations:update:city", args=[self.city.pk])).status_code,
            403,
        )

    def test_player_creation_records_owner(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("locations:create:city"),
            {"name": "Owned city", "description": "A settlement", "gauntlet": 7,
             "shroud": 7, "dimension_barrier": 6, "population": 100},
        )
        self.assertEqual(response.status_code, 302)
        city = City.objects.get(name="Owned city")
        self.assertEqual(city.owner, self.owner)
        self.assertEqual(city.status, "Un")
