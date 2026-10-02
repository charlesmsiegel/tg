"""Game-app rules moved out of views: selectors, text utility, XP request service."""

from datetime import date, datetime, timezone
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from characters.models.core.human import Human
from game.consumers import SceneChatConsumer
from game.models import Chronicle, Post, Scene, Week, WeeklyXPRequest
from game.selectors import annotate_week_scene_counts, count_dates_in_week
from game.text import straighten_quotes
from game.views import SceneDetailView
from locations.models.core import LocationModel


class StraightenQuotesTests(SimpleTestCase):
    def test_one_implementation_serves_views_and_consumer(self):
        self.assertIs(SceneDetailView.straighten_quotes, straighten_quotes)
        self.assertIs(SceneChatConsumer.straighten_quotes, straighten_quotes)
        self.assertEqual(straighten_quotes("“it’s” `x´"), "\"it's\" 'x'")


class WeekSceneCountTests(SimpleTestCase):
    def test_counts_are_inclusive_seven_day_windows(self):
        dates = sorted(
            [
                date(2024, 1, 7),  # start of the week ending Jan 14 (end - 7 days)
                date(2024, 1, 10),
                date(2024, 1, 14),  # end date, inclusive
                date(2024, 1, 15),
                date(2024, 1, 6),
            ]
        )
        self.assertEqual(count_dates_in_week(dates, date(2024, 1, 14)), 3)
        self.assertEqual(count_dates_in_week(dates, date(2024, 1, 7)), 2)
        self.assertEqual(count_dates_in_week([], date(2024, 1, 7)), 0)


class WeekListSceneCountTests(TestCase):
    def test_list_shows_counts_for_visible_finished_scenes(self):
        user = get_user_model().objects.create_user("week-viewer", is_staff=True)
        chronicle = Chronicle.objects.create(name="C")
        location = LocationModel.objects.create(name="L", chronicle=chronicle)
        character = Human.objects.create(name="Poster", owner=user, chronicle=chronicle)
        week = Week.objects.create(end_date=date(2024, 1, 14))
        for day in (8, 13, 20):
            scene = Scene.objects.create(
                name=f"S{day}", chronicle=chronicle, location=location, finished=True
            )
            post = Post.objects.create(
                scene=scene, character=character, display_name="P", message="hi"
            )
            Post.objects.filter(pk=post.pk).update(
                datetime_created=datetime(2024, 1, day, 12, tzinfo=timezone.utc)
            )
        annotate_week_scene_counts([week], user)
        self.assertEqual(week.cached_scene_count, 2)


class WeeklyXPRequestCreateTests(TestCase):
    def test_submission_saves_once(self):
        user = get_user_model().objects.create_user("xp-owner")
        character = Human.objects.create(name="Claimant", owner=user)
        week = Week.objects.create(end_date=date(2024, 1, 14))
        self.client.force_login(user)
        original = WeeklyXPRequest.save
        with mock.patch.object(
            WeeklyXPRequest, "save", autospec=True, side_effect=original
        ) as save:
            response = self.client.post(
                reverse("game:weekly_xp_request:create", args=[week.pk, character.pk]), {}
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(save.call_count, 1)
        xp_request = WeeklyXPRequest.objects.get(character=character, week=week)
        self.assertTrue(xp_request.finishing)

    def test_duplicate_is_refused(self):
        user = get_user_model().objects.create_user("xp-owner-2")
        character = Human.objects.create(name="Claimant", owner=user)
        week = Week.objects.create(end_date=date(2024, 1, 14))
        WeeklyXPRequest.objects.create(character=character, week=week, finishing=True)
        self.client.force_login(user)
        response = self.client.post(
            reverse("game:weekly_xp_request:create", args=[week.pk, character.pk]), {}
        )
        self.assertRedirects(
            response, reverse("game:week:detail", args=[week.pk]), fetch_redirect_response=False
        )
        self.assertEqual(WeeklyXPRequest.objects.filter(character=character).count(), 1)
