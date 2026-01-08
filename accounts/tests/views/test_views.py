"""Tests for accounts views."""

from datetime import date

from characters.models.core import Human
from characters.models.core.human import Human
from characters.models.mage.rote import Rote
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
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


class TestSignUpView(TestCase):
    """Class that Tests SignUpView"""

    def test_correct_template(self):
        self.client.get("/accounts/")
        self.assertTemplateUsed("registration/login.html")


class TestProfileView(TestCase):
    """Class that Tests the ProfileView"""

    def setUp(self) -> None:
        self.user1 = User.objects.create_user("Test User 1", "test@user1.com", "testpass")
        self.user2 = User.objects.create_user("Test User 2", "test@user2.com", "testpass")
        self.storyteller = User.objects.create_user("Test Storyteller", "test@st.com", "testpass")

        mta = Gameline.objects.create(name="Mage: the Ascension")

        chronicle = Chronicle.objects.create(name="Test Chronicle")

        STRelationship.objects.create(user=self.storyteller, gameline=mta, chronicle=chronicle)

        self.char1 = Human.objects.create(name="Test Character 1", owner=self.user1)
        self.char2 = Human.objects.create(
            name="Test Character 2", owner=self.user2, chronicle=chronicle, status="Sub"
        )
        self.char3 = Human.objects.create(name="Test Character 3", owner=self.user1)
        self.char4 = Human.objects.create(name="Test Character 4", owner=self.user2)
        self.char5 = Human.objects.create(name="Test Character 5", owner=self.user1)
        self.char6 = Human.objects.create(name="Test Character 6", owner=self.user2)

    def test_template_logged_in(self):
        self.client.login(username="Test User 1", password="testpass")
        response = self.client.get(self.user1.profile.get_absolute_url())
        self.assertTemplateUsed(response, "accounts/detail.html")

    def test_template_logged_out(self):
        response = self.client.get("/accounts/", follow=True)
        self.assertTemplateUsed(response, "core/index.html")

    def test_character_list(self):
        self.client.login(username="Test User 1", password="testpass")
        response = self.client.get(self.user1.profile.get_absolute_url())
        self.assertTemplateUsed(response, "accounts/detail.html")

        self.assertContains(response, "Test Character 1")
        self.assertNotContains(response, "Test Character 2")
        self.assertContains(response, f"/characters/{self.char1.id}/")

        self.assertContains(response, "Test Character 3")
        self.assertNotContains(response, "Test Character 4")
        self.assertContains(response, f"/characters/{self.char3.id}/")

        self.assertContains(response, "Test Character 5")
        self.assertNotContains(response, "Test Character 6")
        self.assertContains(response, f"/characters/{self.char5.id}/")

    def test_approval_list(self):
        self.client.login(username="Test Storyteller", password="testpass")
        response = self.client.get(self.storyteller.profile.get_absolute_url())
        self.assertContains(response, "Test Character 2")
        self.assertContains(response, "To Approve")


class TestProfileApprovalWorkflow(TestCase):
    """Test the approval workflow in the profile view."""

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
            status="Sub",
        )
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle, status="Sub"
        )
        self.item = ItemModel.objects.create(
            name="Test Item", chronicle=self.chronicle, status="Sub"
        )

    def test_non_st_cannot_approve_character(self):
        """Test that non-storytellers cannot approve characters."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {"approve_character": self.char.id},
        )
        self.assertEqual(response.status_code, 403)
        self.char.refresh_from_db()
        self.assertEqual(self.char.status, "Sub")

    def test_st_can_approve_character(self):
        """Test that storytellers can approve characters."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {"approve_character": self.char.id},
        )
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.status, "App")

    def test_st_can_approve_location(self):
        """Test that storytellers can approve locations."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {"approve_location": self.location.id},
        )
        self.assertEqual(response.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.status, "App")

    def test_st_can_approve_item(self):
        """Test that storytellers can approve items."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {"approve_item": self.item.id},
        )
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, "App")

    def test_non_st_cannot_approve_location(self):
        """Test that non-storytellers cannot approve locations."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {"approve_location": self.location.id},
        )
        self.assertEqual(response.status_code, 403)

    def test_non_st_cannot_approve_item(self):
        """Test that non-storytellers cannot approve items."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {"approve_item": self.item.id},
        )
        self.assertEqual(response.status_code, 403)


class TestSignUpViewIntegration(TestCase):
    """Test the signup view integration."""

    def test_signup_creates_user_and_profile(self):
        """Test that signing up creates both user and profile."""
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "email": "new@test.com",
                "password1": "testpass123!",
                "password2": "testpass123!",
            },
        )
        self.assertEqual(User.objects.filter(username="newuser").count(), 1)
        user = User.objects.get(username="newuser")
        self.assertTrue(hasattr(user, "profile"))

    def test_signup_redirects_on_success(self):
        """Test that successful signup redirects."""
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "email": "new@test.com",
                "password1": "testpass123!",
                "password2": "testpass123!",
            },
        )
        self.assertEqual(response.status_code, 302)


class TestProfileUpdateView(TestCase):
    """Test the profile update view."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")

    def test_requires_login(self):
        """Test that profile update requires authentication."""
        response = self.client.get(
            reverse("accounts:profile_update", kwargs={"pk": self.user.profile.pk})
        )
        self.assertEqual(response.status_code, 401)

    def test_can_update_profile(self):
        """Test that user can update their profile."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("accounts:profile_update", kwargs={"pk": self.user.profile.pk}),
            {
                "preferred_heading": "mta_heading",
                "theme": "dark",
                "highlight_text": True,
                "discord_id": "user#1234",
                "lines": "",
                "veils": "",
                "discord_toggle": False,
                "lines_toggle": False,
                "veils_toggle": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.theme, "dark")
        self.assertEqual(self.user.profile.preferred_heading, "mta_heading")


class TestProfileSceneXPWorkflow(TestCase):
    """Test scene XP awarding workflow in the profile view."""

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
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
            xp_given=False,
        )
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        self.scene.characters.add(self.char)

    def test_st_can_award_scene_xp(self):
        """Test that storytellers can award scene XP."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {
                "submit_scene": self.scene.id,
                f"scene_{self.scene.pk}-{self.char.name}": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.scene.refresh_from_db()
        self.assertEqual(self.char.xp, 1)
        self.assertTrue(self.scene.xp_given)

    def test_non_st_cannot_award_scene_xp(self):
        """Test that non-storytellers cannot award scene XP."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {
                "submit_scene": self.scene.id,
                f"scene_{self.scene.pk}-{self.char.name}": "on",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.char.refresh_from_db()
        self.assertEqual(self.char.xp, 0)


class TestProfileRoteApprovalWorkflow(TestCase):
    """Test rote approval workflow in the profile view."""

    def setUp(self):
        from characters.models.core import Ability, Attribute
        from characters.models.mage.effect import Effect

        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage: the Ascension")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        # Create required related objects for Rote
        effect = Effect.objects.create(name="Test Effect")
        attribute = Attribute.objects.create(name="Strength", property_name="strength")
        ability = Ability.objects.create(name="Athletics", property_name="athletics")
        self.rote = Rote.objects.create(
            name="Test Rote",
            chronicle=self.chronicle,
            status="Sub",
            effect=effect,
            attribute=attribute,
            ability=ability,
        )

    def test_st_can_approve_rote(self):
        """Test that storytellers can approve rotes."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {"approve_rote": self.rote.id},
        )
        self.assertEqual(response.status_code, 302)
        self.rote.refresh_from_db()
        self.assertEqual(self.rote.status, "App")

    def test_non_st_cannot_approve_rote(self):
        """Test that non-storytellers cannot approve rotes."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {"approve_rote": self.rote.id},
        )
        self.assertEqual(response.status_code, 403)
        self.rote.refresh_from_db()
        self.assertEqual(self.rote.status, "Sub")


class TestProfileImageApprovalWorkflow(TestCase):
    """Test image approval workflow in the profile view."""

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
            image_status="sub",
        )
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
            image_status="sub",
        )
        self.item = ItemModel.objects.create(
            name="Test Item",
            chronicle=self.chronicle,
            image_status="sub",
        )

    def test_st_can_approve_character_image(self):
        """Test that storytellers can approve character images."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {"approve_character_image": f"image-{self.char.id}"},
        )
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.image_status, "app")

    def test_st_can_approve_location_image(self):
        """Test that storytellers can approve location images."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {"approve_location_image": f"image-{self.location.id}"},
        )
        self.assertEqual(response.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.image_status, "app")

    def test_st_can_approve_item_image(self):
        """Test that storytellers can approve item images."""
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {"approve_item_image": f"image-{self.item.id}"},
        )
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.image_status, "app")

    def test_non_st_cannot_approve_character_image(self):
        """Test that non-storytellers cannot approve character images."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {"approve_character_image": f"image-{self.char.id}"},
        )
        self.assertEqual(response.status_code, 403)
        self.char.refresh_from_db()
        self.assertEqual(self.char.image_status, "sub")


class TestProfileFreebieWorkflow(TestCase):
    """Test freebie award workflow in the profile view."""

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
            status="Sub",
            freebies_approved=False,
        )

    def test_st_can_award_freebies(self):
        """Test that storytellers can award freebies."""
        initial_freebies = self.char.freebies
        self.client.login(username="stuser", password="password")
        response = self.client.post(
            self.st_user.profile.get_absolute_url(),
            {
                "submit_freebies": self.char.id,
                "backstory_freebies": 5,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.char.refresh_from_db()
        self.assertEqual(self.char.freebies, initial_freebies + 5)
        self.assertTrue(self.char.freebies_approved)

    def test_non_st_cannot_award_freebies(self):
        """Test that non-storytellers cannot award freebies."""
        self.client.login(username="testuser", password="password")
        initial_freebies = self.char.freebies
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {
                "submit_freebies": self.char.id,
                "backstory_freebies": 5,
            },
        )
        self.assertEqual(response.status_code, 403)
        self.char.refresh_from_db()
        self.assertEqual(self.char.freebies, initial_freebies)


class TestProfileWeeklyXPWorkflow(TestCase):
    """Test weekly XP request workflow in the profile view.

    Note: These tests focus on permission checks. Full form submission tests
    require more complex setup (finished scenes within the week's date range).
    """

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.char = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        self.other_char = Human.objects.create(
            name="Other Character",
            owner=self.other_user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        self.week = Week.objects.create(end_date=date.today())
        self.week.characters.add(self.char)
        self.week.characters.add(self.other_char)

    def test_player_cannot_submit_for_other_players_character(self):
        """Test that players cannot submit requests for others' characters."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {
                "submit_weekly_request": f"week-{self.week.pk}-char-{self.other_char.pk}",
            },
        )
        self.assertEqual(response.status_code, 403)


class TestProfileWeeklyXPApprovalWorkflow(TestCase):
    """Test weekly XP approval workflow in the profile view."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
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
        self.week.characters.add(self.char)
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        self.scene.characters.add(self.char)
        # Create a pending XP request
        self.xp_request = WeeklyXPRequest.objects.create(
            character=self.char,
            week=self.week,
            rp_scene=self.scene,
            learning_scene=self.scene,
            standingout_scene=self.scene,
            focus_scene=self.scene,
            approved=False,
        )

    def test_non_st_cannot_approve_weekly_xp(self):
        """Test that non-storytellers cannot approve weekly XP requests."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {
                "submit_weekly_approval": f"week-{self.week.pk}-char-{self.char.pk}",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.xp_request.refresh_from_db()
        self.assertFalse(self.xp_request.approved)


class TestProfileSceneReadWorkflow(TestCase):
    """Test marking scenes as read in the profile view."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )

    def test_user_can_mark_scene_as_read(self):
        """Test that users can mark scenes as read."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {"mark_scene_read": self.scene.id},
        )
        self.assertEqual(response.status_code, 302)
        status = UserSceneReadStatus.objects.get(scene=self.scene, user=self.user)
        self.assertTrue(status.read)


class TestProfileEditPreferencesRedirect(TestCase):
    """Test the edit preferences redirect in the profile view."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")

    def test_edit_preferences_redirects_to_update_view(self):
        """Test that clicking Edit Preferences redirects to profile update."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            self.user.profile.get_absolute_url(),
            {"Edit Preferences": "Edit Preferences"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse("accounts:profile_update", kwargs={"pk": self.user.profile.pk})
        )


class TestProfileViewIDORProtection(TestCase):
    """Test IDOR (Insecure Direct Object Reference) protection for ProfileView.

    Ensures users can only view their own profiles unless they are staff.
    Addresses security issue #1342.
    """

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.staff_user = User.objects.create_user("staffuser", "staff@test.com", "password")
        self.staff_user.is_staff = True
        self.staff_user.save()

    def test_user_can_view_own_profile(self):
        """Test that users can view their own profile."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("accounts:profile", kwargs={"pk": self.user.profile.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_view_other_profile(self):
        """Test that users cannot view another user's profile."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("accounts:profile", kwargs={"pk": self.other_user.profile.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_staff_can_view_any_profile(self):
        """Test that staff users can view any profile."""
        self.client.login(username="staffuser", password="password")
        response = self.client.get(
            reverse("accounts:profile", kwargs={"pk": self.other_user.profile.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_cannot_view_profile(self):
        """Test that unauthenticated users cannot view profiles."""
        response = self.client.get(reverse("accounts:profile", kwargs={"pk": self.user.profile.pk}))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)


class TestProfileUpdateViewIDORProtection(TestCase):
    """Test IDOR (Insecure Direct Object Reference) protection for ProfileUpdateView.

    Ensures users can only update their own profiles unless they are staff.
    Addresses security issue #1343.
    """

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.staff_user = User.objects.create_user("staffuser", "staff@test.com", "password")
        self.staff_user.is_staff = True
        self.staff_user.save()

    def test_user_can_access_own_profile_update(self):
        """Test that users can access the update view for their own profile."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("accounts:profile_update", kwargs={"pk": self.user.profile.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_access_other_profile_update(self):
        """Test that users cannot access the update view for another user's profile."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("accounts:profile_update", kwargs={"pk": self.other_user.profile.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_post_to_other_profile_update(self):
        """Test that users cannot POST updates to another user's profile."""
        self.client.login(username="testuser", password="password")
        original_theme = self.other_user.profile.theme
        response = self.client.post(
            reverse("accounts:profile_update", kwargs={"pk": self.other_user.profile.pk}),
            {
                "preferred_heading": "mta_heading",
                "theme": "dark",
                "highlight_text": True,
                "discord_id": "hacked#1234",
                "lines": "",
                "veils": "",
                "discord_toggle": False,
                "lines_toggle": False,
                "veils_toggle": False,
            },
        )
        self.assertEqual(response.status_code, 403)
        self.other_user.profile.refresh_from_db()
        # Ensure the profile was not modified
        self.assertEqual(self.other_user.profile.theme, original_theme)
        self.assertNotEqual(self.other_user.profile.discord_id, "hacked#1234")

    def test_staff_can_update_any_profile(self):
        """Test that staff users can update any profile."""
        self.client.login(username="staffuser", password="password")
        response = self.client.post(
            reverse("accounts:profile_update", kwargs={"pk": self.other_user.profile.pk}),
            {
                "preferred_heading": "mta_heading",
                "theme": "dark",
                "highlight_text": True,
                "discord_id": "staff_update#1234",
                "lines": "",
                "veils": "",
                "discord_toggle": False,
                "lines_toggle": False,
                "veils_toggle": False,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.other_user.profile.refresh_from_db()
        self.assertEqual(self.other_user.profile.discord_id, "staff_update#1234")


class TestCrossChroniclePermissionSecurity(TestCase):
    """Security tests for cross-chronicle ST permission checks.

    These tests verify that an ST for Chronicle A cannot perform approval
    actions on objects in Chronicle B where they don't have ST privileges.
    This addresses the security vulnerability where ST permission checks
    were not scoped to specific chronicles.
    """

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user_a = User.objects.create_user("st_a", "sta@test.com", "password")
        self.st_user_b = User.objects.create_user("st_b", "stb@test.com", "password")

        # Create two chronicles
        self.chronicle_a = Chronicle.objects.create(name="Chronicle A")
        self.chronicle_b = Chronicle.objects.create(name="Chronicle B")

        # Create gamelines
        self.gameline = Gameline.objects.create(name="Test Gameline")

        # ST A is only an ST for Chronicle A
        STRelationship.objects.create(
            user=self.st_user_a, chronicle=self.chronicle_a, gameline=self.gameline
        )
        # ST B is only an ST for Chronicle B
        STRelationship.objects.create(
            user=self.st_user_b, chronicle=self.chronicle_b, gameline=self.gameline
        )

        # Create objects in Chronicle B (ST A should NOT be able to approve these)
        self.char_b = Human.objects.create(
            name="Character in Chronicle B",
            owner=self.user,
            chronicle=self.chronicle_b,
            status="Sub",
        )
        self.location_b = LocationModel.objects.create(
            name="Location in Chronicle B",
            chronicle=self.chronicle_b,
            status="Sub",
        )
        self.item_b = ItemModel.objects.create(
            name="Item in Chronicle B",
            chronicle=self.chronicle_b,
            status="Sub",
        )
        self.location_for_scene = LocationModel.objects.create(
            name="Scene Location", chronicle=self.chronicle_b
        )
        self.scene_b = Scene.objects.create(
            name="Scene in Chronicle B",
            chronicle=self.chronicle_b,
            location=self.location_for_scene,
            xp_given=False,
        )
        self.scene_b.characters.add(self.char_b)

        # Create character with pending freebies in Chronicle B
        self.char_freebies_b = Human.objects.create(
            name="Freebie Character in Chronicle B",
            owner=self.user,
            chronicle=self.chronicle_b,
            status="Sub",
            freebies_approved=False,
        )

        # Create weekly XP request in Chronicle B
        self.week = Week.objects.create(end_date=date.today())
        self.week.characters.add(self.char_b)
        self.xp_request_b = WeeklyXPRequest.objects.create(
            character=self.char_b,
            week=self.week,
            rp_scene=self.scene_b,
            learning_scene=self.scene_b,
            standingout_scene=self.scene_b,
            focus_scene=self.scene_b,
            approved=False,
        )

    def test_st_cannot_approve_character_in_other_chronicle(self):
        """Test that ST for Chronicle A cannot approve characters in Chronicle B."""
        self.client.login(username="st_a", password="password")
        response = self.client.post(
            self.st_user_a.profile.get_absolute_url(),
            {"approve_character": self.char_b.id},
        )
        self.assertEqual(response.status_code, 403)
        self.char_b.refresh_from_db()
        self.assertEqual(self.char_b.status, "Sub")

    def test_st_cannot_approve_location_in_other_chronicle(self):
        """Test that ST for Chronicle A cannot approve locations in Chronicle B."""
        self.client.login(username="st_a", password="password")
        response = self.client.post(
            self.st_user_a.profile.get_absolute_url(),
            {"approve_location": self.location_b.id},
        )
        self.assertEqual(response.status_code, 403)
        self.location_b.refresh_from_db()
        self.assertEqual(self.location_b.status, "Sub")

    def test_st_cannot_approve_item_in_other_chronicle(self):
        """Test that ST for Chronicle A cannot approve items in Chronicle B."""
        self.client.login(username="st_a", password="password")
        response = self.client.post(
            self.st_user_a.profile.get_absolute_url(),
            {"approve_item": self.item_b.id},
        )
        self.assertEqual(response.status_code, 403)
        self.item_b.refresh_from_db()
        self.assertEqual(self.item_b.status, "Sub")

    def test_st_cannot_award_scene_xp_in_other_chronicle(self):
        """Test that ST for Chronicle A cannot award scene XP in Chronicle B."""
        self.client.login(username="st_a", password="password")
        response = self.client.post(
            self.st_user_a.profile.get_absolute_url(),
            {
                "submit_scene": self.scene_b.id,
                f"scene_{self.scene_b.pk}-{self.char_b.name}": "on",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.scene_b.refresh_from_db()
        self.assertFalse(self.scene_b.xp_given)

    def test_st_cannot_award_freebies_in_other_chronicle(self):
        """Test that ST for Chronicle A cannot award freebies in Chronicle B."""
        self.client.login(username="st_a", password="password")
        initial_freebies = self.char_freebies_b.freebies
        response = self.client.post(
            self.st_user_a.profile.get_absolute_url(),
            {
                "submit_freebies": self.char_freebies_b.id,
                "backstory_freebies": 5,
            },
        )
        self.assertEqual(response.status_code, 403)
        self.char_freebies_b.refresh_from_db()
        self.assertEqual(self.char_freebies_b.freebies, initial_freebies)
        self.assertFalse(self.char_freebies_b.freebies_approved)

    def test_st_cannot_approve_weekly_xp_in_other_chronicle(self):
        """Test that ST for Chronicle A cannot approve weekly XP in Chronicle B."""
        self.client.login(username="st_a", password="password")
        response = self.client.post(
            self.st_user_a.profile.get_absolute_url(),
            {
                "submit_weekly_approval": f"week-{self.week.pk}-char-{self.char_b.pk}",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.xp_request_b.refresh_from_db()
        self.assertFalse(self.xp_request_b.approved)

    def test_st_cannot_approve_image_in_other_chronicle(self):
        """Test that ST for Chronicle A cannot approve character images in Chronicle B."""
        # Set up character with pending image
        self.char_b.image_status = "sub"
        self.char_b.status = "App"  # Must be approved to have image approval
        self.char_b.save()

        self.client.login(username="st_a", password="password")
        response = self.client.post(
            self.st_user_a.profile.get_absolute_url(),
            {"approve_character_image": f"image-{self.char_b.id}"},
        )
        self.assertEqual(response.status_code, 403)
        self.char_b.refresh_from_db()
        self.assertEqual(self.char_b.image_status, "sub")

    def test_st_can_approve_character_in_own_chronicle(self):
        """Test that ST for Chronicle B can approve characters in Chronicle B."""
        self.client.login(username="st_b", password="password")
        response = self.client.post(
            self.st_user_b.profile.get_absolute_url(),
            {"approve_character": self.char_b.id},
        )
        self.assertEqual(response.status_code, 302)
        self.char_b.refresh_from_db()
        self.assertEqual(self.char_b.status, "App")

    def test_head_st_can_approve_in_own_chronicle(self):
        """Test that head ST can approve in their own chronicle."""
        # Make st_user_b the head ST for Chronicle B
        self.chronicle_b.head_st = self.st_user_b
        self.chronicle_b.save()

        # Reset character status
        self.char_b.status = "Sub"
        self.char_b.save()

        self.client.login(username="st_b", password="password")
        response = self.client.post(
            self.st_user_b.profile.get_absolute_url(),
            {"approve_character": self.char_b.id},
        )
        self.assertEqual(response.status_code, 302)
        self.char_b.refresh_from_db()
        self.assertEqual(self.char_b.status, "App")


class TestCustomLoginView(TestCase):
    """Test the custom login view."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")

    def test_successful_login_redirects_to_profile(self):
        """Test that successful login redirects to user profile."""
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "password"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome back")

    def test_failed_login_shows_error(self):
        """Test that failed login shows an error message."""
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertTrue(any("Invalid" in str(m) for m in messages))
