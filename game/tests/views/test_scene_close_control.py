"""The scene page offers "Close scene" only to those allowed to close it."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from game.models import Chronicle, Gameline, Scene, STRelationship


class SceneCloseControlTests(TestCase):
    def setUp(self):
        self.player = User.objects.create_user("player", password="pw")
        self.st = User.objects.create_user("st", password="pw")
        self.other_st = User.objects.create_user("other-st", password="pw")
        chronicle = Chronicle.objects.create(name="Ashes")
        gameline = Gameline.objects.create(name="World of Darkness")
        STRelationship.objects.create(user=self.st, chronicle=chronicle, gameline=gameline)
        # A storyteller of the chronicle, but for another gameline: may read, not close.
        STRelationship.objects.create(
            user=self.other_st,
            chronicle=chronicle,
            gameline=Gameline.objects.create(name="Vampire: the Masquerade"),
        )
        Human.objects.create(name="Player PC", owner=self.player, chronicle=chronicle)
        self.scene = Scene.objects.create(name="Harbour", chronicle=chronicle)
        self.close_url = reverse("game:scene_close", args=[self.scene.pk])

    def page(self, user):
        self.client.force_login(user)
        response = self.client.get(self.scene.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        return response

    def test_scoped_storyteller_sees_close(self):
        response = self.page(self.st)
        self.assertTrue(response.context["can_close_scene"])
        self.assertContains(response, self.close_url)

    def test_player_does_not_see_close(self):
        response = self.page(self.player)
        self.assertFalse(response.context["can_close_scene"])
        self.assertNotContains(response, self.close_url)
        # ... and could not use it anyway.
        self.assertEqual(self.client.post(self.close_url).status_code, 403)

    def test_storyteller_of_another_gameline_does_not_see_close(self):
        response = self.page(self.other_st)
        self.assertFalse(response.context["can_close_scene"])
        self.assertNotContains(response, self.close_url)

    def test_finished_scene_offers_no_close(self):
        self.scene.finished = True
        self.scene.save()
        response = self.page(self.st)
        self.assertFalse(response.context["can_close_scene"])
        self.assertNotContains(response, self.close_url)
