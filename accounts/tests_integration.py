"""
Integration tests for the accounts app.

Tests cover:
- Signal handlers (Profile auto-creation)
- Form validation (ProfileUpdateForm, CustomUserCreationForm, SceneXP, FreebieAwardForm)
- Profile view approval workflows
- ST permission boundaries
"""
from accounts.forms import (
    CustomUserCreationForm,
    FreebieAwardForm,
    ProfileUpdateForm,
    SceneXP,
)
from accounts.models import Profile
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from game.models import Chronicle, Gameline, Scene, STRelationship
from items.models.core import ItemModel
from locations.models.core import LocationModel


class TestProfileSignal(TestCase):
    """Test that Profile is automatically created when User is created."""

    def test_profile_created_on_user_creation(self):
        """Test that creating a user automatically creates a profile."""
        user = User.objects.create_user("testuser", "test@test.com", "password")
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, Profile)
        self.assertEqual(user.profile.user, user)

    def test_profile_has_default_values(self):
        """Test that new profile has correct default values."""
        user = User.objects.create_user("testuser", "test@test.com", "password")
        profile = user.profile
        self.assertEqual(profile.theme, "light")
        self.assertEqual(profile.preferred_heading, "wod_heading")
        self.assertTrue(profile.highlight_text)
        self.assertEqual(profile.discord_id, "")
        self.assertFalse(profile.discord_toggle)
        self.assertFalse(profile.lines_toggle)
        self.assertFalse(profile.veils_toggle)

    def test_multiple_users_get_separate_profiles(self):
        """Test that each user gets their own profile."""
        user1 = User.objects.create_user("user1", "user1@test.com", "password")
        user2 = User.objects.create_user("user2", "user2@test.com", "password")
        self.assertNotEqual(user1.profile.pk, user2.profile.pk)

    def test_profile_str_representation(self):
        """Test profile string representation."""
        user = User.objects.create_user("testuser", "test@test.com", "password")
        self.assertEqual(str(user.profile), "testuser")


class TestCustomUserCreationForm(TestCase):
    """Test CustomUserCreationForm validation and behavior."""

    def test_valid_form(self):
        """Test form with valid data."""
        form = CustomUserCreationForm(
            data={
                "username": "newuser",
                "email": "new@test.com",
                "password1": "testpass123!",
                "password2": "testpass123!",
            }
        )
        self.assertTrue(form.is_valid())

    def test_username_email_must_be_different(self):
        """Test that username and email cannot be the same."""
        form = CustomUserCreationForm(
            data={
                "username": "same@test.com",
                "email": "same@test.com",
                "password1": "testpass123!",
                "password2": "testpass123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Username and Email must be distinct", str(form.errors))

    def test_password_mismatch(self):
        """Test that mismatched passwords are rejected."""
        form = CustomUserCreationForm(
            data={
                "username": "newuser",
                "email": "new@test.com",
                "password1": "testpass123!",
                "password2": "differentpass123!",
            }
        )
        self.assertFalse(form.is_valid())

    def test_email_is_optional(self):
        """Test that email field is optional."""
        form = CustomUserCreationForm(
            data={
                "username": "newuser",
                "email": "",
                "password1": "testpass123!",
                "password2": "testpass123!",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_saves_email(self):
        """Test that form properly saves email."""
        form = CustomUserCreationForm(
            data={
                "username": "newuser",
                "email": "new@test.com",
                "password1": "testpass123!",
                "password2": "testpass123!",
            }
        )
        user = form.save()
        self.assertEqual(user.email, "new@test.com")

    def test_form_has_tg_form_control_class(self):
        """Test that form fields have tg-form-control class."""
        form = CustomUserCreationForm()
        self.assertIn(
            "tg-form-control", form.fields["username"].widget.attrs.get("class", "")
        )
        self.assertIn(
            "tg-form-control", form.fields["email"].widget.attrs.get("class", "")
        )


class TestProfileUpdateForm(TestCase):
    """Test ProfileUpdateForm validation."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.profile = self.user.profile

    def test_valid_form(self):
        """Test form with valid data."""
        form = ProfileUpdateForm(
            data={
                "preferred_heading": "mta_heading",
                "theme": "dark",
                "highlight_text": True,
                "discord_id": "user#1234",
                "lines": "No torture scenes",
                "veils": "No graphic violence",
                "discord_toggle": True,
                "lines_toggle": True,
                "veils_toggle": False,
            },
            instance=self.profile,
        )
        self.assertTrue(form.is_valid())

    def test_all_theme_choices_valid(self):
        """Test that all theme choices are valid."""
        for theme in ["light", "dark"]:
            form = ProfileUpdateForm(
                data={
                    "preferred_heading": "wod_heading",
                    "theme": theme,
                    "highlight_text": True,
                    "discord_id": "",
                    "lines": "",
                    "veils": "",
                    "discord_toggle": False,
                    "lines_toggle": False,
                    "veils_toggle": False,
                },
                instance=self.profile,
            )
            self.assertTrue(form.is_valid(), f"Theme {theme} should be valid")

    def test_all_heading_choices_valid(self):
        """Test that all heading choices are valid."""
        headings = [
            "wod_heading",
            "vtm_heading",
            "wta_heading",
            "mta_heading",
            "ctd_heading",
            "wto_heading",
        ]
        for heading in headings:
            form = ProfileUpdateForm(
                data={
                    "preferred_heading": heading,
                    "theme": "light",
                    "highlight_text": True,
                    "discord_id": "",
                    "lines": "",
                    "veils": "",
                    "discord_toggle": False,
                    "lines_toggle": False,
                    "veils_toggle": False,
                },
                instance=self.profile,
            )
            self.assertTrue(form.is_valid(), f"Heading {heading} should be valid")

    def test_discord_id_optional(self):
        """Test that discord_id is optional."""
        form = ProfileUpdateForm(
            data={
                "preferred_heading": "wod_heading",
                "theme": "light",
                "highlight_text": True,
                "discord_id": "",
                "lines": "",
                "veils": "",
                "discord_toggle": False,
                "lines_toggle": False,
                "veils_toggle": False,
            },
            instance=self.profile,
        )
        self.assertTrue(form.is_valid())


class TestSceneXPForm(TestCase):
    """Test SceneXP form for awarding XP."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location", chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.char1 = Human.objects.create(
            name="Character One",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.char2 = Human.objects.create(
            name="Character Two",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.npc = Human.objects.create(
            name="NPC Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            npc=True,
        )
        self.scene.characters.add(self.char1, self.char2, self.npc)

    def test_form_creates_fields_for_non_npc_characters(self):
        """Test that form creates fields for non-NPC characters only."""
        form = SceneXP(scene=self.scene)
        self.assertIn("Character One", form.fields)
        self.assertIn("Character Two", form.fields)
        self.assertNotIn("NPC Character", form.fields)

    def test_form_awards_xp_to_selected_characters(self):
        """Test that form awards XP correctly."""
        form = SceneXP(
            data={"Character One": True, "Character Two": False}, scene=self.scene
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.char1.refresh_from_db()
        self.char2.refresh_from_db()
        self.assertEqual(self.char1.xp, 1)
        self.assertEqual(self.char2.xp, 0)
        self.assertTrue(self.scene.xp_given)

    def test_form_marks_scene_xp_given(self):
        """Test that scene is marked as XP given."""
        form = SceneXP(data={"Character One": False}, scene=self.scene)
        form.is_valid()
        form.save()
        self.assertTrue(self.scene.xp_given)


class TestFreebieAwardForm(TestCase):
    """Test FreebieAwardForm for awarding freebie points."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.char = Human.objects.create(
            name="Test Character", owner=self.user, concept="Test"
        )

    def test_valid_freebie_award(self):
        """Test valid freebie award."""
        form = FreebieAwardForm(data={"backstory_freebies": 10}, character=self.char)
        self.assertTrue(form.is_valid())
        form.save()
        self.char.refresh_from_db()
        self.assertEqual(self.char.freebies, 10)
        self.assertTrue(self.char.freebies_approved)

    def test_freebie_award_max_15(self):
        """Test that maximum freebie award is 15."""
        form = FreebieAwardForm(data={"backstory_freebies": 16}, character=self.char)
        self.assertFalse(form.is_valid())

    def test_freebie_award_min_0(self):
        """Test that minimum freebie award is 0."""
        form = FreebieAwardForm(data={"backstory_freebies": -1}, character=self.char)
        self.assertFalse(form.is_valid())

    def test_freebie_award_adds_to_existing(self):
        """Test that freebie award adds to existing freebies."""
        self.char.freebies = 5
        self.char.save()
        form = FreebieAwardForm(data={"backstory_freebies": 10}, character=self.char)
        form.is_valid()
        form.save()
        self.char.refresh_from_db()
        self.assertEqual(self.char.freebies, 15)


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


class TestProfileSTMethods(TestCase):
    """Test Profile methods related to ST functionality."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.chronicle1 = Chronicle.objects.create(name="Chronicle 1")
        self.chronicle2 = Chronicle.objects.create(name="Chronicle 2")
        self.gameline1 = Gameline.objects.create(name="Vampire")
        self.gameline2 = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle1, gameline=self.gameline1
        )
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle2, gameline=self.gameline2
        )

    def test_is_st_returns_true_for_storyteller(self):
        """Test that is_st returns True for users with ST relationships."""
        self.assertTrue(self.st_user.profile.is_st())

    def test_is_st_returns_false_for_non_storyteller(self):
        """Test that is_st returns False for regular users."""
        self.assertFalse(self.user.profile.is_st())

    def test_st_relations_returns_grouped_relationships(self):
        """Test that st_relations returns relationships grouped by chronicle."""
        relations = self.st_user.profile.st_relations()
        self.assertIn(self.chronicle1, relations)
        self.assertIn(self.chronicle2, relations)
        self.assertEqual(len(relations[self.chronicle1]), 1)
        self.assertEqual(relations[self.chronicle1][0].gameline, self.gameline1)

    def test_st_relations_empty_for_non_st(self):
        """Test that st_relations is empty for non-storytellers."""
        relations = self.user.profile.st_relations()
        self.assertEqual(len(relations), 0)


class TestProfileObjectQueries(TestCase):
    """Test Profile methods for querying owned objects."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.char1 = Human.objects.create(
            name="Character 1", owner=self.user, concept="Test"
        )
        self.char2 = Human.objects.create(
            name="Character 2", owner=self.user, concept="Test"
        )
        self.location = LocationModel.objects.create(
            name="My Location", owner=self.user
        )
        self.item = ItemModel.objects.create(name="My Item", owner=self.user)

    def test_my_characters_returns_owned_characters(self):
        """Test that my_characters returns all owned characters."""
        chars = self.user.profile.my_characters()
        self.assertEqual(chars.count(), 2)
        self.assertIn(self.char1, chars)
        self.assertIn(self.char2, chars)

    def test_my_locations_returns_owned_locations(self):
        """Test that my_locations returns all owned locations."""
        locs = self.user.profile.my_locations()
        self.assertEqual(locs.count(), 1)
        self.assertIn(self.location, locs)

    def test_my_items_returns_owned_items(self):
        """Test that my_items returns all owned items."""
        items = self.user.profile.my_items()
        self.assertEqual(items.count(), 1)
        self.assertIn(self.item, items)


class TestSignUpView(TestCase):
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
        response = self.client.get(
            reverse("profile_update", kwargs={"pk": self.user.profile.pk})
        )
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


class TestProfileThemeMethods(TestCase):
    """Test Profile theme-related methods."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")

    def test_get_theme_css_path_light(self):
        """Test theme CSS path for light theme."""
        self.user.profile.theme = "light"
        self.user.profile.save()
        path = self.user.profile.get_theme_css_path()
        self.assertEqual(path, "themes/light.css")

    def test_get_theme_css_path_dark(self):
        """Test theme CSS path for dark theme."""
        self.user.profile.theme = "dark"
        self.user.profile.save()
        path = self.user.profile.get_theme_css_path()
        self.assertEqual(path, "themes/dark.css")
