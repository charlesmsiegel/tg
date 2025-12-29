"""Tests for WtAHuman views module."""

from characters.models.werewolf.wtahuman import WtAHuman
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class WtAHumanViewTestCase(TestCase):
    """Base test case with common setup for WtAHuman view tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all test methods."""
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def setUp(self):
        """Set up test users and client."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpassword",
        )
        self.st = User.objects.create_user(
            username="storyteller",
            email="st@test.com",
            password="stpassword",
        )
        self.chronicle.storytellers.add(self.st)


class TestWtAHumanDetailView(WtAHumanViewTestCase):
    """Tests for WtAHumanDetailView."""

    def setUp(self):
        """Set up test characters."""
        super().setUp()
        self.wtahuman = WtAHuman.objects.create(
            name="Test WtA Human",
            owner=self.user,
            status="App",
        )

    def test_detail_view_accessible_by_owner(self):
        """Detail view is accessible for owner."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.wtahuman.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        """Detail view uses the correct template."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.wtahuman.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/wtahuman/detail.html")

    def test_unauthenticated_returns_404(self):
        """Unauthenticated users get 404 (hidden for privacy)."""
        response = self.client.get(self.wtahuman.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_detail_view_context_contains_object(self):
        """Detail view context contains the character object."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.wtahuman.get_absolute_url())
        self.assertEqual(response.context["object"], self.wtahuman)


class TestWtAHumanBasicsView(WtAHumanViewTestCase):
    """Tests for WtAHumanBasicsView (creation form)."""

    def test_view_requires_authentication(self):
        """View requires authentication."""
        response = self.client.get(reverse("characters:werewolf:create:wtahuman"))
        self.assertIn(response.status_code, [302, 401])

    def test_view_accessible_when_logged_in(self):
        """Authenticated users can access the view."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("characters:werewolf:create:wtahuman"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """View uses the correct template."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("characters:werewolf:create:wtahuman"))
        self.assertTemplateUsed(response, "characters/werewolf/wtahuman/basics.html")

    def test_context_contains_storyteller_flag_for_regular_user(self):
        """Context includes storyteller flag (False for regular users)."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("characters:werewolf:create:wtahuman"))
        self.assertIn("storyteller", response.context)
        self.assertFalse(response.context["storyteller"])

    def test_context_contains_storyteller_flag_for_st(self):
        """Context includes storyteller flag (True for STs)."""
        self.client.login(username="storyteller", password="stpassword")
        response = self.client.get(reverse("characters:werewolf:create:wtahuman"))
        self.assertIn("storyteller", response.context)
        self.assertTrue(response.context["storyteller"])

    def test_create_wtahuman_via_post(self):
        """Can create a WtA Human character."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("characters:werewolf:create:wtahuman"),
            data={
                "name": "New WtA Human",
                "concept": "Test Concept",
            },
        )
        self.assertEqual(WtAHuman.objects.count(), 1)
        wtahuman = WtAHuman.objects.first()
        self.assertEqual(wtahuman.name, "New WtA Human")
        self.assertEqual(wtahuman.owner, self.user)


class TestWtAHumanTemplateSelectView(WtAHumanViewTestCase):
    """Tests for WtAHumanTemplateSelectView."""

    def setUp(self):
        """Set up test characters."""
        super().setUp()
        self.wtahuman = WtAHuman.objects.create(
            name="Test WtA Human",
            owner=self.user,
            creation_status=0,
        )

    def test_view_requires_owner(self):
        """View requires owner or redirects."""
        self.client.login(username="storyteller", password="stpassword")
        response = self.client.get(
            reverse("characters:werewolf:wtahuman_template", kwargs={"pk": self.wtahuman.pk})
        )
        # Should return 404 since user is not owner
        self.assertEqual(response.status_code, 404)

    def test_view_accessible_by_owner(self):
        """View is accessible for owner."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("characters:werewolf:wtahuman_template", kwargs={"pk": self.wtahuman.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_redirects_if_creation_started(self):
        """View redirects if creation has already started."""
        self.wtahuman.creation_status = 1
        self.wtahuman.save()
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("characters:werewolf:wtahuman_template", kwargs={"pk": self.wtahuman.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        """View uses the correct template."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("characters:werewolf:wtahuman_template", kwargs={"pk": self.wtahuman.pk})
        )
        self.assertTemplateUsed(response, "characters/werewolf/wtahuman/template_select.html")

    def test_form_valid_without_template(self):
        """Form submission without template sets creation_status and redirects."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("characters:werewolf:wtahuman_template", kwargs={"pk": self.wtahuman.pk}),
            data={"template": ""},
        )
        self.assertEqual(response.status_code, 302)
        self.wtahuman.refresh_from_db()
        self.assertEqual(self.wtahuman.creation_status, 1)


class TestWtAHumanCharacterCreationView(WtAHumanViewTestCase):
    """Tests for WtAHumanCharacterCreationView routing."""

    def setUp(self):
        """Set up test characters at various creation stages."""
        super().setUp()
        self.wtahuman_stage_1 = WtAHuman.objects.create(
            name="WtA Human Stage 1",
            owner=self.user,
            creation_status=1,
        )
        self.wtahuman_complete = WtAHuman.objects.create(
            name="WtA Human Complete",
            owner=self.user,
            creation_status=100,
        )

    def test_routes_to_attribute_at_stage_1(self):
        """Routes to attribute view at stage 1."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("characters:werewolf:wtahuman_creation", kwargs={"pk": self.wtahuman_stage_1.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_routes_correctly_when_complete(self):
        """Routes correctly when creation is complete."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("characters:werewolf:wtahuman_creation", kwargs={"pk": self.wtahuman_complete.pk})
        )
        # May redirect to detail view or show final form
        self.assertIn(response.status_code, [200, 302])


class TestWtAHumanUpdateView(WtAHumanViewTestCase):
    """Tests for WtAHumanUpdateView."""

    def setUp(self):
        """Set up test characters."""
        super().setUp()
        self.wtahuman = WtAHuman.objects.create(
            name="Test WtA Human",
            owner=self.user,
            status="App",
            chronicle=self.chronicle,
        )

    def test_update_view_requires_authentication(self):
        """Update view requires authentication."""
        response = self.client.get(
            reverse("characters:werewolf:update:wtahuman", kwargs={"pk": self.wtahuman.pk})
        )
        self.assertIn(response.status_code, [302, 401, 404])

    def test_update_view_accessible_by_owner(self):
        """Update view is accessible by owner."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("characters:werewolf:update:wtahuman", kwargs={"pk": self.wtahuman.pk})
        )
        # May return 200 or redirect depending on permissions
        self.assertIn(response.status_code, [200, 302])

    def test_update_view_accessible_by_st(self):
        """Update view is accessible by Storyteller."""
        self.client.login(username="storyteller", password="stpassword")
        response = self.client.get(
            reverse("characters:werewolf:update:wtahuman", kwargs={"pk": self.wtahuman.pk})
        )
        self.assertIn(response.status_code, [200, 302])


class TestWtAHumanCreateView(WtAHumanViewTestCase):
    """Tests for WtAHumanCreateView."""

    def test_create_view_accessible(self):
        """Create view is accessible for authenticated users."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("characters:werewolf:create:wtahuman"))
        self.assertEqual(response.status_code, 200)

    def test_create_view_form_has_required_fields(self):
        """Create form shows required fields."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("characters:werewolf:create:wtahuman"))
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertIn("name", form.fields)
