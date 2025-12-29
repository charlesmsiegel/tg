"""Tests for accounts context processors."""

from datetime import date

from accounts.context_processors import notification_count, theme_context
from characters.models.core.human import Human
from characters.models.mage.rote import Rote
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.utils import timezone
from game.models import (
    Chronicle,
    Gameline,
    Journal,
    JournalEntry,
    Scene,
    STRelationship,
    UserSceneReadStatus,
    Week,
    WeeklyXPRequest,
)
from items.models.core import ItemModel
from locations.models.core import LocationModel


class TestThemeContextProcessor(TestCase):
    """Tests for theme_context context processor."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.user.profile.theme = "dark"
        self.user.profile.highlight_text = False
        self.user.profile.save()

    def test_authenticated_user_gets_theme(self):
        """Test that authenticated users get their theme settings."""
        request = self.factory.get("/")
        request.user = self.user
        context = theme_context(request)
        self.assertEqual(context["user_theme"], "dark")
        self.assertEqual(context["user_highlight_text"], False)

    def test_unauthenticated_user_gets_empty_context(self):
        """Test that unauthenticated users get empty context."""
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.get("/")
        request.user = AnonymousUser()
        context = theme_context(request)
        self.assertEqual(context, {})


class TestNotificationCountContextProcessor(TestCase):
    """Tests for notification_count context processor."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)

    def test_unauthenticated_user_gets_zero_notifications(self):
        """Test that unauthenticated users get zero notifications."""
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.get("/")
        request.user = AnonymousUser()
        context = notification_count(request)
        self.assertEqual(context["notification_count"], 0)
        self.assertEqual(context["notification_breakdown"], {})

    def test_authenticated_user_with_no_notifications(self):
        """Test authenticated user with no pending items."""
        request = self.factory.get("/")
        request.user = self.user
        context = notification_count(request)
        self.assertEqual(context["notification_count"], 0)

    def test_unread_scenes_counted(self):
        """Test that unread scenes are counted in notifications."""
        scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        UserSceneReadStatus.objects.create(user=self.user, scene=scene, read=False)
        request = self.factory.get("/")
        request.user = self.user
        context = notification_count(request)
        self.assertEqual(context["notification_count"], 1)
        self.assertIn("Unread Scenes", context["notification_breakdown"])

    def test_weekly_xp_requests_counted(self):
        """Test that pending weekly XP requests are counted."""
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        week = Week.objects.create(end_date=date.today())
        week.characters.add(char)
        # No WeeklyXPRequest exists, so it should be counted as unfulfilled
        request = self.factory.get("/")
        request.user = self.user
        context = notification_count(request)
        self.assertEqual(context["notification_count"], 1)
        self.assertIn("Weekly XP Requests", context["notification_breakdown"])

    def test_st_sees_xp_requests_from_scenes(self):
        """Test that storytellers see scene XP requests."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
            xp_given=False,
            finished=True,
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Scene XP Requests", context["notification_breakdown"])

    def test_st_sees_characters_to_approve(self):
        """Test that storytellers see characters to approve."""
        Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="Sub",
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Characters to Approve", context["notification_breakdown"])

    def test_st_sees_locations_to_approve(self):
        """Test that storytellers see locations to approve."""
        LocationModel.objects.create(
            name="Pending Location", chronicle=self.chronicle, status="Sub"
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Locations to Approve", context["notification_breakdown"])

    def test_st_sees_items_to_approve(self):
        """Test that storytellers see items to approve."""
        ItemModel.objects.create(name="Pending Item", chronicle=self.chronicle, status="Sub")
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Items to Approve", context["notification_breakdown"])

    def test_st_sees_rotes_to_approve(self):
        """Test that storytellers see rotes to approve."""
        from characters.models.core import Ability, Attribute
        from characters.models.mage.effect import Effect

        effect = Effect.objects.create(name="Test Effect")
        attribute = Attribute.objects.create(name="Strength", property_name="strength")
        ability = Ability.objects.create(name="Athletics", property_name="athletics")
        Rote.objects.create(
            name="Pending Rote",
            chronicle=self.chronicle,
            status="Sub",
            effect=effect,
            attribute=attribute,
            ability=ability,
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Rotes to Approve", context["notification_breakdown"])

    def test_st_sees_freebies_to_approve(self):
        """Test that storytellers see freebies to approve.

        Note: Characters need creation_status set to their class's freebie_step
        to show up in freebies_to_approve. For VtMHuman (which Human inherits from),
        freebie_step = 5.
        """
        from characters.models.vampire.vtmhuman import VtMHuman

        VtMHuman.objects.create(
            name="Freebies Char",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            creation_status=5,  # freebie_step for VtMHuman
            freebies_approved=False,
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Freebies to Approve", context["notification_breakdown"])

    def test_st_sees_character_images_to_approve(self):
        """Test that storytellers see character images to approve.

        Note: with_pending_images() requires both image_status="sub" AND an actual image.
        Since we can't easily set an image in tests, we test that the code path works
        by verifying no error is raised and the count includes only valid items.
        """
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            image_status="sub",
            image="test_image.png",  # Simulate having an image
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        # The character has an image, so it should be counted
        self.assertIn("Character Images to Approve", context["notification_breakdown"])

    def test_st_sees_location_images_to_approve(self):
        """Test that storytellers see location images to approve."""
        LocationModel.objects.create(
            name="Test Location 2",
            chronicle=self.chronicle,
            image_status="sub",
            image="test_image.png",
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Location Images to Approve", context["notification_breakdown"])

    def test_st_sees_item_images_to_approve(self):
        """Test that storytellers see item images to approve."""
        ItemModel.objects.create(
            name="Test Item",
            chronicle=self.chronicle,
            image_status="sub",
            image="test_image.png",
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Item Images to Approve", context["notification_breakdown"])

    def test_st_sees_scenes_needing_attention(self):
        """Test that storytellers see scenes needing attention."""
        Scene.objects.create(
            name="Waiting Scene",
            chronicle=self.chronicle,
            location=self.location,
            waiting_for_st=True,
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Scenes Needing Attention", context["notification_breakdown"])

    def test_st_sees_updated_journals(self):
        """Test that storytellers see updated journals."""
        char = Human.objects.create(
            name="Journal Char",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        # Character creation automatically creates a Journal, so get the existing one
        journal = char.journal
        JournalEntry.objects.create(journal=journal, st_message="", date=timezone.now())
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Updated Journals", context["notification_breakdown"])

    def test_st_sees_weekly_xp_to_approve(self):
        """Test that storytellers see weekly XP to approve."""
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        week = Week.objects.create(end_date=date.today())
        week.characters.add(char)
        scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        WeeklyXPRequest.objects.create(
            character=char,
            week=week,
            rp_scene=scene,
            learning_scene=scene,
            standingout_scene=scene,
            focus_scene=scene,
            approved=False,
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("Weekly XP to Approve", context["notification_breakdown"])

    def test_st_sees_xp_spend_requests(self):
        """Test that storytellers see XP spend requests."""
        from game.models import XPSpendingRequest

        char = Human.objects.create(
            name="XP Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        XPSpendingRequest.objects.create(
            character=char,
            trait="strength",
            xp_cost=5,
            approved="Pending",
        )
        request = self.factory.get("/")
        request.user = self.st_user
        context = notification_count(request)
        self.assertIn("XP Spend Requests", context["notification_breakdown"])

    def test_notification_count_handles_exceptions(self):
        """Test that notification_count returns 0 on exception.

        We simulate this by creating a user without a profile (which shouldn't
        happen in normal operation but tests the exception handling).
        """
        from unittest.mock import patch

        request = self.factory.get("/")
        request.user = self.user

        # Patch the profile to raise an exception
        with patch.object(type(self.user), "profile", property(lambda _: (_ for _ in ()).throw(Exception("Test error")))):
            context = notification_count(request)
            self.assertEqual(context["notification_count"], 0)
            self.assertEqual(context["notification_breakdown"], {})


class TestThemeContextHighlightVariations(TestCase):
    """Additional tests for theme_context variations."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_theme_context_with_highlight_true(self):
        """Test theme_context with highlight_text enabled."""
        user = User.objects.create_user("highlight_user", "hl@test.com", "password")
        user.profile.theme = "light"
        user.profile.highlight_text = True
        user.profile.save()

        request = self.factory.get("/")
        request.user = user
        context = theme_context(request)
        self.assertEqual(context["user_theme"], "light")
        self.assertEqual(context["user_highlight_text"], True)

    def test_theme_context_default_theme(self):
        """Test theme_context with default theme."""
        user = User.objects.create_user("default_user", "default@test.com", "password")
        # Don't modify the profile, use defaults

        request = self.factory.get("/")
        request.user = user
        context = theme_context(request)
        self.assertEqual(context["user_theme"], user.profile.theme)
        self.assertEqual(context["user_highlight_text"], user.profile.highlight_text)
