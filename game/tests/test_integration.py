"""
Integration tests for the game app.

Tests cover:
- Signal handlers (Journal auto-creation)
- Form validation (WeeklyXPRequestForm, SceneCreationForm, JournalEntryForm, PostForm)
- Story CRUD operations
- Week management and XP workflows
- Journal entry workflows
- Message processing with rolls and expenditures
"""
from datetime import date, timedelta

from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
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
    Post,
    Scene,
    Story,
    STRelationship,
    Week,
    WeeklyXPRequest,
    get_next_sunday,
    message_processing,
)
from locations.models.core import LocationModel


class TestJournalSignal(TestCase):
    """Test that Journal is automatically created for new characters."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_journal_created_on_character_creation(self):
        """Test that creating a character automatically creates a journal."""
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.assertTrue(Journal.objects.filter(character=char).exists())
        journal = Journal.objects.get(character=char)
        self.assertEqual(journal.character, char)

    def test_journal_string_representation(self):
        """Test journal string representation."""
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        journal = Journal.objects.get(character=char)
        self.assertEqual(str(journal), "Test Character's Journal")

    def test_multiple_characters_get_separate_journals(self):
        """Test that each character gets their own journal."""
        char1 = Human.objects.create(
            name="Character 1",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        char2 = Human.objects.create(
            name="Character 2",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        journal1 = Journal.objects.get(character=char1)
        journal2 = Journal.objects.get(character=char2)
        self.assertNotEqual(journal1.pk, journal2.pk)

    def test_journal_has_get_absolute_url(self):
        """Test that journal has proper absolute URL."""
        char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        journal = Journal.objects.get(character=char)
        url = journal.get_absolute_url()
        self.assertIn(str(journal.pk), url)


class TestWeeklyXPRequestFormValidation(TestCase):
    """Test WeeklyXPRequestForm validation and saving."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.week = Week.objects.create(end_date=date.today())
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
            finished=True,
        )
        # Add character to scene so it appears in the week's finished scenes
        self.scene.characters.add(self.char)
        # Create a post to set the latest_post_date
        Post.objects.create(
            character=self.char,
            display_name=self.char.name,
            scene=self.scene,
            message="Test post",
        )

    def test_learning_requires_scene(self):
        """Test that learning XP requires a scene."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": True,
                "rp": False,
                "focus": False,
                "standingout": False,
                "learning_scene": None,
                "rp_scene": None,
                "focus_scene": None,
                "standingout_scene": None,
            },
            character=self.char,
            week=self.week,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Must include scene for any XP claimed", str(form.errors))

    def test_rp_requires_scene(self):
        """Test that RP XP requires a scene."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": False,
                "rp": True,
                "focus": False,
                "standingout": False,
                "learning_scene": None,
                "rp_scene": None,
                "focus_scene": None,
                "standingout_scene": None,
            },
            character=self.char,
            week=self.week,
        )
        self.assertFalse(form.is_valid())

    def test_focus_requires_scene(self):
        """Test that focus XP requires a scene."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": False,
                "rp": False,
                "focus": True,
                "standingout": False,
                "learning_scene": None,
                "rp_scene": None,
                "focus_scene": None,
                "standingout_scene": None,
            },
            character=self.char,
            week=self.week,
        )
        self.assertFalse(form.is_valid())

    def test_standingout_requires_scene(self):
        """Test that standing out XP requires a scene."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": False,
                "rp": False,
                "focus": False,
                "standingout": True,
                "learning_scene": None,
                "rp_scene": None,
                "focus_scene": None,
                "standingout_scene": None,
            },
            character=self.char,
            week=self.week,
        )
        self.assertFalse(form.is_valid())

    def test_valid_form_with_no_extra_xp(self):
        """Test valid form with just finishing XP."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": False,
                "rp": False,
                "focus": False,
                "standingout": False,
                "learning_scene": "",
                "rp_scene": "",
                "focus_scene": "",
                "standingout_scene": "",
            },
            character=self.char,
            week=self.week,
        )
        self.assertTrue(form.is_valid())

    def test_player_save_sets_finishing_true(self):
        """Test that player_save always sets finishing to True."""
        form = WeeklyXPRequestForm(
            data={
                "finishing": False,  # Even if set to False
                "learning": False,
                "rp": False,
                "focus": False,
                "standingout": False,
                "learning_scene": "",
                "rp_scene": "",
                "focus_scene": "",
                "standingout_scene": "",
            },
            character=self.char,
            week=self.week,
        )
        form.is_valid()
        request = form.player_save()
        self.assertTrue(request.finishing)
        self.assertEqual(request.character, self.char)
        self.assertEqual(request.week, self.week)

    def test_st_save_awards_xp_to_character(self):
        """Test that st_save awards XP to character."""
        # Create existing request
        request = WeeklyXPRequest.objects.create(
            week=self.week, character=self.char, finishing=True, learning=False
        )
        initial_xp = self.char.xp
        form = WeeklyXPRequestForm(
            data={
                "finishing": True,
                "learning": True,
                "rp": True,
                "focus": False,
                "standingout": False,
                "learning_scene": self.scene.pk,
                "rp_scene": self.scene.pk,
                "focus_scene": "",
                "standingout_scene": "",
            },
            character=self.char,
            week=self.week,
            instance=request,
        )
        form.is_valid()
        form.st_save()
        self.char.refresh_from_db()
        # Should gain 3 XP (finishing + learning + rp)
        self.assertEqual(self.char.xp, initial_xp + 3)
        self.assertTrue(request.approved)


class TestSceneCreationForm(TestCase):
    """Test SceneCreationForm validation."""

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location1 = LocationModel.objects.create(
            name="Location 1", chronicle=self.chronicle
        )
        self.location2 = LocationModel.objects.create(
            name="Location 2", chronicle=self.chronicle
        )
        self.other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        self.other_location = LocationModel.objects.create(
            name="Other Location", chronicle=self.other_chronicle
        )

    def test_form_filters_locations_by_chronicle(self):
        """Test that form only shows locations from the chronicle."""
        form = SceneCreationForm(chronicle=self.chronicle)
        location_queryset = form.fields["location"].queryset
        self.assertIn(self.location1, location_queryset)
        self.assertIn(self.location2, location_queryset)
        self.assertNotIn(self.other_location, location_queryset)

    def test_valid_form(self):
        """Test valid scene creation form."""
        form = SceneCreationForm(
            data={
                "name": "Test Scene",
                "location": self.location1.id,
                "date_of_scene": "2024-01-01",
            },
            chronicle=self.chronicle,
        )
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        """Test that name is required."""
        form = SceneCreationForm(
            data={
                "name": "",
                "location": self.location1.id,
                "date_of_scene": "2024-01-01",
            },
            chronicle=self.chronicle,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TestAddCharForm(TestCase):
    """Test AddCharForm for adding characters to scenes."""

    def setUp(self):
        self.user1 = User.objects.create_user("user1", "user1@test.com", "password")
        self.user2 = User.objects.create_user("user2", "user2@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.char1 = Human.objects.create(
            name="Character 1",
            owner=self.user1,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.char2 = Human.objects.create(
            name="Character 2",
            owner=self.user1,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.other_user_char = Human.objects.create(
            name="Other User Char",
            owner=self.user2,
            chronicle=self.chronicle,
            concept="Test",
        )

    def test_form_only_shows_user_characters(self):
        """Test that form only shows characters owned by user."""
        form = AddCharForm(user=self.user1, scene=self.scene)
        queryset = form.fields["character_to_add"].queryset
        self.assertIn(self.char1, queryset)
        self.assertIn(self.char2, queryset)
        self.assertNotIn(self.other_user_char, queryset)

    def test_form_excludes_already_added_characters(self):
        """Test that form excludes characters already in scene."""
        self.scene.characters.add(self.char1)
        form = AddCharForm(user=self.user1, scene=self.scene)
        queryset = form.fields["character_to_add"].queryset
        self.assertNotIn(self.char1, queryset)
        self.assertIn(self.char2, queryset)


class TestPostForm(TestCase):
    """Test PostForm validation."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.characters.add(self.char)

    def test_form_only_shows_user_characters_in_scene(self):
        """Test that form only shows user's characters that are in the scene."""
        form = PostForm(user=self.user, scene=self.scene)
        queryset = form.fields["character"].queryset
        self.assertIn(self.char, queryset)

    def test_message_cannot_be_empty(self):
        """Test that message cannot be empty."""
        form = PostForm(
            data={"character": self.char.id, "display_name": "", "message": ""},
            user=self.user,
            scene=self.scene,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("The message cannot be empty", str(form.errors))

    def test_message_cannot_be_whitespace_only(self):
        """Test that message cannot be just whitespace."""
        form = PostForm(
            data={"character": self.char.id, "display_name": "", "message": "   "},
            user=self.user,
            scene=self.scene,
        )
        self.assertFalse(form.is_valid())

    def test_valid_message(self):
        """Test valid message."""
        form = PostForm(
            data={
                "character": self.char.id,
                "display_name": "",
                "message": "Hello world",
            },
            user=self.user,
            scene=self.scene,
        )
        self.assertTrue(form.is_valid())

    def test_display_name_is_optional(self):
        """Test that display_name is optional."""
        form = PostForm(
            data={
                "character": self.char.id,
                "display_name": "",
                "message": "Test message",
            },
            user=self.user,
            scene=self.scene,
        )
        self.assertTrue(form.is_valid())


class TestJournalEntryForm(TestCase):
    """Test JournalEntryForm validation."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.char = Human.objects.create(
            name="Test Character", owner=self.user, concept="Test"
        )
        self.journal = Journal.objects.get(character=self.char)

    def test_valid_form(self):
        """Test valid journal entry form."""
        form = JournalEntryForm(
            data={"date": "2024-01-01", "message": "Dear diary..."},
            instance=self.journal,
        )
        self.assertTrue(form.is_valid())

    def test_save_creates_entry(self):
        """Test that save creates a journal entry."""
        form = JournalEntryForm(
            data={"date": "2024-01-01", "message": "Dear diary..."},
            instance=self.journal,
        )
        form.is_valid()
        entry = form.save()
        self.assertIsInstance(entry, JournalEntry)
        self.assertEqual(entry.journal, self.journal)
        self.assertIn("Dear diary", entry.message)


class TestSTResponseForm(TestCase):
    """Test STResponseForm for responding to journal entries."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.char = Human.objects.create(
            name="Test Character", owner=self.user, concept="Test"
        )
        self.journal = Journal.objects.get(character=self.char)
        self.entry = JournalEntry.objects.create(
            journal=self.journal, message="Test entry", date=date.today()
        )

    def test_valid_form(self):
        """Test valid ST response form."""
        form = STResponseForm(data={"st_message": "ST response here"}, entry=self.entry)
        self.assertTrue(form.is_valid())

    def test_save_updates_entry(self):
        """Test that save updates the journal entry."""
        form = STResponseForm(data={"st_message": "ST response here"}, entry=self.entry)
        form.is_valid()
        form.save()
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.st_message, "ST response here")


class TestStoryForm(TestCase):
    """Test StoryForm validation."""

    def test_valid_form(self):
        """Test valid story form."""
        form = StoryForm(data={"name": "Epic Adventure"})
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        """Test that name is required."""
        form = StoryForm(data={"name": ""})
        self.assertFalse(form.is_valid())


class TestStoryViews(TestCase):
    """Test Story CRUD views."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.story = Story.objects.create(name="Test Story")

    def test_story_list_view(self):
        """Test story list view."""
        response = self.client.get(reverse("game:story:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Story")

    def test_story_detail_view(self):
        """Test story detail view."""
        response = self.client.get(
            reverse("game:story:detail", kwargs={"pk": self.story.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Story")

    def test_story_create_view(self):
        """Test story create view."""
        initial_count = Story.objects.count()
        response = self.client.post(reverse("game:story:create"), {"name": "New Story"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Story.objects.count(), initial_count + 1)

    def test_story_update_view(self):
        """Test story update view."""
        response = self.client.post(
            reverse("game:story:update", kwargs={"pk": self.story.pk}),
            {"name": "Updated Story"},
        )
        self.assertEqual(response.status_code, 302)
        self.story.refresh_from_db()
        self.assertEqual(self.story.name, "Updated Story")


class TestWeekModel(TestCase):
    """Test Week model methods."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )
        # Create a week that ends on a Sunday
        sunday = get_next_sunday(date.today())
        self.week = Week.objects.create(end_date=sunday)
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )

    def test_start_date_is_7_days_before_end_date(self):
        """Test that start_date is 7 days before end_date."""
        self.assertEqual(self.week.start_date, self.week.end_date - timedelta(days=7))

    def test_week_string_representation(self):
        """Test week string representation."""
        expected = f"{self.week.start_date } - { self.week.end_date }"
        self.assertEqual(str(self.week), expected)

    def test_weekly_characters_returns_scene_participants(self):
        """Test that weekly_characters returns characters who participated in scenes."""
        scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
            finished=True,
        )
        scene.characters.add(self.char)
        # Create a post within the week
        Post.objects.create(
            character=self.char,
            display_name=self.char.name,
            scene=scene,
            message="Test post",
        )
        chars = self.week.weekly_characters()
        self.assertIn(self.char, chars)


class TestSceneModel(TestCase):
    """Test Scene model methods."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )

    def test_close_scene_sets_finished(self):
        """Test that closing scene sets finished to True."""
        self.assertFalse(self.scene.finished)
        self.scene.close()
        self.assertTrue(self.scene.finished)

    def test_close_scene_creates_week(self):
        """Test that closing scene creates or gets appropriate week."""
        self.scene.characters.add(self.char)
        self.scene.close()
        self.assertTrue(Week.objects.exists())

    def test_close_scene_adds_characters_to_week(self):
        """Test that closing scene adds characters to week."""
        self.scene.characters.add(self.char)
        self.scene.close()
        week = Week.objects.first()
        self.assertIn(self.char, week.characters.all())

    def test_add_post_marks_unread_for_other_users(self):
        """Test that adding a post marks scene as unread for other users."""
        user2 = User.objects.create_user("user2", "user2@test.com", "password")
        char2 = Human.objects.create(
            name="Character 2",
            owner=user2,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.characters.add(self.char, char2)
        self.scene.add_post(self.char, "", "Test message")
        from game.models import UserSceneReadStatus

        status = UserSceneReadStatus.objects.get(user=user2, scene=self.scene)
        self.assertFalse(status.read)

    def test_add_post_sets_waiting_for_st_on_at_storyteller(self):
        """Test that @storyteller message sets waiting_for_st."""
        self.scene.characters.add(self.char)
        self.scene.add_post(self.char, "", "@storyteller Need help with something")
        self.assertTrue(self.scene.waiting_for_st)
        self.assertEqual(self.scene.st_message, "Need help with something")


class TestMessageProcessing(TestCase):
    """Test message_processing function for dice rolls and expenditures."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.char = Human.objects.create(
            name="Test Character", owner=self.user, concept="Test"
        )
        self.char.temporary_willpower = 5
        self.char.save()

    def test_wp_expenditure_decrements_willpower(self):
        """Test that #WP decrements temporary willpower."""
        message = "I spend willpower #WP"
        message_processing(self.char, message)
        self.char.refresh_from_db()
        self.assertEqual(self.char.temporary_willpower, 4)

    def test_wp_with_number_decrements_by_amount(self):
        """Test that #WP2 decrements by specified amount."""
        message = "I spend 2 willpower #WP2"
        message_processing(self.char, message)
        self.char.refresh_from_db()
        self.assertEqual(self.char.temporary_willpower, 3)

    def test_bashing_damage(self):
        """Test that #1B adds bashing damage."""
        initial_bashing = self.char.current_health_levels.count("B")
        message = "Take a hit #1B"
        message_processing(self.char, message)
        self.char.refresh_from_db()
        new_bashing = self.char.current_health_levels.count("B")
        self.assertEqual(new_bashing, initial_bashing + 1)

    def test_lethal_damage(self):
        """Test that #1L adds lethal damage."""
        initial_lethal = self.char.current_health_levels.count("L")
        message = "Take a sword hit #1L"
        message_processing(self.char, message)
        self.char.refresh_from_db()
        new_lethal = self.char.current_health_levels.count("L")
        self.assertEqual(new_lethal, initial_lethal + 1)

    def test_aggravated_damage(self):
        """Test that #1A adds aggravated damage."""
        initial_agg = self.char.current_health_levels.count("A")
        message = "Fire damage #1A"
        message_processing(self.char, message)
        self.char.refresh_from_db()
        new_agg = self.char.current_health_levels.count("A")
        self.assertEqual(new_agg, initial_agg + 1)

    def test_roll_command_formats_output(self):
        """Test that /roll command formats the output correctly."""
        message = "Attack /roll 5"
        result = message_processing(self.char, message)
        self.assertIn("roll of 5 dice", result)
        self.assertIn("difficulty 6", result)

    def test_roll_with_difficulty(self):
        """Test roll with custom difficulty."""
        message = "Difficult roll /roll 3 difficulty 8"
        result = message_processing(self.char, message)
        self.assertIn("difficulty 8", result)

    def test_roll_with_specialty(self):
        """Test roll with specialty."""
        message = "Expert roll /roll 4 difficulty 6 true"
        result = message_processing(self.char, message)
        self.assertIn("with relevant specialty", result)

    def test_invalid_roll_raises_error(self):
        """Test that invalid roll command raises ValueError."""
        message = "Bad roll /roll invalid"
        with self.assertRaises(ValueError):
            message_processing(self.char, message)


class TestChronicleModel(TestCase):
    """Test Chronicle model methods."""

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )

    def test_add_scene_creates_new_scene(self):
        """Test that add_scene creates a new scene."""
        scene = self.chronicle.add_scene("New Scene", self.location)
        self.assertIsInstance(scene, Scene)
        self.assertEqual(scene.name, "New Scene")
        self.assertEqual(scene.chronicle, self.chronicle)

    def test_add_scene_with_date(self):
        """Test add_scene with date_of_scene."""
        test_date = date(2024, 1, 15)
        scene = self.chronicle.add_scene(
            "Dated Scene", self.location, date_of_scene=test_date
        )
        self.assertEqual(scene.date_of_scene, test_date)

    def test_add_scene_returns_existing_if_duplicate(self):
        """Test that add_scene returns existing scene if name and location match."""
        scene1 = self.chronicle.add_scene("Same Scene", self.location)
        scene2 = self.chronicle.add_scene("Same Scene", self.location)
        self.assertEqual(scene1.pk, scene2.pk)

    def test_total_scenes(self):
        """Test total_scenes count."""
        self.assertEqual(self.chronicle.total_scenes(), 0)
        self.chronicle.add_scene("Scene 1", self.location)
        self.assertEqual(self.chronicle.total_scenes(), 1)
        self.chronicle.add_scene("Scene 2", self.location)
        self.assertEqual(self.chronicle.total_scenes(), 2)

    def test_get_active_scenes(self):
        """Test get_active_scenes returns only unfinished scenes."""
        scene1 = self.chronicle.add_scene("Active Scene", self.location)
        scene2 = self.chronicle.add_scene("Finished Scene", self.location)
        scene2.finished = True
        scene2.save()
        active = self.chronicle.get_active_scenes()
        self.assertIn(scene1, active)
        self.assertNotIn(scene2, active)

    def test_storyteller_list(self):
        """Test storyteller_list returns comma-separated usernames."""
        user1 = User.objects.create_user("st1", "st1@test.com", "password")
        user2 = User.objects.create_user("st2", "st2@test.com", "password")
        gameline = Gameline.objects.create(name="Test")
        STRelationship.objects.create(
            user=user1, chronicle=self.chronicle, gameline=gameline
        )
        STRelationship.objects.create(
            user=user2, chronicle=self.chronicle, gameline=gameline
        )
        st_list = self.chronicle.storyteller_list()
        self.assertIn("st1", st_list)
        self.assertIn("st2", st_list)


class TestGetNextSunday(TestCase):
    """Test get_next_sunday utility function."""

    def test_sunday_returns_same_day(self):
        """Test that if given date is Sunday, it returns the same date."""
        sunday = date(2024, 1, 7)  # This is a Sunday
        result = get_next_sunday(sunday)
        self.assertEqual(result, sunday)

    def test_monday_returns_next_sunday(self):
        """Test that Monday returns the following Sunday."""
        monday = date(2024, 1, 8)
        expected_sunday = date(2024, 1, 14)
        result = get_next_sunday(monday)
        self.assertEqual(result, expected_sunday)

    def test_saturday_returns_next_day(self):
        """Test that Saturday returns the next day (Sunday)."""
        saturday = date(2024, 1, 13)
        expected_sunday = date(2024, 1, 14)
        result = get_next_sunday(saturday)
        self.assertEqual(result, expected_sunday)

    def test_wednesday_returns_next_sunday(self):
        """Test Wednesday to Sunday calculation."""
        wednesday = date(2024, 1, 10)
        expected_sunday = date(2024, 1, 14)
        result = get_next_sunday(wednesday)
        self.assertEqual(result, expected_sunday)


class TestJournalListView(TestCase):
    """Test JournalListView."""

    def test_journal_list_view(self):
        """Test journal list view."""
        response = self.client.get(reverse("game:journal_list"))
        self.assertEqual(response.status_code, 200)


class TestChronicleListView(TestCase):
    """Test ChronicleListView."""

    def test_chronicle_list_view(self):
        """Test chronicle list view."""
        Chronicle.objects.create(name="Test Chronicle")
        response = self.client.get(reverse("game:chronicle_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Chronicle")


class TestSceneListView(TestCase):
    """Test SceneListView."""

    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )

    def test_scene_list_view(self):
        """Test scene list view."""
        response = self.client.get(reverse("game:scene_list"))
        self.assertEqual(response.status_code, 200)
