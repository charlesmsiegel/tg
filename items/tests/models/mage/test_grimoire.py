from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Instrument, Practice
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from core.models import Language
from django.test import TestCase
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
