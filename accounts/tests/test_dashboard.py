"""Behavioral tests for profile dashboard notification aggregation."""

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.dashboard import ProfileDashboard
from game.models import Chronicle, Scene, UserSceneReadStatus
from locations.models.core import LocationModel


class TestProfileDashboardNotifications(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("dashboard-user", "dashboard@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Dashboard Chronicle")
        self.location = LocationModel.objects.create(
            name="Dashboard Location", chronicle=self.chronicle, status="App"
        )

    def test_notification_context_includes_positive_player_count(self):
        scene = Scene.objects.create(
            name="Unread Scene", chronicle=self.chronicle, location=self.location
        )
        UserSceneReadStatus.objects.create(user=self.user, scene=scene, read=False)

        context = ProfileDashboard(self.user.profile).notification_context()

        self.assertEqual(
            context,
            {
                "notification_count": 1,
                "notification_breakdown": {"Unread Scenes": 1},
            },
        )

    def test_notification_context_omits_zero_counts(self):
        context = ProfileDashboard(self.user.profile).notification_context()

        self.assertEqual(
            context,
            {"notification_count": 0, "notification_breakdown": {}},
        )
