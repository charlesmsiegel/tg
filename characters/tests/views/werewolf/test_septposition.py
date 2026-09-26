"""Tests for the SeptPosition views."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from characters.models.werewolf.septposition import SeptPosition
from characters.views.werewolf.septposition import SeptPositionUpdateView


class TestSeptPositionUpdateView(TestCase):
    """SeptPosition is reference data: only staff may edit it."""

    def setUp(self):
        self.staff = User.objects.create_user("staff", "s@test.com", "password", is_staff=True)
        self.player = User.objects.create_user("player", "p@test.com", "password")
        self.position = SeptPosition.objects.create(name="Warder", description="Guards the caern.")
        self.url = self.position.get_update_url()

    def test_update_url_resolves(self):
        self.assertEqual(self.url, f"/characters/werewolf/update/septposition/{self.position.pk}/")
        self.assertIs(resolve(self.url).func.view_class, SeptPositionUpdateView)

    def test_staff_can_open_update(self):
        self.client.force_login(self.staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/werewolf/septposition/form.html")

    def test_staff_can_save_update(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            self.url, {"name": "Master of the Challenge", "description": "Rules on duels."}
        )
        self.assertEqual(response.status_code, 302)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Master of the Challenge")

    def test_non_staff_cannot_update(self):
        self.client.force_login(self.player)
        response = self.client.post(self.url, {"name": "Hijacked", "description": ""})
        self.assertEqual(response.status_code, 403)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Warder")
