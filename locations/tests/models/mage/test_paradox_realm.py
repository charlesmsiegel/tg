"""Tests for ParadoxRealm model."""

from unittest.mock import patch

from django.test import TestCase
from locations.models.mage.paradox_realm import (
    FinalObstacleTypeChoices,
    ParadoxAtmosphere,
    ParadoxObstacle,
    ParadoxRealm,
    ParadigmChoices,
    SphereChoices,
)


class TestParadoxRealmBasics(TestCase):
    """Test basic ParadoxRealm model functionality."""

    def test_paradox_realm_creation(self):
        """Test creating a basic paradox realm."""
        realm = ParadoxRealm.objects.create(
            name="Test Realm",
            primary_sphere=SphereChoices.CORRESPONDENCE,
            paradigm=ParadigmChoices.ANTIMAGICK,
        )
        self.assertEqual(realm.name, "Test Realm")
        self.assertEqual(realm.primary_sphere, SphereChoices.CORRESPONDENCE)
        self.assertEqual(realm.paradigm, ParadigmChoices.ANTIMAGICK)
        self.assertEqual(realm.type, "paradox_realm")
        self.assertEqual(realm.gameline, "mta")

    def test_paradox_realm_str(self):
        """Test string representation of paradox realm."""
        realm = ParadoxRealm.objects.create(
            name="Twisted Reality",
            primary_sphere=SphereChoices.ENTROPY,
        )
        self.assertIn("Twisted Reality", str(realm))
        self.assertIn("Entropy", str(realm))

    def test_paradox_realm_str_with_secondary_sphere(self):
        """Test string representation with secondary sphere."""
        realm = ParadoxRealm.objects.create(
            name="Dual Realm",
            primary_sphere=SphereChoices.FORCES,
            secondary_sphere=SphereChoices.MATTER,
        )
        result = str(realm)
        self.assertIn("Dual Realm", result)
        self.assertIn("Forces", result)
        self.assertIn("Matter", result)

    def test_paradox_realm_defaults(self):
        """Test default values for paradox realm."""
        realm = ParadoxRealm.objects.create(name="Default Realm")
        self.assertEqual(realm.primary_sphere, SphereChoices.CORRESPONDENCE)
        self.assertEqual(realm.paradigm, ParadigmChoices.ANTIMAGICK)
        self.assertEqual(realm.num_primary_obstacles, 0)
        self.assertEqual(realm.num_random_obstacles, 0)
        self.assertEqual(realm.final_obstacle_type, FinalObstacleTypeChoices.MAZE)
        self.assertEqual(realm.atmosphere_details, [])
        self.assertEqual(realm.final_obstacle_details, {})

    def test_paradox_realm_get_heading(self):
        """Test get_heading returns correct gameline heading."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        self.assertEqual(realm.get_heading(), "mta_heading")

    def test_paradox_realm_get_update_url(self):
        """Test get_update_url returns valid URL."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        url = realm.get_update_url()
        self.assertIn(str(realm.id), url)
        self.assertIn("paradox_realm", url)

    def test_paradox_realm_get_creation_url(self):
        """Test get_creation_url returns valid URL."""
        url = ParadoxRealm.get_creation_url()
        self.assertIn("paradox_realm", url)

    def test_paradox_realm_get_obstacles(self):
        """Test get_obstacles returns ordered obstacles."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        obs1 = ParadoxObstacle.objects.create(
            realm=realm,
            sphere=SphereChoices.ENTROPY,
            obstacle_number=1,
            order=2,
            name="Second",
        )
        obs2 = ParadoxObstacle.objects.create(
            realm=realm,
            sphere=SphereChoices.FORCES,
            obstacle_number=2,
            order=1,
            name="First",
        )
        obstacles = realm.get_obstacles()
        self.assertEqual(obstacles[0], obs2)
        self.assertEqual(obstacles[1], obs1)

    def test_paradox_realm_get_atmosphere_elements(self):
        """Test get_atmosphere_elements returns all atmospheres."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        atm1 = ParadoxAtmosphere.objects.create(
            realm=realm,
            paradigm=ParadigmChoices.CHAOS,
            atmosphere_number=1,
            description="Chaos atmosphere",
        )
        atm2 = ParadoxAtmosphere.objects.create(
            realm=realm,
            paradigm=ParadigmChoices.DATA,
            atmosphere_number=2,
            description="Data atmosphere",
        )
        atmospheres = realm.get_atmosphere_elements()
        self.assertEqual(atmospheres.count(), 2)
        self.assertIn(atm1, atmospheres)
        self.assertIn(atm2, atmospheres)


class TestParadoxRealmDice(TestCase):
    """Test dice rolling methods."""

    def test_roll_d10(self):
        """Test d10 roll returns value in range 1-10."""
        for _ in range(100):
            result = ParadoxRealm.roll_d10()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 10)

    def test_roll_d5(self):
        """Test d5 roll returns value in range 1-5."""
        for _ in range(100):
            result = ParadoxRealm.roll_d5()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 5)

    def test_roll_2d10(self):
        """Test 2d10 roll returns value in range 2-20."""
        for _ in range(100):
            result = ParadoxRealm.roll_2d10()
            self.assertGreaterEqual(result, 2)
            self.assertLessEqual(result, 20)

    def test_roll_d100(self):
        """Test d100 roll returns value in range 1-100."""
        for _ in range(100):
            result = ParadoxRealm.roll_d100()
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 100)


class TestParadoxRealmRandomSphere(TestCase):
    """Test random sphere selection."""

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_correspondence(self, mock_roll):
        """Test roll 1 returns Correspondence."""
        mock_roll.return_value = 1
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.CORRESPONDENCE)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_entropy(self, mock_roll):
        """Test roll 2 returns Entropy."""
        mock_roll.return_value = 2
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.ENTROPY)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_forces(self, mock_roll):
        """Test roll 3 returns Forces."""
        mock_roll.return_value = 3
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.FORCES)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_life(self, mock_roll):
        """Test roll 4 returns Life."""
        mock_roll.return_value = 4
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.LIFE)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_matter(self, mock_roll):
        """Test roll 5 returns Matter."""
        mock_roll.return_value = 5
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.MATTER)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_mind(self, mock_roll):
        """Test roll 6 returns Mind."""
        mock_roll.return_value = 6
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.MIND)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_prime(self, mock_roll):
        """Test roll 7 returns Prime."""
        mock_roll.return_value = 7
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.PRIME)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_spirit(self, mock_roll):
        """Test roll 8 returns Spirit."""
        mock_roll.return_value = 8
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.SPIRIT)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_time(self, mock_roll):
        """Test roll 9 returns Time."""
        mock_roll.return_value = 9
        sphere = ParadoxRealm.random_sphere()
        self.assertEqual(sphere, SphereChoices.TIME)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_sphere_two_spheres(self, mock_roll):
        """Test roll 10 returns None (two spheres indicator)."""
        mock_roll.return_value = 10
        sphere = ParadoxRealm.random_sphere()
        self.assertIsNone(sphere)


class TestParadoxRealmRandomParadigm(TestCase):
    """Test random paradigm selection."""

    @patch.object(ParadoxRealm, "roll_2d10")
    def test_random_paradigm_unstable(self, mock_roll):
        """Test roll 1 returns Unstable."""
        mock_roll.return_value = 1
        paradigm, secondary = ParadoxRealm.random_paradigm()
        self.assertEqual(paradigm, ParadigmChoices.UNSTABLE)
        self.assertIsNone(secondary)

    @patch.object(ParadoxRealm, "roll_2d10")
    def test_random_paradigm_mechanistic(self, mock_roll):
        """Test roll 2 returns Mechanistic Cosmos."""
        mock_roll.return_value = 2
        paradigm, secondary = ParadoxRealm.random_paradigm()
        self.assertEqual(paradigm, ParadigmChoices.MECHANISTIC_COSMOS)

    @patch.object(ParadoxRealm, "roll_2d10")
    def test_random_paradigm_antimagick(self, mock_roll):
        """Test roll 17-19 returns Antimagick."""
        mock_roll.return_value = 17
        paradigm, _ = ParadoxRealm.random_paradigm()
        self.assertEqual(paradigm, ParadigmChoices.ANTIMAGICK)

    @patch.object(ParadoxRealm, "roll_2d10")
    def test_random_paradigm_two_paradigms(self, mock_roll):
        """Test roll 20 returns None (two paradigms indicator)."""
        mock_roll.return_value = 20
        paradigm, secondary = ParadoxRealm.random_paradigm()
        self.assertIsNone(paradigm)
        self.assertIsNone(secondary)

    @patch.object(ParadoxRealm, "roll_2d10")
    def test_random_paradigm_characters_paradigm(self, mock_roll):
        """Test roll 14-16 returns a valid paradigm (character's paradigm)."""
        mock_roll.return_value = 14
        paradigm, _ = ParadoxRealm.random_paradigm()
        # Should be one of the valid paradigms (not UNSTABLE)
        self.assertIsNotNone(paradigm)
        self.assertNotEqual(paradigm, ParadigmChoices.UNSTABLE)


class TestParadoxRealmRandomObstacleCount(TestCase):
    """Test random obstacle count selection."""

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_obstacle_count_no_obstacles(self, mock_roll):
        """Test roll 1 returns 0 obstacles."""
        mock_roll.return_value = 1
        primary, random = ParadoxRealm.random_obstacle_count()
        self.assertEqual(primary, 0)
        self.assertEqual(random, 0)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_obstacle_count_one_primary(self, mock_roll):
        """Test roll 2 returns 1 primary obstacle."""
        mock_roll.return_value = 2
        primary, random = ParadoxRealm.random_obstacle_count()
        self.assertEqual(primary, 1)
        self.assertEqual(random, 0)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_obstacle_count_two_primary(self, mock_roll):
        """Test roll 3 returns 2 primary obstacles."""
        mock_roll.return_value = 3
        primary, random = ParadoxRealm.random_obstacle_count()
        self.assertEqual(primary, 2)
        self.assertEqual(random, 0)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_obstacle_count_three_primary(self, mock_roll):
        """Test roll 4 returns 3 primary obstacles."""
        mock_roll.return_value = 4
        primary, random = ParadoxRealm.random_obstacle_count()
        self.assertEqual(primary, 3)
        self.assertEqual(random, 0)

    @patch.object(ParadoxRealm, "roll_d10")
    @patch.object(ParadoxRealm, "roll_d5")
    def test_random_obstacle_count_d5_primary(self, mock_d5, mock_d10):
        """Test roll 5 returns d5 primary obstacles."""
        mock_d10.return_value = 5
        mock_d5.return_value = 4
        primary, random = ParadoxRealm.random_obstacle_count()
        self.assertEqual(primary, 4)
        self.assertEqual(random, 0)

    @patch.object(ParadoxRealm, "roll_d10")
    @patch.object(ParadoxRealm, "roll_d5")
    def test_random_obstacle_count_mixed(self, mock_d5, mock_d10):
        """Test roll 6 returns d5 primary and 1 random obstacle."""
        mock_d10.return_value = 6
        mock_d5.return_value = 3
        primary, random = ParadoxRealm.random_obstacle_count()
        self.assertEqual(primary, 3)
        self.assertEqual(random, 1)


class TestParadoxRealmRandomFinalObstacle(TestCase):
    """Test random final obstacle selection."""

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_final_obstacle_give_secret(self, mock_roll):
        """Test roll 1 returns Give Secret."""
        mock_roll.return_value = 1
        obstacle, _ = ParadoxRealm.random_final_obstacle()
        self.assertEqual(obstacle, FinalObstacleTypeChoices.GIVE_SECRET)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_final_obstacle_win_game(self, mock_roll):
        """Test roll 2 returns Win Game."""
        mock_roll.return_value = 2
        obstacle, _ = ParadoxRealm.random_final_obstacle()
        self.assertEqual(obstacle, FinalObstacleTypeChoices.WIN_GAME)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_final_obstacle_maze(self, mock_roll):
        """Test roll 5 returns Standard Maze."""
        mock_roll.return_value = 5
        obstacle, _ = ParadoxRealm.random_final_obstacle()
        self.assertEqual(obstacle, FinalObstacleTypeChoices.MAZE)

    @patch.object(ParadoxRealm, "roll_d10")
    def test_random_final_obstacle_combined(self, mock_roll):
        """Test roll 10 returns Combined."""
        mock_roll.return_value = 10
        obstacle, _ = ParadoxRealm.random_final_obstacle()
        self.assertEqual(obstacle, FinalObstacleTypeChoices.COMBINED)


class TestParadoxRealmRandom(TestCase):
    """Test complete random realm generation."""

    def test_random_creates_realm(self):
        """Test random() creates a realm without saving."""
        realm = ParadoxRealm.random(name="Random Test", save=False)
        self.assertEqual(realm.name, "Random Test")
        self.assertIsNone(realm.pk)  # Not saved

    def test_random_saves_realm(self):
        """Test random() with save=True saves realm."""
        realm = ParadoxRealm.random(name="Saved Random", save=True)
        self.assertEqual(realm.name, "Saved Random")
        self.assertIsNotNone(realm.pk)

    def test_random_generates_valid_spheres(self):
        """Test random() generates valid sphere values."""
        realm = ParadoxRealm.random()
        self.assertIn(realm.primary_sphere, SphereChoices.values)
        if realm.secondary_sphere:
            self.assertIn(realm.secondary_sphere, SphereChoices.values)

    def test_random_generates_valid_paradigm(self):
        """Test random() generates valid paradigm values."""
        realm = ParadoxRealm.random()
        self.assertIn(realm.paradigm, ParadigmChoices.values)
        if realm.secondary_paradigm:
            self.assertIn(realm.secondary_paradigm, ParadigmChoices.values)

    def test_random_generates_obstacles_when_saved(self):
        """Test random() generates obstacles when saved."""
        realm = ParadoxRealm.random(save=True)
        expected_total = realm.num_primary_obstacles + realm.num_random_obstacles
        self.assertEqual(realm.realm_obstacles.count(), expected_total)

    def test_random_generates_atmospheres_when_saved(self):
        """Test random() generates atmospheres when saved."""
        realm = ParadoxRealm.random(save=True)
        # Should have 2-3 atmosphere elements
        self.assertGreaterEqual(realm.realm_atmospheres.count(), 2)
        self.assertLessEqual(realm.realm_atmospheres.count(), 3)


class TestParadoxObstacle(TestCase):
    """Test ParadoxObstacle model."""

    def test_obstacle_creation(self):
        """Test creating an obstacle."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        obstacle = ParadoxObstacle.objects.create(
            realm=realm,
            sphere=SphereChoices.FORCES,
            obstacle_number=3,
            order=1,
            name="Gap",
            description="A gap in the forces",
        )
        self.assertEqual(obstacle.realm, realm)
        self.assertEqual(obstacle.sphere, SphereChoices.FORCES)
        self.assertEqual(obstacle.obstacle_number, 3)
        self.assertEqual(obstacle.name, "Gap")

    def test_obstacle_str(self):
        """Test obstacle string representation."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        obstacle = ParadoxObstacle.objects.create(
            realm=realm,
            sphere=SphereChoices.MIND,
            obstacle_number=1,
            name="Two Guards",
        )
        result = str(obstacle)
        self.assertIn("Two Guards", result)
        self.assertIn("Mind", result)

    def test_obstacle_ordering(self):
        """Test obstacles are ordered by order field."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        obs3 = ParadoxObstacle.objects.create(
            realm=realm, sphere=SphereChoices.TIME, obstacle_number=1, order=3, name="Third"
        )
        obs1 = ParadoxObstacle.objects.create(
            realm=realm, sphere=SphereChoices.TIME, obstacle_number=2, order=1, name="First"
        )
        obs2 = ParadoxObstacle.objects.create(
            realm=realm, sphere=SphereChoices.TIME, obstacle_number=3, order=2, name="Second"
        )
        obstacles = list(ParadoxObstacle.objects.filter(realm=realm))
        self.assertEqual(obstacles[0], obs1)
        self.assertEqual(obstacles[1], obs2)
        self.assertEqual(obstacles[2], obs3)

    def test_get_obstacle_name_correspondence(self):
        """Test get_obstacle_name for Correspondence sphere."""
        name = ParadoxObstacle.get_obstacle_name(SphereChoices.CORRESPONDENCE, 1)
        self.assertEqual(name, "Leaning Walls")

    def test_get_obstacle_name_entropy(self):
        """Test get_obstacle_name for Entropy sphere."""
        name = ParadoxObstacle.get_obstacle_name(SphereChoices.ENTROPY, 1)
        self.assertEqual(name, "Shell Game")

    def test_get_obstacle_name_forces(self):
        """Test get_obstacle_name for Forces sphere."""
        name = ParadoxObstacle.get_obstacle_name(SphereChoices.FORCES, 4)
        self.assertEqual(name, "Fire")

    def test_get_obstacle_name_unknown(self):
        """Test get_obstacle_name for unknown sphere/roll."""
        name = ParadoxObstacle.get_obstacle_name("unknown", 99)
        self.assertIn("99", name)

    def test_obstacle_random(self):
        """Test random obstacle generation."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        obstacle = ParadoxObstacle.random(
            realm=realm, sphere=SphereChoices.LIFE, order=0, save=False
        )
        self.assertEqual(obstacle.realm, realm)
        self.assertEqual(obstacle.sphere, SphereChoices.LIFE)
        self.assertIsNone(obstacle.pk)

    def test_obstacle_random_save(self):
        """Test random obstacle generation with save."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        obstacle = ParadoxObstacle.random(
            realm=realm, sphere=SphereChoices.MATTER, order=0, save=True
        )
        self.assertIsNotNone(obstacle.pk)


class TestParadoxAtmosphere(TestCase):
    """Test ParadoxAtmosphere model."""

    def test_atmosphere_creation(self):
        """Test creating an atmosphere element."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        atmosphere = ParadoxAtmosphere.objects.create(
            realm=realm,
            paradigm=ParadigmChoices.CHAOS,
            atmosphere_number=1,
            description="Pulsating colors",
        )
        self.assertEqual(atmosphere.realm, realm)
        self.assertEqual(atmosphere.paradigm, ParadigmChoices.CHAOS)
        self.assertEqual(atmosphere.atmosphere_number, 1)

    def test_atmosphere_str(self):
        """Test atmosphere string representation."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        atmosphere = ParadoxAtmosphere.objects.create(
            realm=realm,
            paradigm=ParadigmChoices.DATA,
            atmosphere_number=5,
            description="Wireframe world",
        )
        result = str(atmosphere)
        self.assertIn("Data", result)
        self.assertIn("5", result)

    def test_get_atmosphere_description_antimagick(self):
        """Test get_atmosphere_description for Antimagick paradigm."""
        desc = ParadoxAtmosphere.get_atmosphere_description(ParadigmChoices.ANTIMAGICK, 1)
        self.assertIn("chains", desc.lower())

    def test_get_atmosphere_description_chaos(self):
        """Test get_atmosphere_description for Chaos paradigm."""
        desc = ParadoxAtmosphere.get_atmosphere_description(ParadigmChoices.CHAOS, 1)
        self.assertIn("color", desc.lower())

    def test_get_atmosphere_description_unknown(self):
        """Test get_atmosphere_description for unknown paradigm."""
        desc = ParadoxAtmosphere.get_atmosphere_description("unknown", 99)
        self.assertIn("99", desc)

    def test_atmosphere_random(self):
        """Test random atmosphere generation."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        atmosphere = ParadoxAtmosphere.random(
            realm=realm, paradigm=ParadigmChoices.FAITH, save=False
        )
        self.assertEqual(atmosphere.realm, realm)
        self.assertEqual(atmosphere.paradigm, ParadigmChoices.FAITH)
        self.assertIsNone(atmosphere.pk)

    def test_atmosphere_random_save(self):
        """Test random atmosphere generation with save."""
        realm = ParadoxRealm.objects.create(name="Test Realm")
        atmosphere = ParadoxAtmosphere.random(
            realm=realm, paradigm=ParadigmChoices.TECH, save=True
        )
        self.assertIsNotNone(atmosphere.pk)


class TestSphereChoices(TestCase):
    """Test SphereChoices enumeration."""

    def test_all_spheres_present(self):
        """Test all nine spheres are present."""
        spheres = SphereChoices.values
        self.assertEqual(len(spheres), 9)
        self.assertIn("correspondence", spheres)
        self.assertIn("entropy", spheres)
        self.assertIn("forces", spheres)
        self.assertIn("life", spheres)
        self.assertIn("matter", spheres)
        self.assertIn("mind", spheres)
        self.assertIn("prime", spheres)
        self.assertIn("spirit", spheres)
        self.assertIn("time", spheres)


class TestParadigmChoices(TestCase):
    """Test ParadigmChoices enumeration."""

    def test_paradigm_choices_exist(self):
        """Test paradigm choices are defined."""
        self.assertGreater(len(ParadigmChoices.values), 0)

    def test_antimagick_paradigm(self):
        """Test antimagick paradigm exists."""
        self.assertIn(ParadigmChoices.ANTIMAGICK, ParadigmChoices.values)

    def test_unstable_paradigm(self):
        """Test unstable paradigm exists."""
        self.assertIn(ParadigmChoices.UNSTABLE, ParadigmChoices.values)


class TestFinalObstacleTypeChoices(TestCase):
    """Test FinalObstacleTypeChoices enumeration."""

    def test_final_obstacle_choices_exist(self):
        """Test final obstacle choices are defined."""
        self.assertGreater(len(FinalObstacleTypeChoices.values), 0)

    def test_maze_obstacle_exists(self):
        """Test maze obstacle type exists."""
        self.assertIn(FinalObstacleTypeChoices.MAZE, FinalObstacleTypeChoices.values)

    def test_combined_obstacle_exists(self):
        """Test combined obstacle type exists."""
        self.assertIn(FinalObstacleTypeChoices.COMBINED, FinalObstacleTypeChoices.values)
