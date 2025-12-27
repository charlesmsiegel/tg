from characters.models.core import CharacterModel
from characters.models.core.character import Character
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from game.models import (
    Chronicle,
    Gameline,
    ObjectType,
    Scene,
    STRelationship,
    Week,
    WeeklyXPRequest,
    extended_roll,
    message_processing,
)
from locations.models.core import LocationModel


class ChronicleTest(TestCase):
    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)

    def test_add_scene(self):
        self.assertEqual(self.chronicle.total_scenes(), 0)
        self.chronicle.add_scene("Test Scene", self.location)
        self.assertEqual(self.chronicle.total_scenes(), 1)


class SceneTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.npc = CharacterModel.objects.create(
            name="Test NPC", chronicle=self.chronicle, npc=True
        )

    def test_close_scene(self):
        self.assertFalse(self.scene.finished)
        self.scene.close()
        self.assertTrue(self.scene.finished)
        self.scene.close()
        self.assertTrue(self.scene.finished)

    def test_add_character(self):
        self.assertEqual(self.scene.total_characters(), 0)
        self.scene.add_character(self.char)
        self.assertEqual(self.scene.total_characters(), 1)
        self.scene.add_character(self.npc)
        self.assertEqual(self.scene.total_characters(), 2)

    def test_add_post(self):
        self.scene.add_character(self.char)
        self.assertEqual(self.scene.total_posts(), 0)
        post = self.scene.add_post(self.char, "", "Here's a post message.")
        self.assertEqual(self.scene.total_posts(), 1)
        self.assertEqual(post.display_name, self.char.name)
        self.assertEqual(post.message, "Here's a post message.")
        self.assertEqual(str(post), "Test Character: Here's a post message.")

    def test_award_xp(self):
        """Test that scene awards XP correctly to characters."""
        initial_xp = self.char.xp
        self.scene.award_xp({self.char: True})
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, initial_xp + 1)
        self.assertTrue(self.scene.xp_given)

    def test_award_xp_multiple_characters(self):
        """Test awarding XP to multiple characters."""
        char2 = Human.objects.create(
            name="Test Character 2",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.award_xp({self.char: True, char2: False})
        self.char.refresh_from_db()
        char2.refresh_from_db()
        self.assertEqual(self.char.xp, 1)
        self.assertEqual(char2.xp, 0)


class TestChronicleDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)

    def test_chronicle_detail_view_requires_login(self):
        """Test that unauthenticated users are redirected."""
        response = self.client.get(f"/game/chronicle/{self.chronicle.id}")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_chronicle_detail_view_status_code(self):
        """Test that authenticated users can access the page."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/chronicle/{self.chronicle.id}")
        self.assertEqual(response.status_code, 200)

    def test_chronicle_detail_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/chronicle/{self.chronicle.id}")
        self.assertTemplateUsed(response, "game/chronicle/detail.html")

    def test_non_st_cannot_create_scene(self):
        """Test that non-storytellers cannot create scenes."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            f"/game/chronicle/{self.chronicle.id}",
            {
                "create_scene": "true",
                "name": "New Scene",
                "location": self.location.id,
                "date_of_scene": "2024-01-01",
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_st_can_create_scene(self):
        """Test that storytellers can create scenes."""
        self.client.login(username="stuser", password="password")
        initial_count = Scene.objects.count()
        response = self.client.post(
            f"/game/chronicle/{self.chronicle.id}",
            {
                "create_scene": "true",
                "name": "New Scene",
                "location": self.location.id,
                "date_of_scene": "2024-01-01",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Scene.objects.count(), initial_count + 1)

    def test_404_for_nonexistent_chronicle(self):
        """Test that accessing nonexistent chronicle returns 404."""
        self.client.login(username="testuser", password="password")
        response = self.client.get("/game/chronicle/99999")
        self.assertEqual(response.status_code, 404)


class TestSceneDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.user2 = User.objects.create_user("testuser2", "test2@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )

    def test_scene_detail_view_requires_login(self):
        """Test that unauthenticated users are redirected."""
        response = self.client.get(f"/game/scene/{self.scene.id}")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_scene_detail_view_status_code(self):
        """Test that authenticated users can access the page."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.id}")
        self.assertEqual(response.status_code, 200)

    def test_scene_detail_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.id}")
        self.assertTemplateUsed(response, "game/scene/detail.html")

    def test_non_st_cannot_close_scene(self):
        """Test that non-storytellers cannot close scenes."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(f"/game/scene/{self.scene.id}", {"close_scene": "true"})
        self.assertEqual(response.status_code, 403)
        self.scene.refresh_from_db()
        self.assertFalse(self.scene.finished)

    def test_st_can_close_scene(self):
        """Test that storytellers can close scenes."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(f"/game/scene/{self.scene.id}", {"close_scene": "true"})
        self.assertEqual(response.status_code, 302)
        self.scene.refresh_from_db()
        self.assertTrue(self.scene.finished)

    def test_user_can_add_own_character(self):
        """Test that users can add their own characters to scenes."""
        self.client.login(username="testuser", password="password")
        initial_count = self.scene.characters.count()
        response = self.client.post(
            f"/game/scene/{self.scene.id}", {"character_to_add": self.char.id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.scene.characters.count(), initial_count + 1)

    def test_user_cannot_add_other_users_character(self):
        """Test that users cannot add other users' characters."""
        char2 = Human.objects.create(
            name="Other Character",
            owner=self.user2,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.client.login(username="testuser", password="password")
        response = self.client.post(f"/game/scene/{self.scene.id}", {"character_to_add": char2.id})
        self.assertEqual(response.status_code, 403)

    def test_404_for_nonexistent_scene(self):
        """Test that accessing nonexistent scene returns 404."""
        self.client.login(username="testuser", password="password")
        response = self.client.get("/game/scene/99999")
        self.assertEqual(response.status_code, 404)


class TestWeeklyXPRequestValidation(TestCase):
    """Test model validation for WeeklyXPRequest."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        from datetime import date

        self.week = Week.objects.create(end_date=date(2024, 1, 7))
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )

    def test_learning_requires_scene(self):
        """Test that learning XP requires a scene."""
        request = WeeklyXPRequest(
            week=self.week, character=self.char, learning=True, learning_scene=None
        )
        with self.assertRaises(ValidationError) as context:
            request.full_clean()
        self.assertIn("learning_scene", context.exception.message_dict)

    def test_rp_requires_scene(self):
        """Test that RP XP requires a scene."""
        request = WeeklyXPRequest(week=self.week, character=self.char, rp=True, rp_scene=None)
        with self.assertRaises(ValidationError) as context:
            request.full_clean()
        self.assertIn("rp_scene", context.exception.message_dict)

    def test_focus_requires_scene(self):
        """Test that focus XP requires a scene."""
        request = WeeklyXPRequest(week=self.week, character=self.char, focus=True, focus_scene=None)
        with self.assertRaises(ValidationError) as context:
            request.full_clean()
        self.assertIn("focus_scene", context.exception.message_dict)

    def test_standingout_requires_scene(self):
        """Test that standing out XP requires a scene."""
        request = WeeklyXPRequest(
            week=self.week,
            character=self.char,
            standingout=True,
            standingout_scene=None,
        )
        with self.assertRaises(ValidationError) as context:
            request.full_clean()
        self.assertIn("standingout_scene", context.exception.message_dict)

    def test_valid_request_with_scenes(self):
        """Test that valid requests pass validation."""
        request = WeeklyXPRequest(
            week=self.week,
            character=self.char,
            learning=True,
            learning_scene=self.scene,
            rp=True,
            rp_scene=self.scene,
        )
        # Should not raise
        request.full_clean()

    def test_total_xp_calculation(self):
        """Test total XP calculation."""
        request = WeeklyXPRequest(
            week=self.week,
            character=self.char,
            finishing=True,
            learning=True,
            rp=False,
            focus=True,
            standingout=False,
        )
        self.assertEqual(request.total_xp(), 3)


class TestObjectType(TestCase):
    def test_str(self):
        x = ObjectType.objects.get_or_create(name="Test", type="loc", gameline="mta")[0]
        self.assertEqual(str(x), "Mage: the Ascension/Location/Test")


class TestCharacterXP(TestCase):
    """Test character XP methods."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )

    def test_add_xp(self):
        """Test adding XP to a character."""
        initial_xp = self.char.xp
        self.char.add_xp(5)
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, initial_xp + 5)

    def test_add_negative_xp(self):
        """Test that negative XP can be added (for spending)."""
        self.char.xp = 10
        self.char.save()
        self.char.add_xp(-3)
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, 7)


class TestExtendedRoll(TestCase):
    """Test extended roll functionality."""

    def test_extended_roll_returns_html(self):
        """Test that extended roll returns formatted HTML."""
        result = extended_roll(5, 10, difficulty=6)
        self.assertIn("Extended Roll:", result)
        self.assertIn("<br>", result)
        self.assertIn("<b>", result)

    def test_extended_roll_shows_cumulative_totals(self):
        """Test that extended roll shows cumulative success totals."""
        result = extended_roll(5, 10, difficulty=6)
        self.assertIn("Total:", result)
        self.assertIn("Roll 1:", result)

    def test_extended_roll_success_message(self):
        """Test that successful extended roll shows success message."""
        # Use high dice pool and low target to ensure success
        result = extended_roll(10, 5, difficulty=4)
        self.assertIn("SUCCESS!", result)
        self.assertIn("Target of 5 reached", result)

    def test_extended_roll_max_rolls_limit(self):
        """Test that extended roll respects max_rolls limit."""
        # Use impossible target with very few max rolls
        result = extended_roll(1, 1000, difficulty=10, max_rolls=3)
        self.assertIn("INCOMPLETE:", result)
        self.assertIn("after 3 rolls", result)

    def test_extended_roll_with_specialty(self):
        """Test extended roll with specialty parameter."""
        result = extended_roll(5, 10, difficulty=6, specialty=True)
        self.assertIn("Extended Roll:", result)

    def test_extended_roll_with_high_difficulty(self):
        """Test extended roll with high difficulty."""
        result = extended_roll(5, 5, difficulty=9)
        self.assertIn("Extended Roll:", result)


class TestExtendedRollMessageProcessing(TestCase):
    """Test extended roll command parsing in message processing."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )

    def test_extended_command_basic(self):
        """Test basic /extended command parsing."""
        msg = "Researching /extended 4 target 12"
        result = message_processing(self.char, msg)
        self.assertIn("extended roll of 4 dice", result)
        self.assertIn("targeting 12 successes", result)
        self.assertIn("Extended Roll:", result)

    def test_extended_command_with_difficulty(self):
        """Test /extended command with difficulty."""
        msg = "Complex task /extended 5 target 10 difficulty 7"
        result = message_processing(self.char, msg)
        self.assertIn("difficulty 7", result)
        self.assertIn("targeting 10 successes", result)

    def test_extended_command_with_specialty(self):
        """Test /extended command with specialty."""
        msg = "Expert work /extended 6 target 15 difficulty 6 True"
        result = message_processing(self.char, msg)
        self.assertIn("with relevant specialty", result)

    def test_extended_command_default_difficulty(self):
        """Test that /extended defaults to difficulty 6."""
        msg = "Simple task /extended 4 target 8"
        result = message_processing(self.char, msg)
        self.assertIn("difficulty 6", result)

    def test_extended_command_preserves_text(self):
        """Test that text before /extended is preserved."""
        msg = "Working on a complex ritual /extended 5 target 10"
        result = message_processing(self.char, msg)
        self.assertIn("Working on a complex ritual:", result)

    def test_extended_command_invalid_format_raises_error(self):
        """Test that invalid /extended format raises ValueError."""
        msg = "Invalid /extended 5"  # Missing target
        with self.assertRaises(ValueError):
            message_processing(self.char, msg)

    def test_extended_command_case_insensitive(self):
        """Test that target keyword is case insensitive."""
        msg = "Test /extended 4 TARGET 10 DIFFICULTY 7 TRUE"
        result = message_processing(self.char, msg)
        self.assertIn("difficulty 7", result)
        self.assertIn("with relevant specialty", result)


class TestStatRollMessageProcessing(TestCase):
    """Test stat-based roll command parsing in message processing."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        # Set some stats for testing
        self.char.dexterity = 3
        self.char.firearms = 2
        self.char.strength = 4
        self.char.brawl = 3
        self.char.save()

    def test_stat_command_two_stats(self):
        """Test basic /stat command with two stats."""
        msg = "Shooting /stat Dexterity + Firearms"
        result = message_processing(self.char, msg)
        self.assertIn("Dexterity (3)", result)
        self.assertIn("Firearms (2)", result)
        self.assertIn("= 5 dice", result)
        self.assertIn("difficulty 6", result)

    def test_stat_command_three_stats(self):
        """Test /stat command with three stats."""
        msg = "Complex action /stat Strength + Brawl + 2"
        result = message_processing(self.char, msg)
        self.assertIn("Strength (4)", result)
        self.assertIn("Brawl (3)", result)
        self.assertIn("2", result)
        self.assertIn("= 9 dice", result)

    def test_stat_command_with_difficulty(self):
        """Test /stat command with custom difficulty."""
        msg = "Difficult shot /stat Dexterity + Firearms difficulty 8"
        result = message_processing(self.char, msg)
        self.assertIn("difficulty 8", result)
        self.assertIn("= 5 dice", result)

    def test_stat_command_with_specialty(self):
        """Test /stat command with specialty."""
        msg = "Expert shot /stat Dexterity + Firearms difficulty 6 True"
        result = message_processing(self.char, msg)
        self.assertIn("with relevant specialty", result)

    def test_stat_command_preserves_text(self):
        """Test that text before /stat is preserved."""
        msg = "I take aim and fire /stat Dexterity + Firearms"
        result = message_processing(self.char, msg)
        self.assertIn("I take aim and fire:", result)

    def test_stat_command_case_insensitive(self):
        """Test that stat names are case insensitive."""
        msg = "Shooting /stat dexterity + firearms"
        result = message_processing(self.char, msg)
        self.assertIn("= 5 dice", result)

    def test_stat_command_invalid_stat_raises_error(self):
        """Test that invalid stat names raise ValueError."""
        msg = "Invalid /stat InvalidStat + Firearms"
        with self.assertRaises(ValueError) as context:
            message_processing(self.char, msg)
        self.assertIn("not found", str(context.exception))

    def test_stat_command_single_stat(self):
        """Test /stat command with single stat."""
        msg = "Raw strength /stat Strength"
        result = message_processing(self.char, msg)
        self.assertIn("Strength (4)", result)
        self.assertIn("= 4 dice", result)

    def test_stat_command_default_difficulty(self):
        """Test that /stat defaults to difficulty 6."""
        msg = "Attack /stat Strength + Brawl"
        result = message_processing(self.char, msg)
        self.assertIn("difficulty 6", result)


class TestWeekListViewQueryOptimization(TestCase):
    """Test that WeekListView uses optimized queries."""

    def setUp(self):
        from datetime import date

        from django.db import connection
        from django.test import Client
        from django.test.utils import CaptureQueriesContext

        self.CaptureQueriesContext = CaptureQueriesContext
        self.connection = connection
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)

        # Create multiple weeks with scenes
        for i in range(3):
            week = Week.objects.create(end_date=date(2024, 1, 7 * (i + 1)))
            # Create a finished scene for each week
            scene = Scene.objects.create(
                name=f"Scene {i}",
                chronicle=self.chronicle,
                location=self.location,
                finished=True,
            )

    def test_list_view_query_count_is_bounded(self):
        """Test that list view query count doesn't scale with number of weeks."""
        self.client.login(username="testuser", password="password")

        with self.CaptureQueriesContext(self.connection) as context:
            response = self.client.get("/game/week/list/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # Base overhead includes session, user/profile, polymorphic lookups, etc.
        # The optimization ensures queries don't scale with number of weeks
        self.assertLessEqual(
            query_count,
            20,
            f"Too many queries ({query_count}). List view may have N+1 issue.",
        )


class TestSceneListViewQueryOptimization(TestCase):
    """Test that SceneListView uses optimized queries."""

    def setUp(self):
        from django.db import connection
        from django.test import Client
        from django.test.utils import CaptureQueriesContext

        self.CaptureQueriesContext = CaptureQueriesContext
        self.connection = connection
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)

        # Create multiple scenes with locations
        for i in range(5):
            location = LocationModel.objects.create(name=f"Location {i}", chronicle=self.chronicle)
            Scene.objects.create(
                name=f"Scene {i}",
                chronicle=self.chronicle,
                location=location,
            )

    def test_list_view_query_count_is_bounded(self):
        """Test that list view query count doesn't scale with number of scenes."""
        self.client.login(username="testuser", password="password")

        with self.CaptureQueriesContext(self.connection) as context:
            response = self.client.get("/game/scenes/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # Base overhead includes session, user/profile, etc.
        # The optimization ensures queries don't scale with number of scenes
        self.assertLessEqual(
            query_count,
            20,
            f"Too many queries ({query_count}). List view may have N+1 issue.",
        )
