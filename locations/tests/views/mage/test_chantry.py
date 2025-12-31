"""Tests for Chantry views."""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.mage.chantry import Chantry


class TestChantryListView(TestCase):
    """Test ChantryListView."""

    def test_list_view_status_code(self):
        """Test list view returns 200."""
        response = self.client.get("/locations/mage/chantry/")
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """Test list view uses correct template."""
        response = self.client.get("/locations/mage/chantry/")
        self.assertTemplateUsed(response, "locations/mage/chantry/list.html")

    def test_list_view_content(self):
        """Test list view shows chantries."""
        for i in range(5):
            Chantry.objects.create(name=f"Test Chantry {i}")
        response = self.client.get("/locations/mage/chantry/")
        for i in range(5):
            self.assertContains(response, f"Test Chantry {i}")

    def test_list_view_ordering(self):
        """Test list view orders by name."""
        Chantry.objects.create(name="Zeta Chantry")
        Chantry.objects.create(name="Alpha Chantry")
        Chantry.objects.create(name="Beta Chantry")
        response = self.client.get("/locations/mage/chantry/")
        content = response.content.decode()
        alpha_pos = content.find("Alpha Chantry")
        beta_pos = content.find("Beta Chantry")
        zeta_pos = content.find("Zeta Chantry")
        self.assertLess(alpha_pos, beta_pos)
        self.assertLess(beta_pos, zeta_pos)


class TestChantryDetailView(TestCase):
    """Test ChantryDetailView."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.chantry = Chantry.objects.create(
            name="Test Chantry",
            description="A test chantry",
            owner=self.user,
            status="App",
            total_points=20,
        )
        self.url = self.chantry.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/chantry/detail.html")

    def test_detail_view_content(self):
        """Test detail view shows chantry details."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertContains(response, "Test Chantry")


class TestChantryCreateView(TestCase):
    """Test ChantryCreateView."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = Chantry.get_creation_url()

    def test_create_view_requires_login(self):
        """Test create view requires authentication."""
        response = self.client.get(self.url)
        # Project uses AuthErrorHandlerMiddleware which returns 401 for unauthenticated users
        self.assertEqual(response.status_code, 401)

    def test_create_view_status_code(self):
        """Test create view returns 200 for logged-in user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/chantry/form.html")

    def test_create_view_post(self):
        """Test successful POST creates chantry."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Chantry",
            "description": "A new chantry",
            "total_points": 30,
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Chantry.objects.filter(name="New Chantry").exists())


class TestChantryUpdateView(TestCase):
    """Test ChantryUpdateView."""

    def setUp(self):
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.chantry = Chantry.objects.create(
            name="Existing Chantry",
            description="An existing chantry",
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
            total_points=25,
        )
        self.url = self.chantry.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200 for ST."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/chantry/form.html")

    def test_update_view_post(self):
        """Test successful POST updates chantry."""
        self.client.login(username="st_user", password="password")
        data = {
            "name": "Updated Chantry",
            "description": "Updated description",
            "total_points": 35,
            "gauntlet": 4,
            "shroud": 5,
            "dimension_barrier": 5,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.name, "Updated Chantry")
        self.assertEqual(self.chantry.total_points, 35)


class TestChantryModel(TestCase):
    """Test Chantry model methods accessed by views."""

    def test_chantry_creation(self):
        """Test creating a chantry."""
        chantry = Chantry.objects.create(
            name="Test Chantry",
            total_points=30,
        )
        self.assertEqual(chantry.name, "Test Chantry")
        self.assertEqual(chantry.total_points, 30)
        self.assertEqual(chantry.type, "chantry")
        self.assertEqual(chantry.gameline, "mta")

    def test_chantry_get_heading(self):
        """Test get_heading returns mta_heading."""
        chantry = Chantry.objects.create(name="Test")
        self.assertEqual(chantry.get_heading(), "mta_heading")

    def test_chantry_points_property(self):
        """Test points property calculation."""
        chantry = Chantry.objects.create(name="Test", total_points=30)
        # Points = total_points - total_cost
        # With no backgrounds or effects, points should equal total_points
        self.assertEqual(chantry.points, 30)

    def test_chantry_rank_property(self):
        """Test rank property based on total_points."""
        # Rank 1: < 11 points
        c1 = Chantry.objects.create(name="Rank1", total_points=10)
        self.assertEqual(c1.rank, 1)

        # Rank 2: 11-20 points
        c2 = Chantry.objects.create(name="Rank2", total_points=15)
        self.assertEqual(c2.rank, 2)

        # Rank 3: 21-30 points
        c3 = Chantry.objects.create(name="Rank3", total_points=25)
        self.assertEqual(c3.rank, 3)

        # Rank 4: 31-70 points
        c4 = Chantry.objects.create(name="Rank4", total_points=50)
        self.assertEqual(c4.rank, 4)

        # Rank 5: > 70 points
        c5 = Chantry.objects.create(name="Rank5", total_points=100)
        self.assertEqual(c5.rank, 5)

    def test_chantry_has_season(self):
        """Test has_season method."""
        chantry = Chantry.objects.create(name="Test")
        self.assertFalse(chantry.has_season())
        chantry.season = "spring"
        chantry.save()
        self.assertTrue(chantry.has_season())

    def test_chantry_set_season(self):
        """Test set_season method."""
        chantry = Chantry.objects.create(name="Test")
        result = chantry.set_season("winter")
        self.assertTrue(result)
        self.assertEqual(chantry.season, "winter")

    def test_chantry_has_chantry_type(self):
        """Test has_chantry_type method."""
        chantry = Chantry.objects.create(name="Test")
        self.assertFalse(chantry.has_chantry_type())
        chantry.chantry_type = "exploration"
        chantry.save()
        self.assertTrue(chantry.has_chantry_type())

    def test_chantry_set_chantry_type(self):
        """Test set_chantry_type method."""
        chantry = Chantry.objects.create(name="Test")
        result = chantry.set_chantry_type("fortress")
        self.assertTrue(result)
        self.assertEqual(chantry.chantry_type, "fortress")

    def test_chantry_trait_cost(self):
        """Test trait_cost method."""
        chantry = Chantry.objects.create(name="Test")
        # Cost 2 traits
        self.assertEqual(chantry.trait_cost("allies"), 2)
        self.assertEqual(chantry.trait_cost("library"), 2)
        # Cost 3 traits
        self.assertEqual(chantry.trait_cost("node"), 3)
        self.assertEqual(chantry.trait_cost("resources"), 3)
        # Cost 4 traits
        self.assertEqual(chantry.trait_cost("enhancement"), 4)
        self.assertEqual(chantry.trait_cost("requisitions"), 4)
        # Cost 5 traits
        self.assertEqual(chantry.trait_cost("sanctum"), 5)
        # Unknown - high cost
        self.assertEqual(chantry.trait_cost("unknown"), 1000)

    def test_chantry_integrated_effects_number(self):
        """Test integrated_effects_number method."""
        chantry = Chantry.objects.create(name="Test")
        # Score 0 -> 0 points
        self.assertEqual(chantry.integrated_effects_number(), 0)
        chantry.integrated_effects_score = 1
        self.assertEqual(chantry.integrated_effects_number(), 4)
        chantry.integrated_effects_score = 5
        self.assertEqual(chantry.integrated_effects_number(), 25)

    def test_chantry_allowed_backgrounds(self):
        """Test allowed_backgrounds class attribute."""
        self.assertIn("allies", Chantry.allowed_backgrounds)
        self.assertIn("node", Chantry.allowed_backgrounds)
        self.assertIn("library", Chantry.allowed_backgrounds)
        self.assertIn("sanctum", Chantry.allowed_backgrounds)


class TestChantryLeadership(TestCase):
    """Test Chantry leadership choices."""

    def test_leadership_choices(self):
        """Test leadership type choices exist."""
        choices = dict(Chantry.LEADERSHIP_CHOICES)
        self.assertIn("panel", choices)
        self.assertIn("democracy", choices)
        self.assertIn("single_deacon", choices)
        self.assertIn("council_of_elders", choices)

    def test_set_leadership(self):
        """Test setting leadership type."""
        chantry = Chantry.objects.create(name="Test")
        chantry.leadership_type = "triumvirate"
        chantry.save()
        chantry.refresh_from_db()
        self.assertEqual(chantry.leadership_type, "triumvirate")


class TestChantrySeasons(TestCase):
    """Test Chantry season choices."""

    def test_season_choices(self):
        """Test season choices exist."""
        choices = dict(Chantry.SEASONS)
        self.assertIn("spring", choices)
        self.assertIn("summer", choices)
        self.assertIn("autumn", choices)
        self.assertIn("winter", choices)


class TestChantryTypes(TestCase):
    """Test Chantry type choices."""

    def test_chantry_type_choices(self):
        """Test chantry type choices exist."""
        choices = dict(Chantry.CHANTRY_TYPES)
        self.assertIn("exploration", choices)
        self.assertIn("ancestral", choices)
        self.assertIn("college", choices)
        self.assertIn("war", choices)
        self.assertIn("library", choices)
        self.assertIn("research", choices)
        self.assertIn("fortress", choices)


class TestChantryFactionalNames(TestCase):
    """Test Chantry factional names mapping."""

    def test_factional_names_exist(self):
        """Test factional names mapping exists."""
        self.assertIn("Order of Hermes", Chantry.factional_names)
        self.assertIn("Virtual Adepts", Chantry.factional_names)
        self.assertIn("Technocratic Union", Chantry.factional_names)

    def test_hermetic_chantry_names(self):
        """Test Order of Hermes chantry names."""
        names = Chantry.factional_names["Order of Hermes"]
        self.assertIn("Covenant", names)
        self.assertIn("Chantry", names)

    def test_technocracy_construct_name(self):
        """Test Technocracy uses Construct."""
        names = Chantry.factional_names["Technocratic Union"]
        self.assertIn("Construct", names)
