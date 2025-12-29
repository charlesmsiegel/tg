"""Tests for accounts forms."""

from accounts.forms import (
    CustomAuthenticationForm,
    CustomUserCreationForm,
    FreebieAwardForm,
    ProfileUpdateForm,
    SceneXP,
    StoryXP,
)
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, Scene, Story
from locations.models.core import LocationModel


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
        self.assertIn("tg-form-control", form.fields["username"].widget.attrs.get("class", ""))
        self.assertIn("tg-form-control", form.fields["email"].widget.attrs.get("class", ""))


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
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
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
        form = SceneXP(data={"Character One": True, "Character Two": False}, scene=self.scene)
        self.assertTrue(form.is_valid())
        form.save()
        self.char1.refresh_from_db()
        self.char2.refresh_from_db()
        self.scene.refresh_from_db()
        self.assertEqual(self.char1.xp, 1)
        self.assertEqual(self.char2.xp, 0)
        self.assertTrue(self.scene.xp_given)

    def test_form_marks_scene_xp_given(self):
        """Test that scene is marked as XP given."""
        form = SceneXP(data={"Character One": False}, scene=self.scene)
        form.is_valid()
        form.save()
        self.scene.refresh_from_db()
        self.assertTrue(self.scene.xp_given)


class TestFreebieAwardForm(TestCase):
    """Test FreebieAwardForm for awarding freebie points."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.char = Human.objects.create(name="Test Character", owner=self.user, concept="Test")

    def test_valid_freebie_award(self):
        """Test valid freebie award."""
        initial_freebies = self.char.freebies  # Default is 15
        form = FreebieAwardForm(data={"backstory_freebies": 10}, character=self.char)
        self.assertTrue(form.is_valid())
        form.save()
        self.char.refresh_from_db()
        # Backstory freebies are added to existing freebies
        self.assertEqual(self.char.freebies, initial_freebies + 10)
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


class TestStoryXPForm(TestCase):
    """Test StoryXP form for awarding story XP."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.story = Story.objects.create(name="Test Story")
        self.char1 = Human.objects.create(
            name="Character One",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        self.char2 = Human.objects.create(
            name="Character Two",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )

    def test_form_creates_fields_for_approved_characters(self):
        """Test that form creates fields for approved characters."""
        form = StoryXP(story=self.story)
        # Form creates fields for each character for success, danger, growth, drama, duration
        self.assertIn("Character One-success", form.fields)
        self.assertIn("Character One-danger", form.fields)
        self.assertIn("Character One-growth", form.fields)
        self.assertIn("Character One-drama", form.fields)
        self.assertIn("Character One-duration", form.fields)

    def test_form_clean_processes_data_correctly(self):
        """Test that form clean method processes data into character dict."""
        form = StoryXP(
            data={
                f"story_{self.story.pk}-Character One-success": "on",
                f"story_{self.story.pk}-Character One-danger": "on",
                f"story_{self.story.pk}-Character One-growth": "",
                f"story_{self.story.pk}-Character One-drama": "",
                f"story_{self.story.pk}-Character One-duration": "2",
            },
            story=self.story,
        )
        self.assertTrue(form.is_valid())
        cleaned = form.cleaned_data
        self.assertIn(self.char1, cleaned)
        self.assertTrue(cleaned[self.char1]["success"])
        self.assertTrue(cleaned[self.char1]["danger"])
        self.assertFalse(cleaned[self.char1]["growth"])
        self.assertFalse(cleaned[self.char1]["drama"])
        self.assertEqual(cleaned[self.char1]["duration"], 2)


class TestCustomAuthenticationForm(TestCase):
    """Test CustomAuthenticationForm styling."""

    def test_form_has_tg_form_control_class(self):
        """Test that form fields have tg-form-control class."""
        form = CustomAuthenticationForm()
        self.assertIn("tg-form-control", form.fields["username"].widget.attrs.get("class", ""))
        self.assertIn("tg-form-control", form.fields["password"].widget.attrs.get("class", ""))
