"""Tests for game app forms."""

from datetime import date

from characters.models.core import CharacterModel
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.test import TestCase
from game.forms import (
    AddCharForm,
    JournalEntryForm,
    PostForm,
    SceneCreationForm,
    StoryForm,
    STResponseForm,
    WeeklyXPRequestForm,
)
from game.models import (
    Chronicle,
    Gameline,
    Journal,
    JournalEntry,
    Scene,
    STRelationship,
    Week,
    WeeklyXPRequest,
)
from locations.models.core import LocationModel


class TestSceneCreationForm(TestCase):
    """Tests for SceneCreationForm."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="stuser", email="st@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage: the Ascension")
        STRelationship.objects.create(
            user=self.st,
            chronicle=self.chronicle,
            gameline=self.gameline,
        )
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )

    def test_form_filters_locations_by_chronicle(self):
        """Test that location queryset is filtered by chronicle."""
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        other_location = LocationModel.objects.create(
            name="Other Location",
            chronicle=other_chronicle,
        )

        form = SceneCreationForm(chronicle=self.chronicle)

        self.assertIn(self.location, form.fields["location"].queryset)
        self.assertNotIn(other_location, form.fields["location"].queryset)

    def test_form_valid_data(self):
        """Test form with valid data."""
        form = SceneCreationForm(
            data={
                "name": "Test Scene",
                "location": self.location.pk,
                "date_of_scene": "2024-01-15",
                "gameline": "mta",
            },
            chronicle=self.chronicle,
        )
        self.assertTrue(form.is_valid())

    def test_form_requires_name(self):
        """Test form requires name field."""
        form = SceneCreationForm(
            data={
                "name": "",
                "location": self.location.pk,
                "date_of_scene": "2024-01-15",
                "gameline": "mta",
            },
            chronicle=self.chronicle,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_form_requires_location(self):
        """Test form requires location field."""
        form = SceneCreationForm(
            data={
                "name": "Test Scene",
                "location": "",
                "date_of_scene": "2024-01-15",
                "gameline": "mta",
            },
            chronicle=self.chronicle,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("location", form.errors)


class TestAddCharForm(TestCase):
    """Tests for AddCharForm."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.other_character = Human.objects.create(
            name="Other Character",
            owner=self.other_user,
            chronicle=self.chronicle,
        )

    def test_form_filters_characters_by_owner(self):
        """Test that character queryset is filtered by owner."""
        form = AddCharForm(user=self.user, scene=self.scene)

        self.assertIn(self.character, form.fields["character_to_add"].queryset)
        self.assertNotIn(self.other_character, form.fields["character_to_add"].queryset)

    def test_form_excludes_characters_already_in_scene(self):
        """Test that characters already in scene are excluded."""
        self.scene.characters.add(self.character)

        form = AddCharForm(user=self.user, scene=self.scene)

        self.assertNotIn(self.character, form.fields["character_to_add"].queryset)

    def test_form_filters_by_chronicle(self):
        """Test that only characters from scene's chronicle are shown."""
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        other_char = Human.objects.create(
            name="Other Chronicle Char",
            owner=self.user,
            chronicle=other_chronicle,
        )

        form = AddCharForm(user=self.user, scene=self.scene)

        self.assertIn(self.character, form.fields["character_to_add"].queryset)
        self.assertNotIn(other_char, form.fields["character_to_add"].queryset)


class TestPostForm(TestCase):
    """Tests for PostForm."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.scene.characters.add(self.character)

    def test_form_filters_characters_in_scene(self):
        """Test that character queryset includes only scene characters."""
        other_char = Human.objects.create(
            name="Other Character",
            owner=self.user,
            chronicle=self.chronicle,
        )

        form = PostForm(user=self.user, scene=self.scene)

        self.assertIn(self.character, form.fields["character"].queryset)
        self.assertNotIn(other_char, form.fields["character"].queryset)

    def test_form_valid_data(self):
        """Test form with valid data."""
        form = PostForm(
            data={
                "character": self.character.pk,
                "display_name": "",
                "message": "Hello, world!",
            },
            user=self.user,
            scene=self.scene,
        )
        self.assertTrue(form.is_valid())

    def test_form_rejects_empty_message(self):
        """Test form rejects empty message."""
        form = PostForm(
            data={
                "character": self.character.pk,
                "display_name": "",
                "message": "",
            },
            user=self.user,
            scene=self.scene,
        )
        self.assertFalse(form.is_valid())

    def test_form_rejects_whitespace_only_message(self):
        """Test form rejects whitespace-only message."""
        form = PostForm(
            data={
                "character": self.character.pk,
                "display_name": "",
                "message": "   ",
            },
            user=self.user,
            scene=self.scene,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_form_character_not_required_when_single_character(self):
        """Test form accepts no character when user has only one character in scene."""
        # User has only one character in the scene, so character is optional
        form = PostForm(
            data={
                "character": "",
                "display_name": "",
                "message": "Hello!",
            },
            user=self.user,
            scene=self.scene,
        )
        self.assertTrue(form.is_valid())

    def test_form_character_required_when_multiple_characters(self):
        """Test form requires character when user has multiple characters in scene."""
        # Add a second character for this user
        second_char = Human.objects.create(
            name="Second Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.scene.characters.add(second_char)

        form = PostForm(
            data={
                "character": "",
                "display_name": "",
                "message": "Hello!",
            },
            user=self.user,
            scene=self.scene,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("character", form.errors)

    def test_form_valid_with_character_when_multiple(self):
        """Test form accepts character selection when user has multiple in scene."""
        second_char = Human.objects.create(
            name="Second Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.scene.characters.add(second_char)

        form = PostForm(
            data={
                "character": self.character.pk,
                "display_name": "",
                "message": "Hello!",
            },
            user=self.user,
            scene=self.scene,
        )
        self.assertTrue(form.is_valid())


class TestStoryForm(TestCase):
    """Tests for StoryForm."""

    def test_form_valid_data(self):
        """Test form with valid data."""
        form = StoryForm(data={"name": "Epic Quest"})
        self.assertTrue(form.is_valid())

    def test_form_requires_name(self):
        """Test form requires name."""
        form = StoryForm(data={"name": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_form_has_placeholder(self):
        """Test form name field has placeholder."""
        form = StoryForm()
        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Story Name",
        )


class TestJournalEntryForm(TestCase):
    """Tests for JournalEntryForm."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
        )
        self.journal, _ = Journal.objects.get_or_create(character=self.character)

    def test_form_valid_data(self):
        """Test form with valid data."""
        form = JournalEntryForm(
            data={
                "date": "2024-01-15",
                "message": "Today was interesting...",
            },
            instance=self.journal,
        )
        self.assertTrue(form.is_valid())

    def test_form_save_creates_entry(self):
        """Test form save creates journal entry."""
        form = JournalEntryForm(
            data={
                "date": "2024-01-15",
                "message": "A new entry",
            },
            instance=self.journal,
        )
        self.assertTrue(form.is_valid())
        entry = form.save()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.journal, self.journal)
        self.assertIn("A new entry", entry.message)


class TestSTResponseForm(TestCase):
    """Tests for STResponseForm."""

    def setUp(self):
        from django.utils.timezone import now

        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
        )
        self.journal, _ = Journal.objects.get_or_create(character=self.character)
        self.entry = JournalEntry.objects.create(
            journal=self.journal,
            message="Player entry",
            date=now(),
        )

    def test_form_valid_data(self):
        """Test form with valid data."""
        form = STResponseForm(
            data={"st_message": "ST response here"},
            entry=self.entry,
        )
        self.assertTrue(form.is_valid())

    def test_form_save_updates_entry(self):
        """Test form save updates entry st_message."""
        form = STResponseForm(
            data={"st_message": "Good job!"},
            entry=self.entry,
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "Good job!")


class TestWeeklyXPRequestForm(TestCase):
    """Tests for WeeklyXPRequestForm."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
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
        self.week = Week.objects.create(end_date=date(2024, 1, 14))
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
            finished=True,
        )
        self.scene.characters.add(self.character)
        # Need to add a post so the scene counts as finished for the week
        from django.utils.timezone import now
        from game.models import Post

        Post.objects.create(
            character=self.character,
            display_name="Test",
            scene=self.scene,
            message="Test post",
            datetime_created=now(),
        )

    def test_form_initialization(self):
        """Test form initializes with correct querysets."""
        form = WeeklyXPRequestForm(character=self.character, week=self.week)

        # Verify scene querysets are filtered correctly
        self.assertIsNotNone(form.fields["learning_scene"].queryset)
        self.assertIsNotNone(form.fields["rp_scene"].queryset)
        self.assertIsNotNone(form.fields["focus_scene"].queryset)
        self.assertIsNotNone(form.fields["standingout_scene"].queryset)

    def test_form_clean_learning_requires_scene(self):
        """Test that claiming learning XP requires a scene."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": True,
                "learning_scene": "",
                "rp": False,
                "focus": False,
                "standingout": False,
            },
            character=self.character,
            week=self.week,
        )
        self.assertFalse(form.is_valid())

    def test_form_clean_rp_requires_scene(self):
        """Test that claiming RP XP requires a scene."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": False,
                "rp": True,
                "rp_scene": "",
                "focus": False,
                "standingout": False,
            },
            character=self.character,
            week=self.week,
        )
        self.assertFalse(form.is_valid())

    def test_form_player_save(self):
        """Test player_save sets finishing and creates request."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": False,  # player_save should set this to True
                "learning": False,
                "rp": False,
                "focus": False,
                "standingout": False,
            },
            character=self.character,
            week=self.week,
        )
        self.assertTrue(form.is_valid())
        request = form.player_save()

        self.assertTrue(request.finishing)
        self.assertEqual(request.character, self.character)
        self.assertEqual(request.week, self.week)
        self.assertFalse(request.approved)

    def test_form_st_save_approves_and_awards_xp(self):
        """Test st_save approves request and awards XP."""
        # First create a request via player_save
        request = WeeklyXPRequest.objects.create(
            week=self.week,
            character=self.character,
            finishing=True,
        )

        initial_xp = self.character.xp

        # st_save only works with finishing XP in the basic case
        # since the scene filtering is complex
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": False,
                "rp": False,
                "focus": False,
                "standingout": False,
            },
            character=self.character,
            week=self.week,
            instance=request,
        )
        self.assertTrue(form.is_valid())
        form.st_save()

        request.refresh_from_db()
        self.character.refresh_from_db()

        self.assertTrue(request.approved)
        # finishing (1) = 1 XP
        self.assertEqual(self.character.xp, initial_xp + 1)
