from unittest.mock import patch

from django.test import TestCase

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Instrument, Practice
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from core.models import Language, Noun
from items.models.core.material import Material
from items.models.core.medium import Medium
from items.models.mage.grimoire import Grimoire


class TestGrimoire(TestCase):
    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="Test Grimoire")
        self.faction = MageFaction.objects.create(name="Test Faction")
        science = Ability.objects.create(name="Science", property_name="science")
        art = Ability.objects.create(name="Art", property_name="art")
        crafts = Ability.objects.create(name="Crafts", property_name="crafts")
        self.abilities = [science, art, crafts]
        self.date_written = 1325
        self.language = Language.objects.create(name="Test Language")
        self.length = 100
        self.practices = [Practice.objects.create(name=f"Test Practice {i}") for i in range(3)]
        self.instruments = [
            Instrument.objects.create(name=f"Test Instrument {i}") for i in range(3)
        ]
        self.cover_material = Material.objects.create(name="Test Cover Material")
        self.inner_material = Material.objects.create(name="Test Inner Material")
        self.medium = Medium.objects.create(name="Test Medium")
        # Create an attribute and ability for Rote requirements
        attribute = Attribute.objects.create(name="Intelligence", property_name="intelligence")
        self.rotes = [
            Rote.objects.create(
                name=f"Test Rote {i}",
                effect=Effect.objects.create(name=f"Test Effect {i}"),
                attribute=attribute,
                ability=science,
            )
            for i in range(4)
        ]
        correspondence = Sphere.objects.create(
            name="Correspondence", property_name="correspondence"
        )
        forces = Sphere.objects.create(name="Forces", property_name="forces")
        matter = Sphere.objects.create(name="Matter", property_name="matter")
        self.spheres = [correspondence, forces, matter]

    def test_set_rank(self):
        self.assertEqual(self.grimoire.rank, 0)
        self.assertTrue(self.grimoire.set_rank(3))
        self.assertEqual(self.grimoire.rank, 3)

    def test_has_rank(self):
        self.assertFalse(self.grimoire.has_rank())
        self.grimoire.set_rank(3)
        self.assertTrue(self.grimoire.has_rank())

    def test_set_is_primer(self):
        self.assertFalse(self.grimoire.is_primer)
        self.assertTrue(self.grimoire.set_is_primer(True))
        self.assertTrue(self.grimoire.is_primer)

    def test_set_faction(self):
        self.assertIsNone(self.grimoire.faction)
        self.assertTrue(self.grimoire.set_faction(self.faction))
        self.assertEqual(self.grimoire.faction, self.faction)

    def test_has_faction(self):
        self.assertFalse(self.grimoire.has_faction())
        self.grimoire.set_faction(self.faction)
        self.assertTrue(self.grimoire.has_faction())

    def test_set_focus(self):
        self.assertEqual(self.grimoire.practices.count(), 0)
        self.assertEqual(self.grimoire.instruments.count(), 0)
        self.assertTrue(self.grimoire.set_focus(self.practices, self.instruments))
        self.assertEqual(set(self.grimoire.practices.all()), set(self.practices))
        self.assertEqual(set(self.grimoire.instruments.all()), set(self.instruments))

    def test_has_focus(self):
        self.assertFalse(self.grimoire.has_focus())
        self.grimoire.set_focus(self.practices, self.instruments)
        self.assertTrue(self.grimoire.has_focus())

    def test_set_abilities(self):
        self.assertEqual(self.grimoire.abilities.count(), 0)
        self.assertTrue(self.grimoire.set_abilities(self.abilities))
        self.assertEqual(set(self.grimoire.abilities.all()), set(self.abilities))

    def test_has_abilities(self):
        self.assertFalse(self.grimoire.has_abilities())
        self.grimoire.set_abilities(self.abilities)
        self.assertTrue(self.grimoire.has_abilities())

    def test_set_materials(self):
        self.assertIsNone(self.grimoire.cover_material)
        self.assertIsNone(self.grimoire.inner_material)
        self.assertTrue(self.grimoire.set_materials(self.cover_material, self.inner_material))
        self.assertEqual(self.grimoire.cover_material, self.cover_material)
        self.assertEqual(self.grimoire.inner_material, self.inner_material)

    def test_has_materials(self):
        self.assertFalse(self.grimoire.has_materials())
        self.grimoire.set_materials(self.cover_material, self.inner_material)
        self.assertTrue(self.grimoire.has_materials())

    def test_set_language(self):
        self.assertIsNone(self.grimoire.language)
        self.assertTrue(self.grimoire.set_language(self.language))
        self.assertEqual(self.grimoire.language, self.language)

    def test_has_language(self):
        self.assertFalse(self.grimoire.has_language())
        self.grimoire.set_language(self.language)
        self.assertTrue(self.grimoire.has_language())

    def test_set_medium(self):
        self.assertIsNone(self.grimoire.medium)
        self.assertTrue(self.grimoire.set_medium(self.medium))
        self.assertEqual(self.grimoire.medium, self.medium)

    def test_has_medium(self):
        self.assertFalse(self.grimoire.has_medium())
        self.grimoire.set_medium(self.medium)
        self.assertTrue(self.grimoire.has_medium())

    def test_set_length(self):
        self.assertEqual(self.grimoire.length, 0)
        self.assertTrue(self.grimoire.set_length(self.length))
        self.assertEqual(self.grimoire.length, self.length)

    def test_has_length(self):
        self.assertFalse(self.grimoire.has_length())
        self.grimoire.set_length(self.length)
        self.assertTrue(self.grimoire.has_length())

    def test_set_date_written(self):
        self.assertEqual(self.grimoire.date_written, -5000)
        self.assertTrue(self.grimoire.set_date_written(self.date_written))
        self.assertEqual(self.grimoire.date_written, self.date_written)

    def test_has_date_written(self):
        self.assertFalse(self.grimoire.has_date_written())
        self.grimoire.set_date_written(self.date_written)
        self.assertTrue(self.grimoire.has_date_written())

    def test_set_spheres(self):
        self.assertEqual(self.grimoire.spheres.count(), 0)
        self.assertTrue(self.grimoire.set_spheres(self.spheres))
        self.assertEqual(set(self.grimoire.spheres.all()), set(self.spheres))

    def test_has_spheres(self):
        self.assertFalse(self.grimoire.has_spheres())
        self.grimoire.set_spheres(self.spheres)
        self.assertTrue(self.grimoire.has_spheres())

    def test_set_rotes(self):
        self.assertEqual(self.grimoire.rotes.count(), 0)
        self.assertTrue(self.grimoire.set_rotes(self.rotes))
        self.assertEqual(set(self.grimoire.rotes.all()), set(self.rotes))

    def test_has_rotes(self):
        self.grimoire.rank = 4
        self.grimoire.save()
        self.grimoire.practices.add(Practice.objects.get(name="Test Practice 0"))
        self.grimoire.abilities.add(Ability.objects.get(name="Science"))
        self.grimoire.spheres.add(Sphere.objects.get(name="Forces"))
        self.assertFalse(self.grimoire.has_rotes())
        self.grimoire.set_rotes(self.rotes)
        self.assertTrue(self.grimoire.has_rotes())


class TestGrimoireDetailView(TestCase):
    def setUp(self) -> None:
        self.grimoire = Grimoire.objects.create(name="Test Grimoire")
        self.url = self.grimoire.get_absolute_url()

    def test_object_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_object_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/grimoire/detail.html")


class TestGrimoireCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Grimoire",
            "description": "Test",
            "date_written": 1000,
            "is_primer": False,
            "length": 3,
            "rank": 2,
            "background_cost": 4,
        }
        self.url = Grimoire.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/grimoire/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Grimoire.objects.count(), 1)
        self.assertEqual(Grimoire.objects.first().name, "Test Grimoire")


class TestGrimoireUpdateView(TestCase):
    def setUp(self):
        self.grimoire = Grimoire.objects.create(
            name="Test Grimoire",
            description="Test description",
        )
        self.valid_data = {
            "name": "Test Grimoire Updated",
            "description": "A test description for the grimoire.",
            "date_written": 1000,
            "is_primer": False,
            "length": 3,
            "rank": 2,
        }
        self.url = self.grimoire.get_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "items/mage/grimoire/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.grimoire.refresh_from_db()
        self.assertEqual(self.grimoire.name, "Test Grimoire Updated")
        self.assertEqual(self.grimoire.description, "A test description for the grimoire.")


class TestGrimoireUrls(TestCase):
    """Test URL generation methods for Grimoire."""

    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="URL Test Grimoire")

    def test_get_update_url(self):
        url = self.grimoire.get_update_url()
        self.assertIn(str(self.grimoire.id), url)
        self.assertIn("grimoire", url)

    def test_get_creation_url(self):
        url = Grimoire.get_creation_url()
        self.assertIn("grimoire", url)
        self.assertIn("create", url)


class TestGrimoireRankBoundaries(TestCase):
    """Test rank boundary clamping behavior."""

    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="Rank Test Grimoire")

    def test_set_rank_clamps_minimum(self):
        self.assertTrue(self.grimoire.set_rank(0))
        self.assertEqual(self.grimoire.rank, 1)

    def test_set_rank_clamps_negative(self):
        self.assertTrue(self.grimoire.set_rank(-5))
        self.assertEqual(self.grimoire.rank, 1)

    def test_set_rank_clamps_maximum(self):
        self.assertTrue(self.grimoire.set_rank(10))
        self.assertEqual(self.grimoire.rank, 5)

    def test_set_rank_within_bounds(self):
        for rank in range(1, 6):
            self.assertTrue(self.grimoire.set_rank(rank))
            self.assertEqual(self.grimoire.rank, rank)


class TestGrimoireAbilitiesValidation(TestCase):
    """Test set_abilities validation logic."""

    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="Ability Test Grimoire")
        self.ability = Ability.objects.create(name="Test Ability", property_name="test_ability")

    def test_set_abilities_with_valid_ability(self):
        result = self.grimoire.set_abilities([self.ability])
        self.assertTrue(result)
        self.assertIn(self.ability, self.grimoire.abilities.all())

    def test_set_abilities_with_non_ability_returns_false(self):
        result = self.grimoire.set_abilities(["not an ability"])
        self.assertFalse(result)

    def test_set_abilities_with_mixed_valid_invalid(self):
        result = self.grimoire.set_abilities([self.ability, "invalid"])
        self.assertFalse(result)


class TestGrimoireSpheresValidation(TestCase):
    """Test set_spheres validation logic."""

    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="Sphere Test Grimoire")
        self.sphere = Sphere.objects.create(name="Forces", property_name="forces")

    def test_set_spheres_with_valid_sphere(self):
        result = self.grimoire.set_spheres([self.sphere])
        self.assertTrue(result)
        self.assertIn(self.sphere, self.grimoire.spheres.all())

    def test_set_spheres_with_non_sphere_returns_false(self):
        result = self.grimoire.set_spheres(["not a sphere"])
        self.assertFalse(result)

    def test_set_spheres_with_mixed_valid_invalid(self):
        result = self.grimoire.set_spheres([self.sphere, "invalid"])
        self.assertFalse(result)


class TestGrimoireHasRotesLogic(TestCase):
    """Test has_rotes calculation with various combinations."""

    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="Rotes Test Grimoire")
        self.practice = Practice.objects.create(name="Test Practice")
        self.sphere = Sphere.objects.create(name="Forces", property_name="forces")
        self.ability = Ability.objects.create(name="Science", property_name="science")
        self.attribute = Attribute.objects.create(name="Intelligence", property_name="intelligence")
        self.effect = Effect.objects.create(name="Test Effect")
        self.rote = Rote.objects.create(
            name="Test Rote",
            effect=self.effect,
            attribute=self.attribute,
            ability=self.ability,
        )

    def test_has_rotes_formula_rank_4_one_each(self):
        """Rank 4 + 3 = 7 total needed. 1 practice + 1 sphere + 1 ability + 4 rotes = 7."""
        self.grimoire.rank = 4
        self.grimoire.save()
        self.grimoire.practices.add(self.practice)
        self.grimoire.spheres.add(self.sphere)
        self.grimoire.abilities.add(self.ability)

        # Without rotes: 1 + 1 + 1 = 3, need 7
        self.assertFalse(self.grimoire.has_rotes())

        # Add 4 rotes
        for i in range(4):
            effect = Effect.objects.create(name=f"Effect {i}")
            rote = Rote.objects.create(
                name=f"Rote {i}",
                effect=effect,
                attribute=self.attribute,
                ability=self.ability,
            )
            self.grimoire.rotes.add(rote)

        self.assertTrue(self.grimoire.has_rotes())

    def test_has_rotes_with_primer_subtracts_one(self):
        """is_primer counts as 1 toward the total."""
        self.grimoire.rank = 3  # 3 + 3 = 6 total needed
        self.grimoire.is_primer = True
        self.grimoire.save()
        self.grimoire.practices.add(self.practice)
        self.grimoire.spheres.add(self.sphere)
        self.grimoire.abilities.add(self.ability)

        # With primer: 1 + 1 + 1 + 1 (primer) = 4, need 6
        # Need 2 more rotes
        self.assertFalse(self.grimoire.has_rotes())

        for i in range(2):
            effect = Effect.objects.create(name=f"Primer Effect {i}")
            rote = Rote.objects.create(
                name=f"Primer Rote {i}",
                effect=effect,
                attribute=self.attribute,
                ability=self.ability,
            )
            self.grimoire.rotes.add(rote)

        self.assertTrue(self.grimoire.has_rotes())

    def test_has_rotes_with_multiple_spheres(self):
        """Multiple spheres each contribute to the total."""
        sphere2 = Sphere.objects.create(name="Matter", property_name="matter")
        self.grimoire.rank = 3  # 3 + 3 = 6 total
        self.grimoire.save()
        self.grimoire.practices.add(self.practice)
        self.grimoire.spheres.add(self.sphere)
        self.grimoire.spheres.add(sphere2)  # 2 spheres
        self.grimoire.abilities.add(self.ability)

        # 1 practice + 2 spheres + 1 ability = 4, need 6
        # Need 2 rotes
        for i in range(2):
            effect = Effect.objects.create(name=f"Multi Sphere Effect {i}")
            rote = Rote.objects.create(
                name=f"Multi Sphere Rote {i}",
                effect=effect,
                attribute=self.attribute,
                ability=self.ability,
            )
            self.grimoire.rotes.add(rote)

        self.assertTrue(self.grimoire.has_rotes())


class TestGrimoireRandomMethods(TestCase):
    """Test random generation methods for Grimoire."""

    @classmethod
    def setUpTestData(cls):
        # Create required reference data
        cls.faction = MageFaction.objects.create(name="Order of Hermes", founded=1000)
        cls.practice = Practice.objects.create(name="High Ritual")
        cls.instrument = Instrument.objects.create(name="Wand")
        cls.practice.instruments.add(cls.instrument)
        cls.faction.practices.add(cls.practice)

        cls.language = Language.objects.create(name="Latin", frequency=5)
        cls.faction.languages.add(cls.language)

        cls.sphere = Sphere.objects.create(name="Forces", property_name="forces")
        cls.sphere2 = Sphere.objects.create(name="Matter", property_name="matter")
        cls.faction.affinities.add(cls.sphere)

        cls.ability = Ability.objects.create(name="Occult", property_name="occult")
        cls.practice.abilities.add(cls.ability)

        cls.cover_material = Material.objects.create(name="Leather", is_hard=False)
        cls.inner_material = Material.objects.create(name="Vellum", is_hard=False)

        cls.medium = Medium.objects.create(
            name="Codex", length_modifier=1, length_modifier_type="*"
        )
        cls.faction.media.add(cls.medium)

        cls.noun = Noun.objects.create(name="mysteries")
        cls.noun2 = Noun.objects.create(name="secrets")

        cls.resonance = Resonance.objects.create(name="Dynamic", forces=True)

        cls.attribute = Attribute.objects.create(name="Intelligence", property_name="intelligence")

    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="Random Test Grimoire")

    def test_random_rank_produces_valid_rank(self):
        self.grimoire.random_rank()
        self.assertGreaterEqual(self.grimoire.rank, 1)
        self.assertLessEqual(self.grimoire.rank, 5)

    def test_random_rank_with_specific_value(self):
        self.grimoire.random_rank(rank=3)
        self.assertEqual(self.grimoire.rank, 3)

    def test_random_is_primer(self):
        # Test with explicit value
        self.grimoire.random_is_primer(is_primer=True)
        self.assertTrue(self.grimoire.is_primer)

        self.grimoire.random_is_primer(is_primer=False)
        self.assertFalse(self.grimoire.is_primer)

    @patch("random.random")
    def test_random_is_primer_uses_probability(self, mock_random):
        mock_random.return_value = 0.05  # Below 0.1 threshold
        self.grimoire.random_is_primer()
        self.assertTrue(self.grimoire.is_primer)

        mock_random.return_value = 0.5  # Above 0.1 threshold
        self.grimoire.random_is_primer()
        self.assertFalse(self.grimoire.is_primer)

    def test_random_faction_with_specific_value(self):
        self.grimoire.random_faction(faction=self.faction)
        self.assertEqual(self.grimoire.faction, self.faction)

    def test_random_faction_when_no_faction_exists(self):
        # This may raise an error if no factions exist
        self.grimoire.random_faction()
        self.assertIsNotNone(self.grimoire.faction)

    def test_random_medium_with_specific_value(self):
        self.grimoire.random_medium(medium=self.medium)
        self.assertEqual(self.grimoire.medium, self.medium)

    def test_random_medium_without_faction(self):
        self.grimoire.random_medium()
        self.assertIsNotNone(self.grimoire.medium)

    def test_random_medium_with_faction(self):
        self.grimoire.faction = self.faction
        self.grimoire.save()
        self.grimoire.random_medium()
        self.assertIsNotNone(self.grimoire.medium)

    def test_random_language_with_specific_value(self):
        self.grimoire.random_language(language=self.language)
        self.assertEqual(self.grimoire.language, self.language)

    def test_random_language_without_faction(self):
        self.grimoire.random_language()
        self.assertIsNotNone(self.grimoire.language)

    def test_random_language_with_faction(self):
        self.grimoire.faction = self.faction
        self.grimoire.save()
        self.grimoire.random_language()
        self.assertIsNotNone(self.grimoire.language)

    def test_random_length_basic(self):
        self.grimoire.random_length()
        self.assertGreater(self.grimoire.length, 0)

    def test_random_length_with_specific_value(self):
        self.grimoire.random_length(length=250)
        self.assertEqual(self.grimoire.length, 250)

    def test_random_length_with_primer(self):
        self.grimoire.is_primer = True
        self.grimoire.random_length()
        # Primer adds 50 to base length
        self.assertGreaterEqual(self.grimoire.length, 100)  # min is 50 + 50

    def test_random_length_with_division_modifier(self):
        div_medium = Medium.objects.create(
            name="Scroll", length_modifier=2, length_modifier_type="/"
        )
        self.grimoire.medium = div_medium
        self.grimoire.random_length()
        self.assertGreater(self.grimoire.length, 0)

    def test_random_length_with_addition_modifier(self):
        add_medium = Medium.objects.create(
            name="Stone Tablet", length_modifier=50, length_modifier_type="+"
        )
        self.grimoire.medium = add_medium
        self.grimoire.random_length()
        self.assertGreaterEqual(self.grimoire.length, 100)

    def test_random_length_with_subtraction_modifier(self):
        sub_medium = Medium.objects.create(
            name="Compact", length_modifier=10, length_modifier_type="-"
        )
        self.grimoire.medium = sub_medium
        self.grimoire.random_length()
        self.assertGreater(self.grimoire.length, 0)

    def test_random_length_with_multiplication_modifier(self):
        self.grimoire.medium = self.medium  # Has * modifier
        self.grimoire.random_length()
        self.assertGreater(self.grimoire.length, 0)

    def test_random_date_written_with_specific_value(self):
        self.grimoire.random_date_written(date_written=1500)
        self.assertEqual(self.grimoire.date_written, 1500)

    def test_random_date_written_without_faction(self):
        self.grimoire.random_date_written()
        self.assertNotEqual(self.grimoire.date_written, -5000)

    def test_random_date_written_with_faction(self):
        self.grimoire.faction = self.faction
        self.grimoire.save()
        self.grimoire.random_date_written()
        self.assertNotEqual(self.grimoire.date_written, -5000)

    def test_random_focus_sets_practices_and_instruments(self):
        self.grimoire.faction = self.faction
        self.grimoire.save()
        self.grimoire.random_focus()
        self.assertGreater(self.grimoire.practices.count(), 0)
        self.assertGreater(self.grimoire.instruments.count(), 0)

    def test_random_focus_with_specific_values(self):
        self.grimoire.faction = self.faction
        self.grimoire.save()
        self.grimoire.random_focus(practices=[self.practice], instruments=[self.instrument])
        self.assertIn(self.practice, self.grimoire.practices.all())
        self.assertIn(self.instrument, self.grimoire.instruments.all())

    def test_random_practices_requires_faction(self):
        with self.assertRaises(ValueError):
            self.grimoire.random_practices(None)

    def test_random_practices_with_faction(self):
        self.grimoire.faction = self.faction
        self.grimoire.save()
        practices = self.grimoire.random_practices(None)
        self.assertGreater(len(practices), 0)

    def test_random_instruments_without_practices(self):
        instruments = self.grimoire.random_instruments(None, practices=None)
        self.assertGreater(len(instruments), 0)

    def test_random_instruments_with_practices(self):
        instruments = self.grimoire.random_instruments(None, practices=[self.practice])
        self.assertGreater(len(instruments), 0)

    def test_random_abilities_requires_practices(self):
        with self.assertRaises(ValueError):
            self.grimoire.random_abilities()

    def test_random_abilities_with_practices(self):
        self.grimoire.practices.add(self.practice)
        self.grimoire.random_abilities()
        self.assertGreater(self.grimoire.abilities.count(), 0)

    def test_random_abilities_with_specific_value(self):
        self.grimoire.practices.add(self.practice)
        self.grimoire.random_abilities(abilities=[self.ability])
        self.assertIn(self.ability, self.grimoire.abilities.all())

    def test_random_spheres_basic(self):
        self.grimoire.random_spheres()
        self.assertGreater(self.grimoire.spheres.count(), 0)

    def test_random_spheres_with_specific_value(self):
        self.grimoire.random_spheres(spheres=[self.sphere])
        self.assertIn(self.sphere, self.grimoire.spheres.all())

    def test_random_spheres_with_faction_affinity(self):
        self.grimoire.faction = self.faction
        self.grimoire.save()
        self.grimoire.random_spheres()
        self.assertGreater(self.grimoire.spheres.count(), 0)

    def test_random_rotes_requires_spheres(self):
        with self.assertRaises(ValueError):
            self.grimoire.random_rotes()

    def test_random_rotes_with_specific_value(self):
        self.grimoire.rank = 1
        self.grimoire.save()
        self.grimoire.spheres.add(self.sphere)
        self.grimoire.practices.add(self.practice)
        self.grimoire.abilities.add(self.ability)

        effect = Effect.objects.create(name="Specific Effect", forces=1)
        rote = Rote.objects.create(
            name="Specific Rote",
            effect=effect,
            attribute=self.attribute,
            ability=self.ability,
        )
        self.grimoire.random_rotes(rotes=[rote])
        self.assertIn(rote, self.grimoire.rotes.all())


class TestGrimoireRandomName(TestCase):
    """Test random name generation for Grimoire."""

    @classmethod
    def setUpTestData(cls):
        cls.sphere = Sphere.objects.create(name="Forces", property_name="forces")
        cls.resonance = Resonance.objects.create(name="Dynamic", forces=True)
        cls.noun = Noun.objects.create(name="mysteries")
        cls.noun2 = Noun.objects.create(name="secrets")
        cls.medium = Medium.objects.create(name="Codex")

    def test_random_name_generates_name(self):
        # Create grimoire with temporary name, then clear it to test random_name
        grimoire = Grimoire.objects.create(name="Temporary Name")
        grimoire.spheres.add(self.sphere)
        grimoire.medium = self.medium
        # Manually set name to empty to simulate unnamed state (bypass validation)
        Grimoire.objects.filter(pk=grimoire.pk).update(name="")
        grimoire.refresh_from_db()
        result = grimoire.random_name()
        self.assertTrue(result)
        self.assertNotEqual(grimoire.name, "")

    def test_random_name_returns_false_if_name_exists(self):
        grimoire = Grimoire.objects.create(name="Already Named")
        grimoire.spheres.add(self.sphere)
        grimoire.medium = self.medium
        grimoire.save()
        result = grimoire.random_name()
        self.assertFalse(result)
        self.assertEqual(grimoire.name, "Already Named")


class TestGrimoireRandomMaterial(TestCase):
    """Test random material assignment."""

    @classmethod
    def setUpTestData(cls):
        cls.cover = Material.objects.create(name="Leather", is_hard=True)
        cls.inner = Material.objects.create(name="Vellum", is_hard=False)
        cls.faction = MageFaction.objects.create(name="Test Faction")
        cls.faction.materials.add(cls.cover, cls.inner)

    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="Material Test")

    def test_random_material_with_specific_values(self):
        self.grimoire.random_material(cover_material=self.cover, inner_material=self.inner)
        self.assertEqual(self.grimoire.cover_material, self.cover)
        self.assertEqual(self.grimoire.inner_material, self.inner)

    def test_random_material_without_faction(self):
        self.grimoire.random_material()
        self.assertIsNotNone(self.grimoire.cover_material)
        self.assertIsNotNone(self.grimoire.inner_material)


class TestGrimoireHasMethods(TestCase):
    """Test has_* methods for edge cases."""

    def setUp(self):
        self.grimoire = Grimoire.objects.create(name="Has Test")

    def test_has_materials_partial(self):
        cover = Material.objects.create(name="Cover Only")
        self.grimoire.cover_material = cover
        self.grimoire.save()
        self.assertFalse(self.grimoire.has_materials())

    def test_has_focus_partial_practices_only(self):
        practice = Practice.objects.create(name="Solo Practice")
        self.grimoire.practices.add(practice)
        self.assertFalse(self.grimoire.has_focus())

    def test_has_focus_partial_instruments_only(self):
        instrument = Instrument.objects.create(name="Solo Instrument")
        self.grimoire.instruments.add(instrument)
        self.assertFalse(self.grimoire.has_focus())


class TestGrimoireRandomAbilitiesEdgeCases(TestCase):
    """Test random_abilities with practices that have no abilities."""

    @classmethod
    def setUpTestData(cls):
        cls.practice = Practice.objects.create(name="Empty Practice")
        # Don't add any abilities to this practice

    def test_random_abilities_raises_when_no_abilities_available(self):
        grimoire = Grimoire.objects.create(name="No Abilities Test")
        grimoire.practices.add(self.practice)
        with self.assertRaises(ValueError) as ctx:
            grimoire.random_abilities()
        self.assertIn("No Abilties", str(ctx.exception))


class TestGrimoireRandomFactionHierarchy(TestCase):
    """Test random_faction with different hierarchy levels."""

    @classmethod
    def setUpTestData(cls):
        # Create faction hierarchy
        cls.top_faction = MageFaction.objects.create(name="Council of Nine", parent=None)
        cls.mid_faction = MageFaction.objects.create(name="Order of Hermes", parent=cls.top_faction)
        cls.sub_faction = MageFaction.objects.create(name="House Bonisagus", parent=cls.mid_faction)
        cls.deep_faction = MageFaction.objects.create(name="Deep Sub-House", parent=cls.sub_faction)

    def test_random_faction_selects_from_hierarchy(self):
        grimoire = Grimoire.objects.create(name="Faction Hierarchy Test")
        grimoire.random_faction()
        self.assertIsNotNone(grimoire.faction)


class TestGrimoireRandomPracticesFallback(TestCase):
    """Test random_practices when faction has no practices."""

    @classmethod
    def setUpTestData(cls):
        # Faction with no practices
        cls.empty_faction = MageFaction.objects.create(name="Orphan Faction")
        # At least one practice must exist globally
        cls.global_practice = Practice.objects.create(name="Global Practice")

    def test_random_practices_fallback_to_all_practices(self):
        grimoire = Grimoire.objects.create(name="Practice Fallback Test")
        grimoire.faction = self.empty_faction
        grimoire.save()
        practices = grimoire.random_practices(None)
        self.assertGreater(len(practices), 0)


class TestGrimoireRandomInstrumentsFallback(TestCase):
    """Test random_instruments when practices have no instruments."""

    @classmethod
    def setUpTestData(cls):
        # Practice with no instruments
        cls.empty_practice = Practice.objects.create(name="Empty Practice")
        # Global instrument
        cls.global_instrument = Instrument.objects.create(name="Global Instrument")

    def test_random_instruments_fallback_when_practices_have_none(self):
        grimoire = Grimoire.objects.create(name="Instruments Fallback Test")
        instruments = grimoire.random_instruments(None, practices=[self.empty_practice])
        self.assertGreater(len(instruments), 0)


class TestGrimoireRandomLanguageFallback(TestCase):
    """Test random_language when faction has no languages."""

    @classmethod
    def setUpTestData(cls):
        cls.faction = MageFaction.objects.create(name="No Language Faction")
        cls.language = Language.objects.create(name="Global Language", frequency=5)

    def test_random_language_fallback_when_faction_has_none(self):
        grimoire = Grimoire.objects.create(name="Language Fallback Test")
        grimoire.faction = self.faction
        grimoire.save()
        grimoire.random_language()
        self.assertIsNotNone(grimoire.language)


class TestGrimoireRandomMaterialWithFaction(TestCase):
    """Test random_material with faction materials."""

    @classmethod
    def setUpTestData(cls):
        cls.faction = MageFaction.objects.create(name="Material Faction")
        cls.cover = Material.objects.create(name="Faction Leather", is_hard=False)
        cls.inner = Material.objects.create(name="Faction Vellum", is_hard=False)
        cls.hard_inner = Material.objects.create(name="Faction Metal", is_hard=True)
        cls.faction.materials.add(cls.cover, cls.inner, cls.hard_inner)

    def test_random_material_uses_faction_materials(self):
        grimoire = Grimoire.objects.create(name="Faction Material Test")
        grimoire.faction = self.faction
        grimoire.save()
        grimoire.random_material()
        self.assertIsNotNone(grimoire.cover_material)
        self.assertIsNotNone(grimoire.inner_material)


class TestGrimoireRandomMediumFallback(TestCase):
    """Test random_medium when faction has no media."""

    @classmethod
    def setUpTestData(cls):
        cls.faction = MageFaction.objects.create(name="No Media Faction")
        cls.medium = Medium.objects.create(name="Global Medium")

    def test_random_medium_fallback_when_faction_has_none(self):
        grimoire = Grimoire.objects.create(name="Medium Fallback Test")
        grimoire.faction = self.faction
        grimoire.save()
        grimoire.random_medium()
        self.assertIsNotNone(grimoire.medium)
