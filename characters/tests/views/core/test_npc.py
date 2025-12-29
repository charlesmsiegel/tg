"""
Tests for NPC views.

Tests cover:
- NPCProfileCreateView GET request
- NPCProfileCreateView POST request
- Authentication requirements
- Related character functionality
- Form validation and error handling
"""

from characters.models.core.human import Human
from characters.models.vampire.vtmhuman import VtMHuman
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from game.models import Chronicle


class NPCProfileCreateViewAuthenticationTestCase(TestCase):
    """Test NPCProfileCreateView authentication requirements."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )

    def assertRequiresAuth(self, response):
        """Assert that the response indicates authentication is required.

        The application may return either:
        - 302 redirect to login page
        - 401 Unauthorized for some views
        """
        self.assertIn(
            response.status_code,
            [302, 401],
            f"Expected 302 or 401, got {response.status_code}",
        )
        if response.status_code == 302:
            self.assertIn("/accounts/login/", response.url)

    def test_get_requires_authentication(self):
        """Test GET request requires authentication."""
        response = self.client.get(reverse("characters:create:npc"))
        self.assertRequiresAuth(response)

    def test_post_requires_authentication(self):
        """Test POST request requires authentication."""
        data = {
            "npc_type": "vtm_human",
            "name": "Test NPC",
            "concept": "Test concept",
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)
        self.assertRequiresAuth(response)

    def test_get_accessible_when_logged_in(self):
        """Test GET request accessible when logged in."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("characters:create:npc"))
        self.assertEqual(response.status_code, 200)

    def test_get_for_character_requires_authentication(self):
        """Test GET request for specific character requires authentication."""
        character = Human.objects.create(name="Test PC", owner=self.user)
        url = reverse("characters:create:npc_for_character", kwargs={"pk": character.pk})
        response = self.client.get(url)
        self.assertRequiresAuth(response)


class NPCProfileCreateViewGETTestCase(TestCase):
    """Test NPCProfileCreateView GET requests."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.client.login(username="testuser", password="password")

    def test_get_returns_form(self):
        """Test GET request returns form in context."""
        response = self.client.get(reverse("characters:create:npc"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_get_uses_correct_template(self):
        """Test GET request uses correct template."""
        response = self.client.get(reverse("characters:create:npc"))
        self.assertTemplateUsed(response, "characters/core/npc/create.html")

    def test_get_for_related_character(self):
        """Test GET request with related character."""
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        character = Human.objects.create(name="Test PC", owner=self.user, chronicle=chronicle)

        url = reverse("characters:create:npc_for_character", kwargs={"pk": character.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("related_character", response.context)
        self.assertEqual(response.context["related_character"], character)

    def test_get_for_nonexistent_character_returns_404(self):
        """Test GET request for nonexistent character returns 404."""
        url = reverse("characters:create:npc_for_character", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_form_has_expected_fields(self):
        """Test form in GET response has expected fields."""
        response = self.client.get(reverse("characters:create:npc"))
        form = response.context["form"]

        self.assertIn("npc_type", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("concept", form.fields)
        self.assertIn("npc_role", form.fields)
        self.assertIn("chronicle", form.fields)


class NPCProfileCreateViewPOSTTestCase(TestCase):
    """Test NPCProfileCreateView POST requests."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.client.login(username="testuser", password="password")

    def test_post_creates_npc(self):
        """Test successful POST creates NPC."""
        data = {
            "npc_type": "vtm_human",
            "name": "New NPC",
            "concept": "Street informant",
            "npc_role": "contact",
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)

        # Should redirect to NPC detail page on success
        self.assertEqual(response.status_code, 302)

        # Verify NPC was created
        npc = VtMHuman.objects.get(name="New NPC")
        self.assertEqual(npc.concept, "Street informant")
        self.assertTrue(npc.npc)
        self.assertEqual(npc.owner, self.user)

    def test_post_invalid_data_returns_form(self):
        """Test POST with invalid data returns form with errors."""
        data = {
            "npc_type": "vtm_human",
            # Missing required name
            "concept": "Some concept",
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertIn("name", response.context["form"].errors)

    def test_post_with_missing_concept(self):
        """Test POST with missing concept returns form with errors."""
        data = {
            "npc_type": "vtm_human",
            "name": "Test NPC",
            # Missing required concept
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("concept", response.context["form"].errors)

    def test_post_with_invalid_npc_type(self):
        """Test POST with invalid NPC type returns form with errors."""
        data = {
            "npc_type": "invalid_type",
            "name": "Test NPC",
            "concept": "Some concept",
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("npc_type", response.context["form"].errors)

    def test_post_with_chronicle(self):
        """Test POST with chronicle assigns it to NPC."""
        chronicle = Chronicle.objects.create(name="Test Chronicle")
        data = {
            "npc_type": "vtm_human",
            "name": "NPC With Chronicle",
            "concept": "Some concept",
            "chronicle": chronicle.pk,
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)

        self.assertEqual(response.status_code, 302)
        npc = VtMHuman.objects.get(name="NPC With Chronicle")
        self.assertEqual(npc.chronicle, chronicle)

    def test_post_with_related_character(self):
        """Test POST with related character includes it in notes."""
        character = Human.objects.create(name="Main PC", owner=self.user)

        data = {
            "npc_type": "vtm_human",
            "name": "Related NPC",
            "concept": "PC's contact",
        }
        url = reverse("characters:create:npc_for_character", kwargs={"pk": character.pk})
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        npc = VtMHuman.objects.get(name="Related NPC")
        self.assertIn("Related to: Main PC", npc.notes)

    def test_post_redirects_to_npc_detail(self):
        """Test successful POST redirects to NPC detail page."""
        data = {
            "npc_type": "vtm_human",
            "name": "Redirect Test NPC",
            "concept": "Test concept",
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)

        npc = VtMHuman.objects.get(name="Redirect Test NPC")
        self.assertRedirects(
            response,
            npc.get_absolute_url(),
            fetch_redirect_response=False,
        )

    def test_post_shows_success_message(self):
        """Test successful POST shows success message."""
        data = {
            "npc_type": "vtm_human",
            "name": "Message Test NPC",
            "concept": "Test concept",
        }
        response = self.client.post(reverse("characters:create:npc"), data=data, follow=True)

        # Check for success message in response
        messages = list(response.context.get("messages", []))
        self.assertTrue(
            any("Message Test NPC" in str(m) for m in messages),
            "Success message should mention NPC name",
        )


class NPCProfileCreateViewEdgeCasesTestCase(TestCase):
    """Test edge cases for NPCProfileCreateView."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.client.login(username="testuser", password="password")

    def test_post_with_all_optional_fields(self):
        """Test POST with all optional fields."""
        data = {
            "npc_type": "vtm_human",
            "name": "Full NPC",
            "concept": "Detailed character",
            "npc_role": "mentor",
            "description": "Tall and mysterious",
            "public_info": "Known in local circles",
            "st_notes": "Secret plot connection",
            "notes": "Additional notes",
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)

        self.assertEqual(response.status_code, 302)
        npc = VtMHuman.objects.get(name="Full NPC")
        self.assertEqual(npc.description, "Tall and mysterious")
        self.assertEqual(npc.public_info, "Known in local circles")
        self.assertEqual(npc.st_notes, "Secret plot connection")

    def test_post_creates_correct_character_type(self):
        """Test POST creates the correct character type for each NPC type."""
        from characters.models.mage.mtahuman import MtAHuman
        from characters.models.werewolf.wtahuman import WtAHuman
        from characters.models.wraith.wtohuman import WtOHuman

        test_cases = [
            ("vtm_human", VtMHuman),
            ("wta_human", WtAHuman),
            ("mta_human", MtAHuman),
            ("wto_human", WtOHuman),
        ]

        for npc_type, expected_class in test_cases:
            data = {
                "npc_type": npc_type,
                "name": f"Test {npc_type}",
                "concept": "Test concept",
            }
            response = self.client.post(reverse("characters:create:npc"), data=data)
            self.assertEqual(response.status_code, 302, f"Failed for {npc_type}")

            npc = expected_class.objects.get(name=f"Test {npc_type}")
            self.assertIsInstance(npc, expected_class)

    def test_form_preserves_data_on_error(self):
        """Test form preserves data when validation fails."""
        data = {
            "npc_type": "vtm_human",
            "name": "",  # Invalid - empty
            "concept": "Some concept",
            "description": "Should be preserved",
        }
        response = self.client.post(reverse("characters:create:npc"), data=data)

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(form.data.get("description"), "Should be preserved")
        self.assertEqual(form.data.get("concept"), "Some concept")
