"""Weekly XP request pages: double submits and concurrent approvals end in a message."""

from datetime import date
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from game.forms import WeeklyXPRequestForm
from game.models import Chronicle, Gameline, STRelationship, Week, WeeklyXPRequest


class WeeklyXPRequestPagesTests(TestCase):
    def setUp(self):
        self.player = User.objects.create_user("player", password="pw")
        self.st = User.objects.create_user("st", password="pw")
        chronicle = Chronicle.objects.create(name="Ashes")
        STRelationship.objects.create(
            user=self.st,
            chronicle=chronicle,
            gameline=Gameline.objects.create(name="World of Darkness"),
        )
        self.char = Human.objects.create(
            name="Claimant", owner=self.player, chronicle=chronicle, status="App"
        )
        self.week = Week.objects.create(end_date=date(2024, 1, 14))

    def messages(self, response):
        return [str(m) for m in response.context["messages"]]

    def test_approval_that_loses_a_race_is_reported(self):
        """Another ST approves between the view's check and approve(): no 500, no double XP."""
        xp_request = WeeklyXPRequest.objects.create(character=self.char, week=self.week)
        original = WeeklyXPRequestForm.is_valid

        def approved_meanwhile(form):
            other = WeeklyXPRequest.objects.get(pk=xp_request.pk)
            other.approve()
            return original(form)

        self.client.force_login(self.st)
        with mock.patch.object(WeeklyXPRequestForm, "is_valid", approved_meanwhile):
            response = self.client.post(
                reverse("game:weekly_xp_request:approve", args=[xp_request.pk]),
                {"finishing": True},
                follow=True,
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("This XP request has already been approved.", self.messages(response))
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, 1)

    def test_create_that_loses_a_race_files_one_request(self):
        """A request filed between the create view's check and its insert wins."""
        original = WeeklyXPRequestForm.player_save

        def racing_player_save(form, commit=True):
            WeeklyXPRequest.objects.create(character=self.char, week=self.week)
            return original(form, commit=commit)

        self.client.force_login(self.player)
        with mock.patch.object(WeeklyXPRequestForm, "player_save", racing_player_save):
            response = self.client.post(
                reverse("game:weekly_xp_request:create", args=[self.week.pk, self.char.pk]), {}
            )
        self.assertRedirects(
            response,
            reverse("game:week:detail", args=[self.week.pk]),
            fetch_redirect_response=False,
        )
        self.assertEqual(WeeklyXPRequest.objects.filter(character=self.char).count(), 1)

    def test_create_reports_success(self):
        self.client.force_login(self.player)
        response = self.client.post(
            reverse("game:weekly_xp_request:create", args=[self.week.pk, self.char.pk]),
            {},
            follow=True,
        )
        self.assertIn("Weekly XP request submitted successfully!", self.messages(response))
        self.assertTrue(WeeklyXPRequest.objects.get(character=self.char).finishing)
