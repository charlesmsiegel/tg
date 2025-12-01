"""
Cross-app integration tests.

Tests cover:
- Full character lifecycle (creation → chronicle → scene → XP)
- Complete XP approval workflow
- Chronicle management with multiple users
- Permission boundaries across apps
- Character status transitions
"""

from datetime import date

from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import (
    Chronicle,
    Gameline,
    Journal,
    Post,
    Scene,
    STRelationship,
    Week,
    WeeklyXPRequest,
)
from items.models.core import ItemModel
from locations.models.core import LocationModel


class TestCharacterLifecycleIntegration(TestCase):
    """Test complete character lifecycle from creation to retirement."""

    def setUp(self):
        self.user = User.objects.create_user("player", "player@test.com", "password")
        self.st_user = User.objects.create_user("st", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Main Chronicle")
        self.gameline = Gameline.objects.create(name="Vampire")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Downtown", chronicle=self.chronicle)

    def test_character_creation_creates_journal(self):
        """Test that character creation triggers journal creation."""
        char = Human.objects.create(
            name="New Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.assertTrue(Journal.objects.filter(character=char).exists())

    def test_character_submission_workflow(self):
        """Test character submission and approval workflow."""
        char = Human.objects.create(
            name="New Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="Un",  # Unfinished
        )

        # Submit character
        char.status = "Sub"
        char.save()
        self.assertEqual(char.status, "Sub")

        # ST approves character
        self.client.login(username="st", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(), {"approve_character": char.id}
        )
        char.refresh_from_db()
        self.assertEqual(char.status, "App")

    def test_approved_character_can_join_scenes(self):
        """Test that approved characters can join scenes."""
        char = Human.objects.create(
            name="Approved Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )

        self.client.login(username="player", password="password")
        response = self.client.post(f"/game/scene/{scene.id}", {"character_to_add": char.id})
        scene.refresh_from_db()
        self.assertIn(char, scene.characters.all())

    def test_scene_participation_to_xp_workflow(self):
        """Test complete scene participation to XP award workflow."""
        char = Human.objects.create(
            name="Active Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        scene.characters.add(char)

        # Create post in scene
        post = scene.add_post(char, "", "Character acts")
        self.assertIsNotNone(post)
        self.assertEqual(scene.total_posts(), 1)

        # Close scene (creates week and adds character)
        initial_xp = char.xp
        scene.close()
        self.assertTrue(scene.finished)
        self.assertTrue(Week.objects.exists())
        week = Week.objects.first()
        self.assertIn(char, week.characters.all())

        # Award scene XP
        scene.award_xp({char: True})
        char.refresh_from_db()
        self.assertEqual(char.xp, initial_xp + 1)
        self.assertTrue(scene.xp_given)

    def test_character_retirement(self):
        """Test character retirement workflow."""
        char = Human.objects.create(
            name="Old Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        char.status = "Ret"  # Retired
        char.save()
        self.assertEqual(char.status, "Ret")

    def test_character_death(self):
        """Test character deceased status."""
        char = Human.objects.create(
            name="Dead Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        char.status = "Dec"  # Deceased
        char.save()
        self.assertEqual(char.status, "Dec")


class TestXPApprovalWorkflowIntegration(TestCase):
    """Test complete XP approval workflow across apps."""

    def setUp(self):
        self.user = User.objects.create_user("player", "player@test.com", "password")
        self.st_user = User.objects.create_user("st", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Main Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        self.week = Week.objects.create(end_date=date.today())
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
            finished=True,
        )
        self.scene.characters.add(self.char)
        # Create a post to establish latest_post_date
        Post.objects.create(
            character=self.char,
            display_name=self.char.name,
            scene=self.scene,
            message="Test post",
        )

    def test_player_submits_weekly_xp_request(self):
        """Test that player can submit weekly XP request."""
        self.week.characters.add(self.char)
        self.client.login(username="player", password="password")

        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {
                f"submit_weekly_request": f"week-{self.week.pk}-char-{self.char.pk}",
                "finishing": "on",
                "learning": "off",
                "rp": "off",
                "focus": "off",
                "standingout": "off",
                "learning_scene": "",
                "rp_scene": "",
                "focus_scene": "",
                "standingout_scene": "",
            },
        )
        self.assertTrue(
            WeeklyXPRequest.objects.filter(character=self.char, week=self.week).exists()
        )
        request = WeeklyXPRequest.objects.get(character=self.char, week=self.week)
        self.assertTrue(request.finishing)
        self.assertFalse(request.approved)

    def test_player_cannot_submit_for_other_character(self):
        """Test that player cannot submit request for another user's character."""
        other_user = User.objects.create_user("other", "other@test.com", "password")
        other_char = Human.objects.create(
            name="Other Character",
            owner=other_user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.week.characters.add(other_char)
        self.client.login(username="player", password="password")

        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {
                f"submit_weekly_request": f"week-{self.week.pk}-char-{other_char.pk}",
                "finishing": "on",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_st_approves_weekly_xp_request(self):
        """Test that ST can approve weekly XP request and award XP."""
        self.week.characters.add(self.char)
        request = WeeklyXPRequest.objects.create(
            week=self.week,
            character=self.char,
            finishing=True,
            learning=False,
            rp=False,
            focus=False,
            standingout=False,
            approved=False,
        )
        initial_xp = self.char.xp

        self.client.login(username="st", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {
                f"submit_weekly_approval": f"week-{self.week.pk}-char-{self.char.pk}",
                "finishing": "on",
                "learning": "on",
                "rp": "off",
                "focus": "off",
                "standingout": "off",
                "learning_scene": str(self.scene.pk),
                "rp_scene": "",
                "focus_scene": "",
                "standingout_scene": "",
            },
        )

        request.refresh_from_db()
        self.char.refresh_from_db()
        self.assertTrue(request.approved)
        # Should gain 2 XP (finishing + learning)
        self.assertEqual(self.char.xp, initial_xp + 2)


class TestChronicleManagementIntegration(TestCase):
    """Test chronicle management with multiple users and objects."""

    def setUp(self):
        self.st1 = User.objects.create_user("st1", "st1@test.com", "password")
        self.st2 = User.objects.create_user("st2", "st2@test.com", "password")
        self.player1 = User.objects.create_user("player1", "player1@test.com", "password")
        self.player2 = User.objects.create_user("player2", "player2@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Multi-User Chronicle")
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st1, chronicle=self.chronicle, gameline=self.gameline
        )
        STRelationship.objects.create(
            user=self.st2, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)

    def test_multiple_sts_can_approve_different_characters(self):
        """Test that multiple STs can approve characters."""
        char1 = Human.objects.create(
            name="Character 1",
            owner=self.player1,
            chronicle=self.chronicle,
            concept="Test",
            status="Sub",
        )
        char2 = Human.objects.create(
            name="Character 2",
            owner=self.player2,
            chronicle=self.chronicle,
            concept="Test",
            status="Sub",
        )

        # ST1 approves character 1
        self.client.login(username="st1", password="password")
        self.client.post(self.st1.profile.get_absolute_url(), {"approve_character": char1.id})
        char1.refresh_from_db()
        self.assertEqual(char1.status, "App")

        # ST2 approves character 2
        self.client.login(username="st2", password="password")
        self.client.post(self.st2.profile.get_absolute_url(), {"approve_character": char2.id})
        char2.refresh_from_db()
        self.assertEqual(char2.status, "App")

    def test_chronicle_tracks_all_objects(self):
        """Test that chronicle properly tracks all associated objects."""
        # Create characters
        char1 = Human.objects.create(
            name="Player 1 Char",
            owner=self.player1,
            chronicle=self.chronicle,
            concept="Test",
        )
        char2 = Human.objects.create(
            name="Player 2 Char",
            owner=self.player2,
            chronicle=self.chronicle,
            concept="Test",
        )

        # Create items
        item = ItemModel.objects.create(name="Chronicle Item", chronicle=self.chronicle)

        # Create locations
        loc = LocationModel.objects.create(name="Chronicle Location", chronicle=self.chronicle)

        # Create scenes
        scene1 = self.chronicle.add_scene("Scene 1", self.location)
        scene2 = self.chronicle.add_scene("Scene 2", self.location)

        # Verify counts
        self.assertEqual(self.chronicle.total_scenes(), 2)
        self.assertEqual(LocationModel.objects.filter(chronicle=self.chronicle).count(), 2)
        self.assertEqual(ItemModel.objects.filter(chronicle=self.chronicle).count(), 1)

    def test_scene_with_multiple_player_characters(self):
        """Test scene with characters from multiple players."""
        char1 = Human.objects.create(
            name="Player 1 Char",
            owner=self.player1,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        char2 = Human.objects.create(
            name="Player 2 Char",
            owner=self.player2,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        scene = Scene.objects.create(
            name="Multi-Player Scene", chronicle=self.chronicle, location=self.location
        )

        # Player 1 adds their character
        self.client.login(username="player1", password="password")
        self.client.post(f"/game/scene/{scene.id}", {"character_to_add": char1.id})
        scene.refresh_from_db()
        self.assertIn(char1, scene.characters.all())

        # Player 2 adds their character
        self.client.login(username="player2", password="password")
        self.client.post(f"/game/scene/{scene.id}", {"character_to_add": char2.id})
        scene.refresh_from_db()
        self.assertIn(char2, scene.characters.all())

        # Verify both are in scene
        self.assertEqual(scene.total_characters(), 2)


class TestPermissionBoundariesIntegration(TestCase):
    """Test permission boundaries across the application."""

    def setUp(self):
        self.user = User.objects.create_user("player", "player@test.com", "password")
        self.st_user = User.objects.create_user("st", "st@test.com", "password")
        self.other_user = User.objects.create_user("other", "other@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)

    def test_non_st_cannot_perform_approval_actions(self):
        """Test that regular users cannot perform ST-only actions."""
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="Sub",
        )
        location = LocationModel.objects.create(
            name="Sub Location", chronicle=self.chronicle, status="Sub"
        )
        item = ItemModel.objects.create(name="Sub Item", chronicle=self.chronicle, status="Sub")

        self.client.login(username="player", password="password")

        # Try to approve character
        response = self.client.post(
            self.user.profile.get_absolute_url(), {"approve_character": char.id}
        )
        self.assertEqual(response.status_code, 403)

        # Try to approve location
        response = self.client.post(
            self.user.profile.get_absolute_url(), {"approve_location": location.id}
        )
        self.assertEqual(response.status_code, 403)

        # Try to approve item
        response = self.client.post(self.user.profile.get_absolute_url(), {"approve_item": item.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_add_other_users_characters_to_scene(self):
        """Test that user cannot add another user's character to scene."""
        other_char = Human.objects.create(
            name="Other User Char",
            owner=self.other_user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )

        self.client.login(username="player", password="password")
        response = self.client.post(f"/game/scene/{scene.id}", {"character_to_add": other_char.id})
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_post_as_other_users_character(self):
        """Test that user cannot post as another user's character."""
        other_char = Human.objects.create(
            name="Other User Char",
            owner=self.other_user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        scene.characters.add(other_char)

        self.client.login(username="player", password="password")
        response = self.client.post(
            f"/game/scene/{scene.id}",
            {
                "character": other_char.id,
                "display_name": "",
                "message": "Trying to post as someone else",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_non_st_cannot_close_scene(self):
        """Test that regular users cannot close scenes."""
        scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )

        self.client.login(username="player", password="password")
        response = self.client.post(f"/game/scene/{scene.id}", {"close_scene": "true"})
        self.assertEqual(response.status_code, 403)
        scene.refresh_from_db()
        self.assertFalse(scene.finished)

    def test_non_st_cannot_create_scene(self):
        """Test that regular users cannot create scenes."""
        self.client.login(username="player", password="password")
        response = self.client.post(
            f"/game/chronicle/{self.chronicle.id}",
            {
                "create_scene": "true",
                "name": "Unauthorized Scene",
                "location": self.location.id,
                "date_of_scene": "2024-01-01",
            },
        )
        self.assertEqual(response.status_code, 403)


class TestProfileUnreadScenesIntegration(TestCase):
    """Test unread scene tracking across users."""

    def setUp(self):
        self.user1 = User.objects.create_user("user1", "user1@test.com", "password")
        self.user2 = User.objects.create_user("user2", "user2@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.char1 = Human.objects.create(
            name="Character 1",
            owner=self.user1,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.char2 = Human.objects.create(
            name="Character 2",
            owner=self.user2,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.scene.characters.add(self.char1, self.char2)

    def test_post_marks_scene_unread_for_other_users(self):
        """Test that posting marks scene unread for other participants."""
        self.scene.add_post(self.char1, "", "Test message")
        unread = self.user2.profile.unread_scenes()
        self.assertIn(self.scene, unread)

    def test_poster_does_not_see_scene_as_unread(self):
        """Test that poster does not see their own scene as unread."""
        self.scene.add_post(self.char1, "", "Test message")
        unread = self.user1.profile.unread_scenes()
        self.assertNotIn(self.scene, unread)

    def test_mark_scene_read_clears_unread_status(self):
        """Test that marking scene read clears unread status."""
        self.scene.add_post(self.char1, "", "Test message")
        self.client.login(username="user2", password="password")
        self.client.post(
            self.user2.profile.get_absolute_url(),
            {"mark_scene_read": self.scene.id},
        )
        unread = self.user2.profile.unread_scenes()
        self.assertNotIn(self.scene, unread)


class TestCharacterXPIntegration(TestCase):
    """Test character XP integration across the application."""

    def setUp(self):
        self.user = User.objects.create_user("player", "player@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )

    def test_add_xp_method(self):
        """Test add_xp method updates XP correctly."""
        initial_xp = self.char.xp
        self.char.add_xp(5)
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, initial_xp + 5)

    def test_multiple_xp_sources_accumulate(self):
        """Test that XP from multiple sources accumulates."""
        self.char.add_xp(3)  # Scene XP
        self.char.add_xp(2)  # Story XP
        self.char.add_xp(1)  # Weekly XP
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, 6)

    def test_negative_xp_allowed_for_spending(self):
        """Test that negative XP can be added for spending."""
        self.char.xp = 10
        self.char.save()
        self.char.add_xp(-3)
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, 7)


class TestJournalWorkflowIntegration(TestCase):
    """Test complete journal workflow from entry to ST response."""

    def setUp(self):
        self.user = User.objects.create_user("player", "player@test.com", "password")
        self.st_user = User.objects.create_user("st", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.journal = Journal.objects.get(character=self.char)

    def test_complete_journal_entry_workflow(self):
        """Test complete workflow: entry creation, ST response."""
        # Player adds journal entry
        entry = self.journal.add_post(date.today(), "Dear diary, today was eventful...")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.st_message, "")

        # ST responds
        entry.st_message = "Interesting development. +1 XP for good roleplay."
        entry.save()
        entry.refresh_from_db()
        self.assertEqual(entry.st_message, "Interesting development. +1 XP for good roleplay.")

    def test_journal_tracks_all_entries(self):
        """Test that journal tracks all entries."""
        self.journal.add_post(date.today(), "Entry 1")
        self.journal.add_post(date.today(), "Entry 2")
        self.journal.add_post(date.today(), "Entry 3")
        entries = self.journal.all_entries()
        self.assertEqual(entries.count(), 3)

    def test_unfulfilled_journal_entries_tracking(self):
        """Test tracking of journal entries without ST responses."""
        entry1 = self.journal.add_post(date.today(), "Entry 1")
        entry2 = self.journal.add_post(date.today(), "Entry 2")

        # No responses yet
        updated_journals = self.st_user.profile.get_updated_journals()
        self.assertIn(self.journal, updated_journals)

        # Respond to one
        entry1.st_message = "Response"
        entry1.save()

        # Still should appear (entry2 has no response)
        updated_journals = self.st_user.profile.get_updated_journals()
        self.assertIn(self.journal, updated_journals)

        # Respond to the other
        entry2.st_message = "Another response"
        entry2.save()

        # Should no longer appear
        updated_journals = self.st_user.profile.get_updated_journals()
        self.assertNotIn(self.journal, updated_journals)
