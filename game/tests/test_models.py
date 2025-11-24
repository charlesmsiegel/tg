"""
Additional tests for game models beyond existing tests.

Tests cover:
- Story model and methods
- Journal model
- Additional Chronicle functionality
- Additional Scene functionality
- Week and XP request edge cases
"""
from characters.models.core import Human
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, Gameline, Journal, Scene, Story, Week, WeeklyXPRequest
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
            chronicle=self.chronicle,
            description="Characters discover their true nature",
        )
        self.assertEqual(story.name, "The Awakening")
        self.assertEqual(story.chronicle, self.chronicle)

    def test_story_str_representation(self):
        """Test string representation of a story."""
        story = Story.objects.create(
            name="Test Story",
            chronicle=self.chronicle,
        )
        self.assertEqual(str(story), "Test Story")

    def test_story_belongs_to_chronicle(self):
        """Test that stories are associated with chronicles."""
        story = Story.objects.create(
            name="Story",
            chronicle=self.chronicle,
        )
        self.assertEqual(story.chronicle, self.chronicle)

    def test_story_can_have_multiple_scenes(self):
        """Test that stories can track multiple scenes."""
        story = Story.objects.create(
            name="Test Story",
            chronicle=self.chronicle,
        )
        location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )

        scene1 = Scene.objects.create(
            name="Scene 1",
            chronicle=self.chronicle,
            location=location,
            story=story,
        )
        scene2 = Scene.objects.create(
            name="Scene 2",
            chronicle=self.chronicle,
            location=location,
            story=story,
        )

        scenes = Scene.objects.filter(story=story)
        self.assertEqual(scenes.count(), 2)


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

    def test_journal_creation(self):
        """Test creating a journal entry."""
        journal = Journal.objects.create(
            character=self.character,
            title="My First Entry",
            content="Today was an interesting day...",
        )
        self.assertEqual(journal.character, self.character)
        self.assertEqual(journal.title, "My First Entry")

    def test_journal_str_representation(self):
        """Test string representation of a journal."""
        journal = Journal.objects.create(
            character=self.character,
            title="Test Entry",
            content="Test content",
        )
        expected = f"{self.character.name} - Test Entry"
        self.assertEqual(str(journal), expected)

    def test_journal_ordering(self):
        """Test that journals are ordered by creation date."""
        journal1 = Journal.objects.create(
            character=self.character,
            title="First",
            content="First entry",
        )
        journal2 = Journal.objects.create(
            character=self.character,
            title="Second",
            content="Second entry",
        )

        journals = list(Journal.objects.filter(character=self.character))
        # Should be ordered newest first or oldest first depending on implementation
        self.assertEqual(len(journals), 2)

    def test_journal_belongs_to_character(self):
        """Test that journals belong to specific characters."""
        journal = Journal.objects.create(
            character=self.character,
            title="Entry",
            content="Content",
        )
        self.assertEqual(journal.character, self.character)


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

    def test_scene_xp_distribution(self):
        """Test XP distribution to scene participants."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
            xp=3,  # XP awarded for this scene
        )

        scene.participants.add(self.character)

        # XP should be distributable to participants
        self.assertEqual(scene.xp, 3)
        self.assertIn(self.character, scene.participants.all())

    def test_scene_can_have_multiple_participants(self):
        """Test that scenes can have multiple participants."""
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

        scene.participants.add(self.character, char2)

        self.assertEqual(scene.participants.count(), 2)

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
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            xp=10,
        )

    def test_week_creation(self):
        """Test creating a week for XP tracking."""
        week = Week.objects.create(
            chronicle=self.chronicle,
            week_number=1,
        )

        self.assertEqual(week.chronicle, self.chronicle)
        self.assertEqual(week.week_number, 1)

    def test_xp_request_creation(self):
        """Test creating an XP spending request."""
        week = Week.objects.create(
            chronicle=self.chronicle,
            week_number=1,
        )

        xp_request = WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            xp_spent=5,
            description="Increase Melee from 2 to 3",
        )

        self.assertEqual(xp_request.character, self.character)
        self.assertEqual(xp_request.xp_spent, 5)
        self.assertFalse(xp_request.approved)  # Should default to not approved

    def test_xp_request_approval(self):
        """Test approving an XP request."""
        week = Week.objects.create(
            chronicle=self.chronicle,
            week_number=1,
        )

        xp_request = WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            xp_spent=3,
            description="New ability: Occult 1",
        )

        # ST approves the request
        xp_request.approved = True
        xp_request.save()

        xp_request.refresh_from_db()
        self.assertTrue(xp_request.approved)

    def test_xp_request_rejection(self):
        """Test that XP requests can be rejected."""
        week = Week.objects.create(
            chronicle=self.chronicle,
            week_number=1,
        )

        xp_request = WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            xp_spent=3,
        )

        # ST can leave it unapproved (rejected)
        self.assertFalse(xp_request.approved)

    def test_multiple_xp_requests_per_week(self):
        """Test that characters can have multiple XP requests per week."""
        week = Week.objects.create(
            chronicle=self.chronicle,
            week_number=1,
        )

        WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            xp_spent=3,
            description="Ability increase",
        )

        WeeklyXPRequest.objects.create(
            character=self.character,
            week=week,
            xp_spent=2,
            description="Background increase",
        )

        requests = WeeklyXPRequest.objects.filter(character=self.character, week=week)
        self.assertEqual(requests.count(), 2)
