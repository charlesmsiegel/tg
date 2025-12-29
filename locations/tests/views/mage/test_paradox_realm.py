"""Tests for ParadoxRealm views."""

from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from locations.models.mage.paradox_realm import (
    ParadoxAtmosphere,
    ParadoxObstacle,
    ParadoxRealm,
    ParadigmChoices,
    SphereChoices,
)


class TestParadoxRealmListView(TestCase):
    """Test ParadoxRealmListView."""

    def test_list_view_status_code(self):
        """Test list view returns 200."""
        response = self.client.get("/locations/mage/paradox_realm/")
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """Test list view uses correct template."""
        response = self.client.get("/locations/mage/paradox_realm/")
        self.assertTemplateUsed(response, "locations/mage/paradox_realm/list.html")

    def test_list_view_content(self):
        """Test list view shows realms."""
        for i in range(5):
            ParadoxRealm.objects.create(name=f"Test Realm {i}")
        response = self.client.get("/locations/mage/paradox_realm/")
        for i in range(5):
            self.assertContains(response, f"Test Realm {i}")

    def test_list_view_ordering(self):
        """Test list view orders by name."""
        ParadoxRealm.objects.create(name="Zeta Realm")
        ParadoxRealm.objects.create(name="Alpha Realm")
        ParadoxRealm.objects.create(name="Beta Realm")
        response = self.client.get("/locations/mage/paradox_realm/")
        content = response.content.decode()
        alpha_pos = content.find("Alpha Realm")
        beta_pos = content.find("Beta Realm")
        zeta_pos = content.find("Zeta Realm")
        self.assertLess(alpha_pos, beta_pos)
        self.assertLess(beta_pos, zeta_pos)


class TestParadoxRealmDetailView(TestCase):
    """Test ParadoxRealmDetailView."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.realm = ParadoxRealm.objects.create(
            name="Test Realm",
            primary_sphere=SphereChoices.FORCES,
            paradigm=ParadigmChoices.CHAOS,
            description="A chaotic realm of forces",
            owner=self.user,
            status="App",
        )
        self.url = self.realm.get_absolute_url()

    def test_detail_view_status_code(self):
        """Test detail view returns 200."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """Test detail view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/paradox_realm/detail.html")

    def test_detail_view_content(self):
        """Test detail view shows realm details."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertContains(response, "Test Realm")
        self.assertContains(response, "Forces")

    def test_detail_view_shows_obstacles(self):
        """Test detail view shows obstacles in context."""
        self.client.login(username="testuser", password="password")
        ParadoxObstacle.objects.create(
            realm=self.realm,
            sphere=SphereChoices.FORCES,
            obstacle_number=4,
            order=0,
            name="Fire",
        )
        response = self.client.get(self.url)
        self.assertIn("obstacles", response.context)

    def test_detail_view_shows_atmospheres(self):
        """Test detail view shows atmospheres in context."""
        self.client.login(username="testuser", password="password")
        ParadoxAtmosphere.objects.create(
            realm=self.realm,
            paradigm=ParadigmChoices.CHAOS,
            atmosphere_number=1,
            description="Colors pulsating",
        )
        response = self.client.get(self.url)
        self.assertIn("atmospheres", response.context)


class TestParadoxRealmCreateView(TestCase):
    """Test ParadoxRealmCreateView."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.url = ParadoxRealm.get_creation_url()

    def test_create_view_requires_login(self):
        """Test create view requires authentication."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_create_view_status_code(self):
        """Test create view returns 200 for logged-in user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test create view uses correct template."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/paradox_realm/form.html")

    def test_create_view_post(self):
        """Test successful POST creates realm."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "New Paradox Realm",
            "description": "A new realm",
            "primary_sphere": SphereChoices.MIND,
            "paradigm": ParadigmChoices.ILLUSION,
            "num_primary_obstacles": 2,
            "num_random_obstacles": 1,
            "final_obstacle_type": "maze",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            "obstacles-TOTAL_FORMS": "0",
            "obstacles-INITIAL_FORMS": "0",
            "obstacles-MIN_NUM_FORMS": "0",
            "obstacles-MAX_NUM_FORMS": "1000",
            "atmospheres-TOTAL_FORMS": "0",
            "atmospheres-INITIAL_FORMS": "0",
            "atmospheres-MIN_NUM_FORMS": "0",
            "atmospheres-MAX_NUM_FORMS": "1000",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ParadoxRealm.objects.filter(name="New Paradox Realm").exists())

    def test_create_view_random_generation(self):
        """Test POST with generate_random creates random realm."""
        self.client.login(username="testuser", password="password")
        data = {
            "name": "Random Realm",
            "description": "",
            "primary_sphere": SphereChoices.PRIME,
            "paradigm": ParadigmChoices.ANTIMAGICK,
            "num_primary_obstacles": 0,
            "num_random_obstacles": 0,
            "final_obstacle_type": "maze",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            "generate_random": True,
            "obstacles-TOTAL_FORMS": "0",
            "obstacles-INITIAL_FORMS": "0",
            "obstacles-MIN_NUM_FORMS": "0",
            "obstacles-MAX_NUM_FORMS": "1000",
            "atmospheres-TOTAL_FORMS": "0",
            "atmospheres-INITIAL_FORMS": "0",
            "atmospheres-MIN_NUM_FORMS": "0",
            "atmospheres-MAX_NUM_FORMS": "1000",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        realm = ParadoxRealm.objects.get(name="Random Realm")
        # Random generation creates atmosphere elements
        self.assertGreaterEqual(realm.realm_atmospheres.count(), 2)


class TestParadoxRealmUpdateView(TestCase):
    """Test ParadoxRealmUpdateView."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.st = User.objects.create_user(username="st_user", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.realm = ParadoxRealm.objects.create(
            name="Existing Realm",
            primary_sphere=SphereChoices.ENTROPY,
            paradigm=ParadigmChoices.OBLIVION,
            owner=self.st,
            chronicle=self.chronicle,
            status="App",
        )
        self.url = self.realm.get_update_url()

    def test_update_view_status_code(self):
        """Test update view returns 200 for ST."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test update view uses correct template."""
        self.client.login(username="st_user", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "locations/mage/paradox_realm/form.html")

    def test_update_view_post(self):
        """Test successful POST updates realm."""
        self.client.login(username="st_user", password="password")
        data = {
            "name": "Updated Realm",
            "description": "Updated description",
            "primary_sphere": SphereChoices.TIME,
            "paradigm": ParadigmChoices.TECH,
            "num_primary_obstacles": 3,
            "num_random_obstacles": 2,
            "final_obstacle_type": "button",
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
            "obstacles-TOTAL_FORMS": "0",
            "obstacles-INITIAL_FORMS": "0",
            "obstacles-MIN_NUM_FORMS": "0",
            "obstacles-MAX_NUM_FORMS": "1000",
            "atmospheres-TOTAL_FORMS": "0",
            "atmospheres-INITIAL_FORMS": "0",
            "atmospheres-MIN_NUM_FORMS": "0",
            "atmospheres-MAX_NUM_FORMS": "1000",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.realm.refresh_from_db()
        self.assertEqual(self.realm.name, "Updated Realm")
        self.assertEqual(self.realm.primary_sphere, SphereChoices.TIME)
