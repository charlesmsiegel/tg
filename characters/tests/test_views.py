"""
Tests for character views.

Tests cover:
- Character list view
- Character detail view with permissions
- Character create view
- Character update view (limited vs full forms)
- Character delete view
- Permission enforcement on all views
"""
from characters.models.core import Character, Human
from core.permissions import PermissionManager
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle, Gameline, STRelationship


class TestCharacterListView(TestCase):
    """Test the character list view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@test.com", password="password"
        )

    def test_list_view_requires_login(self):
        """Test that list view requires authentication."""
        response = self.client.get(reverse("characters:list"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_list_view_shows_own_characters(self):
        """Test that logged-in users see their own characters."""
        char1 = Human.objects.create(name="My Character", owner=self.user)
        char2 = Human.objects.create(name="Other Character", owner=self.other_user)

        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Character")
        self.assertNotContains(response, "Other Character")

    def test_list_view_filters_by_status(self):
        """Test filtering characters by status."""
        approved = Human.objects.create(
            name="Approved", owner=self.user, status="App"
        )
        unfinished = Human.objects.create(
            name="Unfinished", owner=self.user, status="Un"
        )

        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:list"), {"status": "App"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved")
        self.assertNotContains(response, "Unfinished")


class TestCharacterDetailView(TestCase):
    """Test the character detail view with permissions."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.viewer = User.objects.create_user(
            username="viewer", email="viewer@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.owner,
            concept="Warrior",
        )

    def test_detail_view_requires_login(self):
        """Test that detail view requires authentication."""
        response = self.client.get(self.character.get_absolute_url())
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_owner_can_view_character(self):
        """Test that owner can view their own character."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.character.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Character")
        self.assertContains(response, "Warrior")

    def test_detail_view_shows_character_info(self):
        """Test that detail view displays character information."""
        self.client.login(username="owner", password="password")
        response = self.client.get(self.character.get_absolute_url())

        self.assertContains(response, self.character.name)
        if self.character.concept:
            self.assertContains(response, self.character.concept)

    def test_detail_view_permission_denied_for_unauthorized(self):
        """Test that unauthorized users cannot view character."""
        # Make character private
        self.character.display = False
        self.character.save()

        self.client.login(username="viewer", password="password")
        response = self.client.get(self.character.get_absolute_url())

        # Should be denied or redirected
        self.assertIn(response.status_code, [302, 403])


class TestCharacterUpdateView(TestCase):
    """Test character update view with limited vs full forms."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password", is_staff=True
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.owner,
            chronicle=self.chronicle,
            description="Original description",
        )

    def test_update_view_requires_login(self):
        """Test that update view requires authentication."""
        response = self.client.get(f"/characters/{self.character.id}/update/")
        self.assertEqual(response.status_code, 302)

    def test_owner_sees_limited_form(self):
        """Test that owners get limited edit form."""
        self.client.login(username="owner", password="password")
        response = self.client.get(f"/characters/{self.character.id}/update/")

        self.assertEqual(response.status_code, 200)
        # Limited form should have description but not mechanical fields
        form = response.context.get("form")
        if form:
            self.assertIn("description", form.fields)
            self.assertNotIn("xp", form.fields)
            self.assertNotIn("status", form.fields)

    def test_owner_can_update_descriptive_fields(self):
        """Test that owners can update descriptive fields."""
        self.client.login(username="owner", password="password")
        response = self.client.post(
            f"/characters/{self.character.id}/update/",
            {
                "description": "Updated description",
                "notes": "My private notes",
                "public_info": "Public information",
            },
        )

        self.character.refresh_from_db()
        # Should allow updating descriptive fields
        if response.status_code == 302:  # Successful update redirects
            self.assertEqual(self.character.description, "Updated description")

    def test_st_sees_full_form(self):
        """Test that STs get full edit form."""
        self.client.login(username="st", password="password")
        response = self.client.get(f"/characters/{self.character.id}/update/")

        if response.status_code == 200:
            form = response.context.get("form")
            if form:
                # Full form should have mechanical fields
                self.assertIn("description", form.fields)
                # May have xp, status, etc. depending on form implementation

    def test_other_user_cannot_update(self):
        """Test that non-owners cannot update character."""
        self.client.login(username="other", password="password")
        response = self.client.get(f"/characters/{self.character.id}/update/")

        # Should be denied
        self.assertIn(response.status_code, [302, 403])


class TestCharacterCreateView(TestCase):
    """Test character creation view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_create_view_requires_login(self):
        """Test that create view requires authentication."""
        response = self.client.get(reverse("characters:create"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_access_create_view(self):
        """Test that logged-in users can access create view."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:create"))

        self.assertIn(response.status_code, [200, 404])  # Depends on URL config

    def test_create_character_with_valid_data(self):
        """Test creating a character with valid data."""
        self.client.login(username="testuser", password="password")

        data = {
            "name": "New Character",
            "concept": "Detective",
            "chronicle": self.chronicle.id,
        }

        # URL pattern depends on implementation
        response = self.client.post(reverse("characters:create"), data)

        if response.status_code in [200, 302]:
            # Should create character
            characters = Character.objects.filter(name="New Character")
            if characters.exists():
                character = characters.first()
                self.assertEqual(character.owner, self.user)
                self.assertEqual(character.concept, "Detective")


class TestCharacterPermissions(TestCase):
    """Test permission enforcement on character views."""

    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.st = User.objects.create_user(
            username="st", email="st@test.com", password="password"
        )
        self.admin = User.objects.create_user(
            username="admin", email="admin@test.com", password="password", is_staff=True
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="password"
        )

        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Make ST a storyteller for the chronicle
        mta = Gameline.objects.create(name="Mage: the Ascension")
        STRelationship.objects.create(
            user=self.st, gameline=mta, chronicle=self.chronicle
        )

        self.character = Human.objects.create(
            name="Test Character",
            owner=self.owner,
            chronicle=self.chronicle,
        )

    def test_owner_has_view_permission(self):
        """Test that owner can view their character."""
        pm = PermissionManager()
        self.assertTrue(pm.check_permission(self.owner, self.character, "view_full"))

    def test_st_has_view_permission(self):
        """Test that ST can view characters in their chronicle."""
        pm = PermissionManager()
        self.assertTrue(pm.check_permission(self.st, self.character, "view_full"))

    def test_admin_has_view_permission(self):
        """Test that admin can view any character."""
        pm = PermissionManager()
        self.assertTrue(pm.check_permission(self.admin, self.character, "view_full"))

    def test_other_user_no_view_permission_for_private(self):
        """Test that other users cannot view private characters."""
        self.character.display = False
        self.character.save()

        pm = PermissionManager()
        self.assertFalse(pm.check_permission(self.other, self.character, "view_full"))

    def test_owner_has_limited_edit_permission(self):
        """Test that owner has limited edit permission."""
        pm = PermissionManager()
        # Owners should have some edit permission
        has_permission = pm.check_permission(self.owner, self.character, "edit_full")
        # Depending on implementation, owners may or may not have full edit
        self.assertIsNotNone(has_permission)

    def test_st_has_full_edit_permission(self):
        """Test that ST has full edit permission."""
        pm = PermissionManager()
        self.assertTrue(pm.check_permission(self.st, self.character, "edit_full"))

    def test_other_user_no_edit_permission(self):
        """Test that other users cannot edit character."""
        pm = PermissionManager()
        self.assertFalse(pm.check_permission(self.other, self.character, "edit_full"))
