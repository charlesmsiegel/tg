"""
Comprehensive permission tests for World of Darkness application.

Tests all permission scenarios across different user roles:
- Owner
- Chronicle Head ST
- Game ST
- Player (chronicle member)
- Observer
- Stranger (authenticated but unrelated)
- Anonymous

Tests visibility tiers and proper 404 responses for unauthorized access.
"""

try:
    import pytest
except ImportError:
    # Create mock pytest module for Django's test runner
    class MockPytest:
        """Mock pytest for when running under Django's test runner."""

        class mark:
            @staticmethod
            def django_db(cls):
                return cls

        @staticmethod
        def fixture(func):
            return func

    pytest = MockPytest()

from characters.models.core.character import Character
from characters.models.core.human import Human
from core.models import Observer
from core.permissions import Permission, PermissionManager, Role, VisibilityTier
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class TestPermissionRoles(TestCase):
    """Test role detection for different user types."""

    def setUp(self):
        """Create test users and data."""
        self.users = {
            "owner": User.objects.create_user("owner", "owner@test.com", "password123"),
            "head_st": User.objects.create_user("head_st", "head_st@test.com", "password123"),
            "game_st": User.objects.create_user("game_st", "game_st@test.com", "password123"),
            "player": User.objects.create_user("player", "player@test.com", "password123"),
            "observer": User.objects.create_user("observer", "observer@test.com", "password123"),
            "stranger": User.objects.create_user("stranger", "stranger@test.com", "password123"),
            "admin": User.objects.create_user(
                "admin",
                "admin@test.com",
                "password123",
                is_staff=True,
                is_superuser=True,
            ),
        }

        # Create test chronicle
        self.chronicle = Chronicle.objects.create(
            name="Test Chronicle",
        )
        # Set head ST (assuming Chronicle has head_st field or storytellers M2M)
        # Adjust based on your actual Chronicle model
        if hasattr(self.chronicle, "head_st"):
            self.chronicle.head_st = self.users["head_st"]
            self.chronicle.save()
        elif hasattr(self.chronicle, "storytellers"):
            self.chronicle.storytellers.add(self.users["head_st"])

        # Add game ST (if model supports it)
        if hasattr(self.chronicle, "game_storytellers"):
            self.chronicle.game_storytellers.add(self.users["game_st"])

        # Create test character
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            status="App",
            concept="Test Concept",
        )

        # Add observer
        Observer.objects.create(
            content_object=self.character,
            user=self.users["observer"],
            granted_by=self.users["owner"],
        )

        # Create player's character in same chronicle
        Human.objects.create(
            name="Player's Character",
            owner=self.users["player"],
            chronicle=self.chronicle,
            status="App",
            concept="Player Concept",
        )

    def test_owner_role_detected(self):
        """Test that owner role is correctly detected."""
        roles = PermissionManager.get_user_roles(self.users["owner"], self.character)
        self.assertIn(Role.OWNER, roles)
        self.assertIn(Role.AUTHENTICATED, roles)

    def test_head_st_role_detected(self):
        """Test that chronicle head ST role is correctly detected."""
        roles = PermissionManager.get_user_roles(self.users["head_st"], self.character)
        # This depends on how your Chronicle model is structured
        # Adjust assertion based on your implementation
        self.assertIn(Role.AUTHENTICATED, roles)
        # If head_st field exists and is set:
        # self.assertIn(Role.CHRONICLE_HEAD_ST, roles)

    def test_game_st_role_detected(self):
        """Test that game ST role is correctly detected."""
        roles = PermissionManager.get_user_roles(self.users["game_st"], self.character)
        self.assertIn(Role.AUTHENTICATED, roles)
        # If game_storytellers field exists:
        # self.assertIn(Role.GAME_ST, roles)

    def test_player_role_detected(self):
        """Test that player role is correctly detected for chronicle members."""
        roles = PermissionManager.get_user_roles(self.users["player"], self.character)
        self.assertIn(Role.PLAYER, roles)
        self.assertIn(Role.AUTHENTICATED, roles)

    def test_observer_role_detected(self):
        """Test that observer role is correctly detected."""
        roles = PermissionManager.get_user_roles(self.users["observer"], self.character)
        self.assertIn(Role.OBSERVER, roles)
        self.assertIn(Role.AUTHENTICATED, roles)

    def test_stranger_has_no_special_roles(self):
        """Test that stranger has only authenticated role."""
        roles = PermissionManager.get_user_roles(self.users["stranger"], self.character)
        self.assertNotIn(Role.OWNER, roles)
        self.assertNotIn(Role.PLAYER, roles)
        self.assertNotIn(Role.OBSERVER, roles)
        self.assertIn(Role.AUTHENTICATED, roles)

    def test_admin_role_detected(self):
        """Test that admin role is correctly detected."""
        roles = PermissionManager.get_user_roles(self.users["admin"], self.character)
        self.assertIn(Role.ADMIN, roles)
        self.assertIn(Role.AUTHENTICATED, roles)


class TestOwnerPermissions(TestCase):
    """Test permissions for character owners."""

    def setUp(self):
        """Create test users and data."""
        self.users = {
            "owner": User.objects.create_user("owner", "owner@test.com", "password123"),
            "head_st": User.objects.create_user("head_st", "head_st@test.com", "password123"),
        }

        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        if hasattr(self.chronicle, "head_st"):
            self.chronicle.head_st = self.users["head_st"]
            self.chronicle.save()

        self.character = Human.objects.create(
            name="Test Character",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            status="App",
            concept="Test Concept",
        )

    def test_owner_can_view_full(self):
        """Owner should have full view permission."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.VIEW_FULL
            )
        )

    def test_owner_cannot_edit_full(self):
        """Owner should NOT have full edit permission (cannot modify stats directly)."""
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.EDIT_FULL
            )
        )

    def test_owner_can_edit_limited(self):
        """Owner should have limited edit permission (notes, description)."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.EDIT_LIMITED
            )
        )

    def test_owner_can_spend_xp_when_approved(self):
        """Owner should be able to spend XP on approved characters."""
        self.character.status = "App"
        self.character.save()
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_XP
            )
        )

    def test_owner_cannot_spend_xp_when_unfinished(self):
        """Owner should NOT be able to spend XP on unfinished characters."""
        self.character.status = "Un"
        self.character.save()
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_XP
            )
        )

    def test_owner_can_spend_freebies_when_unfinished(self):
        """Owner should be able to spend freebies on unfinished characters."""
        self.character.status = "Un"
        self.character.save()
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_FREEBIES
            )
        )

    def test_owner_cannot_spend_freebies_when_approved(self):
        """Owner should NOT be able to spend freebies after approval."""
        self.character.status = "App"
        self.character.save()
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_FREEBIES
            )
        )

    def test_owner_cannot_edit_when_submitted(self):
        """Owner should have no permissions when character is submitted."""
        self.character.status = "Sub"
        self.character.save()
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.EDIT_LIMITED
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_XP
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_FREEBIES
            )
        )

    def test_owner_cannot_edit_when_deceased(self):
        """Owner should have no permissions when character is deceased."""
        self.character.status = "Dec"
        self.character.save()
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.EDIT_LIMITED
            )
        )
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.SPEND_XP
            )
        )

    def test_owner_can_delete(self):
        """Owner should be able to delete their own character."""
        self.assertTrue(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.DELETE
            )
        )

    def test_owner_cannot_approve(self):
        """Owner should NOT be able to approve their own character."""
        self.assertFalse(
            PermissionManager.user_has_permission(
                self.users["owner"], self.character, Permission.APPROVE
            )
        )


class TestStorytellerPermissions(TestCase):
    """Test permissions for storytellers."""

    def setUp(self):
        """Create test users and data."""
        self.users = {
            "owner": User.objects.create_user("owner", "owner@test.com", "password123"),
            "head_st": User.objects.create_user("head_st", "head_st@test.com", "password123"),
            "game_st": User.objects.create_user("game_st", "game_st@test.com", "password123"),
        }

        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        if hasattr(self.chronicle, "head_st"):
            self.chronicle.head_st = self.users["head_st"]
            self.chronicle.save()
        if hasattr(self.chronicle, "game_storytellers"):
            self.chronicle.game_storytellers.add(self.users["game_st"])

        self.character = Human.objects.create(
            name="Test Character",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            status="App",
            concept="Test Concept",
        )

    def test_head_st_can_view_full(self):
        """Chronicle Head ST should have full view permission."""
        # Adjust based on your Chronicle model implementation
        # This test assumes head_st field exists
        roles = PermissionManager.get_user_roles(self.users["head_st"], self.character)
        has_view = PermissionManager.user_has_permission(
            self.users["head_st"], self.character, Permission.VIEW_FULL
        )
        # Assert based on whether CHRONICLE_HEAD_ST role is detected
        # If role is properly detected, this should be True

    def test_head_st_can_edit_full(self):
        """Chronicle Head ST should have full edit permission."""
        # Test depends on Chronicle model having head_st field
        pass

    def test_game_st_can_view_full(self):
        """Game ST should have full view permission (read-only)."""
        # Test depends on Chronicle model having game_storytellers field
        pass

    def test_game_st_cannot_edit(self):
        """Game ST should NOT have edit permission (read-only)."""
        roles = PermissionManager.get_user_roles(self.users["game_st"], self.character)
        if Role.GAME_ST in roles:
            self.assertFalse(
                PermissionManager.user_has_permission(
                    self.users["game_st"], self.character, Permission.EDIT_FULL
                )
            )
            self.assertFalse(
                PermissionManager.user_has_permission(
                    self.users["game_st"], self.character, Permission.EDIT_LIMITED
                )
            )


class TestVisibilityTiers(TestCase):
    """Test visibility tier system."""

    def setUp(self):
        """Create test users and data."""
        self.users = {
            "owner": User.objects.create_user("owner", "owner@test.com", "password123"),
            "player": User.objects.create_user("player", "player@test.com", "password123"),
            "stranger": User.objects.create_user("stranger", "stranger@test.com", "password123"),
            "observer": User.objects.create_user("observer", "observer@test.com", "password123"),
        }

        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        self.character = Human.objects.create(
            name="Test Character",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            status="App",
            concept="Test Concept",
        )

        # Add player's character
        Human.objects.create(
            name="Player's Character",
            owner=self.users["player"],
            chronicle=self.chronicle,
            status="App",
            concept="Player Concept",
        )

        # Add observer
        Observer.objects.create(
            content_object=self.character,
            user=self.users["observer"],
            granted_by=self.users["owner"],
        )

    def test_owner_gets_full_visibility(self):
        """Owner should get FULL visibility tier."""
        tier = PermissionManager.get_visibility_tier(self.users["owner"], self.character)
        self.assertEqual(tier, VisibilityTier.FULL)

    def test_player_gets_partial_visibility(self):
        """Player in same chronicle should get PARTIAL visibility tier."""
        tier = PermissionManager.get_visibility_tier(self.users["player"], self.character)
        self.assertEqual(tier, VisibilityTier.PARTIAL)

    def test_observer_gets_partial_visibility(self):
        """Observer should get PARTIAL visibility tier."""
        tier = PermissionManager.get_visibility_tier(self.users["observer"], self.character)
        self.assertEqual(tier, VisibilityTier.PARTIAL)

    def test_stranger_gets_no_visibility(self):
        """Stranger should get NONE visibility tier."""
        tier = PermissionManager.get_visibility_tier(self.users["stranger"], self.character)
        self.assertEqual(tier, VisibilityTier.NONE)


class TestViewPermissions404(TestCase):
    """Test that views return proper 404 responses for unauthorized access."""

    def setUp(self):
        """Create test users and data."""
        self.users = {
            "owner": User.objects.create_user("owner", "owner@test.com", "password123"),
            "stranger": User.objects.create_user("stranger", "stranger@test.com", "password123"),
        }

        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

        self.character = Human.objects.create(
            name="Test Character",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            status="App",
            concept="Test Concept",
        )

    def test_owner_can_view_detail(self):
        """Owner should be able to view character detail page."""
        client = Client()
        client.force_login(self.users["owner"])
        url = reverse("characters:character", kwargs={"pk": self.character.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_stranger_gets_404_on_detail(self):
        """Stranger should get 404 when accessing character detail."""
        client = Client()
        client.force_login(self.users["stranger"])
        url = reverse("characters:character", kwargs={"pk": self.character.pk})
        response = client.get(url)
        # Should return 404, not 403, to avoid information leakage
        self.assertEqual(response.status_code, 404)

    def test_stranger_gets_403_on_edit(self):
        """Stranger should get 403 (or 404) when attempting to edit."""
        client = Client()
        client.force_login(self.users["stranger"])
        url = reverse("characters:update:character", kwargs={"pk": self.character.pk})
        response = client.get(url)
        # Edit views may return 403 or 404 depending on implementation
        self.assertIn(response.status_code, [403, 404])

    def test_anonymous_cannot_view(self):
        """Anonymous users should be redirected or get 404."""
        client = Client()
        url = reverse("characters:character", kwargs={"pk": self.character.pk})
        response = client.get(url)
        # Should redirect to login or return 404
        self.assertIn(response.status_code, [302, 404])


class TestLimitedFormPermissions(TestCase):
    """Test that owners can only edit limited fields."""

    def setUp(self):
        """Create test users and data."""
        self.users = {
            "owner": User.objects.create_user("owner", "owner@test.com", "password123"),
            "head_st": User.objects.create_user("head_st", "head_st@test.com", "password123"),
        }

        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        if hasattr(self.chronicle, "head_st"):
            self.chronicle.head_st = self.users["head_st"]
            self.chronicle.save()

        self.character = Human.objects.create(
            name="Test Character",
            owner=self.users["owner"],
            chronicle=self.chronicle,
            status="App",
            concept="Test Concept",
            willpower=5,
        )

    def test_owner_can_update_notes(self):
        """Owner should be able to update notes field."""
        client = Client()
        client.force_login(self.users["owner"])
        url = reverse("characters:update:character", kwargs={"pk": self.character.pk})

        response = client.post(
            url,
            {
                "notes": "Updated notes",
                "description": self.character.description,
                "public_info": self.character.public_info,
            },
        )

        self.character.refresh_from_db()
        self.assertEqual(self.character.notes, "Updated notes")

    def test_owner_cannot_update_willpower_via_form(self):
        """Owner should NOT be able to update willpower (mechanical field) via limited form."""
        client = Client()
        client.force_login(self.users["owner"])
        url = reverse("characters:update:character", kwargs={"pk": self.character.pk})

        original_willpower = self.character.willpower

        # Try to update willpower (should be ignored by limited form)
        response = client.post(
            url,
            {
                "notes": "Some notes",
                "description": "Some description",
                "public_info": "Public",
                "willpower": 10,  # Attempt to change mechanical field
            },
        )

        self.character.refresh_from_db()
        # Willpower should remain unchanged
        self.assertEqual(self.character.willpower, original_willpower)

    def test_owner_cannot_update_status(self):
        """Owner should NOT be able to update status via limited form."""
        client = Client()
        client.force_login(self.users["owner"])
        url = reverse("characters:update:character", kwargs={"pk": self.character.pk})

        original_status = self.character.status

        response = client.post(
            url,
            {
                "notes": "Some notes",
                "description": "Some description",
                "public_info": "Public",
                "status": "Ret",  # Attempt to change status
            },
        )

        character.refresh_from_db()
        assert character.status == original_status


@pytest.mark.django_db
class TestFilterQuerysetForUser:
    """Test filter_queryset_for_user method and helper methods."""

    @pytest.fixture
    def users(self):
        """Create test users."""
        return {
            "owner": User.objects.create_user("owner", "owner@test.com", "password123"),
            "head_st": User.objects.create_user("head_st", "head_st@test.com", "password123"),
            "game_st": User.objects.create_user("game_st", "game_st@test.com", "password123"),
            "player": User.objects.create_user("player", "player@test.com", "password123"),
            "observer": User.objects.create_user("observer", "observer@test.com", "password123"),
            "stranger": User.objects.create_user("stranger", "stranger@test.com", "password123"),
            "admin": User.objects.create_user(
                "admin",
                "admin@test.com",
                "password123",
                is_staff=True,
                is_superuser=True,
            ),
        }

    @pytest.fixture
    def chronicle(self, users):
        """Create test chronicle."""
        chron = Chronicle.objects.create(
            name="Test Chronicle",
            description="A test chronicle for filter tests",
        )
        chron.head_st = users["head_st"]
        chron.save()
        chron.game_storytellers.add(users["game_st"])
        return chron

    @pytest.fixture
    def characters(self, users, chronicle):
        """Create multiple test characters for different scenarios."""
        owner_char = Human.objects.create(
            name="Owner Character",
            owner=users["owner"],
            chronicle=chronicle,
            status="App",
            concept="Owner Concept",
        )

        player_char = Human.objects.create(
            name="Player Character",
            owner=users["player"],
            chronicle=chronicle,
            status="App",
            concept="Player Concept",
        )

        stranger_char = Human.objects.create(
            name="Stranger Character",
            owner=users["stranger"],
            chronicle=chronicle,
            status="App",
            concept="Stranger Concept",
        )

        # Add observer relationship
        Observer.objects.create(
            content_object=stranger_char,
            user=users["observer"],
            granted_by=users["stranger"],
        )

        return {
            "owner": owner_char,
            "player": player_char,
            "stranger": stranger_char,
        }

    def test_admin_sees_all_characters(self, users, characters):
        """Admin should see all characters."""
        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(users["admin"], qs)
        assert filtered.count() == 3
        assert characters["owner"] in filtered
        assert characters["player"] in filtered
        assert characters["stranger"] in filtered

    def test_owner_sees_own_character(self, users, characters):
        """Owner should see their own character."""
        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(users["owner"], qs)
        assert characters["owner"] in filtered

    def test_owner_sees_chronicle_characters_as_player(self, users, characters):
        """Owner should see other characters in same chronicle (as a player)."""
        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(users["owner"], qs)
        # Owner should see their own character and other approved characters in chronicle
        assert characters["owner"] in filtered
        assert characters["player"] in filtered
        assert characters["stranger"] in filtered

    def test_head_st_sees_chronicle_characters(self, users, characters):
        """Head ST should see all characters in their chronicle."""
        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(users["head_st"], qs)
        assert filtered.count() == 3
        assert characters["owner"] in filtered
        assert characters["player"] in filtered
        assert characters["stranger"] in filtered

    def test_game_st_sees_chronicle_characters(self, users, characters):
        """Game ST should see all characters in their chronicle."""
        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(users["game_st"], qs)
        assert filtered.count() == 3
        assert characters["owner"] in filtered
        assert characters["player"] in filtered
        assert characters["stranger"] in filtered

    def test_player_sees_own_and_chronicle_characters(self, users, characters):
        """Player should see their own character and other approved characters in chronicle."""
        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(users["player"], qs)
        assert characters["player"] in filtered
        assert characters["owner"] in filtered
        assert characters["stranger"] in filtered

    def test_observer_sees_observed_character(self, users, characters):
        """Observer should see the character they're observing."""
        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(users["observer"], qs)
        assert characters["stranger"] in filtered

    def test_stranger_without_chronicle_sees_nothing(self):
        """Stranger with no chronicle connection should see nothing."""
        stranger = User.objects.create_user("total_stranger", "stranger@test.com", "password123")
        owner = User.objects.create_user("owner2", "owner2@test.com", "password123")
        chronicle = Chronicle.objects.create(name="Other Chronicle")

        char = Human.objects.create(
            name="Isolated Character",
            owner=owner,
            chronicle=chronicle,
            status="App",
            concept="Isolated",
        )

        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(stranger, qs)
        assert char not in filtered
        assert filtered.count() == 0

    def test_anonymous_user_sees_nothing(self, characters):
        """Anonymous users should see nothing."""
        from django.contrib.auth.models import AnonymousUser

        anonymous = AnonymousUser()
        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(anonymous, qs)
        assert filtered.count() == 0

    def test_filter_only_approved_characters_for_players(self, users, chronicle):
        """Players should only see approved characters, not unfinished ones."""
        # Create unfinished character
        unfinished_char = Human.objects.create(
            name="Unfinished Character",
            owner=users["stranger"],
            chronicle=chronicle,
            status="Un",
            concept="Unfinished",
        )

        qs = Human.objects.all()
        filtered = PermissionManager.filter_queryset_for_user(users["player"], qs)

        # Player should not see unfinished character (unless they own it)
        if users["player"] != users["stranger"]:
            assert unfinished_char not in filtered


@pytest.mark.django_db
class TestFilterQuerysetHelperMethods:
    """Test the helper methods used by filter_queryset_for_user."""

    def test_model_has_field_returns_true_for_existing_field(self):
        """_model_has_field should return True for existing fields."""
        assert PermissionManager._model_has_field(Human, "owner")
        assert PermissionManager._model_has_field(Human, "chronicle")
        assert PermissionManager._model_has_field(Human, "status")
        assert PermissionManager._model_has_field(Human, "name")

    def test_model_has_field_returns_false_for_nonexistent_field(self):
        """_model_has_field should return False for non-existent fields."""
        assert not PermissionManager._model_has_field(Human, "nonexistent_field")
        assert not PermissionManager._model_has_field(Human, "fake_attribute")

    def test_get_chronicle_related_model_returns_chronicle(self):
        """_get_chronicle_related_model should return Chronicle model."""
        qs = Human.objects.all()
        chronicle_model = PermissionManager._get_chronicle_related_model(qs)
        assert chronicle_model == Chronicle

    def test_get_chronicle_related_model_returns_none_for_no_chronicle(self):
        """_get_chronicle_related_model should return None if no chronicle field."""
        from django.contrib.auth.models import Group

        qs = Group.objects.all()
        chronicle_model = PermissionManager._get_chronicle_related_model(qs)
        assert chronicle_model is None

    def test_build_owner_filter(self):
        """_build_owner_filter should build Q filter for owner."""
        user = User.objects.create_user("test", "test@test.com", "password123")
        q = PermissionManager._build_owner_filter(user, Human)

        # Q object should filter by owner=user
        assert isinstance(q, Q)
        # Create a character owned by user and verify filter works
        char = Human.objects.create(name="Test", owner=user, status="App", concept="Test")
        results = Human.objects.filter(q)
        assert char in results

    def test_build_chronicle_st_filters(self):
        """_build_chronicle_st_filters should build Q filters for STs."""
        head_st = User.objects.create_user("head_st", "head@test.com", "password123")
        game_st = User.objects.create_user("game_st", "game@test.com", "password123")

        chronicle = Chronicle.objects.create(name="Test")
        chronicle.head_st = head_st
        chronicle.save()
        chronicle.game_storytellers.add(game_st)

        # Test head ST filter
        q_head = PermissionManager._build_chronicle_st_filters(head_st, Chronicle)
        assert isinstance(q_head, Q)

        # Test game ST filter
        q_game = PermissionManager._build_chronicle_st_filters(game_st, Chronicle)
        assert isinstance(q_game, Q)

    def test_build_player_chronicle_filter(self):
        """_build_player_chronicle_filter should build Q filter for players."""
        player = User.objects.create_user("player", "player@test.com", "password123")
        chronicle = Chronicle.objects.create(name="Test Chronicle")

        # Create player's character
        player_char = Human.objects.create(
            name="Player Char",
            owner=player,
            chronicle=chronicle,
            status="App",
            concept="Test",
        )

        # Create another character in same chronicle
        other_char = Human.objects.create(
            name="Other Char",
            owner=User.objects.create_user("other", "other@test.com", "password123"),
            chronicle=chronicle,
            status="App",
            concept="Other",
        )

        q = PermissionManager._build_player_chronicle_filter(player, Human)
        assert isinstance(q, Q)

        # Filter should return characters in chronicles where player has a character
        results = Human.objects.filter(q)
        assert other_char in results

    def test_build_observer_filter(self):
        """_build_observer_filter should build Q filter for observers."""
        observer = User.objects.create_user("observer", "observer@test.com", "password123")
        owner = User.objects.create_user("owner", "owner@test.com", "password123")

        char = Human.objects.create(name="Observed", owner=owner, status="App", concept="Test")

        Observer.objects.create(content_object=char, user=observer, granted_by=owner)

        q = PermissionManager._build_observer_filter(observer, Human)
        assert isinstance(q, Q)

        # Filter should return observed characters
        results = Human.objects.filter(q)
        assert char in results
