"""Tests for character_template forms module."""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from core.forms.character_template import (
    CharacterTemplateForm,
    CharacterTemplateImportForm,
)
from core.models import CharacterTemplate
from game.models import Chronicle, Gameline, STRelationship

User = get_user_model()


class CharacterTemplateFormTest(TestCase):
    """Test CharacterTemplateForm functionality."""

    def setUp(self):
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="other_user", email="other@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_form_initialization_with_user(self):
        """Test that form initializes correctly with user."""
        form = CharacterTemplateForm(user=self.st_user)
        self.assertEqual(form.user, self.st_user)

    def test_chronicle_queryset_filtered_for_st(self):
        """Test that chronicle choices are filtered to ST's chronicles."""
        form = CharacterTemplateForm(user=self.st_user)
        chronicle_queryset = form.fields["chronicle"].queryset
        self.assertIn(self.chronicle, chronicle_queryset)
        self.assertNotIn(self.other_chronicle, chronicle_queryset)

    def test_chronicle_not_required(self):
        """Test that chronicle field is not required."""
        form = CharacterTemplateForm(user=self.st_user)
        self.assertFalse(form.fields["chronicle"].required)

    def test_clean_sets_owner(self):
        """Test that clean() sets the owner to current user."""
        form_data = {
            "name": "Test Template",
            "gameline": "mta",
            "character_type": "mage",
            "concept": "",
            "faction": "",
            "description": "",
            "basic_info": "{}",
            "attributes": "{}",
            "abilities": "{}",
            "backgrounds": "[]",
            "powers": "{}",
            "merits_flaws": "[]",
            "specialties": "[]",
            "languages": "[]",
            "equipment": "",
            "suggested_freebie_spending": "{}",
            "is_public": True,
        }
        form = CharacterTemplateForm(data=form_data, user=self.st_user)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.instance.owner, self.st_user)

    def test_clean_marks_as_not_official(self):
        """Test that clean() marks template as not official."""
        form_data = {
            "name": "Test Template",
            "gameline": "mta",
            "character_type": "mage",
            "concept": "",
            "faction": "",
            "description": "",
            "basic_info": "{}",
            "attributes": "{}",
            "abilities": "{}",
            "backgrounds": "[]",
            "powers": "{}",
            "merits_flaws": "[]",
            "specialties": "[]",
            "languages": "[]",
            "equipment": "",
            "suggested_freebie_spending": "{}",
            "is_public": True,
        }
        form = CharacterTemplateForm(data=form_data, user=self.st_user)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertFalse(form.instance.is_official)

    def test_save_sets_owner(self):
        """Test that save() sets the owner to current user."""
        form_data = {
            "name": "Saved Template",
            "gameline": "mta",
            "character_type": "mage",
            "concept": "",
            "faction": "",
            "description": "",
            "basic_info": "{}",
            "attributes": "{}",
            "abilities": "{}",
            "backgrounds": "[]",
            "powers": "{}",
            "merits_flaws": "[]",
            "specialties": "[]",
            "languages": "[]",
            "equipment": "",
            "suggested_freebie_spending": "{}",
            "is_public": True,
        }
        form = CharacterTemplateForm(data=form_data, user=self.st_user)
        self.assertTrue(form.is_valid(), form.errors)
        template = form.save()
        self.assertEqual(template.owner, self.st_user)
        self.assertFalse(template.is_official)

    def test_save_without_commit(self):
        """Test that save(commit=False) doesn't save to database."""
        form_data = {
            "name": "Uncommitted Template",
            "gameline": "mta",
            "character_type": "mage",
            "concept": "",
            "faction": "",
            "description": "",
            "basic_info": "{}",
            "attributes": "{}",
            "abilities": "{}",
            "backgrounds": "[]",
            "powers": "{}",
            "merits_flaws": "[]",
            "specialties": "[]",
            "languages": "[]",
            "equipment": "",
            "suggested_freebie_spending": "{}",
            "is_public": True,
        }
        form = CharacterTemplateForm(data=form_data, user=self.st_user)
        self.assertTrue(form.is_valid(), form.errors)
        template = form.save(commit=False)
        self.assertIsNone(template.pk)
        self.assertEqual(template.owner, self.st_user)

    def test_form_without_user(self):
        """Test that form works without user (owner not set)."""
        form_data = {
            "name": "No User Template",
            "gameline": "mta",
            "character_type": "mage",
            "concept": "",
            "faction": "",
            "description": "",
            "basic_info": "{}",
            "attributes": "{}",
            "abilities": "{}",
            "backgrounds": "[]",
            "powers": "{}",
            "merits_flaws": "[]",
            "specialties": "[]",
            "languages": "[]",
            "equipment": "",
            "suggested_freebie_spending": "{}",
            "is_public": True,
        }
        form = CharacterTemplateForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        # Owner should be None when no user provided
        self.assertIsNone(form.instance.owner)

    def test_form_with_unauthenticated_user(self):
        """Test form behavior when user is not authenticated."""
        from django.contrib.auth.models import AnonymousUser

        anon = AnonymousUser()
        form = CharacterTemplateForm(user=anon)
        # Should not crash, just won't filter chronicles
        self.assertEqual(form.user, anon)

    def test_update_existing_template(self):
        """Test updating an existing template."""
        template = CharacterTemplate.objects.create(
            name="Original Name",
            gameline="mta",
            character_type="mage",
            owner=self.st_user,
        )
        form_data = {
            "name": "Updated Name",
            "gameline": "mta",
            "character_type": "mage",
            "concept": "Updated",
            "faction": "",
            "description": "",
            "basic_info": "{}",
            "attributes": "{}",
            "abilities": "{}",
            "backgrounds": "[]",
            "powers": "{}",
            "merits_flaws": "[]",
            "specialties": "[]",
            "languages": "[]",
            "equipment": "",
            "suggested_freebie_spending": "{}",
            "is_public": True,
        }
        form = CharacterTemplateForm(data=form_data, instance=template, user=self.st_user)
        self.assertTrue(form.is_valid(), form.errors)
        updated = form.save()
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.concept, "Updated")


class CharacterTemplateImportFormTest(TestCase):
    """Test CharacterTemplateImportForm functionality."""

    def setUp(self):
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_form_initialization_with_user(self):
        """Test that form initializes correctly with user."""
        form = CharacterTemplateImportForm(user=self.st_user)
        self.assertEqual(form.user, self.st_user)

    def test_chronicle_queryset_filtered_for_st(self):
        """Test that chronicle choices are filtered to ST's chronicles."""
        form = CharacterTemplateImportForm(user=self.st_user)
        chronicle_queryset = form.fields["chronicle"].queryset
        self.assertIn(self.chronicle, chronicle_queryset)
        self.assertNotIn(self.other_chronicle, chronicle_queryset)

    def test_clean_json_file_validates_presence(self):
        """Test that clean_json_file validates file is present."""
        form = CharacterTemplateImportForm(
            data={"is_public": False},
            files={},  # No file
            user=self.st_user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("json_file", form.errors)

    def test_clean_json_file_validates_size(self):
        """Test that clean_json_file validates file size (max 5MB)."""
        # Create a file larger than 5MB
        large_content = b"x" * (6 * 1024 * 1024)  # 6MB
        large_file = SimpleUploadedFile(
            "large.json",
            large_content,
            content_type="application/json",
        )
        form = CharacterTemplateImportForm(
            data={"is_public": False},
            files={"json_file": large_file},
            user=self.st_user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("json_file", form.errors)
        self.assertIn("5MB", str(form.errors["json_file"]))

    def test_clean_json_file_validates_extension(self):
        """Test that clean_json_file validates .json extension."""
        wrong_ext_file = SimpleUploadedFile(
            "template.txt",
            b'{"name": "test"}',
            content_type="text/plain",
        )
        form = CharacterTemplateImportForm(
            data={"is_public": False},
            files={"json_file": wrong_ext_file},
            user=self.st_user,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("json_file", form.errors)
        self.assertIn(".json", str(form.errors["json_file"]))

    def test_valid_json_file_passes_validation(self):
        """Test that valid JSON file passes validation."""
        valid_file = SimpleUploadedFile(
            "template.json",
            b'{"name": "test", "gameline": "mta", "character_type": "mage"}',
            content_type="application/json",
        )
        form = CharacterTemplateImportForm(
            data={"is_public": False},
            files={"json_file": valid_file},
            user=self.st_user,
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_without_user(self):
        """Test form behavior without user."""
        form = CharacterTemplateImportForm()
        self.assertIsNone(form.user)

    def test_is_public_default_false(self):
        """Test that is_public defaults to False."""
        form = CharacterTemplateImportForm(user=self.st_user)
        self.assertFalse(form.fields["is_public"].initial)

    def test_chronicle_not_required(self):
        """Test that chronicle field is not required."""
        form = CharacterTemplateImportForm(user=self.st_user)
        self.assertFalse(form.fields["chronicle"].required)
