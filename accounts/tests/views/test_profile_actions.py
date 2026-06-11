"""Tests for profile action views (extracted from ProfileView POST handlers)."""

from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from game.models import (
    Chronicle,
    Gameline,
    Scene,
    STRelationship,
    UserSceneReadStatus,
    Week,
    WeeklyXPRequest,
)
from items.models.core import ItemModel
from locations.models.core import LocationModel


class TestSceneXPAwardView(TestCase):
    """Test the scene XP award action view."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.char = Human.objects.create(
            name="Test Char", owner=self.user, chronicle=self.chronicle, status="App"
        )
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, finished=True
        )
        self.scene.characters.add(self.char)

    def test_st_can_award_xp(self):
        self.client.login(username="stuser", password="password")
        url = reverse("accounts:scene_xp_award", kwargs={"scene_pk": self.scene.pk})
        response = self.client.post(url, {f"scene_{self.scene.pk}-{self.char.name}": True})
        self.assertEqual(response.status_code, 302)

    def test_non_st_cannot_award_xp(self):
        self.client.login(username="player", password="password")
        url = reverse("accounts:scene_xp_award", kwargs={"scene_pk": self.scene.pk})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 403)

    def test_not_logged_in_redirects(self):
        url = reverse("accounts:scene_xp_award", kwargs={"scene_pk": self.scene.pk})
        response = self.client.post(url)
        # AuthErrorHandlerMiddleware returns 401; plain Django would redirect
        self.assertIn(response.status_code, [302, 401])
        if response.status_code == 302:
            self.assertIn("login", response.url)

    def test_nonexistent_scene_404(self):
        self.client.login(username="stuser", password="password")
        url = reverse("accounts:scene_xp_award", kwargs={"scene_pk": 99999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class TestObjectApprovalView(TestCase):
    """Test object approval for character, location, item, rote."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.char = Human.objects.create(
            name="Char", owner=self.user, chronicle=self.chronicle, status="Sub"
        )
        self.location = LocationModel.objects.create(
            name="Loc", owner=self.user, chronicle=self.chronicle, status="Sub"
        )
        self.item = ItemModel.objects.create(
            name="Item", owner=self.user, chronicle=self.chronicle, status="Sub"
        )

    def test_st_can_approve_character(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:object_approval",
            kwargs={"object_type": "character", "pk": self.char.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.status, "App")

    def test_st_can_approve_location(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:object_approval",
            kwargs={"object_type": "location", "pk": self.location.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.status, "App")

    def test_st_can_approve_item(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:object_approval",
            kwargs={"object_type": "item", "pk": self.item.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, "App")

    def test_st_can_approve_rote(self):
        from characters.models.core import Ability, Attribute
        from characters.models.mage.effect import Effect
        from characters.models.mage.rote import Rote

        effect = Effect.objects.create(name="Test Effect")
        attribute = Attribute.objects.create(name="Strength", property_name="strength")
        ability = Ability.objects.create(name="Athletics", property_name="athletics")
        rote = Rote.objects.create(
            name="Test Rote",
            chronicle=self.chronicle,
            status="Sub",
            effect=effect,
            attribute=attribute,
            ability=ability,
        )
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:object_approval", kwargs={"object_type": "rote", "pk": rote.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        rote.refresh_from_db()
        self.assertEqual(rote.status, "App")

    def test_non_st_cannot_approve(self):
        self.client.login(username="player", password="password")
        url = reverse(
            "accounts:object_approval",
            kwargs={"object_type": "character", "pk": self.char.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_invalid_object_type_404(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:object_approval", kwargs={"object_type": "bogus", "pk": 1}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_not_logged_in_redirects(self):
        url = reverse(
            "accounts:object_approval",
            kwargs={"object_type": "character", "pk": self.char.pk},
        )
        response = self.client.post(url)
        # AuthErrorHandlerMiddleware returns 401; plain Django would redirect
        self.assertIn(response.status_code, [302, 401])
        if response.status_code == 302:
            self.assertIn("login", response.url)


class TestImageApprovalView(TestCase):
    """Test image approval for character, location, item."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.char = Human.objects.create(
            name="Char",
            owner=self.user,
            chronicle=self.chronicle,
            status="App",
            image_status="sub",
        )

    def test_st_can_approve_image(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:image_approval",
            kwargs={"object_type": "character", "pk": self.char.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.image_status, "app")

    def test_non_st_cannot_approve_image(self):
        self.client.login(username="player", password="password")
        url = reverse(
            "accounts:image_approval",
            kwargs={"object_type": "character", "pk": self.char.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_not_logged_in_redirects(self):
        url = reverse(
            "accounts:image_approval",
            kwargs={"object_type": "character", "pk": self.char.pk},
        )
        response = self.client.post(url)
        # AuthErrorHandlerMiddleware returns 401; plain Django would redirect
        self.assertIn(response.status_code, [302, 401])
        if response.status_code == 302:
            self.assertIn("login", response.url)

    def test_nonexistent_object_404(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:image_approval",
            kwargs={"object_type": "character", "pk": 99999},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_invalid_type_404(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:image_approval", kwargs={"object_type": "bogus", "pk": 1}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class TestFreebieAwardView(TestCase):
    """Test freebie award action view."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.char = Human.objects.create(
            name="Char", owner=self.user, chronicle=self.chronicle, status="Sub"
        )

    def test_st_can_award_freebies(self):
        self.client.login(username="stuser", password="password")
        url = reverse("accounts:freebie_award", kwargs={"character_pk": self.char.pk})
        response = self.client.post(url, {"backstory_freebies": 5})
        self.assertEqual(response.status_code, 302)

    def test_non_st_cannot_award_freebies(self):
        self.client.login(username="player", password="password")
        url = reverse("accounts:freebie_award", kwargs={"character_pk": self.char.pk})
        response = self.client.post(url, {"backstory_freebies": 5})
        self.assertEqual(response.status_code, 403)

    def test_not_logged_in_redirects(self):
        url = reverse("accounts:freebie_award", kwargs={"character_pk": self.char.pk})
        response = self.client.post(url)
        # AuthErrorHandlerMiddleware returns 401; plain Django would redirect
        self.assertIn(response.status_code, [302, 401])
        if response.status_code == 302:
            self.assertIn("login", response.url)

    def test_nonexistent_character_404(self):
        self.client.login(username="stuser", password="password")
        url = reverse("accounts:freebie_award", kwargs={"character_pk": 99999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class TestWeeklyXPRequestView(TestCase):
    """Test weekly XP request submission."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.other_user = User.objects.create_user("other", "o@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.char = Human.objects.create(
            name="Char", owner=self.user, chronicle=self.chronicle, status="App"
        )
        self.week = Week.objects.create(end_date=date.today())

    def test_owner_can_submit_request(self):
        self.client.login(username="player", password="password")
        url = reverse(
            "accounts:weekly_xp_request",
            kwargs={"week_pk": self.week.pk, "character_pk": self.char.pk},
        )
        response = self.client.post(
            url,
            {"learning": True, "rp": False, "focus": False, "standingout": False},
        )
        self.assertEqual(response.status_code, 302)

    def test_non_owner_cannot_submit(self):
        self.client.login(username="other", password="password")
        url = reverse(
            "accounts:weekly_xp_request",
            kwargs={"week_pk": self.week.pk, "character_pk": self.char.pk},
        )
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 403)

    def test_not_logged_in_redirects(self):
        url = reverse(
            "accounts:weekly_xp_request",
            kwargs={"week_pk": self.week.pk, "character_pk": self.char.pk},
        )
        response = self.client.post(url)
        # AuthErrorHandlerMiddleware returns 401; plain Django would redirect
        self.assertIn(response.status_code, [302, 401])
        if response.status_code == 302:
            self.assertIn("login", response.url)

    def test_nonexistent_week_404(self):
        self.client.login(username="player", password="password")
        url = reverse(
            "accounts:weekly_xp_request",
            kwargs={"week_pk": 99999, "character_pk": self.char.pk},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_character_404(self):
        self.client.login(username="player", password="password")
        url = reverse(
            "accounts:weekly_xp_request",
            kwargs={"week_pk": self.week.pk, "character_pk": 99999},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class TestWeeklyXPApprovalView(TestCase):
    """Test weekly XP approval by ST."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.char = Human.objects.create(
            name="Char", owner=self.user, chronicle=self.chronicle, status="App"
        )
        self.week = Week.objects.create(end_date=date.today())
        self.xp_request = WeeklyXPRequest.objects.create(character=self.char, week=self.week)

    def test_st_can_approve(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:weekly_xp_approval",
            kwargs={"week_pk": self.week.pk, "character_pk": self.char.pk},
        )
        response = self.client.post(url, {"finishing": True})
        self.assertEqual(response.status_code, 302)

    def test_non_st_cannot_approve(self):
        self.client.login(username="player", password="password")
        url = reverse(
            "accounts:weekly_xp_approval",
            kwargs={"week_pk": self.week.pk, "character_pk": self.char.pk},
        )
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 403)

    def test_nonexistent_week_404(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:weekly_xp_approval",
            kwargs={"week_pk": 99999, "character_pk": self.char.pk},
        )
        response = self.client.post(url, {"finishing": True})
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_character_404(self):
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:weekly_xp_approval",
            kwargs={"week_pk": self.week.pk, "character_pk": 99999},
        )
        response = self.client.post(url, {"finishing": True})
        self.assertEqual(response.status_code, 404)

    def test_no_pending_request_404(self):
        """Approving a week/character pair with no submitted request is a 404."""
        other_week = Week.objects.create(end_date=date.today())
        self.client.login(username="stuser", password="password")
        url = reverse(
            "accounts:weekly_xp_approval",
            kwargs={"week_pk": other_week.pk, "character_pk": self.char.pk},
        )
        response = self.client.post(url, {"finishing": True})
        self.assertEqual(response.status_code, 404)


class TestMarkSceneReadView(TestCase):
    """Test marking a scene as read."""

    def setUp(self):
        self.user = User.objects.create_user("player", "p@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, finished=True
        )

    def test_logged_in_user_can_mark_read(self):
        self.client.login(username="player", password="password")
        url = reverse("accounts:mark_scene_read", kwargs={"scene_pk": self.scene.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            UserSceneReadStatus.objects.filter(
                scene=self.scene, user=self.user, read=True
            ).exists()
        )

    def test_not_logged_in_redirects(self):
        url = reverse("accounts:mark_scene_read", kwargs={"scene_pk": self.scene.pk})
        response = self.client.post(url)
        # AuthErrorHandlerMiddleware returns 401; plain Django would redirect
        self.assertIn(response.status_code, [302, 401])
        if response.status_code == 302:
            self.assertIn("login", response.url)

    def test_nonexistent_scene_404(self):
        self.client.login(username="player", password="password")
        url = reverse("accounts:mark_scene_read", kwargs={"scene_pk": 99999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_marking_already_read_scene_is_idempotent(self):
        self.client.login(username="player", password="password")
        url = reverse("accounts:mark_scene_read", kwargs={"scene_pk": self.scene.pk})
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            UserSceneReadStatus.objects.filter(scene=self.scene, user=self.user).count(),
            1,
        )
