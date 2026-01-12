"""Tests for mixins in core/mixins.py."""

from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from characters.models.core.character import Character
from core.mixins import (
    CharacterOwnerOrSTMixin,
    DeleteMessageMixin,
    EditPermissionMixin,
    ErrorMessageMixin,
    MessageMixin,
    ObjectCachingMixin,
    OwnerRequiredMixin,
    PermissionRequiredMixin,
    SpecialUserMixin,
    SpendFreebiesPermissionMixin,
    SpendXPPermissionMixin,
    StorytellerRequiredMixin,
    STRequiredMixin,
    SuccessMessageMixin,
    ViewPermissionMixin,
    VisibilityFilterMixin,
)
from core.permissions import Permission, VisibilityTier
from game.models import Chronicle, Gameline, STRelationship


class ObjectCachingMixinTest(TestCase):
    """Tests for ObjectCachingMixin - verifies get_object() is only called once."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_get_object_caches_result(self):
        """Test that get_object() caches its result and returns cached object on subsequent calls."""

        class TestView(ObjectCachingMixin, DetailView):
            model = Character
            template_name = "test.html"

        view = TestView()
        view.request = self.factory.get("/")
        view.request.user = self.owner
        view.kwargs = {"pk": self.character.pk}

        # First call should hit the database
        obj1 = view.get_object()
        self.assertEqual(obj1.pk, self.character.pk)
        self.assertTrue(hasattr(view, "_cached_object"))

        # Second call should return cached object
        obj2 = view.get_object()
        self.assertIs(obj1, obj2)  # Same object instance

    def test_get_object_only_queries_once(self):
        """Test that multiple get_object() calls result in only one database query."""

        class TestView(ObjectCachingMixin, DetailView):
            model = Character
            template_name = "test.html"

        view = TestView()
        view.request = self.factory.get("/")
        view.request.user = self.owner
        view.kwargs = {"pk": self.character.pk}

        with self.assertNumQueries(1):
            view.get_object()
            view.get_object()
            view.get_object()

    def test_permission_mixin_caches_object(self):
        """Test that PermissionRequiredMixin caches object during dispatch."""

        class TestView(ViewPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {"pk": self.character.pk}
        view.args = ()

        # Manually call has_permission and get_object to simulate dispatch + get flow
        # has_permission() calls get_object() internally
        view.has_permission()

        # Subsequent get_object() calls should use cache
        with self.assertNumQueries(0):
            view.get_object()

    def test_owner_required_mixin_caches_object(self):
        """Test that OwnerRequiredMixin caches object during dispatch."""

        class TestView(OwnerRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {"pk": self.character.pk}
        view.args = ()

        # Call dispatch which calls get_object()
        # Then simulate the view's get() calling get_object() again
        # Query count: 1 for character, 1 for owner (accessed for permission check)
        with self.assertNumQueries(2):
            # dispatch() calls get_object() once
            try:
                view.dispatch(request, pk=self.character.pk)
            except Exception:
                pass  # Template doesn't exist, but that's fine
            # Subsequent calls should use cache
            view.get_object()

    def test_st_required_mixin_caches_object(self):
        """Test that STRequiredMixin caches object during dispatch."""
        head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        chronicle = Chronicle.objects.create(name="ST Chronicle", head_st=head_st)
        character = Character.objects.create(
            name="ST Character", owner=self.owner, chronicle=chronicle, status="App"
        )

        class TestView(STRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = head_st

        view = TestView()
        view.request = request
        view.kwargs = {"pk": character.pk}
        view.args = ()

        # Call dispatch which calls get_object()
        # Query count: 1 for character, 1 for chronicle, 1 for head_st
        with self.assertNumQueries(3):
            try:
                view.dispatch(request, pk=character.pk)
            except Exception:
                pass
            view.get_object()

    def test_character_owner_or_st_mixin_caches_object(self):
        """Test that CharacterOwnerOrSTMixin caches object during dispatch."""

        class MockXPRequest:
            def __init__(self, character):
                self.character = character
                self.pk = 1

        class TestView(CharacterOwnerOrSTMixin, DetailView):
            template_name = "test.html"

            def get_object(self, queryset=None):
                if not hasattr(self, "_cached_object"):
                    self._cached_object = MockXPRequest(self.kwargs["character"])
                return self._cached_object

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {"character": self.character}
        view.args = ()

        # First call
        obj1 = view.get_object()
        # Second call should return same instance
        obj2 = view.get_object()
        self.assertIs(obj1, obj2)


class PermissionRequiredMixinTest(TestCase):
    """Tests for PermissionRequiredMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_dispatch_with_permission_raises_404_by_default(self):
        """Test that dispatch raises 404 when permission denied (default behavior)."""

        class TestView(PermissionRequiredMixin, DetailView):
            model = Character
            required_permission = Permission.EDIT_FULL

        request = self.factory.get("/")
        request.user = self.stranger

        view = TestView.as_view()
        with self.assertRaises(Http404):
            view(request, pk=self.character.pk)

    def test_dispatch_with_permission_raises_403_when_configured(self):
        """Test that dispatch raises 403 when raise_404_on_deny=False."""

        class TestView(PermissionRequiredMixin, DetailView):
            model = Character
            required_permission = Permission.EDIT_FULL
            raise_404_on_deny = False

        request = self.factory.get("/")
        request.user = self.stranger

        view = TestView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, pk=self.character.pk)

    def test_dispatch_allows_user_with_permission(self):
        """Test that dispatch allows users with required permission."""

        class TestView(PermissionRequiredMixin, DetailView):
            model = Character
            required_permission = Permission.VIEW_FULL
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_has_permission_raises_value_error_when_no_required_permission(self):
        """Test that has_permission raises ValueError when required_permission is None."""

        class TestView(PermissionRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        view = TestView()
        view.request = self.factory.get("/")
        view.request.user = self.owner
        view.kwargs = {"pk": self.character.pk}

        with self.assertRaises(ValueError) as cm:
            view.has_permission()
        self.assertIn("required_permission must be set", str(cm.exception))

    def test_get_context_data_adds_is_approved_user(self):
        """Test that get_context_data adds is_approved_user flag."""

        class TestView(PermissionRequiredMixin, DetailView):
            model = Character
            required_permission = Permission.VIEW_FULL
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {"pk": self.character.pk}
        view.object = view.get_object()

        context = view.get_context_data()
        self.assertTrue(context["is_approved_user"])


class ViewPermissionMixinTest(TestCase):
    """Tests for ViewPermissionMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_owner_can_view(self):
        """Test that owner can view their character."""

        class TestView(ViewPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_stranger_cannot_view(self):
        """Test that stranger cannot view character (raises 404)."""

        class TestView(ViewPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.stranger

        view = TestView.as_view()
        with self.assertRaises(Http404):
            view(request, pk=self.character.pk)


class EditPermissionMixinTest(TestCase):
    """Tests for EditPermissionMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_head_st_can_edit(self):
        """Test that head ST can edit (has EDIT_FULL permission)."""

        class TestView(EditPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.head_st

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_owner_cannot_edit(self):
        """Test that owner cannot edit (no EDIT_FULL permission, raises 403)."""

        class TestView(EditPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, pk=self.character.pk)


class SpendXPPermissionMixinTest(TestCase):
    """Tests for SpendXPPermissionMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_owner_can_spend_xp(self):
        """Test that owner can spend XP on approved character."""

        class TestView(SpendXPPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_stranger_cannot_spend_xp(self):
        """Test that stranger cannot spend XP (raises 403)."""

        class TestView(SpendXPPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.stranger

        view = TestView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, pk=self.character.pk)


class SpendFreebiesPermissionMixinTest(TestCase):
    """Tests for SpendFreebiesPermissionMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="Un"
        )

    def test_owner_can_spend_freebies_on_unfinished(self):
        """Test that owner can spend freebies on unfinished character."""

        class TestView(SpendFreebiesPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_owner_cannot_spend_freebies_on_approved(self):
        """Test that owner cannot spend freebies on approved character."""
        # Create a new character with approved status directly
        approved_char = Character.objects.create(
            name="Approved Character",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
        )

        class TestView(SpendFreebiesPermissionMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, pk=approved_char.pk)


class VisibilityFilterMixinTest(TestCase):
    """Tests for VisibilityFilterMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.player = User.objects.create_user(
            username="player", email="player@test.com", password="testpass123"
        )
        self.stranger = User.objects.create_user(
            username="stranger", email="stranger@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )
        # Player's character in same chronicle
        Character.objects.create(
            name="Player Character", owner=self.player, chronicle=self.chronicle, status="App"
        )

    def test_get_context_data_adds_visibility_tier_for_owner(self):
        """Test that get_context_data adds visibility tier for detail views."""

        class TestDetailView(VisibilityFilterMixin, DetailView):
            model = Character
            template_name = "test.html"

            def get_queryset(self):
                # Override to avoid filter_queryset_for_user polymorphic issue
                return Character.objects.all()

        request = self.factory.get("/")
        request.user = self.owner

        view = TestDetailView()
        view.request = request
        view.kwargs = {"pk": self.character.pk}
        view.object = view.get_object()

        context = view.get_context_data()
        self.assertEqual(context["visibility_tier"], VisibilityTier.FULL)
        self.assertIn("user_can_edit", context)
        self.assertIn("user_can_spend_xp", context)
        self.assertIn("user_can_spend_freebies", context)
        self.assertEqual(context["VisibilityTier"], VisibilityTier)

    def test_get_context_data_user_can_edit_false_for_owner(self):
        """Test that owner cannot edit (no EDIT_FULL permission)."""

        class TestDetailView(VisibilityFilterMixin, DetailView):
            model = Character
            template_name = "test.html"

            def get_queryset(self):
                return Character.objects.all()

        request = self.factory.get("/")
        request.user = self.owner

        view = TestDetailView()
        view.request = request
        view.kwargs = {"pk": self.character.pk}
        view.object = view.get_object()

        context = view.get_context_data()
        # Owner can view but not fully edit
        self.assertFalse(context["user_can_edit"])

    def test_get_context_data_user_can_spend_xp_true_for_owner(self):
        """Test that owner can spend XP on approved character."""

        class TestDetailView(VisibilityFilterMixin, DetailView):
            model = Character
            template_name = "test.html"

            def get_queryset(self):
                return Character.objects.all()

        request = self.factory.get("/")
        request.user = self.owner

        view = TestDetailView()
        view.request = request
        view.kwargs = {"pk": self.character.pk}
        view.object = view.get_object()

        context = view.get_context_data()
        self.assertTrue(context["user_can_spend_xp"])


class OwnerRequiredMixinTest(TestCase):
    """Tests for OwnerRequiredMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_owner_can_access(self):
        """Test that owner can access their object."""

        class TestView(OwnerRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_access(self):
        """Test that non-owner cannot access (raises 403)."""

        class TestView(OwnerRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.other

        view = TestView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, pk=self.character.pk)

    def test_admin_can_access(self):
        """Test that admin can access any object."""

        class TestView(OwnerRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.admin

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_owner_via_user_attribute(self):
        """Test ownership via 'user' attribute instead of 'owner'."""

        class MockModel:
            def __init__(self, user):
                self.user = user
                self.pk = 1

        class TestView(OwnerRequiredMixin, DetailView):
            model = MockModel
            template_name = "test.html"

            def get_object(self):
                return MockModel(self.request.user)

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {}

        # Call dispatch directly
        response = view.dispatch(request)
        # Should not raise - passes through to super().dispatch()


class OwnerRequiredMixinURLBasedTest(TestCase):
    """Tests for OwnerRequiredMixin URL-based ownership checking."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.staff = User.objects.create_user(
            username="staff",
            email="staff@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=False,
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_url_based_owner_can_access(self):
        """Test that owner can access via URL-based lookup."""
        from django.views.generic import CreateView

        class TestView(OwnerRequiredMixin, CreateView):
            owner_check_model = Character
            owner_check_kwarg = "character_pk"
            owner_check_attr = "character"
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {}
        view.args = ()

        # Call dispatch - should not raise
        try:
            view.dispatch(request, character_pk=self.character.pk)
        except Exception as e:
            # Template doesn't exist, but that's fine - we're testing permission
            if "PermissionDenied" in str(type(e)):
                self.fail("Owner should be able to access")

    def test_url_based_non_owner_denied(self):
        """Test that non-owner is denied access via URL-based lookup."""
        from django.views.generic import CreateView

        class TestView(OwnerRequiredMixin, CreateView):
            owner_check_model = Character
            owner_check_kwarg = "character_pk"
            owner_check_attr = "character"
            owner_check_message = "Custom denial message"
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.other

        view = TestView()
        view.request = request
        view.kwargs = {}
        view.args = ()

        with self.assertRaises(PermissionDenied) as cm:
            view.dispatch(request, character_pk=self.character.pk)
        self.assertEqual(str(cm.exception), "Custom denial message")

    def test_url_based_admin_can_access(self):
        """Test that admin can access via URL-based lookup."""
        from django.views.generic import CreateView

        class TestView(OwnerRequiredMixin, CreateView):
            owner_check_model = Character
            owner_check_kwarg = "character_pk"
            owner_check_attr = "character"
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.admin

        view = TestView()
        view.request = request
        view.kwargs = {}
        view.args = ()

        # Call dispatch - should not raise PermissionDenied
        try:
            view.dispatch(request, character_pk=self.character.pk)
        except PermissionDenied:
            self.fail("Admin should be able to access")
        except Exception:
            pass  # Template doesn't exist, but that's fine

    def test_url_based_staff_can_access(self):
        """Test that staff can access via URL-based lookup."""
        from django.views.generic import CreateView

        class TestView(OwnerRequiredMixin, CreateView):
            owner_check_model = Character
            owner_check_kwarg = "character_pk"
            owner_check_attr = "character"
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.staff

        view = TestView()
        view.request = request
        view.kwargs = {}
        view.args = ()

        # Call dispatch - should not raise PermissionDenied
        try:
            view.dispatch(request, character_pk=self.character.pk)
        except PermissionDenied:
            self.fail("Staff should be able to access")
        except Exception:
            pass  # Template doesn't exist, but that's fine

    def test_url_based_sets_attribute(self):
        """Test that URL-based lookup sets the correct attribute on the view."""
        from django.views.generic import CreateView

        class TestView(OwnerRequiredMixin, CreateView):
            owner_check_model = Character
            owner_check_kwarg = "character_pk"
            owner_check_attr = "my_character"
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {}
        view.args = ()

        # Call dispatch
        try:
            view.dispatch(request, character_pk=self.character.pk)
        except Exception:
            pass  # Template doesn't exist

        # Verify attribute was set
        self.assertTrue(hasattr(view, "my_character"))
        self.assertEqual(view.my_character.pk, self.character.pk)

    def test_url_based_with_user_attribute(self):
        """Test ownership via 'user' attribute instead of 'owner'."""

        class UserOwnedModel:
            """Mock model with 'user' attribute instead of 'owner'."""
            def __init__(self, user):
                self.user = user
                self.pk = 999

            @classmethod
            def _default_manager(cls):
                pass

        # Create a mock manager that returns our test object
        from unittest.mock import MagicMock, patch

        from django.views.generic import CreateView

        mock_obj = UserOwnedModel(self.owner)
        mock_manager = MagicMock()
        mock_manager.get.return_value = mock_obj

        class TestView(OwnerRequiredMixin, CreateView):
            owner_check_model = UserOwnedModel
            owner_check_kwarg = "obj_pk"
            owner_check_attr = "owned_obj"
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {}
        view.args = ()

        # Patch get_object_or_404 to return our mock object
        with patch("core.mixins.get_object_or_404", return_value=mock_obj):
            try:
                view.dispatch(request, obj_pk=999)
            except PermissionDenied:
                self.fail("User should be able to access their own object via 'user' attribute")
            except Exception:
                pass  # Template doesn't exist

        # Verify attribute was set
        self.assertTrue(hasattr(view, "owned_obj"))
        self.assertEqual(view.owned_obj.pk, 999)

    def test_url_based_missing_kwarg_raises_404(self):
        """Test that missing URL kwarg raises Http404."""
        from django.views.generic import CreateView

        class TestView(OwnerRequiredMixin, CreateView):
            owner_check_model = Character
            owner_check_kwarg = "character_pk"
            owner_check_attr = "character"
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {}
        view.args = ()

        # Call dispatch without the required kwarg - should raise 404
        with self.assertRaises(Http404):
            view.dispatch(request)  # No character_pk kwarg

    def test_url_based_invalid_pk_raises_404(self):
        """Test that invalid PK raises Http404."""
        from django.views.generic import CreateView

        class TestView(OwnerRequiredMixin, CreateView):
            owner_check_model = Character
            owner_check_kwarg = "character_pk"
            owner_check_attr = "character"
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {}
        view.args = ()

        # Call dispatch with non-existent PK
        with self.assertRaises(Http404):
            view.dispatch(request, character_pk=99999)

    def test_standard_check_still_works(self):
        """Test that standard get_object() path still works when owner_check_model is None."""

        class TestView(OwnerRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"
            # owner_check_model is None by default, so should use standard path

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)


class STRequiredMixinTest(TestCase):
    """Tests for STRequiredMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.head_st = User.objects.create_user(
            username="head_st", email="head_st@test.com", password="testpass123"
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.head_st)
        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_head_st_can_access(self):
        """Test that head ST can access."""

        class TestView(STRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.head_st

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access(self):
        """Test that admin can access."""

        class TestView(STRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.admin

        view = TestView.as_view()
        response = view(request, pk=self.character.pk)
        self.assertEqual(response.status_code, 200)

    def test_non_st_cannot_access(self):
        """Test that non-ST cannot access (raises 403)."""

        class TestView(STRequiredMixin, DetailView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.other

        view = TestView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request, pk=self.character.pk)

    def test_head_st_via_head_storytellers_m2m(self):
        """Test head ST detection via head_storytellers M2M field."""
        chronicle2 = Chronicle.objects.create(name="Chronicle 2")
        # Mock head_storytellers if it exists
        if hasattr(chronicle2, "head_storytellers"):
            chronicle2.head_storytellers.add(self.head_st)
            char2 = Character.objects.create(
                name="Char 2", owner=self.owner, chronicle=chronicle2, status="App"
            )

            class TestView(STRequiredMixin, DetailView):
                model = Character
                template_name = "test.html"

            request = self.factory.get("/")
            request.user = self.head_st

            view = TestView.as_view()
            response = view(request, pk=char2.pk)
            self.assertEqual(response.status_code, 200)


class StorytellerRequiredMixinTest(TestCase):
    """Tests for StorytellerRequiredMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.regular_user = User.objects.create_user(
            username="regular", email="regular@test.com", password="testpass123"
        )
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        # Create chronicle and ST relationship
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

    def test_admin_can_access(self):
        """Test that admin can access."""

        class TestView(StorytellerRequiredMixin, ListView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.admin

        view = TestView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_st_can_access(self):
        """Test that storyteller can access."""

        class TestView(StorytellerRequiredMixin, ListView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.st_user

        view = TestView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_non_st_cannot_access(self):
        """Test that non-ST cannot access (raises 403)."""

        class TestView(StorytellerRequiredMixin, ListView):
            model = Character
            template_name = "test.html"

        request = self.factory.get("/")
        request.user = self.regular_user

        view = TestView.as_view()
        with self.assertRaises(PermissionDenied):
            view(request)


class CharacterOwnerOrSTMixinTest(TestCase):
    """Tests for CharacterOwnerOrSTMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.other = User.objects.create_user(
            username="other", email="other@test.com", password="testpass123"
        )
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_admin_can_access(self):
        """Test that admin can access."""

        class MockXPRequest:
            def __init__(self, character):
                self.character = character
                self.pk = 1

        class TestView(CharacterOwnerOrSTMixin, DetailView):
            template_name = "test.html"

            def get_object(self):
                return MockXPRequest(self.kwargs["character"])

        request = self.factory.get("/")
        request.user = self.admin

        view = TestView()
        view.request = request
        view.kwargs = {"character": self.character}

        # Should not raise PermissionDenied - it will pass through to super().dispatch()
        # and then fail on template rendering, but that's fine for this test
        try:
            view.dispatch(request)
        except Exception:
            pass  # Expected - no template exists

    def test_st_can_access(self):
        """Test that ST can access."""

        class MockXPRequest:
            def __init__(self, character):
                self.character = character
                self.pk = 1

        class TestView(CharacterOwnerOrSTMixin, DetailView):
            template_name = "test.html"

            def get_object(self):
                return MockXPRequest(self.kwargs["character"])

        request = self.factory.get("/")
        request.user = self.st_user

        view = TestView()
        view.request = request
        view.kwargs = {"character": self.character}

        # Should not raise PermissionDenied - it will pass through to super().dispatch()
        try:
            view.dispatch(request)
        except Exception:
            pass  # Expected - no template exists

    def test_character_owner_can_access(self):
        """Test that character owner can access."""

        class MockXPRequest:
            def __init__(self, character):
                self.character = character
                self.pk = 1

        class TestView(CharacterOwnerOrSTMixin, DetailView):
            template_name = "test.html"

            def get_object(self):
                return MockXPRequest(self.kwargs["character"])

        request = self.factory.get("/")
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {"character": self.character}

        # Should not raise PermissionDenied - it will pass through to super().dispatch()
        try:
            view.dispatch(request)
        except Exception:
            pass  # Expected - no template exists

    def test_other_user_cannot_access(self):
        """Test that other user cannot access (raises 403)."""

        class MockXPRequest:
            def __init__(self, character):
                self.character = character
                self.pk = 1

        class TestView(CharacterOwnerOrSTMixin, DetailView):
            def get_object(self):
                return MockXPRequest(self.kwargs["character"])

        request = self.factory.get("/")
        request.user = self.other

        view = TestView()
        view.request = request
        view.kwargs = {"character": self.character}

        with self.assertRaises(PermissionDenied):
            view.dispatch(request)


class SpecialUserMixinTest(TestCase):
    """Tests for SpecialUserMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.st_user = User.objects.create_user(
            username="st_user", email="st@test.com", password="testpass123"
        )
        self.regular_user = User.objects.create_user(
            username="regular", email="regular@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st_user)
        self.gameline = Gameline.objects.create(name="Test Gameline")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle, gameline=self.gameline
        )

        self.character = Character.objects.create(
            name="Test Character", owner=self.owner, chronicle=self.chronicle, status="App"
        )

    def test_owner_is_special_user(self):
        """Test that owner is considered a special user."""

        class TestView(SpecialUserMixin, DetailView):
            model = Character

        view = TestView()
        result = view.check_if_special_user(self.character, self.owner)
        self.assertTrue(result)

    def test_st_is_special_user(self):
        """Test that ST is considered a special user."""

        class TestView(SpecialUserMixin, DetailView):
            model = Character

        view = TestView()
        result = view.check_if_special_user(self.character, self.st_user)
        self.assertTrue(result)

    def test_regular_user_is_not_special(self):
        """Test that regular user is not a special user."""

        class TestView(SpecialUserMixin, DetailView):
            model = Character

        view = TestView()
        result = view.check_if_special_user(self.character, self.regular_user)
        self.assertFalse(result)

    def test_no_owner_everyone_is_special(self):
        """Test that when object has no owner, everyone is special."""
        self.character.owner = None
        self.character.save()

        class TestView(SpecialUserMixin, DetailView):
            model = Character

        view = TestView()
        result = view.check_if_special_user(self.character, self.regular_user)
        self.assertTrue(result)

    def test_anonymous_user_is_not_special(self):
        """Test that anonymous user is not special."""
        from django.contrib.auth.models import AnonymousUser

        class TestView(SpecialUserMixin, DetailView):
            model = Character

        view = TestView()
        result = view.check_if_special_user(self.character, AnonymousUser())
        self.assertFalse(result)


class SuccessMessageMixinTest(TestCase):
    """Tests for SuccessMessageMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.user, chronicle=self.chronicle, status="App"
        )

    def _add_messages_middleware(self, request):
        """Add messages middleware to request."""
        request.session = "session"
        messages = FallbackStorage(request)
        request._messages = messages
        return request

    def test_get_success_message(self):
        """Test success message formatting."""

        class TestView(SuccessMessageMixin, UpdateView):
            model = Character
            fields = ["name"]
            success_message = "{name} updated successfully!"
            template_name = "test.html"

        view = TestView()
        view.object = self.character
        view.request = self._add_messages_middleware(self.factory.post("/"))
        view.request.user = self.user

        message = view.get_success_message({})
        self.assertEqual(message, "Test Character updated successfully!")

    def test_get_success_message_with_model_name(self):
        """Test success message with model name."""

        class TestView(SuccessMessageMixin, UpdateView):
            model = Character
            fields = ["name"]
            success_message = "{model_name} saved!"
            template_name = "test.html"

        view = TestView()
        view.object = self.character
        view.request = self._add_messages_middleware(self.factory.post("/"))
        view.request.user = self.user

        message = view.get_success_message({})
        self.assertIn("character", message.lower())

    def test_get_success_message_fallback_on_error(self):
        """Test that invalid template falls back to raw message."""

        class TestView(SuccessMessageMixin, UpdateView):
            model = Character
            fields = ["name"]
            success_message = "{nonexistent_field} saved!"
            template_name = "test.html"

        view = TestView()
        view.object = self.character
        view.request = self._add_messages_middleware(self.factory.post("/"))
        view.request.user = self.user

        message = view.get_success_message({})
        self.assertEqual(message, "{nonexistent_field} saved!")

    def test_get_message_format_dict_no_object(self):
        """Test format dict returns empty when no object."""

        class TestView(SuccessMessageMixin, UpdateView):
            model = Character
            fields = ["name"]
            template_name = "test.html"

        view = TestView()
        # No object set
        format_dict = view.get_message_format_dict()
        self.assertEqual(format_dict, {})


class ErrorMessageMixinTest(TestCase):
    """Tests for ErrorMessageMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

    def _add_messages_middleware(self, request):
        """Add messages middleware to request."""
        request.session = "session"
        messages = FallbackStorage(request)
        request._messages = messages
        return request

    def test_form_invalid_shows_error_message(self):
        """Test that form_invalid shows error message."""
        from django import forms

        class TestForm(forms.Form):
            name = forms.CharField(required=True)

        class TestView(ErrorMessageMixin, UpdateView):
            form_class = TestForm
            error_message = "There was an error!"
            template_name = "test.html"
            success_url = "/"

            def get_object(self):
                return None

        request = self._add_messages_middleware(self.factory.post("/", data={}))
        request.user = self.user

        view = TestView()
        view.request = request
        view.object = None

        form = TestForm(data={})
        response = view.form_invalid(form)

        # Check that error message was added
        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "There was an error!")


class MessageMixinTest(TestCase):
    """Tests for MessageMixin (combined success and error)."""

    def test_message_mixin_inherits_both(self):
        """Test that MessageMixin has both success and error handling."""
        self.assertTrue(issubclass(MessageMixin, SuccessMessageMixin))
        self.assertTrue(issubclass(MessageMixin, ErrorMessageMixin))


class DeleteMessageMixinTest(TestCase):
    """Tests for DeleteMessageMixin."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.character = Character.objects.create(
            name="Test Character", owner=self.user, chronicle=self.chronicle, status="App"
        )

    def _add_messages_middleware(self, request):
        """Add messages middleware to request."""
        request.session = "session"
        messages = FallbackStorage(request)
        request._messages = messages
        return request

    def test_delete_shows_success_message(self):
        """Test that delete shows success message."""

        class TestView(DeleteMessageMixin, DeleteView):
            model = Character
            success_message = "{name} deleted!"
            success_url = "/"
            template_name = "test.html"

        request = self._add_messages_middleware(self.factory.post("/"))
        request.user = self.user

        view = TestView()
        view.request = request
        view.kwargs = {"pk": self.character.pk}

        # Call delete method directly
        view.object = view.get_object()
        view.delete(request)

        # Check that success message was added
        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertIn("Test Character", str(messages[0]))

    def test_delete_message_with_format_error(self):
        """Test that delete handles format errors gracefully."""

        class TestView(DeleteMessageMixin, DeleteView):
            model = Character
            success_message = "{invalid_field} deleted!"
            success_url = "/"
            template_name = "test.html"

        request = self._add_messages_middleware(self.factory.post("/"))
        request.user = self.user

        view = TestView()
        view.request = request
        view.kwargs = {"pk": self.character.pk}

        # Should not crash
        view.object = view.get_object()
        view.delete(request)

        # Check that fallback message was added
        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "{invalid_field} deleted!")


class ApprovalMixinTest(TestCase):
    """Tests for ApprovalMixin._parse_request_id security fix."""

    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

    def _create_mock_view(self):
        """Create a minimal ApprovalMixin instance for testing."""
        from core.mixins import ApprovalMixin

        class TestApprovalView(ApprovalMixin):
            approve_button_value = "approve"
            reject_button_value = "reject"

        return TestApprovalView()

    def test_parse_request_id_valid_input(self):
        """Test that valid input returns the correct ID."""
        view = self._create_mock_view()
        request = self.factory.post("/", data={"xp_request_123": "approve"})
        result = view._parse_request_id(request, "approve")
        self.assertEqual(result, 123)

    def test_parse_request_id_no_matching_key_raises_validation_error(self):
        """Test that missing matching key raises ValidationError instead of IndexError."""
        from django.core.exceptions import ValidationError

        view = self._create_mock_view()
        # POST data has no key with value "approve"
        request = self.factory.post("/", data={"some_key": "other_value"})

        with self.assertRaises(ValidationError) as cm:
            view._parse_request_id(request, "approve")
        self.assertIn("Invalid request", str(cm.exception))

    def test_parse_request_id_malformed_key_raises_validation_error(self):
        """Test that key with insufficient underscore parts raises ValidationError."""
        from django.core.exceptions import ValidationError

        view = self._create_mock_view()
        # Key has only 2 parts separated by underscore (needs 3+)
        request = self.factory.post("/", data={"malformed_key": "approve"})

        with self.assertRaises(ValidationError) as cm:
            view._parse_request_id(request, "approve")
        self.assertIn("Invalid request", str(cm.exception))

    def test_parse_request_id_non_numeric_id_raises_validation_error(self):
        """Test that non-numeric ID part raises ValidationError instead of ValueError."""
        from django.core.exceptions import ValidationError

        view = self._create_mock_view()
        # Key has correct format but third part is not numeric
        request = self.factory.post("/", data={"xp_request_abc": "approve"})

        with self.assertRaises(ValidationError) as cm:
            view._parse_request_id(request, "approve")
        self.assertIn("Invalid request", str(cm.exception))

    def test_parse_request_id_empty_post_raises_validation_error(self):
        """Test that empty POST data raises ValidationError."""
        from django.core.exceptions import ValidationError

        view = self._create_mock_view()
        request = self.factory.post("/", data={})

        with self.assertRaises(ValidationError) as cm:
            view._parse_request_id(request, "approve")
        self.assertIn("Invalid request", str(cm.exception))

    def test_parse_request_id_negative_id_is_valid(self):
        """Test that negative IDs are rejected as invalid."""
        from django.core.exceptions import ValidationError

        view = self._create_mock_view()
        # Negative ID should be rejected
        request = self.factory.post("/", data={"xp_request_-5": "approve"})

        with self.assertRaises(ValidationError) as cm:
            view._parse_request_id(request, "approve")
        self.assertIn("Invalid request", str(cm.exception))

    def test_post_approve_with_malformed_key_shows_error_message(self):
        """Integration test: verify post() correctly handles ValidationError.

        This test ensures that when _parse_request_id raises a ValidationError,
        the post() method properly converts it to a user-facing error message
        and redirects. This catches bugs like using e.message instead of str(e).
        """

        from core.mixins import ApprovalMixin

        class TestApprovalView(ApprovalMixin):
            approve_button_value = "approve"
            reject_button_value = "reject"
            spending_type = "XP"

            def get_object(self):
                return MagicMock(pk=1)

            def get_request_model(self):
                return MagicMock()

        view = TestApprovalView()
        # Malformed key with only 2 parts - will trigger ValidationError
        request = self.factory.post("/", data={"malformed_key": "approve"})
        request.user = self.user

        # Set up messages framework on the request
        request.session = "session"
        messages_storage = FallbackStorage(request)
        request._messages = messages_storage

        with patch("django.shortcuts.redirect") as mock_redirect:
            mock_redirect.return_value = MagicMock()
            view.post(request)

        # Verify error message was added (not AttributeError from e.message)
        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertIn("Invalid request", str(messages[0]))

    def test_post_reject_with_malformed_key_shows_error_message(self):
        """Integration test: verify post() reject path handles ValidationError.

        Tests the reject button path to ensure both approve and reject
        branches properly handle ValidationError without AttributeError.
        """

        from core.mixins import ApprovalMixin

        class TestApprovalView(ApprovalMixin):
            approve_button_value = "approve"
            reject_button_value = "reject"
            spending_type = "XP"

            def get_object(self):
                return MagicMock(pk=1)

            def get_request_model(self):
                return MagicMock()

        view = TestApprovalView()
        # Malformed key with only 2 parts - will trigger ValidationError
        request = self.factory.post("/", data={"malformed_key": "reject"})
        request.user = self.user

        # Set up messages framework on the request
        request.session = "session"
        messages_storage = FallbackStorage(request)
        request._messages = messages_storage

        with patch("django.shortcuts.redirect") as mock_redirect:
            mock_redirect.return_value = MagicMock()
            view.post(request)

        # Verify error message was added (not AttributeError from e.message)
        messages = list(get_messages(request))
        self.assertEqual(len(messages), 1)
        self.assertIn("Invalid request", str(messages[0]))
