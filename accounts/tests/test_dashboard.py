"""Behavioral tests for profile dashboard notification aggregation."""

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.dashboard import ProfileDashboard
from characters.models.core import Human
from game.models import Chronicle, Gameline, Scene, STRelationship, UserSceneReadStatus
from items.models.core import ItemModel
from locations.models.core import LocationModel


class TestProfileDashboardNotifications(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("dashboard-user", "dashboard@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Dashboard Chronicle")
        Human.objects.create(name="Dashboard character", owner=self.user, chronicle=self.chronicle)
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


class TestProfileDashboardSelectors(TestCase):
    def setUp(self):
        self.st_user = User.objects.create_user("selector-st", "st@test.com", "password")
        self.owner = User.objects.create_user("selector-owner", "owner@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Selector Chronicle")
        gameline = Gameline.objects.create(name="Selector Gameline")
        STRelationship.objects.create(
            user=self.st_user,
            chronicle=self.chronicle,
            gameline=gameline,
        )

        self.owned = {
            "my_characters": Human.objects.create(
                name="Owned Character",
                owner=self.st_user,
                chronicle=self.chronicle,
                concept="Test",
                status="App",
            ),
            "my_locations": LocationModel.objects.create(
                name="Owned Location",
                owner=self.st_user,
                chronicle=self.chronicle,
                status="App",
            ),
            "my_items": ItemModel.objects.create(
                name="Owned Item",
                owner=self.st_user,
                chronicle=self.chronicle,
                status="App",
            ),
        }
        self.pending = {
            "characters_to_approve": Human.objects.create(
                name="Pending Character",
                owner=self.owner,
                chronicle=self.chronicle,
                concept="Test",
                status="Sub",
            ),
            "locations_to_approve": LocationModel.objects.create(
                name="Pending Location",
                owner=self.owner,
                chronicle=self.chronicle,
                status="Sub",
            ),
            "items_to_approve": ItemModel.objects.create(
                name="Pending Item",
                owner=self.owner,
                chronicle=self.chronicle,
                status="Sub",
            ),
        }
        self.pending_images = {
            "character_images_to_approve": Human.objects.create(
                name="Pending Character Image",
                owner=self.owner,
                chronicle=self.chronicle,
                concept="Test",
                status="App",
                image_status="sub",
                image="test_image.png",
            ),
            "location_images_to_approve": LocationModel.objects.create(
                name="Pending Location Image",
                owner=self.owner,
                chronicle=self.chronicle,
                status="App",
                image_status="sub",
                image="test_image.png",
            ),
            "item_images_to_approve": ItemModel.objects.create(
                name="Pending Item Image",
                owner=self.owner,
                chronicle=self.chronicle,
                status="App",
                image_status="sub",
                image="test_image.png",
            ),
        }

    def assert_dashboard_matches_profile(self, method_name, expected):
        dashboard_result = getattr(self.st_user.profile.dashboard, method_name)()
        profile_result = getattr(self.st_user.profile, method_name)()

        self.assertQuerySetEqual(dashboard_result, profile_result, transform=lambda obj: obj)
        self.assertIn(expected, dashboard_result)

    def test_owned_selectors_match_profile_compatibility_methods(self):
        for method_name, expected in self.owned.items():
            with self.subTest(method=method_name):
                self.assert_dashboard_matches_profile(method_name, expected)

    def test_pending_approval_selectors_match_profile_compatibility_methods(self):
        for method_name, expected in self.pending.items():
            with self.subTest(method=method_name):
                self.assert_dashboard_matches_profile(method_name, expected)

    def test_pending_image_selectors_match_profile_compatibility_methods(self):
        for method_name, expected in self.pending_images.items():
            with self.subTest(method=method_name):
                self.assert_dashboard_matches_profile(method_name, expected)


class TestHeadStorytellerDashboard(TestCase):
    def test_head_storyteller_sees_submitted_objects_without_legacy_m2m(self):
        head = User.objects.create_user("dashboard-head")
        owner = User.objects.create_user("dashboard-owner")
        chronicle = Chronicle.objects.create(name="Head dashboard", head_st=head)
        character = Human.objects.create(
            name="Submitted character", owner=owner,
            chronicle=chronicle, status="Sub",
        )
        item = ItemModel.objects.create(
            name="Submitted item", owner=owner,
            chronicle=chronicle, status="Sub",
        )

        dashboard = head.profile.dashboard
        self.assertIn(character, dashboard.characters_to_approve())
        self.assertIn(item, dashboard.items_to_approve())
        self.assertNotIn(character, owner.profile.dashboard.characters_to_approve())

    def test_staff_sees_submitted_object_without_chronicle(self):
        staff = User.objects.create_user("dashboard-staff", is_staff=True)
        owner = User.objects.create_user("dashboard-global-owner")
        item = ItemModel.objects.create(
            name="Global pending item", owner=owner, status="Sub"
        )
        self.assertIn(item, staff.profile.dashboard.items_to_approve())
