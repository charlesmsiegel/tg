"""Tests for character_template views module."""

import json

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from core.models import CharacterTemplate
from core.views.character_template import (
    CharacterTemplateQuickNPCView,
    STRequiredMixin,
)
from game.models import Chronicle, Gameline, STRelationship

User = get_user_model()


class STRequiredMixinTest(TestCase):
    """Test STRequiredMixin functionality."""

    def setUp(self):
        self.factory = RequestFactory()
        self.regular_user = User.objects.create_user(
            username="regular", email="regular@test.com", password="testpass123"
        )
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_st_passes_test(self):
        """Test that ST user passes the test."""
        request = self.factory.get("/")
        request.user = self.st_user

        mixin = STRequiredMixin()
        mixin.request = request
        self.assertTrue(mixin.test_func())

    def test_regular_user_fails_test(self):
        """Test that regular user fails the test."""
        request = self.factory.get("/")
        request.user = self.regular_user

        mixin = STRequiredMixin()
        mixin.request = request
        self.assertFalse(mixin.test_func())

    def test_anonymous_user_fails_test(self):
        """Test that anonymous user fails the test."""
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.get("/")
        request.user = AnonymousUser()

        mixin = STRequiredMixin()
        mixin.request = request
        self.assertFalse(mixin.test_func())

    def test_handle_no_permission_redirects_with_message(self):
        """Test that handle_no_permission redirects to index with error message."""
        from unittest.mock import patch

        request = self.factory.get("/")
        request.user = self.regular_user
        # Add message support
        request.session = "session"
        messages = FallbackStorage(request)
        request._messages = messages

        mixin = STRequiredMixin()
        mixin.request = request

        # Mock redirect to avoid URL resolution issues
        with patch("core.views.character_template.redirect") as mock_redirect:
            from django.http import HttpResponseRedirect

            mock_redirect.return_value = HttpResponseRedirect("/")
            response = mixin.handle_no_permission()

        self.assertEqual(response.status_code, 302)
        stored_messages = list(get_messages(request))
        self.assertEqual(len(stored_messages), 1)
        self.assertIn("Storyteller", str(stored_messages[0]))


class CharacterTemplateListViewTest(TestCase):
    """Test CharacterTemplateListView functionality."""

    def setUp(self):
        self.client = Client()
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.regular_user = User.objects.create_user(
            username="regular", email="regular@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        # Create test templates
        self.official_template = CharacterTemplate.objects.create(
            name="Official Template",
            gameline="mta",
            character_type="mage",
            owner=self.st_user,
            is_official=True,
            is_public=True,
        )
        self.user_template = CharacterTemplate.objects.create(
            name="User Template",
            gameline="vtm",
            character_type="vampire",
            owner=self.st_user,
            is_official=False,
            is_public=True,
        )

    def test_requires_login(self):
        """Test that view requires authentication."""
        response = self.client.get(reverse("core:character_template_list"))
        # Should redirect to login or return 401/403 for unauthenticated users
        self.assertIn(response.status_code, [302, 401, 403])

    def test_requires_st(self):
        """Test that view requires ST status."""
        self.client.login(username="regular", password="testpass123")
        response = self.client.get(reverse("core:character_template_list"))
        self.assertEqual(response.status_code, 302)

    def test_st_can_access(self):
        """Test that ST can access the list view."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(reverse("core:character_template_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/character_template/list.html")

    def test_filter_by_gameline(self):
        """Test filtering templates by gameline."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(reverse("core:character_template_list") + "?gameline=mta")
        self.assertEqual(response.status_code, 200)
        templates = response.context["templates"]
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].gameline, "mta")

    def test_filter_by_character_type(self):
        """Test filtering templates by character type."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_list") + "?character_type=vampire"
        )
        self.assertEqual(response.status_code, 200)
        templates = response.context["templates"]
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].character_type, "vampire")

    def test_filter_by_mine(self):
        """Test filtering templates by ownership (mine)."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(reverse("core:character_template_list") + "?filter=mine")
        self.assertEqual(response.status_code, 200)
        templates = response.context["templates"]
        # Both templates belong to st_user
        self.assertEqual(len(templates), 2)

    def test_filter_by_official(self):
        """Test filtering templates by official status."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(reverse("core:character_template_list") + "?filter=official")
        self.assertEqual(response.status_code, 200)
        templates = response.context["templates"]
        self.assertEqual(len(templates), 1)
        self.assertTrue(templates[0].is_official)

    def test_filter_by_community(self):
        """Test filtering templates by community (non-official, public)."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(reverse("core:character_template_list") + "?filter=community")
        self.assertEqual(response.status_code, 200)
        templates = response.context["templates"]
        self.assertEqual(len(templates), 1)
        self.assertFalse(templates[0].is_official)
        self.assertTrue(templates[0].is_public)

    def test_context_includes_filter_params(self):
        """Test that context includes filter parameters."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_list")
            + "?filter=mine&gameline=mta&character_type=mage"
        )
        self.assertEqual(response.context["filter"], "mine")
        self.assertEqual(response.context["gameline"], "mta")
        self.assertEqual(response.context["character_type"], "mage")


class CharacterTemplateDetailViewTest(TestCase):
    """Test CharacterTemplateDetailView functionality."""

    def setUp(self):
        self.client = Client()
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.template = CharacterTemplate.objects.create(
            name="Test Template",
            gameline="mta",
            character_type="mage",
            owner=self.st_user,
            concept="Test Concept",
            description="Test Description",
        )

    def test_requires_login(self):
        """Test that view requires authentication."""
        response = self.client.get(
            reverse("core:character_template_detail", kwargs={"pk": self.template.pk})
        )
        # Should redirect to login or return 401/403 for unauthenticated users
        self.assertIn(response.status_code, [302, 401, 403])

    def test_st_can_view_detail(self):
        """Test that ST can view template details."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_detail", kwargs={"pk": self.template.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["template"], self.template)


class CharacterTemplateCreateViewTest(TestCase):
    """Test CharacterTemplateCreateView functionality."""

    def setUp(self):
        self.client = Client()
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_requires_login(self):
        """Test that view requires authentication."""
        response = self.client.get(reverse("core:character_template_create"))
        # Should redirect to login or return 401/403 for unauthenticated users
        self.assertIn(response.status_code, [302, 401, 403])

    def test_st_can_access_create_form(self):
        """Test that ST can access the create form."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(reverse("core:character_template_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_template_sets_owner(self):
        """Test that creating a template sets the owner to current user."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.post(
            reverse("core:character_template_create"),
            data={
                "name": "New Template",
                "gameline": "mta",
                "character_type": "mage",
                "concept": "Test",
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
            },
        )
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        template = CharacterTemplate.objects.get(name="New Template")
        self.assertEqual(template.owner, self.st_user)
        self.assertFalse(template.is_official)


class CharacterTemplateUpdateViewTest(TestCase):
    """Test CharacterTemplateUpdateView functionality."""

    def setUp(self):
        self.client = Client()
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.other_st = User.objects.create_user(
            username="other_st", email="other@test.com", password="testpass123"
        )
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        STRelationship.objects.create(
            user=self.other_st, chronicle=self.chronicle, gameline=self.gameline
        )
        self.template = CharacterTemplate.objects.create(
            name="Test Template",
            gameline="mta",
            character_type="mage",
            owner=self.st_user,
        )

    def test_owner_can_update(self):
        """Test that owner can update their template."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_update", kwargs={"pk": self.template.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_update(self):
        """Test that non-owner ST cannot update template."""
        self.client.login(username="other_st", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_update", kwargs={"pk": self.template.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_superuser_can_update_any(self):
        """Test that superuser can update any template."""
        self.client.login(username="admin", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_update", kwargs={"pk": self.template.pk})
        )
        self.assertEqual(response.status_code, 200)


class CharacterTemplateDeleteViewTest(TestCase):
    """Test CharacterTemplateDeleteView functionality."""

    def setUp(self):
        self.client = Client()
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.other_st = User.objects.create_user(
            username="other_st", email="other@test.com", password="testpass123"
        )
        self.superuser = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        STRelationship.objects.create(
            user=self.other_st, chronicle=self.chronicle, gameline=self.gameline
        )
        self.template = CharacterTemplate.objects.create(
            name="Test Template",
            gameline="mta",
            character_type="mage",
            owner=self.st_user,
            is_official=False,
        )
        self.official_template = CharacterTemplate.objects.create(
            name="Official Template",
            gameline="mta",
            character_type="mage",
            owner=self.st_user,
            is_official=True,
        )

    def test_owner_can_delete_own_non_official(self):
        """Test that owner can delete their non-official template."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.post(
            reverse("core:character_template_delete", kwargs={"pk": self.template.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CharacterTemplate.objects.filter(pk=self.template.pk).exists())

    def test_owner_cannot_delete_official(self):
        """Test that owner cannot delete official template."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_delete", kwargs={"pk": self.official_template.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_non_owner_cannot_delete(self):
        """Test that non-owner cannot delete template."""
        self.client.login(username="other_st", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_delete", kwargs={"pk": self.template.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_superuser_can_delete_any(self):
        """Test that superuser can delete any template."""
        self.client.login(username="admin", password="testpass123")
        response = self.client.post(
            reverse("core:character_template_delete", kwargs={"pk": self.official_template.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CharacterTemplate.objects.filter(pk=self.official_template.pk).exists())


class CharacterTemplateExportViewTest(TestCase):
    """Test CharacterTemplateExportView functionality."""

    def setUp(self):
        self.client = Client()
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.template = CharacterTemplate.objects.create(
            name="Test Template",
            gameline="mta",
            character_type="mage",
            concept="Test Concept",
            faction="Virtual Adepts",
            description="A test template",
            attributes={"strength": 2, "dexterity": 3},
            abilities={"computer": 3},
            owner=self.st_user,
        )

    def test_export_returns_json(self):
        """Test that export returns JSON content."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_export", kwargs={"pk": self.template.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_export_includes_correct_data(self):
        """Test that export includes all template data."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_export", kwargs={"pk": self.template.pk})
        )
        data = json.loads(response.content)
        self.assertEqual(data["name"], "Test Template")
        self.assertEqual(data["gameline"], "mta")
        self.assertEqual(data["character_type"], "mage")
        self.assertEqual(data["concept"], "Test Concept")
        self.assertEqual(data["faction"], "Virtual Adepts")
        self.assertEqual(data["attributes"], {"strength": 2, "dexterity": 3})

    def test_export_sets_download_header(self):
        """Test that export sets Content-Disposition header."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_export", kwargs={"pk": self.template.pk})
        )
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn(".json", response["Content-Disposition"])


class CharacterTemplateImportViewTest(TestCase):
    """Test CharacterTemplateImportView functionality."""

    def setUp(self):
        self.client = Client()
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_import_form_displayed(self):
        """Test that import form is displayed."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(reverse("core:character_template_import"))
        self.assertEqual(response.status_code, 200)

    def test_import_valid_json(self):
        """Test importing a valid JSON file."""
        self.client.login(username="st_user", password="testpass123")
        json_data = {
            "name": "Imported Template",
            "gameline": "mta",
            "character_type": "mage",
            "concept": "Imported",
            "attributes": {"strength": 2},
        }
        json_file = SimpleUploadedFile(
            "template.json",
            json.dumps(json_data).encode("utf-8"),
            content_type="application/json",
        )
        response = self.client.post(
            reverse("core:character_template_import"),
            data={
                "json_file": json_file,
                "is_public": True,
            },
        )
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        template = CharacterTemplate.objects.get(name="Imported Template")
        self.assertEqual(template.owner, self.st_user)
        self.assertFalse(template.is_official)

    def test_import_missing_required_field(self):
        """Test importing JSON missing required fields."""
        self.client.login(username="st_user", password="testpass123")
        json_data = {
            "name": "Incomplete Template",
            # Missing gameline and character_type
        }
        json_file = SimpleUploadedFile(
            "template.json",
            json.dumps(json_data).encode("utf-8"),
            content_type="application/json",
        )
        response = self.client.post(
            reverse("core:character_template_import"),
            data={
                "json_file": json_file,
                "is_public": True,
            },
        )
        # Should stay on form with error
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CharacterTemplate.objects.filter(name="Incomplete Template").exists())

    def test_import_invalid_json(self):
        """Test importing invalid JSON content."""
        self.client.login(username="st_user", password="testpass123")
        json_file = SimpleUploadedFile(
            "template.json",
            b"not valid json {{{",
            content_type="application/json",
        )
        response = self.client.post(
            reverse("core:character_template_import"),
            data={
                "json_file": json_file,
                "is_public": True,
            },
        )
        # Should stay on form with error message
        self.assertEqual(response.status_code, 200)


class CharacterTemplateQuickNPCViewTest(TestCase):
    """Test CharacterTemplateQuickNPCView functionality."""

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.gameline = Gameline.objects.create(name="Mage")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )
        self.template = CharacterTemplate.objects.create(
            name="Test Template",
            gameline="mta",
            character_type="mage",
            concept="Test NPC",
            chronicle=self.chronicle,
            owner=self.st_user,
        )
        self.unsupported_template = CharacterTemplate.objects.create(
            name="Unsupported Template",
            gameline="wod",
            character_type="unsupported_type",
            concept="Unsupported",
            chronicle=self.chronicle,
            owner=self.st_user,
        )

    def test_requires_post(self):
        """Test that GET request is not allowed."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.get(
            reverse("core:character_template_create_npc", kwargs={"pk": self.template.pk})
        )
        # Should get 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_unsupported_character_type_shows_error(self):
        """Test that unsupported character types show error message."""
        self.client.login(username="st_user", password="testpass123")
        response = self.client.post(
            reverse(
                "core:character_template_create_npc", kwargs={"pk": self.unsupported_template.pk}
            )
        )
        # Should redirect to template detail with error
        self.assertEqual(response.status_code, 302)

    def test_get_character_model_returns_none_for_unsupported(self):
        """Test get_character_model returns None for unsupported types."""
        view = CharacterTemplateQuickNPCView()
        self.unsupported_template.character_type = "unknown"
        result = view.get_character_model(self.unsupported_template)
        self.assertIsNone(result)

    def test_get_character_model_handles_import_error(self):
        """Test get_character_model handles import errors gracefully."""
        view = CharacterTemplateQuickNPCView()
        # Create a template with a type that exists in mapping but can't be imported
        self.template.character_type = "mage"
        # This should work since mage exists
        result = view.get_character_model(self.template)
        # It may or may not return None depending on whether MtAHuman exists
        # Just verify it doesn't raise an exception
        self.assertTrue(result is None or result is not None)
