"""The week page links a player to the weekly XP request page for their characters."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from characters.models.core.human import Human
from game.models import Chronicle, Post, Scene, Week, WeeklyXPRequest


class WeekRequestLinkTests(TestCase):
    def setUp(self):
        self.player = User.objects.create_user("player", password="pw")
        self.other = User.objects.create_user("other", password="pw")
        chronicle = Chronicle.objects.create(name="Ashes")
        self.mine = Human.objects.create(name="Mine", owner=self.player, chronicle=chronicle)
        self.theirs = Human.objects.create(name="Theirs", owner=self.other, chronicle=chronicle)
        scene = Scene.objects.create(name="Harbour", chronicle=chronicle, finished=True)
        scene.characters.add(self.mine, self.theirs)
        Post.objects.create(scene=scene, character=self.mine, display_name="Mine", message="hi")
        self.week = Week.objects.create(end_date=timezone.localdate())
        self.client.force_login(self.player)

    def create_url(self, character):
        return reverse("game:weekly_xp_request:create", args=[self.week.pk, character.pk])

    def test_links_only_the_viewers_characters_without_a_request(self):
        response = self.client.get(self.week.get_absolute_url())
        self.assertEqual(response.context["characters_to_file"], [self.mine])
        self.assertContains(response, self.create_url(self.mine))
        self.assertNotContains(response, self.create_url(self.theirs))

    def test_no_link_once_filed(self):
        WeeklyXPRequest.objects.create(week=self.week, character=self.mine)
        response = self.client.get(self.week.get_absolute_url())
        self.assertEqual(response.context["characters_to_file"], [])
        self.assertNotContains(response, self.create_url(self.mine))
