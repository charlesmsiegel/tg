"""Grimoire.random() and Library.random_book() run end to end on small reference data."""

import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Instrument, Practice
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from core.models import Language, Noun
from items.models.core.material import Material
from items.models.core.medium import Medium
from items.models.mage.grimoire import Grimoire
from locations.models.mage.library import Library

RUNS = 30


class GrimoireGeneratorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.parent = MageFaction.objects.create(name="Traditions")
        cls.faction = MageFaction.objects.create(name="Order of Hermes", parent=cls.parent)
        spheres = [
            Sphere.objects.create(name=name.title(), property_name=name)
            for name in ("forces", "matter", "prime")
        ]
        cls.faction.affinities.add(spheres[0])
        for index, name in enumerate(("High Ritual", "Alchemy")):
            practice = Practice.objects.create(name=name)
            ability = Ability.objects.create(
                name=f"Ability {index}", property_name=f"occult{index}"
            )
            practice.abilities.add(ability)
            practice.instruments.add(Instrument.objects.create(name=f"Instrument {index}"))
            cls.faction.practices.add(practice)
        cls.faction.languages.add(Language.objects.create(name="Latin", frequency=5))
        Material.objects.create(name="Leather", is_hard=False)
        Material.objects.create(name="Brass", is_hard=True)
        cls.faction.media.add(
            Medium.objects.create(name="Codex", length_modifier=1, length_modifier_type="*")
        )
        Noun.objects.create(name="mysteries")
        Noun.objects.create(name="secrets")
        for sphere in spheres:
            Resonance.objects.create(name=f"{sphere.name}ful", **{sphere.property_name: True})
        Attribute.objects.create(name="Intelligence", property_name="intelligence")
        for rating in range(1, 6):
            for sphere in spheres:
                Effect.objects.create(
                    name=f"{sphere.name} {rating}", **{sphere.property_name: rating}
                )
        cls.user = User.objects.create_user(username="librarian")

    def new_grimoire(self):
        grimoire = Grimoire(name="")
        grimoire.save(skip_validation=True)
        return grimoire

    def test_random_runs_repeatedly(self):
        for run in range(RUNS):
            with self.subTest(run=run):
                grimoire = self.new_grimoire()
                grimoire.random(faction=self.faction)
                grimoire.refresh_from_db()
                self.assertTrue(grimoire.name)
                self.assertTrue(1 <= grimoire.rank <= 5)
                self.assertTrue(grimoire.has_focus())
                self.assertTrue(grimoire.spheres.exists())

    def test_random_keeps_given_materials(self):
        cover = Material.objects.get(name="Leather")
        inner = Material.objects.get(name="Brass")
        grimoire = self.new_grimoire()
        grimoire.random(faction=self.faction, cover_material=cover, inner_material=inner)
        self.assertEqual(grimoire.cover_material, cover)
        self.assertEqual(grimoire.inner_material, inner)

    def test_random_date_uses_faction_founding(self):
        founded = datetime.date.today().year - 5
        self.faction.founded = founded
        self.faction.save()
        for _ in range(RUNS):
            grimoire = self.new_grimoire()
            grimoire.random_faction(self.faction)
            grimoire.random_date_written()
            self.assertGreaterEqual(grimoire.date_written, founded)

    def test_random_rotes_trims_abilities_not_practices(self):
        grimoire = self.new_grimoire()
        grimoire.random_rank(1)
        grimoire.spheres.add(Sphere.objects.get(property_name="forces"))
        practice = self.faction.practices.first()
        grimoire.practices.add(practice)
        grimoire.abilities.add(*Ability.objects.all())
        grimoire.name = "Trim Test"
        grimoire.save()
        grimoire.random_rotes()
        self.assertEqual(list(grimoire.practices.all()), [practice])
        self.assertTrue(grimoire.has_rotes())

    def test_library_random_book(self):
        library = Library.objects.create(name="Athenaeum", rank=3, faction=self.faction)
        for _ in range(5):
            library.random_book()
        self.assertEqual(library.books.count(), 5)
