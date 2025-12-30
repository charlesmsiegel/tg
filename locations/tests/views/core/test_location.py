from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle, ObjectType
from locations.models.core.location import LocationModel


class TestLocationIndexView(TestCase):
    def setUp(self) -> None:
        self.url = "/locations/index/"
        ObjectType.objects.get_or_create(name="location", type="loc", gameline="wod")[0]
        return super().setUp()

    def test_index_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/index.html")

    def test_index_content(self):
        for i in range(10):
            LocationModel.objects.create(
                name=f"Location {i}",
            )
        response = self.client.get(self.url)
        for i in range(10):
            self.assertContains(response, f"Location {i}")


class TestLocationIndexViewPost(TestCase):
    """Test POST actions on LocationIndexView."""

    def setUp(self):
        self.url = "/locations/index/"
        # Create object types for different gamelines
        ObjectType.objects.get_or_create(name="node", type="loc", gameline="mta")
        ObjectType.objects.get_or_create(name="caern", type="loc", gameline="wta")

    def test_post_create_action_mta(self):
        """Test create action redirects to Mage location create."""
        response = self.client.post(
            self.url,
            {"action": "create", "loc_type": "node"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("mage", response.url)
        self.assertIn("create", response.url)

    def test_post_create_action_wta(self):
        """Test create action redirects to Werewolf location create."""
        response = self.client.post(
            self.url,
            {"action": "create", "loc_type": "caern"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("werewolf", response.url)
        self.assertIn("create", response.url)

    def test_post_index_action_mta(self):
        """Test index action redirects to Mage location list."""
        response = self.client.post(
            self.url,
            {"action": "index", "loc_type": "node"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("mage", response.url)

    def test_post_index_action_wta(self):
        """Test index action redirects to Werewolf location list."""
        response = self.client.post(
            self.url,
            {"action": "index", "loc_type": "caern"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("werewolf", response.url)


class TestLocationIndexViewContext(TestCase):
    """Test context data in LocationIndexView."""

    def setUp(self):
        self.url = "/locations/index/"
        ObjectType.objects.get_or_create(name="location", type="loc", gameline="wod")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")

    def test_context_contains_form(self):
        """Test context contains location creation form."""
        response = self.client.get(self.url)
        self.assertIn("form", response.context)

    def test_context_contains_chrondict(self):
        """Test context contains chronicle dictionary."""
        response = self.client.get(self.url)
        self.assertIn("chrondict", response.context)

    def test_context_header_for_anonymous_user(self):
        """Test header defaults for anonymous user."""
        response = self.client.get(self.url)
        self.assertEqual(response.context["header"], "wod_heading")

    def test_context_header_for_authenticated_user(self):
        """Test header uses user's preferred heading."""
        user = User.objects.create_user(username="testuser", password="password")
        user.profile.preferred_heading = "vtm_heading"
        user.profile.save()
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.context["header"], "vtm_heading")


class TestGenericLocationDetailView(TestCase):
    """Test GenericLocationDetailView routing."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_invalid_location_returns_404(self):
        """Test non-existent location returns 404."""
        self.client.login(username="testuser", password="password")
        response = self.client.get("/locations/99999/")
        self.assertEqual(response.status_code, 404)
