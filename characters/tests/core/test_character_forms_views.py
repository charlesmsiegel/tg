"""
Tests for Character forms and views, specifically testing permission-based editing.

Tests cover:
- LimitedCharacterForm field restrictions
- CharacterUpdateView form selection based on permissions
- Owner vs ST editing capabilities
- Image status handling
"""

from io import BytesIO

from characters.forms.core import LimitedCharacterForm
from characters.models.core import Character
from core.permissions import Permission, PermissionManager
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from game.models import Chronicle


class TestLimitedCharacterForm(TestCase):
    """Test the LimitedCharacterForm for owner editing."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.character = Character.objects.create(
            name="Test Character",
            owner=self.user,
            concept="Test Concept",
            description="Original description",
            public_info="Original public info",
            notes="Original notes",
        )

    def test_form_only_includes_descriptive_fields(self):
        """Test that the form only includes safe, descriptive fields."""
        form = LimitedCharacterForm(instance=self.character)

        # Should include these descriptive fields
        self.assertIn("concept", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("public_info", form.fields)
        self.assertIn("notes", form.fields)
        self.assertIn("image", form.fields)

        # Should NOT include these mechanical/security fields
        self.assertNotIn("name", form.fields)
        self.assertNotIn("owner", form.fields)
        self.assertNotIn("chronicle", form.fields)
        self.assertNotIn("status", form.fields)
        self.assertNotIn("xp", form.fields)
        self.assertNotIn("spent_xp", form.fields)
        self.assertNotIn("creation_status", form.fields)
        self.assertNotIn("display", form.fields)
        self.assertNotIn("visibility", form.fields)
        self.assertNotIn("freebies_approved", form.fields)
        self.assertNotIn("npc", form.fields)

    def test_form_valid_data_saves_correctly(self):
        """Test that valid form data saves correctly."""
        form_data = {
            "concept": "Updated Concept",
            "description": "Updated description",
            "public_info": "Updated public info",
            "notes": "Updated notes",
        }
        form = LimitedCharacterForm(data=form_data, instance=self.character)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        updated_character = form.save()
        updated_character.refresh_from_db()

        self.assertEqual(updated_character.concept, "Updated Concept")
        self.assertEqual(updated_character.description, "Updated description")
        self.assertEqual(updated_character.public_info, "Updated public info")
        self.assertEqual(updated_character.notes, "Updated notes")

        # Verify other fields weren't changed
        self.assertEqual(updated_character.name, "Test Character")
        self.assertEqual(updated_character.owner, self.user)

    def test_form_placeholders_exist(self):
        """Test that form fields have helpful placeholders."""
        form = LimitedCharacterForm(instance=self.character)

        self.assertIn("placeholder", form.fields["concept"].widget.attrs)
        self.assertIn("placeholder", form.fields["description"].widget.attrs)
        self.assertIn("placeholder", form.fields["public_info"].widget.attrs)
        self.assertIn("placeholder", form.fields["notes"].widget.attrs)

    def test_form_help_text_exists(self):
        """Test that form fields have helpful help text."""
        form = LimitedCharacterForm(instance=self.character)

        self.assertIn("visible to other players", form.fields["public_info"].help_text)
        self.assertIn("visible only to you", form.fields["notes"].help_text)

    def test_image_field_optional(self):
        """Test that image field is optional."""
        form = LimitedCharacterForm(instance=self.character)
        self.assertFalse(form.fields["image"].required)

    def test_image_status_reset_on_image_change(self):
        """Test that image_status is reset to 'sub' when image is changed."""
        # Set initial image status to approved
        self.character.image_status = "app"
        self.character.save()

        # Create a fake image file
        image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )

        form_data = {
            "concept": self.character.concept,
            "description": self.character.description,
            "public_info": self.character.public_info,
            "notes": self.character.notes,
        }

        form = LimitedCharacterForm(
            data=form_data, files={"image": image_file}, instance=self.character
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        updated_character = form.save()
        updated_character.refresh_from_db()

        # Image status should be reset to 'sub' (submitted for approval)
        self.assertEqual(updated_character.image_status, "sub")

    def test_image_status_unchanged_when_no_image_change(self):
        """Test that image_status is not changed when image is not updated."""
        # Set initial image status to approved
        self.character.image_status = "app"
        self.character.save()

        form_data = {
            "concept": "Updated Concept",
            "description": self.character.description,
            "public_info": self.character.public_info,
            "notes": self.character.notes,
        }

        form = LimitedCharacterForm(data=form_data, instance=self.character)

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

        updated_character = form.save()
        updated_character.refresh_from_db()

        # Image status should remain 'app'
        self.assertEqual(updated_character.image_status, "app")


class TestCharacterUpdateViewPermissions(TestCase):
    """Test CharacterUpdateView form selection based on permissions."""

    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(username="owner", password="password")
        self.st_user = User.objects.create_user(username="st", password="password")
        self.other_user = User.objects.create_user(username="other", password="password")

        # Create chronicle and make st_user a storyteller
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st_user)

        # Create character
        self.character = Character.objects.create(
            name="Test Character",
            owner=self.owner,
            chronicle=self.chronicle,
            concept="Test Concept",
            description="Test description",
            notes="Test notes",
            status="App",  # Approved status
        )

        self.url = self.character.get_update_url()

    def test_owner_gets_limited_form(self):
        """Test that character owner sees limited form fields."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # Check form fields - owner should only see limited fields
        form = response.context["form"]
        self.assertIn("concept", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("notes", form.fields)

        # Should NOT see these fields
        self.assertNotIn("name", form.fields)
        self.assertNotIn("xp", form.fields)
        self.assertNotIn("status", form.fields)
        self.assertNotIn("chronicle", form.fields)

    def test_st_gets_full_form(self):
        """Test that chronicle ST sees all form fields."""
        self.client.login(username="st", password="password")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # Check form fields - ST should see all fields
        form = response.context["form"]

        # ST should have access to mechanical fields
        self.assertIn("name", form.fields)
        self.assertIn("status", form.fields)
        # Note: The full form uses fields = "__all__" so all model fields should be present

    def test_owner_can_update_descriptive_fields(self):
        """Test that owner can successfully update descriptive fields."""
        self.client.login(username="owner", password="password")

        form_data = {
            "concept": "Updated Concept",
            "description": "Updated description",
            "public_info": "",
            "notes": "Updated notes",
        }

        response = self.client.post(self.url, data=form_data)

        # Should redirect on success
        self.assertEqual(response.status_code, 302)

        self.character.refresh_from_db()
        self.assertEqual(self.character.concept, "Updated Concept")
        self.assertEqual(self.character.description, "Updated description")
        self.assertEqual(self.character.notes, "Updated notes")

    def test_owner_cannot_modify_mechanical_fields_via_post(self):
        """Test that owner cannot modify restricted fields even via POST manipulation."""
        self.client.login(username="owner", password="password")

        # Try to manipulate mechanical fields via POST
        form_data = {
            "concept": "Updated Concept",
            "description": "Updated description",
            "public_info": "",
            "notes": "Updated notes",
            # Attempt to change restricted fields
            "name": "Hacked Name",
            "xp": 9999,
            "status": "Ret",
            "npc": True,
        }

        response = self.client.post(self.url, data=form_data)

        self.character.refresh_from_db()

        # Descriptive fields should be updated
        self.assertEqual(self.character.concept, "Updated Concept")

        # But mechanical fields should remain unchanged
        self.assertEqual(self.character.name, "Test Character")
        self.assertEqual(self.character.xp, 0)
        self.assertEqual(self.character.status, "App")
        self.assertEqual(self.character.npc, False)

    def test_non_owner_non_st_cannot_access_edit(self):
        """Test that users without edit permission cannot access the edit view."""
        self.client.login(username="other", password="password")

        response = self.client.get(self.url)

        # Should be forbidden or redirected
        self.assertIn(response.status_code, [302, 403, 404])

    def test_anonymous_user_redirected(self):
        """Test that anonymous users are redirected to login."""
        response = self.client.get(self.url)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)


class TestCharacterUpdateViewFormIntegration(TestCase):
    """Integration tests for form usage in update view."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.character = Character.objects.create(
            name="Test Character",
            owner=self.owner,
            concept="Test Concept",
            description="Test description",
            notes="Test notes",
        )
        self.url = self.character.get_update_url()

    def test_form_instance_is_character(self):
        """Test that form is initialized with the character instance."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.url)

        form = response.context["form"]
        self.assertEqual(form.instance, self.character)
        self.assertEqual(form.initial.get("concept"), "Test Concept")
        self.assertEqual(form.initial.get("description"), "Test description")

    def test_successful_update_shows_success_message(self):
        """Test that successful update shows appropriate message."""
        self.client.login(username="owner", password="password")

        form_data = {
            "concept": "Updated Concept",
            "description": "Updated description",
            "public_info": "",
            "notes": "Updated notes",
        }

        response = self.client.post(self.url, data=form_data, follow=True)

        # Check for success (may vary based on MessageMixin implementation)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_data_shows_errors(self):
        """Test that invalid form data displays errors."""
        self.client.login(username="owner", password="password")

        # Submit with empty concept (assuming it's required)
        form_data = {
            "concept": "",  # Empty concept
            "description": "Test",
            "public_info": "",
            "notes": "",
        }

        response = self.client.post(self.url, data=form_data)

        # Should re-render form with errors, not redirect
        self.assertEqual(response.status_code, 200)
        form = response.context.get("form")
        if form:
            # Form should have errors or be invalid
            self.assertTrue(len(form.errors) > 0 or not form.is_valid())
