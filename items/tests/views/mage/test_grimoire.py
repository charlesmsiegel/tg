"""Tests for the grimoire detail view: the contents strip and the teachings lists."""

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase

from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.mage import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Paradigm, Practice
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from items.models.mage.grimoire import Grimoire
from items.views.mage.grimoire import faction_chain, grimoire_contents


class GrimoireContentsTest(SimpleTestCase):
    """grimoire_contents mirrors Grimoire.has_rotes: rotes + practices + spheres +
    abilities (+1 for a primer) against rank + 3."""

    def test_complete_grimoire_fills_every_slot_in_order(self):
        contents = grimoire_contents(4, True, practices=1, spheres=2, abilities=1, rotes=2)
        self.assertEqual((contents["total"], contents["filled"]), (7, 7))
        self.assertEqual(contents["state"], "complete")
        self.assertEqual(
            [cell["label"] for cell in contents["cells"]],
            ["Primer", "Practices", "Spheres", "Spheres", "Abilities", "Rotes", "Rotes"],
        )
        self.assertTrue(all(cell["filled"] and not cell["over"] for cell in contents["cells"]))

    def test_under_filled_grimoire_ends_with_empty_slots(self):
        contents = grimoire_contents(2, False, practices=1, spheres=1, abilities=0, rotes=1)
        self.assertEqual(contents["state"], "under")
        self.assertEqual(len(contents["cells"]), 5)
        self.assertEqual([cell["filled"] for cell in contents["cells"]], [True] * 3 + [False] * 2)

    def test_over_filled_grimoire_marks_the_extra_cells(self):
        contents = grimoire_contents(1, False, practices=2, spheres=1, abilities=1, rotes=1)
        self.assertEqual((contents["total"], contents["filled"]), (4, 5))
        self.assertEqual(contents["state"], "over")
        self.assertEqual([cell["over"] for cell in contents["cells"]], [False] * 4 + [True])

    def test_rank_zero_still_has_three_slots(self):
        contents = grimoire_contents(0, False, 0, 0, 0, 0)
        self.assertEqual(contents["total"], 3)
        self.assertEqual(contents["state"], "under")


class GrimoireDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("st", is_staff=True)
        parent = MageFaction.objects.create(name="Order of Hermes")
        faction = MageFaction.objects.create(name="House Quaesitor", parent=parent)
        paradigm = Paradigm.objects.create(name="Divine Order and Earthly Chaos")
        parent.paradigms.add(paradigm)
        occult = Ability.objects.create(name="Occult", property_name="occult")
        intelligence = Attribute.objects.create(name="Intelligence", property_name="intelligence")
        practice = Practice.objects.create(name="High Ritual Magick")
        cls.grimoire = Grimoire.objects.create(
            name="Book of Precise Streets",
            rank=4,
            is_primer=True,
            faction=faction,
            date_written=1873,
            background_cost=8,
            quintessence_max=20,
            owner=cls.user,
        )
        cls.grimoire.practices.add(practice)
        cls.grimoire.abilities.add(occult)
        cls.grimoire.spheres.add(
            Sphere.objects.create(name="Correspondence", property_name="correspondence"),
            Sphere.objects.create(name="Prime", property_name="prime"),
        )
        for name in ("Surveyor's Line", "Ward of Closed Doors"):
            cls.grimoire.rotes.add(
                Rote.objects.create(
                    name=name,
                    effect=Effect.objects.create(name=name, correspondence=2),
                    practice=practice,
                    attribute=intelligence,
                    ability=occult,
                )
            )

    def setUp(self):
        self.client.force_login(self.user)

    def test_contents_agree_with_has_rotes(self):
        response = self.client.get(self.grimoire.get_absolute_url())
        contents = response.context["contents"]
        self.assertTrue(self.grimoire.has_rotes())
        self.assertEqual(contents["state"], "complete")
        self.assertEqual((contents["filled"], contents["total"]), (7, 7))
        self.assertContains(response, "7 of 7 filled")
        self.assertContains(response, "Rank 4 + 3 = 7 slots")

    def test_teachings_are_lists_not_html_strings(self):
        response = self.client.get(self.grimoire.get_absolute_url())
        self.assertEqual([p.name for p in response.context["practices"]], ["High Ritual Magick"])
        self.assertEqual(
            [p.name for p in response.context["paradigms"]], ["Divine Order and Earthly Chaos"]
        )
        self.assertContains(response, "Divine Order and Earthly Chaos")
        self.assertContains(response, "Surveyor&#x27;s Line")

    def test_cover_shows_bibliographic_facts(self):
        response = self.client.get(self.grimoire.get_absolute_url())
        self.assertEqual([f.name for f in response.context["faction_chain"]][0], "Order of Hermes")
        self.assertContains(response, "1873")
        self.assertContains(response, "AD")
        self.assertContains(response, 'class="tl-stamp">Primer<')

    def test_faction_chain_stops_on_a_cycle(self):
        faction = MageFaction.objects.create(name="Loop")
        faction.parent = faction
        faction.save()
        self.assertEqual(faction_chain(faction), [faction])
        self.assertEqual(faction_chain(None), [])
