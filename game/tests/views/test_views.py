from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from characters.models.core import CharacterModel
from characters.models.core.human import Human
from game.models import (
    Chronicle,
    FreebieSpendingRecord,
    Gameline,
    Journal,
    JournalEntry,
    ObjectType,
    Scene,
    Story,
    StoryXPRequest,
    STRelationship,
    Week,
    WeeklyXPRequest,
    XPSpendingRequest,
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
        self.scene.refresh_from_db()  # Refresh to see updated xp_given
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
        """Test that unauthenticated users get a 401 response."""
        response = self.client.get(f"/game/chronicle/{self.chronicle.id}/")
        self.assertEqual(response.status_code, 401)

    def test_chronicle_detail_view_status_code(self):
        """Test that authenticated users can access the page."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/chronicle/{self.chronicle.id}/")
        self.assertEqual(response.status_code, 200)

    def test_chronicle_detail_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/chronicle/{self.chronicle.id}/")
        self.assertTemplateUsed(response, "game/chronicle/detail.html")

    def test_non_st_cannot_create_scene(self):
        """Test that non-storytellers cannot create scenes."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            f"/game/chronicle/{self.chronicle.id}/",
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
            f"/game/chronicle/{self.chronicle.id}/",
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
        response = self.client.get("/game/chronicle/99999/")
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
        """Test that unauthenticated users get a 401 response."""
        response = self.client.get(f"/game/scene/{self.scene.id}/")
        self.assertEqual(response.status_code, 401)

    def test_scene_detail_view_status_code(self):
        """Test that authenticated users can access the page."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.id}/")
        self.assertEqual(response.status_code, 200)

    def test_scene_detail_view_template(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.id}/")
        self.assertTemplateUsed(response, "game/scene/detail.html")

    def test_non_st_cannot_close_scene(self):
        """Test that non-storytellers cannot close scenes."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(f"/game/scene/{self.scene.id}/", {"close_scene": "true"})
        self.assertEqual(response.status_code, 403)
        self.scene.refresh_from_db()
        self.assertFalse(self.scene.finished)

    def test_st_can_close_scene(self):
        """Test that storytellers can close scenes."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(f"/game/scene/{self.scene.id}/", {"close_scene": "true"})
        self.assertEqual(response.status_code, 302)
        self.scene.refresh_from_db()
        self.assertTrue(self.scene.finished)

    def test_user_can_add_own_character(self):
        """Test that users can add their own characters to scenes."""
        self.client.login(username="testuser", password="password")
        initial_count = self.scene.characters.count()
        response = self.client.post(
            f"/game/scene/{self.scene.id}/", {"character_to_add": self.char.id}
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
        response = self.client.post(f"/game/scene/{self.scene.id}/", {"character_to_add": char2.id})
        self.assertEqual(response.status_code, 403)

    def test_404_for_nonexistent_scene(self):
        """Test that accessing nonexistent scene returns 404."""
        self.client.login(username="testuser", password="password")
        response = self.client.get("/game/scene/99999/")
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
        """Test that extended roll respects max_rolls limit or ends on botch."""
        # Use impossible target with very few max rolls
        # Result can be INCOMPLETE (max rolls reached) or BOTCH (catastrophic failure)
        result = extended_roll(1, 1000, difficulty=10, max_rolls=3)
        # Either we hit max rolls (INCOMPLETE) or botched before reaching max
        self.assertTrue(
            "INCOMPLETE:" in result or "BOTCH!" in result,
            f"Expected INCOMPLETE or BOTCH in result: {result}",
        )

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


class TestXPSpendingRequestViews(TestCase):
    """Test views for XPSpendingRequest."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
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
        self.xp_request = XPSpendingRequest.objects.create(
            character=self.char,
            trait_name="Strength",
            trait_type="Attribute",
            trait_value=4,
            cost=16,
        )

    def test_list_view_requires_login(self):
        """Test that list view requires authentication."""
        response = self.client.get(reverse("game:xp_spending_request:list"))
        self.assertEqual(response.status_code, 401)

    def test_list_view_accessible_to_logged_in_user(self):
        """Test that list view is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:xp_spending_request:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/xp_spending_request/list.html")

    def test_list_view_filters_by_owner_for_non_st(self):
        """Test that non-STs only see their own requests."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:xp_spending_request:list"))
        self.assertContains(response, "Strength")

    def test_detail_view_requires_login(self):
        """Test that detail view requires authentication."""
        response = self.client.get(
            reverse("game:xp_spending_request:detail", kwargs={"pk": self.xp_request.pk})
        )
        # CharacterOwnerOrSTMixin returns 403 for anonymous users
        self.assertEqual(response.status_code, 403)

    def test_detail_view_accessible_to_owner(self):
        """Test that detail view is accessible to character owner."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:xp_spending_request:detail", kwargs={"pk": self.xp_request.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/xp_spending_request/detail.html")

    def test_detail_view_accessible_to_st(self):
        """Test that detail view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(
            reverse("game:xp_spending_request:detail", kwargs={"pk": self.xp_request.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_create_view_requires_login(self):
        """Test that create view requires authentication."""
        response = self.client.get(
            reverse("game:xp_spending_request:create", kwargs={"character_pk": self.char.pk})
        )
        # Anonymous user accessing character-specific page returns 403
        self.assertEqual(response.status_code, 403)

    def test_create_view_accessible_to_owner(self):
        """Test that create view is accessible to character owner."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:xp_spending_request:create", kwargs={"character_pk": self.char.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/xp_spending_request/form.html")

    def test_create_view_forbidden_for_non_owner(self):
        """Test that create view is forbidden for non-owners."""
        self.client.login(username="otheruser", password="password")
        response = self.client.get(
            reverse("game:xp_spending_request:create", kwargs={"character_pk": self.char.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_create_view_creates_request(self):
        """Test that create view creates a new XP spending request."""
        self.client.login(username="testuser", password="password")
        initial_count = XPSpendingRequest.objects.count()
        response = self.client.post(
            reverse("game:xp_spending_request:create", kwargs={"character_pk": self.char.pk}),
            {
                "trait_name": "Dexterity",
                "trait_type": "Attribute",
                "trait_value": 3,
                "cost": 12,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(XPSpendingRequest.objects.count(), initial_count + 1)

    def test_update_view_accessible_to_owner(self):
        """Test that update view is accessible to character owner."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:xp_spending_request:update", kwargs={"pk": self.xp_request.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/xp_spending_request/form.html")

    def test_approve_view_requires_st(self):
        """Test that approve view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("game:xp_spending_request:approve", kwargs={"pk": self.xp_request.pk}),
            {"approved": "Approved"},
        )
        self.assertEqual(response.status_code, 403)

    def test_approve_view_st_can_approve(self):
        """Test that storyteller can approve requests."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            reverse("game:xp_spending_request:approve", kwargs={"pk": self.xp_request.pk}),
            {"approved": "Approved"},
        )
        self.assertEqual(response.status_code, 302)
        self.xp_request.refresh_from_db()
        self.assertEqual(self.xp_request.approved, "Approved")


class TestFreebieSpendingRecordViews(TestCase):
    """Test views for FreebieSpendingRecord."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
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
        self.freebie_record = FreebieSpendingRecord.objects.create(
            character=self.char,
            trait_name="Strength",
            trait_type="Attribute",
            trait_value=4,
            cost=5,
        )

    def test_list_view_requires_login(self):
        """Test that list view requires authentication."""
        response = self.client.get(reverse("game:freebie_spending_record:list"))
        self.assertEqual(response.status_code, 401)

    def test_list_view_accessible_to_logged_in_user(self):
        """Test that list view is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:freebie_spending_record:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/freebie_spending_record/list.html")

    def test_detail_view_accessible_to_owner(self):
        """Test that detail view is accessible to character owner."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:freebie_spending_record:detail", kwargs={"pk": self.freebie_record.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/freebie_spending_record/detail.html")

    def test_create_view_accessible_to_owner(self):
        """Test that create view is accessible to character owner."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:freebie_spending_record:create", kwargs={"character_pk": self.char.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/freebie_spending_record/form.html")

    def test_create_view_forbidden_for_non_owner(self):
        """Test that create view is forbidden for non-owners."""
        self.client.login(username="otheruser", password="password")
        response = self.client.get(
            reverse("game:freebie_spending_record:create", kwargs={"character_pk": self.char.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_create_view_creates_record(self):
        """Test that create view creates a new freebie spending record."""
        self.client.login(username="testuser", password="password")
        initial_count = FreebieSpendingRecord.objects.count()
        response = self.client.post(
            reverse("game:freebie_spending_record:create", kwargs={"character_pk": self.char.pk}),
            {
                "trait_name": "Dexterity",
                "trait_type": "Attribute",
                "trait_value": 3,
                "cost": 5,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FreebieSpendingRecord.objects.count(), initial_count + 1)


class TestStoryXPRequestViews(TestCase):
    """Test views for StoryXPRequest."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
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
        self.story = Story.objects.create(name="Test Story")
        self.story_xp_request = StoryXPRequest.objects.create(
            character=self.char,
            story=self.story,
            success=True,
            danger=False,
            growth=True,
            drama=False,
            duration=2,
        )

    def test_list_view_accessible_to_logged_in_user(self):
        """Test that list view is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:story_xp_request:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/story_xp_request/list.html")

    def test_detail_view_accessible_to_owner(self):
        """Test that detail view is accessible to character owner."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:story_xp_request:detail", kwargs={"pk": self.story_xp_request.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/story_xp_request/detail.html")

    def test_create_view_requires_st(self):
        """Test that create view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:story_xp_request:create", kwargs={"character_pk": self.char.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_create_view_accessible_to_st(self):
        """Test that create view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(
            reverse("game:story_xp_request:create", kwargs={"character_pk": self.char.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/story_xp_request/form.html")

    def test_update_view_requires_st(self):
        """Test that update view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:story_xp_request:update", kwargs={"pk": self.story_xp_request.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_view_accessible_to_st(self):
        """Test that update view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(
            reverse("game:story_xp_request:update", kwargs={"pk": self.story_xp_request.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/story_xp_request/form.html")


class TestChronicleCreateUpdateViews(TestCase):
    """Test views for Chronicle create/update."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_create_view_requires_st(self):
        """Test that create view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:chronicle_manage:create"))
        self.assertEqual(response.status_code, 403)

    def test_create_view_accessible_to_st(self):
        """Test that create view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(reverse("game:chronicle_manage:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/chronicle/form.html")

    def test_create_view_creates_chronicle(self):
        """Test that create view creates a new chronicle."""
        self.client.login(username="stuser", password="password")
        initial_count = Chronicle.objects.count()
        response = self.client.post(
            reverse("game:chronicle_manage:create"),
            {
                "name": "New Chronicle",
                "year": 2024,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Chronicle.objects.count(), initial_count + 1)

    def test_update_view_requires_st(self):
        """Test that update view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:chronicle_manage:update", kwargs={"pk": self.chronicle.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_view_accessible_to_st(self):
        """Test that update view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(
            reverse("game:chronicle_manage:update", kwargs={"pk": self.chronicle.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/chronicle/form.html")


class TestSceneCreateUpdateViews(TestCase):
    """Test views for Scene create/update."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
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

    def test_create_view_requires_st(self):
        """Test that create view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:scene_manage:create"))
        self.assertEqual(response.status_code, 403)

    def test_create_view_accessible_to_st(self):
        """Test that create view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(reverse("game:scene_manage:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/scene/form.html")

    def test_create_for_chronicle_accessible_to_st(self):
        """Test that create for chronicle view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(
            reverse(
                "game:scene_manage:create_for_chronicle", kwargs={"chronicle_pk": self.chronicle.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/scene/form.html")

    def test_update_view_requires_st(self):
        """Test that update view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:scene_manage:update", kwargs={"pk": self.scene.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_view_accessible_to_st(self):
        """Test that update view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(
            reverse("game:scene_manage:update", kwargs={"pk": self.scene.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/scene/form.html")

    def test_update_view_updates_scene(self):
        """Test that update view updates a scene."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            reverse("game:scene_manage:update", kwargs={"pk": self.scene.pk}),
            {
                "name": "Updated Scene Name",
                "location": self.location.pk,
                "date_of_scene": "2024-01-15",
                "gameline": "wod",
                "finished": False,
                "xp_given": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.scene.refresh_from_db()
        self.assertEqual(self.scene.name, "Updated Scene Name")


class TestCommandsView(TestCase):
    """Test the CommandsView."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")

    def test_commands_view_requires_login(self):
        """Test that commands view requires authentication."""
        response = self.client.get("/game/commands/")
        self.assertEqual(response.status_code, 401)

    def test_commands_view_accessible(self):
        """Test that commands view is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get("/game/commands/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/scene/commands.html")


class TestJournalListView(TestCase):
    """Test the JournalListView."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        # Create characters with journals
        self.char1 = Human.objects.create(
            name="My Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.char2 = Human.objects.create(
            name="Other Character",
            owner=self.other_user,
            chronicle=self.chronicle,
        )

    def test_list_view_requires_login(self):
        """Test that journal list requires authentication."""
        response = self.client.get(reverse("game:journals"))
        self.assertEqual(response.status_code, 401)

    def test_list_view_accessible(self):
        """Test that journal list is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:journals"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/journal/list.html")

    def test_filter_by_mine(self):
        """Test filtering journals by own characters."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:journals") + "?filter=mine")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["current_filter"], "mine")

    def test_filter_by_st(self):
        """Test filtering journals by ST chronicles."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(reverse("game:journals") + "?filter=st")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["current_filter"], "st")

    def test_journal_list_has_entry_count_annotation(self):
        """Test that journals are annotated with entry_count."""
        from django.utils import timezone

        self.client.login(username="testuser", password="password")
        # Get the journal created by signal
        journal1, _ = Journal.objects.get_or_create(character=self.char1)
        # Add entries
        JournalEntry.objects.create(journal=journal1, message="Entry 1", date=timezone.now())
        JournalEntry.objects.create(journal=journal1, message="Entry 2", date=timezone.now())
        response = self.client.get(reverse("game:journals"))
        # Check that journals in object_list have entry_count annotation
        for journal in response.context["object_list"]:
            if journal.pk == journal1.pk:
                self.assertEqual(journal.entry_count, 2)

    def test_journal_list_has_latest_entry_annotation(self):
        """Test that journals are annotated with latest_entry date."""
        from django.utils import timezone

        self.client.login(username="testuser", password="password")
        journal1, _ = Journal.objects.get_or_create(character=self.char1)
        # Add entries with different dates
        earlier = timezone.now() - timezone.timedelta(days=5)
        later = timezone.now()
        JournalEntry.objects.create(journal=journal1, message="Earlier", date=earlier)
        JournalEntry.objects.create(journal=journal1, message="Later", date=later)
        response = self.client.get(reverse("game:journals"))
        for journal in response.context["object_list"]:
            if journal.pk == journal1.pk:
                # latest_entry should be the most recent date
                self.assertIsNotNone(journal.latest_entry)
                # Should be close to 'later' date (within a second)
                self.assertAlmostEqual(
                    journal.latest_entry.timestamp(),
                    later.timestamp(),
                    delta=1,
                )

    def test_journal_list_optimized_queries(self):
        """Test that journal list view uses optimized queries (not N+1)."""
        from django.db import connection
        from django.test.utils import CaptureQueriesContext
        from django.utils import timezone

        self.client.login(username="testuser", password="password")
        # Create multiple journals with entries
        for i in range(5):
            char = Human.objects.create(
                name=f"Char {i}",
                owner=self.user,
                chronicle=self.chronicle,
            )
            journal, _ = Journal.objects.get_or_create(character=char)
            for j in range(3):
                JournalEntry.objects.create(
                    journal=journal,
                    message=f"Entry {j}",
                    date=timezone.now(),
                )
        # Now fetch the page and count queries
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse("game:journals"))
        self.assertEqual(response.status_code, 200)
        # With 7 journals (2 from setUp + 5 new), N+1 would cause many more queries
        # Current optimized implementation uses around 13 queries for session,
        # user/profile, journals, annotations, and permission checks
        self.assertLess(
            len(context.captured_queries),
            20,
            f"Too many queries ({len(context.captured_queries)}): "
            f"{[q['sql'][:100] for q in context.captured_queries]}",
        )


class TestJournalDetailView(TestCase):
    """Test the JournalDetailView."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        from game.models import Journal

        self.journal, _ = Journal.objects.get_or_create(character=self.char)

    def test_owner_can_add_entry(self):
        """Test that character owner can add journal entries."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("game:journal", kwargs={"pk": self.journal.pk}),
            {
                "submit_entry": "true",
                "date": "2024-01-15",
                "message": "Test journal entry",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_add_entry(self):
        """Test that non-owners cannot add entries.

        ViewPermissionMixin returns 404 (not 403) to hide object existence from unauthorized users.
        """
        other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.client.login(username="otheruser", password="password")
        response = self.client.post(
            reverse("game:journal", kwargs={"pk": self.journal.pk}),
            {
                "submit_entry": "true",
                "date": "2024-01-15",
                "message": "Malicious entry",
            },
        )
        self.assertEqual(response.status_code, 404)


class TestSettingElementViews(TestCase):
    """Test views for SettingElement."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        from game.models import SettingElement

        self.element = SettingElement.objects.create(
            name="The Camarilla",
            description="A sect of vampires",
            gameline="vtm",
        )
        self.chronicle.common_knowledge_elements.add(self.element)

    def test_list_view_requires_login(self):
        """Test that list view requires authentication."""
        response = self.client.get(reverse("game:setting_element:list"))
        self.assertEqual(response.status_code, 401)

    def test_list_view_accessible(self):
        """Test that list view is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:setting_element:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/setting_element/list.html")
        self.assertContains(response, "The Camarilla")

    def test_detail_view_accessible(self):
        """Test that detail view is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:setting_element:detail", kwargs={"pk": self.element.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/setting_element/detail.html")
        self.assertContains(response, "The Camarilla")

    def test_create_view_requires_st(self):
        """Test that create view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:setting_element:create"))
        self.assertEqual(response.status_code, 403)

    def test_create_view_accessible_to_st(self):
        """Test that create view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(reverse("game:setting_element:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/setting_element/form.html")

    def test_create_view_creates_element(self):
        """Test that create view creates a new element."""
        from game.models import SettingElement

        self.client.login(username="stuser", password="password")
        initial_count = SettingElement.objects.count()
        response = self.client.post(
            reverse("game:setting_element:create"),
            {
                "name": "The Sabbat",
                "description": "Another sect of vampires",
                "gameline": "vtm",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SettingElement.objects.count(), initial_count + 1)

    def test_update_view_requires_st(self):
        """Test that update view requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("game:setting_element:update", kwargs={"pk": self.element.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_view_accessible_to_st(self):
        """Test that update view is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(
            reverse("game:setting_element:update", kwargs={"pk": self.element.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/setting_element/form.html")


class TestWeeklyXPRequestBatchApproveView(TestCase):
    """Test the WeeklyXPRequestBatchApproveView."""

    def setUp(self):
        from datetime import date

        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.week = Week.objects.create(end_date=date(2024, 1, 14))
        self.xp_request = WeeklyXPRequest.objects.create(
            week=self.week,
            character=self.char,
            finishing=True,
            learning_scene=self.scene,
            rp_scene=self.scene,
            focus_scene=self.scene,
            standingout_scene=self.scene,
        )

    def test_batch_approve_requires_st(self):
        """Test that batch approve requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("game:weekly_xp_request:batch_approve"),
            {"request_ids": [self.xp_request.pk]},
        )
        self.assertEqual(response.status_code, 403)

    def test_batch_approve_with_no_requests(self):
        """Test batch approve with no request IDs."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            reverse("game:weekly_xp_request:batch_approve"),
            {"request_ids": []},
        )
        self.assertEqual(response.status_code, 302)

    def test_batch_approve_approves_requests(self):
        """Test that batch approve approves multiple requests."""
        self.client.login(username="stuser", password="password")
        initial_xp = self.char.xp
        response = self.client.post(
            reverse("game:weekly_xp_request:batch_approve"),
            {"request_ids": [self.xp_request.pk]},
        )
        self.assertEqual(response.status_code, 302)
        self.xp_request.refresh_from_db()
        self.char.refresh_from_db()
        self.assertTrue(self.xp_request.approved)
        self.assertEqual(self.char.xp, initial_xp + 1)


class TestChronicleDetailViewPost(TestCase):
    """Test ChronicleDetailView POST actions."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        # Create object types for character/location/item creation
        ObjectType.objects.create(name="human", type="char", gameline="wod")

    def test_non_st_cannot_create_story(self):
        """Test that non-storytellers cannot create stories."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            f"/game/chronicle/{self.chronicle.pk}/",
            {"create_story": "true", "name": "New Story"},
        )
        self.assertEqual(response.status_code, 403)

    def test_st_can_create_story(self):
        """Test that storytellers can create stories."""
        from game.models import Story

        self.client.login(username="stuser", password="password")
        initial_count = Story.objects.count()
        response = self.client.post(
            f"/game/chronicle/{self.chronicle.pk}/",
            {"create_story": "true", "name": "Epic Quest"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Story.objects.count(), initial_count + 1)


class TestWeekViews(TestCase):
    """Test Week-related views."""

    def setUp(self):
        from datetime import date

        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.week = Week.objects.create(end_date=date(2024, 1, 14))

    def test_week_list_view_requires_login(self):
        """Test that week list requires authentication."""
        response = self.client.get("/game/week/list/")
        self.assertEqual(response.status_code, 401)

    def test_week_list_view_accessible(self):
        """Test that week list is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get("/game/week/list/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/week/list.html")

    def test_week_list_view_context(self):
        """Test that week list includes is_st context."""
        self.client.login(username="stuser", password="password")
        response = self.client.get("/game/week/list/")
        self.assertTrue(response.context["is_st"])

    def test_week_detail_view_accessible(self):
        """Test that week detail is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/week/{self.week.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/week/detail.html")

    def test_week_create_requires_st(self):
        """Test that week creation requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:week:create"))
        self.assertEqual(response.status_code, 403)

    def test_week_create_accessible_to_st(self):
        """Test that week creation is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(reverse("game:week:create"))
        self.assertEqual(response.status_code, 200)

    def test_week_update_requires_st(self):
        """Test that week update requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:week:update", kwargs={"pk": self.week.pk}))
        self.assertEqual(response.status_code, 403)


class TestStoryViews(TestCase):
    """Test Story-related views."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        from game.models import Story

        self.story = Story.objects.create(name="Test Story")

    def test_story_list_view_requires_login(self):
        """Test that story list requires authentication."""
        response = self.client.get(reverse("game:story:list"))
        self.assertEqual(response.status_code, 401)

    def test_story_list_view_accessible(self):
        """Test that story list is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:story:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/story/list.html")
        self.assertContains(response, "Test Story")

    def test_story_detail_view_accessible(self):
        """Test that story detail is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:story:detail", kwargs={"pk": self.story.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/story/detail.html")

    def test_story_create_requires_st(self):
        """Test that story creation requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:story:create"))
        self.assertEqual(response.status_code, 403)

    def test_story_create_accessible_to_st(self):
        """Test that story creation is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(reverse("game:story:create"))
        self.assertEqual(response.status_code, 200)

    def test_story_update_requires_st(self):
        """Test that story update requires storyteller permissions."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:story:update", kwargs={"pk": self.story.pk}))
        self.assertEqual(response.status_code, 403)

    def test_story_update_accessible_to_st(self):
        """Test that story update is accessible to storytellers."""
        self.client.login(username="stuser", password="password")
        response = self.client.get(reverse("game:story:update", kwargs={"pk": self.story.pk}))
        self.assertEqual(response.status_code, 200)


class TestSceneDetailViewPost(TestCase):
    """Test SceneDetailView POST actions."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
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
        )
        self.scene.characters.add(self.char)

    def test_post_with_invalid_form_shows_error(self):
        """Test that posting with invalid form shows error message."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            f"/game/scene/{self.scene.pk}/",
            {
                "character": self.char.pk,
                "display_name": "",
                "message": "",  # Empty message is invalid
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_post_straightens_quotes(self):
        """Test that curly quotes are straightened in posts."""
        from game.views import SceneDetailView

        # Test the static method directly
        input_text = "\u201cHello\u201d \u2018World\u2019"
        result = SceneDetailView.straighten_quotes(input_text)
        self.assertEqual(result, "\"Hello\" 'World'")


class TestChronicleDetailViewQueryOptimization(TestCase):
    """Test that ChronicleDetailView uses optimized queries for characters."""

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

        # Create multiple characters with different owners to trigger N+1 if not optimized
        for i in range(5):
            owner = User.objects.create_user(
                username=f"owner{i}", email=f"owner{i}@test.com", password="password"
            )
            Human.objects.create(
                name=f"Character {i}",
                owner=owner,
                chronicle=self.chronicle,
                concept="Test",
                status="App",
            )

    def test_chronicle_detail_query_count_is_bounded(self):
        """Test that chronicle detail query count doesn't scale with number of characters.

        Without select_related, accessing character.owner.username and
        character.owner.profile for each character causes N+1 queries.
        With optimization, query count should be bounded regardless of character count.
        """
        self.client.login(username="testuser", password="password")

        with self.CaptureQueriesContext(self.connection) as context:
            response = self.client.get(f"/game/chronicle/{self.chronicle.pk}/")

        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        # Base overhead includes session, user/profile, polymorphic lookups, etc.
        # The current implementation includes prefetches for characters, locations,
        # items, scenes, stories, and other chronicle-related data.
        self.assertLessEqual(
            query_count,
            150,
            f"Too many queries ({query_count}). Chronicle detail view may have N+1 issue for characters.",
        )


class TestChronicleListView(TestCase):
    """Test ChronicleListView."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        Chronicle.objects.create(name="Chronicle A")
        Chronicle.objects.create(name="Chronicle B")

    def test_list_view_requires_login(self):
        """Test that list view requires authentication."""
        response = self.client.get(reverse("game:chronicles"))
        self.assertEqual(response.status_code, 401)

    def test_list_view_accessible(self):
        """Test that list view is accessible to logged-in users."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("game:chronicles"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "game/chronicle/list.html")
        self.assertContains(response, "Chronicle A")
        self.assertContains(response, "Chronicle B")
