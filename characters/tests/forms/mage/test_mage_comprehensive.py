"""Comprehensive tests for mage forms."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.forms.mage.mage import MageCreationForm, MageSpheresForm
from characters.models.core.archetype import Archetype
from characters.models.mage.faction import MageFaction
from characters.models.mage.mage import Mage
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from characters.tests.utils import mage_setup


class TestMageCreationForm(TestCase):
    """Test MageCreationForm."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test", password="password")
        self.st = User.objects.create_user(username="ST", password="password")
        # Set up ST profile
        from game.models import Chronicle

        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)

        self.affiliation = MageFaction.objects.filter(parent=None).first()
        self.faction = MageFaction.objects.filter(parent=self.affiliation).first()
        self.nature = Archetype.objects.first()
        self.demeanor = Archetype.objects.last()

    def test_form_initialization(self):
        """Test form initializes correctly."""
        form = MageCreationForm(user=self.player)
        self.assertIn("name", form.fields)
        self.assertIn("affiliation", form.fields)
        self.assertIn("faction", form.fields)
        self.assertIn("subfaction", form.fields)

    def test_form_excludes_nephandi_for_non_st(self):
        """Test form excludes Nephandi for non-storytellers."""
        nephandi = MageFaction.objects.create(name="Nephandi", parent=None)
        form = MageCreationForm(user=self.player)
        self.assertNotIn(nephandi, form.fields["affiliation"].queryset)

    def test_form_excludes_marauders_for_non_st(self):
        """Test form excludes Marauders for non-storytellers."""
        marauders = MageFaction.objects.create(name="Marauders", parent=None)
        form = MageCreationForm(user=self.player)
        self.assertNotIn(marauders, form.fields["affiliation"].queryset)

    def test_form_includes_nephandi_for_st(self):
        """Test form includes Nephandi for storytellers."""
        nephandi = MageFaction.objects.create(name="Nephandi", parent=None)
        form = MageCreationForm(user=self.st)
        self.assertIn(nephandi, form.fields["affiliation"].queryset)

    def test_form_valid_data(self):
        """Test form with valid data."""
        form = MageCreationForm(
            user=self.player,
            data={
                "name": "Test Mage",
                "nature": self.nature.id,
                "demeanor": self.demeanor.id,
                "concept": "Test Concept",
                "affiliation": self.affiliation.id,
                "faction": str(self.faction.id),  # ChainedChoiceField expects string
                "essence": "Dynamic",
            },
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_save_sets_owner(self):
        """Test form save sets owner."""
        form = MageCreationForm(
            user=self.player,
            data={
                "name": "Test Mage",
                "nature": self.nature.id,
                "demeanor": self.demeanor.id,
                "concept": "Test Concept",
                "affiliation": self.affiliation.id,
                "faction": str(self.faction.id),  # ChainedChoiceField expects string
                "essence": "Dynamic",
            },
        )
        if form.is_valid():
            mage = form.save()
            self.assertEqual(mage.owner, self.player)

    def test_form_faction_uses_chained_select(self):
        """Test faction field uses ChainedChoiceField with choices_callback."""
        form = MageCreationForm(user=self.player)
        # ChainedChoiceField uses choices_callback instead of queryset
        self.assertTrue(hasattr(form.fields["faction"], "choices_callback"))
        self.assertIsNotNone(form.fields["faction"].choices_callback)


class TestMageSpheresForm(TestCase):
    """Test MageSpheresForm."""

    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player)
        self.forces = Sphere.objects.get(property_name="forces")
        self.resonance = Resonance.objects.create(name="Dynamic", forces=True)

    def test_form_initialization(self):
        """Test form initializes correctly."""
        form = MageSpheresForm(instance=self.mage)
        self.assertIn("arete", form.fields)
        self.assertIn("correspondence", form.fields)
        self.assertIn("affinity_sphere", form.fields)

    def test_clean_arete_valid(self):
        """Test clean_arete with valid value."""
        form = MageSpheresForm(
            instance=self.mage,
            data={
                "arete": 2,
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "forces": 2,  # Spheres must be <= arete
                "matter": 2,
                "life": 0,
                "entropy": 0,
                "mind": 0,
                "prime": 2,
                "affinity_sphere": self.forces.id,
                "corr_name": "correspondence",
                "prime_name": "prime",
                "spirit_name": "spirit",
                "resonance": [self.resonance.id],
            },
        )
        self.assertTrue(form.is_valid())

    def test_clean_arete_too_high(self):
        """Test clean_arete rejects values above 3."""
        form = MageSpheresForm(
            instance=self.mage,
            data={
                "arete": 5,
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "forces": 3,
                "matter": 0,
                "life": 0,
                "entropy": 0,
                "mind": 0,
                "prime": 3,
                "affinity_sphere": self.forces.id,
                "corr_name": "correspondence",
                "prime_name": "prime",
                "spirit_name": "spirit",
                "resonance": [self.resonance.id],
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("arete", form.errors)

    def test_clean_affinity_sphere_required(self):
        """Test affinity sphere is required."""
        form = MageSpheresForm(
            instance=self.mage,
            data={
                "arete": 2,
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "forces": 3,
                "matter": 0,
                "life": 0,
                "entropy": 0,
                "mind": 0,
                "prime": 3,
                "affinity_sphere": "",
                "corr_name": "correspondence",
                "prime_name": "prime",
                "spirit_name": "spirit",
                "resonance": [self.resonance.id],
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("affinity_sphere", form.errors)

    def test_clean_spheres_total_must_be_six(self):
        """Test spheres must total 6."""
        form = MageSpheresForm(
            instance=self.mage,
            data={
                "arete": 2,
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "forces": 2,
                "matter": 0,
                "life": 0,
                "entropy": 0,
                "mind": 0,
                "prime": 2,
                "affinity_sphere": self.forces.id,
                "corr_name": "correspondence",
                "prime_name": "prime",
                "spirit_name": "spirit",
                "resonance": [self.resonance.id],
            },
        )
        self.assertFalse(form.is_valid())
        # Should have an error about sphere total

    def test_clean_sphere_exceeds_arete(self):
        """Test sphere rating cannot exceed arete."""
        form = MageSpheresForm(
            instance=self.mage,
            data={
                "arete": 2,
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "forces": 3,  # Exceeds arete of 2
                "matter": 0,
                "life": 0,
                "entropy": 0,
                "mind": 0,
                "prime": 3,
                "affinity_sphere": self.forces.id,
                "corr_name": "correspondence",
                "prime_name": "prime",
                "spirit_name": "spirit",
                "resonance": [self.resonance.id],
            },
        )
        self.assertFalse(form.is_valid())

    def test_valid_sphere_distribution(self):
        """Test valid sphere distribution."""
        form = MageSpheresForm(
            instance=self.mage,
            data={
                "arete": 3,
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "forces": 3,
                "matter": 0,
                "life": 0,
                "entropy": 0,
                "mind": 0,
                "prime": 3,
                "affinity_sphere": self.forces.id,
                "corr_name": "correspondence",
                "prime_name": "prime",
                "spirit_name": "spirit",
                "resonance": [self.resonance.id],
            },
        )
        self.assertTrue(form.is_valid())
