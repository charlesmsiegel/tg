"""Tests for the Drone update routes."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from characters.models.werewolf.drone import Drone
from characters.views.werewolf.drone import DroneCharacterCreationView, DroneUpdateView
from game.models import Chronicle


class TestDroneUpdateRoutes(TestCase):
    """Drone follows the fomor pattern: a router route and a full-edit route."""

    def setUp(self):
        self.player = User.objects.create_user("player", "p@test.com", "password")
        self.st = User.objects.create_user("st", "st@test.com", "password")
        self.other = User.objects.create_user("other", "o@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st)
        self.drone = Drone.objects.create(
            name="Test Drone",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
            gnosis=1,
        )

    def test_update_url_resolves_to_creation_router(self):
        url = self.drone.get_update_url()
        self.assertEqual(url, f"/characters/werewolf/update/drone/{self.drone.pk}/")
        self.assertIs(resolve(url).func.view_class, DroneCharacterCreationView)

    def test_full_update_url_resolves_to_update_view(self):
        url = self.drone.get_full_update_url()
        self.assertEqual(url, f"/characters/werewolf/update/drone/full/{self.drone.pk}/")
        self.assertIs(resolve(url).func.view_class, DroneUpdateView)

    def test_st_can_open_full_update(self):
        self.client.force_login(self.st)
        response = self.client.get(self.drone.get_full_update_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/werewolf/drone/form.html")

    def test_st_can_save_full_update(self):
        self.client.force_login(self.st)
        url = self.drone.get_full_update_url()
        form = self.client.get(url).context["form"]
        data = {name: form[name].value() for name in form.fields if form[name].value() is not None}
        data.update({"name": "Renamed Drone", "gnosis": 3})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.drone.refresh_from_db()
        self.assertEqual(self.drone.name, "Renamed Drone")
        self.assertEqual(self.drone.gnosis, 3)

    def test_unrelated_user_cannot_open_full_update(self):
        self.client.force_login(self.other)
        response = self.client.get(self.drone.get_full_update_url())
        self.assertEqual(response.status_code, 403)
