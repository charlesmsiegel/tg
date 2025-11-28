"""
Additional tests for game models beyond existing tests.

Tests cover:
- Story model and methods
- Journal model
- Additional Chronicle functionality
- Additional Scene functionality
- Week and XP request edge cases
"""
from datetime import date, timedelta

from characters.models.core import Human
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now
from game.models import Chronicle, Gameline, Journal, JournalEntry, Scene, Story, Week, WeeklyXPRequest
from locations.models.core import LocationModel


class TestStory(TestCase):
    """Test the Story model."""

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.user = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )

    def test_story_creation(self):
        """Test creating a story."""
        story = Story.objects.create(
            name="The Awakening",
        )
        self.assertEqual(story.name, "The Awakening")
        self.assertFalse(story.xp_given)

    def test_story_str_representation(self):
        """Test string representation of a story."""
        story = Story.objects.create(
            name="Test Story",
        )
        self.assertEqual(str(story), "Test Story")

    def test_story_xp_given_flag(self):
        """Test that stories track XP given status."""
        story = Story.objects.create(
            name="Story",
        )
        self.assertFalse(story.xp_given)
        story.xp_given = True
        story.save()
        story.refresh_from_db()
        self.assertTrue(story.xp_given)

    def test_story_get_absolute_url(self):
        """Test that stories have an absolute URL."""
        story = Story.objects.create(
            name="Test Story",
        )
        url = story.get_absolute_url()
        self.assertIn(str(story.pk), url)


class TestJournal(TestCase):
    """Test the Journal model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
        )
        # Journal is auto-created by signal when character is created
        # Use get_or_create to handle both cases
        self.journal, _ = Journal.objects.get_or_create(
            character=self.character,
        )

    def test_journal_creation(self):
        """Test creating a journal for a character."""
        # Compare by pk since Journal.character is FK to CharacterModel (polymorphic)
        self.assertEqual(self.journal.character.pk, self.character.pk)

    def test_journal_str_representation(self):
        """Test string representation of a journal."""
        expected = f"{self.character.name}'s Journal"
        self.assertEqual(str(self.journal), expected)

    def test_journal_add_post(self):
        """Test adding entries to a journal."""
        entry = self.journal.add_post(now(), "Today was an interesting day...")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.journal, self.journal)

    def test_journal_belongs_to_character(self):
        """Test that journals belong to specific characters."""
        # Compare by pk since Journal.character is FK to CharacterModel (polymorphic)
        self.assertEqual(self.journal.character.pk, self.character.pk)

    def test_journal_all_entries(self):
        """Test getting all entries for a journal."""
        self.journal.add_post(now(), "Entry 1")
        self.journal.add_post(now(), "Entry 2")

        entries = self.journal.all_entries()
        self.assertEqual(entries.count(), 2)


class TestChronicleAdvanced(TestCase):
    """Test advanced Chronicle functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_chronicle_total_scenes(self):
        """Test counting total scenes in a chronicle."""
        location = LocationModel.objects.create(
            name="Location",
            chronicle=self.chronicle,
        )

        Scene.objects.create(
            name="Scene 1",
            chronicle=self.chronicle,
            location=location,
        )
        Scene.objects.create(
            name="Scene 2",
            chronicle=self.chronicle,
            location=location,
        )

        total = self.chronicle.total_scenes()
        self.assertEqual(total, 2)

    def test_chronicle_can_have_storytellers(self):
        """Test that chronicles can have storytellers."""
        gameline = Gameline.objects.create(name="Test Gameline")
        # STRelationship should link user to chronicle
        from game.models import STRelationship

        STRelationship.objects.create(
            user=self.user,
            chronicle=self.chronicle,
            gameline=gameline,
        )

        # Verify relationship exists
        st_rels = STRelationship.objects.filter(chronicle=self.chronicle)
        self.assertEqual(st_rels.count(), 1)

    def test_chronicle_can_have_players(self):
        """Test that chronicles can have player characters."""
        player = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        character = Human.objects.create(
            name="Player Character",
            owner=player,
            chronicle=self.chronicle,
        )

        characters = Human.objects.filter(chronicle=self.chronicle)
        self.assertEqual(characters.count(), 1)


class TestSceneAdvanced(TestCase):
    """Test advanced Scene functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
        )

    def test_scene_xp_tracking(self):
        """Test XP tracking on scenes."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )

        scene.characters.add(self.character)

        # xp_given tracks whether XP has been awarded
        self.assertFalse(scene.xp_given)
        scene.xp_given = True
        scene.save()
        scene.refresh_from_db()
        self.assertTrue(scene.xp_given)
        self.assertIn(self.character, scene.characters.all())

    def test_scene_can_have_multiple_characters(self):
        """Test that scenes can have multiple characters."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )

        char2 = Human.objects.create(
            name="Character 2",
            owner=self.user,
            chronicle=self.chronicle,
        )

        scene.characters.add(self.character, char2)

        self.assertEqual(scene.characters.count(), 2)

    def test_scene_belongs_to_chronicle(self):
        """Test that scenes belong to chronicles."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )

        self.assertEqual(scene.chronicle, self.chronicle)

    def test_scene_has_location(self):
        """Test that scenes have locations."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )

        self.assertEqual(scene.location, self.location)

    def test_scene_close(self):
        """Test closing a scene."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        scene.characters.add(self.character)

        self.assertFalse(scene.finished)
        scene.close()
        scene.refresh_from_db()
        self.assertTrue(scene.finished)


class TestWeekAndXPRequests(TestCase):
    """Test Week and XP request functionality."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="player", email="player@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            xp=10,
        )
        # Create a scene that can be used for all XP request tests
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )

    def test_week_creation(self):
        """Test creating a week for XP tracking."""
        end_date = date.today() + timedelta(days=7)
        week = Week.objects.create(
            end_date=end_date,
        )

        self.assertEqual(week.end_date, end_date)

    def test_week_start_date(self):
        """Test that week start_date is 7 days before end_date."""
        end_date = date.today() + timedelta(days=7)
        week = Week.objects.create(
            end_date=end_date,
        )

        expected_start = end_date - timedelta(days=7)
        self.assertEqual(week.start_date, expected_start)

    def test_xp_request_creation(self):
        """Test creating an XP request."""
        end_date = date.today() + timedelta(days=7)
        week = Week.objects.create(
            end_date=end_date,
        )

        # WeeklyXPRequest requires scene FKs - provide them all
        xp_request = WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            finishing=True,
            learning=False,
            learning_scene=self.scene,
            rp_scene=self.scene,
            focus_scene=self.scene,
            standingout_scene=self.scene,
        )

        self.assertEqual(xp_request.character, self.character)
        self.assertTrue(xp_request.finishing)
        self.assertFalse(xp_request.approved)  # Should default to not approved

    def test_xp_request_approval(self):
        """Test approving an XP request."""
        end_date = date.today() + timedelta(days=7)
        week = Week.objects.create(
            end_date=end_date,
        )

        xp_request = WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            finishing=True,
            learning_scene=self.scene,
            rp_scene=self.scene,
            focus_scene=self.scene,
            standingout_scene=self.scene,
        )

        # ST approves the request
        xp_request.approved = True
        xp_request.save()

        xp_request.refresh_from_db()
        self.assertTrue(xp_request.approved)

    def test_xp_request_rejection(self):
        """Test that XP requests can be rejected."""
        end_date = date.today() + timedelta(days=7)
        week = Week.objects.create(
            end_date=end_date,
        )

        xp_request = WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            finishing=True,
            learning_scene=self.scene,
            rp_scene=self.scene,
            focus_scene=self.scene,
            standingout_scene=self.scene,
        )

        # ST can leave it unapproved (rejected)
        self.assertFalse(xp_request.approved)

    def test_xp_request_total_xp(self):
        """Test calculating total XP from request categories."""
        end_date = date.today() + timedelta(days=7)
        week = Week.objects.create(
            end_date=end_date,
        )

        xp_request = WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            finishing=True,
            learning=True,
            learning_scene=self.scene,
            rp=False,
            rp_scene=self.scene,
            focus=False,
            focus_scene=self.scene,
            standingout=False,
            standingout_scene=self.scene,
        )

        # finishing + learning = 2 XP
        self.assertEqual(xp_request.total_xp(), 2)
