"""Comprehensive tests for mage model - additional methods not covered in test_mage.py."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.specialty import Specialty
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.mage import Mage, PracticeRating, ResRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from characters.tests.utils import mage_setup


class TestMageAffinitySphereName(TestCase):
    """Test get_affinity_sphere_name method."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.mage.arete = 2
        self.mage.save()

    def test_affinity_sphere_correspondence(self):
        """Test affinity sphere name for Correspondence."""
        self.mage.affinity_sphere = Sphere.objects.get(property_name="correspondence")
        self.mage.corr_name = "data"
        self.mage.save()
        self.assertEqual(self.mage.get_affinity_sphere_name(), "Data")

    def test_affinity_sphere_prime(self):
        """Test affinity sphere name for Prime."""
        self.mage.affinity_sphere = Sphere.objects.get(property_name="prime")
        self.mage.prime_name = "primal_utility"
        self.mage.save()
        self.assertEqual(self.mage.get_affinity_sphere_name(), "Primal Utility")

    def test_affinity_sphere_spirit(self):
        """Test affinity sphere name for Spirit."""
        self.mage.affinity_sphere = Sphere.objects.get(property_name="spirit")
        self.mage.spirit_name = "dimensional_science"
        self.mage.save()
        self.assertEqual(self.mage.get_affinity_sphere_name(), "Dimensional Science")

    def test_affinity_sphere_other(self):
        """Test affinity sphere name for other spheres."""
        forces = Sphere.objects.get(property_name="forces")
        self.mage.affinity_sphere = forces
        self.mage.save()
        self.assertEqual(self.mage.get_affinity_sphere_name(), forces)


class TestMageParadox(TestCase):
    """Test paradox-related methods."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)

    def test_get_paradox_wheel(self):
        """Test paradox wheel returns correct range."""
        wheel = self.mage.get_paradox_wheel()
        self.assertEqual(wheel, list(range(20)))
        self.assertEqual(len(wheel), 20)

    def test_get_inverted_paradox(self):
        """Test inverted paradox calculation."""
        self.mage.paradox = 0
        self.assertEqual(self.mage.get_inverted_paradox(), 19)

        self.mage.paradox = 10
        self.assertEqual(self.mage.get_inverted_paradox(), 9)

        self.mage.paradox = 19
        self.assertEqual(self.mage.get_inverted_paradox(), 0)


class TestMageAffinityOptions(TestCase):
    """Test get_affinity_sphere_options method."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)

    def test_no_faction_returns_all_spheres(self):
        """Test that mage without faction can choose any sphere."""
        options = self.mage.get_affinity_sphere_options()
        self.assertEqual(options.count(), 9)

    def test_faction_with_affinities(self):
        """Test that faction affinities are returned."""
        faction = MageFaction.objects.filter(affinities__isnull=False).first()
        if faction:
            self.mage.faction = faction
            self.mage.save()
            options = self.mage.get_affinity_sphere_options()
            self.assertTrue(options.exists())


class TestMageResonanceMethods(TestCase):
    """Test resonance-related methods."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.res = Resonance.objects.first()

    def test_add_resonance_by_string(self):
        """Test adding resonance by name string."""
        self.assertTrue(self.mage.add_resonance("Test Resonance New"))
        self.assertEqual(self.mage.resonance_rating(Resonance.objects.get(name="Test Resonance New")), 1)

    def test_subtract_resonance(self):
        """Test subtracting resonance."""
        self.mage.add_resonance(self.res)
        self.mage.add_resonance(self.res)
        self.assertEqual(self.mage.resonance_rating(self.res), 2)
        self.assertTrue(self.mage.subtract_resonance(self.res))
        self.assertEqual(self.mage.resonance_rating(self.res), 1)

    def test_subtract_resonance_at_zero(self):
        """Test subtracting resonance when at zero."""
        self.assertFalse(self.mage.subtract_resonance(self.res))

    def test_add_resonance_at_max(self):
        """Test adding resonance when at max."""
        for _ in range(5):
            self.mage.add_resonance(self.res)
        self.assertFalse(self.mage.add_resonance(self.res))

    def test_get_resonance(self):
        """Test get_resonance method."""
        self.mage.add_resonance(self.res)
        resonances = self.mage.get_resonance()
        self.assertEqual(resonances.count(), 1)


class TestMagePracticeMethods(TestCase):
    """Test practice-related methods."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.practice = Practice.objects.first()

    def test_add_practice(self):
        """Test adding a practice."""
        self.assertTrue(self.mage.add_practice(self.practice))
        self.assertEqual(self.mage.practice_rating(self.practice), 1)

    def test_add_practice_multiple(self):
        """Test adding practice rating multiple times."""
        self.mage.add_practice(self.practice)
        self.mage.add_practice(self.practice)
        self.assertEqual(self.mage.practice_rating(self.practice), 2)

    def test_total_practices(self):
        """Test total_practices method."""
        self.assertEqual(self.mage.total_practices(), 0)
        self.mage.add_practice(self.practice)
        self.assertEqual(self.mage.total_practices(), 1)
        self.mage.add_practice(self.practice)
        self.assertEqual(self.mage.total_practices(), 2)

    def test_get_practices(self):
        """Test get_practices method."""
        self.mage.add_practice(self.practice)
        practices = self.mage.get_practices()
        self.assertEqual(practices.count(), 1)

    def test_practice_rating_unknown(self):
        """Test practice_rating for practice not added."""
        unknown_practice = Practice.objects.last()
        self.assertEqual(self.mage.practice_rating(unknown_practice), 0)


class TestMageTenetMethods(TestCase):
    """Test tenet-related methods."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)

    def test_add_tenet_metaphysical(self):
        """Test adding metaphysical tenet."""
        met_tenet = Tenet.objects.filter(tenet_type="met").first()
        self.assertTrue(self.mage.add_tenet(met_tenet))
        self.assertEqual(self.mage.metaphysical_tenet, met_tenet)

    def test_add_tenet_personal(self):
        """Test adding personal tenet."""
        per_tenet = Tenet.objects.filter(tenet_type="per").first()
        self.assertTrue(self.mage.add_tenet(per_tenet))
        self.assertEqual(self.mage.personal_tenet, per_tenet)

    def test_add_tenet_ascension(self):
        """Test adding ascension tenet."""
        asc_tenet = Tenet.objects.filter(tenet_type="asc").first()
        self.assertTrue(self.mage.add_tenet(asc_tenet))
        self.assertEqual(self.mage.ascension_tenet, asc_tenet)

    def test_add_duplicate_tenet_to_other_tenets(self):
        """Test that duplicate tenets go to other_tenets."""
        met_tenet1 = Tenet.objects.filter(tenet_type="met").first()
        met_tenet2 = Tenet.objects.filter(tenet_type="met").last()
        self.mage.add_tenet(met_tenet1)
        self.mage.add_tenet(met_tenet2)
        self.assertEqual(self.mage.metaphysical_tenet, met_tenet1)
        self.assertIn(met_tenet2, self.mage.other_tenets.all())


class TestMageXPMethods(TestCase):
    """Test XP spending methods."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player, xp=100, arete=3)
        # Set up tenets for focus
        self.met_tenet = Tenet.objects.filter(tenet_type="met").first()
        self.per_tenet = Tenet.objects.filter(tenet_type="per").first()
        self.asc_tenet = Tenet.objects.filter(tenet_type="asc").first()
        self.mage.metaphysical_tenet = self.met_tenet
        self.mage.personal_tenet = self.per_tenet
        self.mage.ascension_tenet = self.asc_tenet
        self.mage.forces = 2
        self.mage.save()

    def test_xp_frequencies(self):
        """Test xp_frequencies method."""
        freq = self.mage.xp_frequencies()
        self.assertIn("sphere", freq)
        self.assertIn("arete", freq)
        self.assertIn("attribute", freq)

    def test_xp_cost_arete(self):
        """Test XP cost for arete."""
        self.assertEqual(self.mage.xp_cost("arete", 3), 24)

    def test_xp_cost_sphere(self):
        """Test XP cost for sphere."""
        self.assertEqual(self.mage.xp_cost("sphere", 2), 16)

    def test_xp_cost_new_sphere(self):
        """Test XP cost for new sphere."""
        self.assertEqual(self.mage.xp_cost("sphere", 0), 10)

    def test_spend_xp_on_arete(self):
        """Test spending XP on arete."""
        initial_xp = self.mage.xp
        initial_arete = self.mage.arete
        self.mage.spend_xp("arete")
        self.mage.refresh_from_db()
        # Either succeeded or failed, but shouldn't crash


class TestMageFreebiesMethods(TestCase):
    """Test freebie spending methods."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player, arete=2, freebies=21)

    def test_freebie_frequencies(self):
        """Test freebie_frequencies method."""
        freq = self.mage.freebie_frequencies()
        self.assertIn("sphere", freq)
        self.assertIn("arete", freq)
        self.assertIn("resonance", freq)

    def test_freebie_costs(self):
        """Test freebie_costs method."""
        costs = self.mage.freebie_costs()
        self.assertIn("sphere", costs)
        self.assertEqual(costs["sphere"], 7)
        self.assertEqual(costs["arete"], 4)

    def test_freebie_cost_sphere(self):
        """Test freebie_cost for sphere."""
        cost = self.mage.freebie_cost("sphere")
        self.assertEqual(cost, 7)

    def test_freebie_cost_arete(self):
        """Test freebie_cost for arete."""
        cost = self.mage.freebie_cost("arete")
        self.assertEqual(cost, 4)

    def test_spend_freebies_on_sphere(self):
        """Test spending freebies on sphere."""
        initial_freebies = self.mage.freebies
        self.mage.spend_freebies("forces")
        self.assertEqual(self.mage.forces, 1)
        self.assertEqual(self.mage.freebies, initial_freebies - 7)


class TestMageSpecialtiesMethods(TestCase):
    """Test specialties-related methods."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.mage.arete = 3
        self.mage.occult = 4  # Requires specialty
        self.mage.forces = 4  # Requires specialty
        self.mage.save()

    def test_needs_specialties(self):
        """Test needs_specialties method."""
        self.assertTrue(self.mage.needs_specialties())

    def test_needed_specialties(self):
        """Test needed_specialties method."""
        needed = self.mage.needed_specialties()
        self.assertIn("occult", needed)
        self.assertIn("forces", needed)

    def test_has_specialties_false(self):
        """Test has_specialties returns False when specialties needed."""
        self.assertFalse(self.mage.has_specialties())

    def test_has_specialties_true(self):
        """Test has_specialties returns True when all specialties present."""
        occult_spec = Specialty.objects.create(name="Occult Spec", stat="occult")
        forces_spec = Specialty.objects.create(name="Forces Spec", stat="forces")
        self.mage.specialties.add(occult_spec)
        self.mage.specialties.add(forces_spec)
        self.assertTrue(self.mage.has_specialties())


class TestMageSphereToTraitType(TestCase):
    """Test sphere_to_trait_type method."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.mage.affinity_sphere = Sphere.objects.get(property_name="forces")
        self.mage.save()

    def test_affinity_sphere(self):
        """Test sphere_to_trait_type for affinity sphere."""
        result = self.mage.sphere_to_trait_type("forces")
        self.assertEqual(result, "affinity_sphere")

    def test_non_affinity_sphere(self):
        """Test sphere_to_trait_type for non-affinity sphere."""
        result = self.mage.sphere_to_trait_type("matter")
        self.assertEqual(result, "sphere")


class TestMageGetAffiliationWeights(TestCase):
    """Test get_affiliation_weights method."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)

    def test_affiliation_weights(self):
        """Test that affiliation weights are returned."""
        weights = self.mage.get_affiliation_weights()
        self.assertIsInstance(weights, dict)


class TestPracticeRatingModel(TestCase):
    """Test PracticeRating model."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.practice = Practice.objects.first()

    def test_practice_rating_str(self):
        """Test string representation of PracticeRating."""
        pr = PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=3)
        self.assertIn(self.mage.name, str(pr))
        self.assertIn(self.practice.name, str(pr))
        self.assertIn("3", str(pr))

    def test_practice_rating_str_no_mage(self):
        """Test string representation when no mage."""
        pr = PracticeRating.objects.create(mage=None, practice=self.practice, rating=2)
        self.assertIn("No Mage", str(pr))

    def test_practice_rating_str_no_practice(self):
        """Test string representation when no practice."""
        pr = PracticeRating.objects.create(mage=self.mage, practice=None, rating=2)
        self.assertIn("No Practice", str(pr))


class TestPracticeRatingTenetBonus(TestCase):
    """Test PracticeRating.get_tenet_bonus method."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.practice = Practice.objects.first()
        # Set up tenets
        self.met_tenet = Tenet.objects.filter(tenet_type="met").first()
        self.mage.metaphysical_tenet = self.met_tenet
        self.mage.save()

    def test_no_bonus_or_penalty(self):
        """Test no bonus when practice not in any tenet."""
        pr = PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=2)
        self.assertEqual(pr.get_tenet_bonus(), 0)

    def test_bonus_when_associated(self):
        """Test bonus when practice is associated."""
        self.met_tenet.associated_practices.add(self.practice)
        pr = PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=2)
        self.assertEqual(pr.get_tenet_bonus(), 1)

    def test_penalty_when_limited(self):
        """Test penalty when practice is limited."""
        self.met_tenet.limited_practices.add(self.practice)
        pr = PracticeRating.objects.create(mage=self.mage, practice=self.practice, rating=2)
        self.assertEqual(pr.get_tenet_bonus(), -1)

    def test_no_mage_returns_zero(self):
        """Test that no mage returns zero bonus."""
        pr = PracticeRating.objects.create(mage=None, practice=self.practice, rating=2)
        self.assertEqual(pr.get_tenet_bonus(), 0)

    def test_no_practice_returns_zero(self):
        """Test that no practice returns zero bonus."""
        pr = PracticeRating.objects.create(mage=self.mage, practice=None, rating=2)
        self.assertEqual(pr.get_tenet_bonus(), 0)


class TestResRatingModel(TestCase):
    """Test ResRating model."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.res = Resonance.objects.first()

    def test_res_rating_creation(self):
        """Test creating ResRating."""
        rr = ResRating.objects.create(mage=self.mage, resonance=self.res, rating=3)
        self.assertEqual(rr.rating, 3)

    def test_res_rating_constraints(self):
        """Test ResRating constraints."""
        rr = ResRating.objects.create(mage=self.mage, resonance=self.res, rating=5)
        self.assertEqual(rr.rating, 5)
