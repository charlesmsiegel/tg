"""
Tests for Freehold creation, both multi-step and direct.
Tests cover the complete creation workflow from Book of Freeholds.
"""
from characters.models.core import Human
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from locations.models.changeling import Freehold


class TestFreeholdMultiStepCreation(TestCase):
    """Test multi-step freehold creation workflow"""

    def setUp(self):
        """Set up test user and client"""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

        # Create a character for the user (needed for owned_by)
        self.character = Human.objects.create(name="Test Changeling", owner=self.user)

    def test_step1_basics_creates_freehold(self):
        """Test Step 1: Creating freehold with basics sets creation_status = 1"""
        url = reverse("locations:changeling:create:freehold")
        data = {
            "name": "Mirror Lights",
            "archetype": "hearth",
            "aspect": "Sexy nightclub with hidden primal darkness",
            "description": "Found in the Dreaming and claimed",
        }

        response = self.client.post(url, data, follow=True)

        # Should create freehold successfully
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Freehold.objects.filter(name="Mirror Lights").exists())

        freehold = Freehold.objects.get(name="Mirror Lights")
        self.assertEqual(freehold.creation_status, 1)
        self.assertEqual(freehold.archetype, "hearth")
        self.assertEqual(freehold.status, "Un")  # Unfinished

    def test_step2_features_increments_status(self):
        """Test Step 2: Features allocation increments creation_status to 2"""
        # Create freehold at step 1
        freehold = Freehold.objects.create(
            name="Test Freehold",
            archetype="academy",
            creation_status=1,
            status="Un",
            owned_by=self.character,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])
        data = {
            "balefire": 4,
            "size": 3,
            "sanctuary": 2,
            "resources": 2,
            "passages": 1,
            "balefire_description": "Column of light illuminating the stage",
        }

        response = self.client.post(url, data, follow=True)

        freehold.refresh_from_db()
        self.assertEqual(freehold.creation_status, 2)
        self.assertEqual(freehold.balefire, 4)
        self.assertEqual(freehold.size, 3)

    def test_step3_powers_increments_status(self):
        """Test Step 3: Powers selection increments creation_status to 3"""
        freehold = Freehold.objects.create(
            name="Test Freehold",
            archetype="hearth",
            creation_status=2,
            status="Un",
            owned_by=self.character,
            balefire=4,
            size=3,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])
        data = {
            "powers": ["glamour_to_dross", "resonant_dreams"],
            "dual_nature_archetype": "",
            "dual_nature_ability": "",
        }

        response = self.client.post(url, data, follow=True)

        freehold.refresh_from_db()
        self.assertEqual(freehold.creation_status, 3)
        self.assertIn("glamour_to_dross", freehold.powers)
        self.assertIn("resonant_dreams", freehold.powers)

    def test_step4_details_completes_creation(self):
        """Test Step 4: Details finalizes freehold with creation_status = 5"""
        freehold = Freehold.objects.create(
            name="Test Freehold",
            archetype="hearth",
            hearth_ability="",  # Will be set in step 4
            creation_status=3,
            status="Un",
            owned_by=self.character,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])
        data = {
            "academy_ability": "",
            "hearth_ability": "leadership",
            "resource_description": "Generates mundane revenue",
            "passage_description": "One trod to the Near Dreaming",
            "quirks": "The grass whispers encouragement",
            "parent": "",
            "owned_by": self.character.pk,
        }

        response = self.client.post(url, data, follow=True)

        freehold.refresh_from_db()
        self.assertEqual(freehold.creation_status, 5)  # Complete
        self.assertEqual(freehold.hearth_ability, "leadership")

        # Should redirect to detail view
        self.assertRedirects(response, freehold.get_absolute_url())

    def test_resume_creation_at_correct_step(self):
        """Test that accessing update URL resumes at correct step based on creation_status"""
        # Create freehold at step 2
        freehold = Freehold.objects.create(
            name="Resumed Freehold",
            archetype="market",
            creation_status=2,  # Should go to powers step
            status="Un",
            owned_by=self.character,
            balefire=3,
            size=2,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])
        response = self.client.get(url)

        # Should render powers template (step 3)
        self.assertTemplateUsed(
            response, "locations/changeling/freehold/chargen/powers.html"
        )

    def test_feature_point_calculation(self):
        """Test that feature points are calculated correctly"""
        freehold = Freehold.objects.create(
            name="Test Freehold",
            balefire=4,  # 4 points
            size=3,  # 3 points
            sanctuary=2,  # 2 points
            resources=2,  # 2 points
            passages=3,  # 2 points (first free, +2)
            powers=["glamour_to_dross", "resonant_dreams"],  # 2 + 2 = 4 points
        )

        # Total: 4 + 3 + 2 + 2 + 2 + 4 = 17 points
        self.assertEqual(freehold.get_total_feature_points(), 17)

        # Holdings required: ceil(17 / 3) = 6 dots
        self.assertEqual(freehold.get_holdings_required(), 6)

    def test_academy_archetype_requires_ability(self):
        """Test that Academy archetype requires an associated ability in step 4"""
        freehold = Freehold.objects.create(
            name="Test Academy",
            archetype="academy",
            creation_status=3,
            status="Un",
            owned_by=self.character,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])

        # Try without ability - should fail validation
        data = {
            "academy_ability": "",  # Missing required field
            "hearth_ability": "",
            "resource_description": "",
            "passage_description": "",
            "quirks": "",
            "parent": "",
            "owned_by": self.character.pk,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors

        freehold.refresh_from_db()
        self.assertEqual(freehold.creation_status, 3)  # Should not advance

        # Now with ability - should succeed
        data["academy_ability"] = "Kenning"
        response = self.client.post(url, data, follow=True)

        freehold.refresh_from_db()
        self.assertEqual(freehold.creation_status, 5)  # Complete
        self.assertEqual(freehold.academy_ability, "Kenning")

    def test_hearth_archetype_requires_choice(self):
        """Test that Hearth archetype requires Leadership or Socialize choice"""
        freehold = Freehold.objects.create(
            name="Test Hearth",
            archetype="hearth",
            creation_status=3,
            status="Un",
            owned_by=self.character,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])

        # Try without choice - should fail
        data = {
            "academy_ability": "",
            "hearth_ability": "",  # Missing required field
            "resource_description": "",
            "passage_description": "",
            "quirks": "",
            "parent": "",
            "owned_by": self.character.pk,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered

        # With choice - should succeed
        data["hearth_ability"] = "socialize"
        response = self.client.post(url, data, follow=True)

        freehold.refresh_from_db()
        self.assertEqual(freehold.hearth_ability, "socialize")

    def test_dual_nature_power_requires_archetype(self):
        """Test that Dual Nature power requires selecting a second archetype"""
        freehold = Freehold.objects.create(
            name="Test Dual Nature",
            archetype="stronghold",
            creation_status=2,
            status="Un",
            owned_by=self.character,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])

        # Try Dual Nature without second archetype - should fail
        data = {
            "powers": ["dual_nature"],
            "dual_nature_archetype": "",  # Missing
            "dual_nature_ability": "",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors

        # With archetype - should succeed
        data["dual_nature_archetype"] = "repository"
        response = self.client.post(url, data, follow=True)

        freehold.refresh_from_db()
        self.assertEqual(freehold.dual_nature_archetype, "repository")
        self.assertIn("dual_nature", freehold.powers)

    def test_dual_nature_academy_requires_ability(self):
        """Test that Dual Nature Academy requires specifying an ability"""
        freehold = Freehold.objects.create(
            name="Test Dual Nature Academy",
            archetype="stronghold",
            creation_status=2,
            status="Un",
            owned_by=self.character,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])

        # Dual Nature with Academy but no ability - should fail
        data = {
            "powers": ["dual_nature"],
            "dual_nature_archetype": "academy",
            "dual_nature_ability": "",  # Missing
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Form error

        # With ability - should succeed
        data["dual_nature_ability"] = "Melee"
        response = self.client.post(url, data, follow=True)

        freehold.refresh_from_db()
        self.assertEqual(freehold.dual_nature_ability, "Melee")

    def test_approved_freehold_redirects_to_detail(self):
        """Test that approved freeholds can't access creation steps - redirect to detail"""
        freehold = Freehold.objects.create(
            name="Approved Freehold",
            archetype="manor",
            creation_status=5,
            status="App",  # Approved
            owned_by=self.character,
        )

        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])
        response = self.client.get(url, follow=True)

        # Should redirect to detail view, not show creation steps
        self.assertRedirects(response, freehold.get_absolute_url())
        self.assertTemplateUsed(response, "locations/changeling/freehold/detail.html")

    def test_complete_workflow_all_steps(self):
        """Test complete workflow through all 4 steps"""
        # Step 1: Basics
        url = reverse("locations:changeling:create:freehold")
        data = {
            "name": "Complete Test Freehold",
            "archetype": "repository",
            "aspect": "Ancient library of lost knowledge",
            "description": "Discovered in the ruins",
        }
        response = self.client.post(url, data, follow=True)

        freehold = Freehold.objects.get(name="Complete Test Freehold")
        self.assertEqual(freehold.creation_status, 1)

        # Step 2: Features
        url = reverse("locations:changeling:update:freehold", args=[freehold.pk])
        data = {
            "balefire": 3,
            "size": 4,
            "sanctuary": 3,
            "resources": 1,
            "passages": 2,
            "balefire_description": "Glowing tomes",
        }
        response = self.client.post(url, data, follow=True)
        freehold.refresh_from_db()
        self.assertEqual(freehold.creation_status, 2)

        # Step 3: Powers
        data = {
            "powers": ["warning_call"],
            "dual_nature_archetype": "",
            "dual_nature_ability": "",
        }
        response = self.client.post(url, data, follow=True)
        freehold.refresh_from_db()
        self.assertEqual(freehold.creation_status, 3)

        # Step 4: Details
        data = {
            "academy_ability": "",
            "hearth_ability": "",
            "resource_description": "Ancient texts",
            "passage_description": "Portal to the Deep Dreaming",
            "quirks": "Books rearrange themselves",
            "parent": "",
            "owned_by": self.character.pk,
        }
        response = self.client.post(url, data, follow=True)
        freehold.refresh_from_db()

        # Final checks
        self.assertEqual(freehold.creation_status, 5)  # Complete
        self.assertEqual(freehold.balefire, 3)
        self.assertEqual(freehold.size, 4)
        self.assertIn("warning_call", freehold.powers)
        self.assertEqual(freehold.quirks, "Books rearrange themselves")

    def test_direct_creation_backwards_compatibility(self):
        """Test that direct (all-at-once) creation still works"""
        url = reverse("locations:changeling:create:freehold_direct")
        response = self.client.get(url)

        # Should load direct creation form
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/changeling/freehold/form.html")


class TestFreeholdModel(TestCase):
    """Test Freehold model methods and properties"""

    def test_archetype_display_with_benefit(self):
        """Test get_archetype_display_with_benefit() method"""
        freehold = Freehold.objects.create(
            name="Test", archetype="academy", academy_ability="Occult"
        )

        display = freehold.get_archetype_display_with_benefit()
        self.assertIn("Academy", display)
        self.assertIn("Occult", display)
        self.assertIn("-2 difficulty", display)

    def test_has_power(self):
        """Test has_power() method"""
        freehold = Freehold.objects.create(
            name="Test", powers=["glamour_to_dross", "warning_call"]
        )

        self.assertTrue(freehold.has_power("glamour_to_dross"))
        self.assertTrue(freehold.has_power("warning_call"))
        self.assertFalse(freehold.has_power("dual_nature"))

    def test_size_description(self):
        """Test get_size_description() method"""
        freehold = Freehold.objects.create(name="Test", size=0)
        self.assertEqual(
            freehold.get_size_description(), "Miniscule, out in the open with no walls"
        )

        freehold.size = 3
        freehold.save()
        self.assertIn("mansion", freehold.get_size_description().lower())

    def test_get_urls(self):
        """Test URL generation methods"""
        freehold = Freehold.objects.create(name="Test Freehold")

        self.assertIn(str(freehold.pk), freehold.get_absolute_url())
        self.assertIn(str(freehold.pk), freehold.get_update_url())
        self.assertIsNotNone(Freehold.get_creation_url())

    def test_get_heading(self):
        """Test that Changeling heading is returned"""
        freehold = Freehold.objects.create(name="Test")
        self.assertEqual(freehold.get_heading(), "ctd_heading")
