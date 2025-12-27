"""Tests for accounts views."""

from characters.models.core import Human
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle, Gameline, STRelationship
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
            name="Test Character 2", owner=self.user2, chronicle=chronicle
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
            reverse("signup"),
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
            reverse("signup"),
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
        response = self.client.get(reverse("profile_update", kwargs={"pk": self.user.profile.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_can_update_profile(self):
        """Test that user can update their profile."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("profile_update", kwargs={"pk": self.user.profile.pk}),
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
