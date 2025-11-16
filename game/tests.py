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
)
from locations.models.core import LocationModel


class ChronicleTest(TestCase):
    def setUp(self):
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )

    def test_add_scene(self):
        self.assertEqual(self.chronicle.total_scenes(), 0)
        self.chronicle.add_scene("Test Scene", self.location)
        self.assertEqual(self.chronicle.total_scenes(), 1)


class SceneTest(TestCase):
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
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )

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
        response = self.client.post(
            f"/game/scene/{self.scene.id}", {"close_scene": "true"}
        )
        self.assertEqual(response.status_code, 403)
        self.scene.refresh_from_db()
        self.assertFalse(self.scene.finished)

    def test_st_can_close_scene(self):
        """Test that storytellers can close scenes."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            f"/game/scene/{self.scene.id}", {"close_scene": "true"}
        )
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
        response = self.client.post(
            f"/game/scene/{self.scene.id}", {"character_to_add": char2.id}
        )
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
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )
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
        request = WeeklyXPRequest(
            week=self.week, character=self.char, rp=True, rp_scene=None
        )
        with self.assertRaises(ValidationError) as context:
            request.full_clean()
        self.assertIn("rp_scene", context.exception.message_dict)

    def test_focus_requires_scene(self):
        """Test that focus XP requires a scene."""
        request = WeeklyXPRequest(
            week=self.week, character=self.char, focus=True, focus_scene=None
        )
        with self.assertRaises(ValidationError) as context:
            request.full_clean()
        self.assertIn("focus_scene", context.exception.message_dict)

    def test_standingout_requires_scene(self):
        """Test that standing out XP requires a scene."""
        request = WeeklyXPRequest(
            week=self.week, character=self.char, standingout=True, standingout_scene=None
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
