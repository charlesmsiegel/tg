from unittest import mock
from unittest.mock import Mock

from characters.models.core.archetype import Archetype
from characters.models.core.specialty import Specialty
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.mage import Mage, ResRating
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from characters.tests.utils import mage_setup
from django.contrib.auth.models import User
from django.test import TestCase
from locations.models.mage.library import Library
from locations.models.mage.node import Node


class TestMage(TestCase):
    def setUp(self):
        mage_setup()
        self.player = User.objects.create_user(username="Test")
        self.character = Mage.objects.create(name="Test Mage", owner=self.player)

    def set_abilities(self):
        self.character.alertness = 1
        self.character.art = 2
        self.character.empathy = 3
        self.character.streetwise = 2
        self.character.firearms = 3
        self.character.melee = 4
        self.character.stealth = 2
        self.character.technology = 1
        self.character.cosmology = 3
        self.character.law = 2
        self.character.area_knowledge = 1
        self.character.belief_systems = 1
        self.character.cryptography = 1

    def set_spheres(self):
        self.character.correspondence = 1
        self.character.time = 2
        self.character.spirit = 3
        self.character.matter = 4
        self.character.forces = 5
        self.character.life = 4
        self.character.entropy = 3
        self.character.mind = 2
        self.character.prime = 1

    def test_get_spheres(self):
        self.assertEqual(
            self.character.get_spheres(),
            {
                "correspondence": 0,
                "time": 0,
                "spirit": 0,
                "matter": 0,
                "forces": 0,
                "life": 0,
                "entropy": 0,
                "mind": 0,
                "prime": 0,
            },
        )
        self.set_spheres()
        self.assertEqual(
            self.character.get_spheres(),
            {
                "correspondence": 1,
                "time": 2,
                "spirit": 3,
                "matter": 4,
                "forces": 5,
                "life": 4,
                "entropy": 3,
                "mind": 2,
                "prime": 1,
            },
        )

    def test_add_sphere(self):
        self.character.arete = 2
        self.assertTrue(self.character.add_sphere("forces"))
        self.assertTrue(self.character.add_sphere("forces"))
        self.assertEqual(self.character.forces, 2)
        self.assertFalse(self.character.add_sphere("forces"))
        self.character.arete = 3
        self.assertTrue(self.character.add_sphere("forces"))
        self.character.arete = 7
        self.assertTrue(self.character.add_sphere("forces"))
        self.assertTrue(self.character.add_sphere("forces"))
        self.assertFalse(self.character.add_sphere("forces"))

    def test_batini_no_entropy(self):
        self.character.faction = MageFaction.objects.create(name="Ahl-i-Batin")
        self.character.add_arete()
        self.assertTrue(self.character.add_sphere("forces"))
        self.assertFalse(self.character.add_sphere("entropy"))

    def test_filter_spheres(self):
        self.character.arete = 3
        self.assertEqual(len(self.character.filter_spheres().keys()), 9)
        self.set_spheres()
        self.assertEqual(len(self.character.filter_spheres(maximum=2).keys()), 4)
        self.assertEqual(len(self.character.filter_spheres(minimum=2, maximum=2).keys()), 2)
        self.assertEqual(len(self.character.filter_spheres(maximum=1).keys()), 2)

    def test_has_spheres(self):
        self.assertFalse(self.character.has_spheres())
        self.character.arete = 3
        self.character.set_affinity_sphere("forces")
        self.assertFalse(self.character.has_spheres())
        self.character.add_sphere("forces")
        self.assertFalse(self.character.has_spheres())
        self.character.add_sphere("forces")
        self.assertFalse(self.character.has_spheres())
        self.character.add_sphere("matter")
        self.assertFalse(self.character.has_spheres())
        self.character.add_sphere("matter")
        self.assertFalse(self.character.has_spheres())
        self.character.add_sphere("matter")
        self.assertTrue(self.character.has_spheres())

    def test_set_affinity_sphere(self):
        self.character.arete = 1
        self.assertFalse(self.character.has_affinity_sphere())
        self.assertTrue(self.character.set_affinity_sphere("forces"))
        self.assertTrue(self.character.has_affinity_sphere())
        self.assertEqual(self.character.forces, 1)

    def test_has_affinity_sphere(self):
        self.character.arete = 1
        self.assertFalse(self.character.has_affinity_sphere())
        self.character.affinity_sphere = Sphere.objects.get(property_name="forces")
        self.character.forces = 1
        self.assertTrue(self.character.has_affinity_sphere())

    def test_sphere_names(self):
        spheres = [
            "correspondence",
            "forces",
            "time",
            "life",
            "spirit",
            "matter",
            "prime",
            "mind",
            "entropy",
        ]
        for sphere in spheres:
            self.assertTrue(hasattr(self.character, f"{sphere}"))
        self.assertEqual(self.character.get_corr_name_display(), "Correspondence")
        self.assertEqual(self.character.get_spirit_name_display(), "Spirit")
        self.assertEqual(self.character.get_prime_name_display(), "Prime")
        self.character.set_corr_name("data")
        self.character.set_prime_name("primal_utility")
        self.character.set_spirit_name("dimensional_science")
        self.assertEqual(self.character.get_corr_name_display(), "Data")
        self.assertEqual(self.character.get_spirit_name_display(), "Dimensional Science")
        self.assertEqual(self.character.get_prime_name_display(), "Primal Utility")
        with self.assertRaises(ValueError):
            self.character.set_corr_name("blah")

    def test_add_arete(self):
        self.assertEqual(self.character.arete, 0)
        self.assertTrue(self.character.add_arete())
        self.assertEqual(self.character.arete, 1)
        self.character.arete = 10
        self.assertFalse(self.character.add_arete())

    def test_total_spheres(self):
        self.character.forces = 2
        self.assertEqual(self.character.total_spheres(), 2)
        self.character.matter = 3
        self.assertEqual(self.character.total_spheres(), 5)
        self.character.matter = 2
        self.character.life = 1
        self.assertEqual(self.character.total_spheres(), 5)

    def test_mage_numbers(self):
        self.assertEqual(self.character.background_points, 7)

    def test_add_background(self):
        num = self.character.total_backgrounds()
        self.assertFalse(self.character.add_background("test"))
        self.assertEqual(num, self.character.total_backgrounds())
        self.assertTrue(self.character.add_background("avatar"))
        self.assertEqual(num + 1, self.character.total_backgrounds())

    def test_get_backgrounds(self):
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "allies": 0,
                "alternate_identity": 0,
                "arcane": 0,
                "avatar": 0,
                "backup": 0,
                "blessing": 0,
                "certification": 0,
                "chantry": 0,
                "contacts": 0,
                "cult": 0,
                "demesne": 0,
                "destiny": 0,
                "dream": 0,
                "enhancement": 0,
                "fame": 0,
                "familiar": 0,
                "influence": 0,
                "legend": 0,
                "library": 0,
                "mentor": 0,
                "node": 0,
                "past_lives": 0,
                "patron": 0,
                "rank": 0,
                "requisitions": 0,
                "resources": 0,
                "retainers": 0,
                "sanctum": 0,
                "secret_weapons": 0,
                "spies": 0,
                "status_background": 0,
                "totem": 0,
                "wonder": 0,
            },
        )
        self.character.allies = 1
        self.character.avatar = 3
        self.character.chantry = 3
        self.character.legend = 2
        self.character.node = 2
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "allies": 1,
                "alternate_identity": 0,
                "arcane": 0,
                "avatar": 3,
                "backup": 0,
                "blessing": 0,
                "certification": 0,
                "chantry": 3,
                "contacts": 0,
                "cult": 0,
                "demesne": 0,
                "destiny": 0,
                "dream": 0,
                "enhancement": 0,
                "fame": 0,
                "familiar": 0,
                "influence": 0,
                "legend": 2,
                "library": 0,
                "mentor": 0,
                "node": 2,
                "past_lives": 0,
                "patron": 0,
                "rank": 0,
                "requisitions": 0,
                "resources": 0,
                "retainers": 0,
                "sanctum": 0,
                "secret_weapons": 0,
                "spies": 0,
                "status_background": 0,
                "totem": 0,
                "wonder": 0,
            },
        )

    def test_total_backgrounds(self):
        self.character.allies = 3
        self.character.avatar = 4
        self.character.resources = 1
        self.character.sanctum = 2
        self.assertEqual(self.character.total_backgrounds(), 12)
        self.character.wonder = 2
        self.assertEqual(self.character.total_backgrounds(), 14)

    def test_technocracy_only_backgrounds(self):
        tech_char = Mage.objects.create(name="Tech", owner=self.player)
        tech_char.affiliation = MageFaction.objects.create(name="Technocratic Union")
        trad_char = Mage.objects.create(name="Trad", owner=self.player)
        trad_char.affiliation = MageFaction.objects.get(name="Traditions")
        self.assertTrue(tech_char.add_background("secret_weapons"))
        self.assertFalse(trad_char.add_background("secret_weapons"))
        self.assertEqual(tech_char.total_backgrounds(), 1)
        self.assertEqual(trad_char.total_backgrounds(), 0)
        self.assertTrue(tech_char.add_background("requisitions"))
        self.assertFalse(trad_char.add_background("requisitions"))
        self.assertEqual(tech_char.total_backgrounds(), 2)
        self.assertEqual(trad_char.total_backgrounds(), 0)

    def test_set_faction(self):
        self.assertFalse(self.character.has_focus())
        affiliation = MageFaction.objects.create(name="Affiliation")
        faction = MageFaction.objects.create(name="Faction", parent=affiliation)
        subfaction = MageFaction.objects.create(name="Subfaction", parent=faction)

        affiliation2 = MageFaction.objects.create(name="Affiliation2")
        faction2 = MageFaction.objects.create(name="Faction2", parent=affiliation2)
        subfaction2 = MageFaction.objects.create(name="Subfaction2", parent=faction2)

        self.assertFalse(self.character.set_faction(affiliation, faction, subfaction=subfaction2))
        self.assertTrue(self.character.set_faction(affiliation, faction, subfaction=subfaction))
        self.assertTrue(self.character.has_faction())
        self.assertTrue(
            self.character.set_faction(
                subfaction2.parent.parent, subfaction2.parent, subfaction=subfaction2
            )
        )
        self.assertTrue(self.character.has_faction())

    def test_has_faction(self):
        self.assertFalse(self.character.has_focus())
        affiliation = MageFaction.objects.create(name="Affiliation")
        faction = MageFaction.objects.create(name="Faction", parent=affiliation)
        subfaction = MageFaction.objects.create(name="Subfaction", parent=faction)
        self.character.set_faction(affiliation=affiliation, faction=faction, subfaction=subfaction)
        self.assertTrue(self.character.has_faction())

    def test_set_focus(self):
        ascension_tenet = Tenet.objects.filter(tenet_type="asc").first()
        personal_tenet = Tenet.objects.filter(tenet_type="per").first()
        metaphysical_tenet = Tenet.objects.filter(tenet_type="met").first()
        prac = Practice.objects.first()
        self.character.arete = 2
        tenets = [ascension_tenet, metaphysical_tenet, personal_tenet]
        practices = [prac, prac]

        self.assertFalse(self.character.has_focus())
        self.assertTrue(self.character.set_focus(tenets, practices))
        self.assertTrue(self.character.has_focus())

    def test_has_focus(self):
        ascension_tenet = Tenet.objects.filter(tenet_type="asc").first()
        personal_tenet = Tenet.objects.filter(tenet_type="per").first()
        metaphysical_tenet = Tenet.objects.filter(tenet_type="met").first()

        self.assertFalse(self.character.has_focus())
        self.character.add_tenet(ascension_tenet)
        self.character.add_tenet(personal_tenet)
        self.character.add_tenet(metaphysical_tenet)
        self.character.arete = 2
        prac = Practice.objects.first()
        self.character.add_practice(prac)
        self.character.add_practice(prac)
        self.assertTrue(self.character.has_focus())

    def test_set_essence(self):
        self.assertFalse(self.character.has_essence())
        self.assertTrue(self.character.set_essence("questing"))
        self.assertTrue(self.character.has_essence())

    def test_has_essence(self):
        self.assertFalse(self.character.has_essence())
        self.character.set_essence("questing")
        self.assertTrue(self.character.has_essence())

    def test_add_resonance(self):
        res = Resonance.objects.order_by("?").first()
        self.assertEqual(self.character.resonance_rating(res), 0)
        self.assertTrue(self.character.add_resonance(res))
        self.assertEqual(self.character.resonance_rating(res), 1)

    def test_filter_resonance(self):
        self.assertEqual(len(self.character.filter_resonance()), 65)
        for res in Resonance.objects.order_by("?")[:3]:
            self.assertTrue(self.character.add_resonance(res))
        self.assertEqual(len(self.character.filter_resonance(maximum=0)), 62)

    def test_total_resonance(self):
        resonance = Resonance.objects.order_by("?")[:2]
        for res in resonance:
            self.character.add_resonance(res)
            self.character.add_resonance(res)
        self.assertEqual(self.character.total_resonance(), 4)
        self.assertNotEqual(self.character.total_resonance(), 5)
        self.character.add_resonance(resonance[0])
        self.assertEqual(self.character.total_resonance(), 5)

    def test_add_effect(self):
        self.character.arete = 3
        self.character.forces = 3
        self.character.prime = 2
        e = Effect.objects.create(name="Fireball", forces=3, prime=2)
        e2 = Effect.objects.create(name="Teleport", correspondence=3)
        num = self.character.rotes.count()
        self.assertTrue(self.character.add_effect(e))
        r = Rote.objects.get(effect=e)
        self.assertEqual(self.character.rotes.count(), num + 1)
        self.assertIn(r, self.character.rotes.all())
        self.assertFalse(self.character.add_effect(e2))
        self.character.correspondence = 3
        self.assertNotIn(e2, self.character.rotes.all().values_list("effect", flat=True))
        self.assertTrue(self.character.add_effect(e2))
        r2 = Rote.objects.get(effect=e2)
        self.assertIn(r2, self.character.rotes.all())

    def test_has_effects(self):
        self.character.arete = 3
        self.character.forces = 3
        self.character.prime = 2
        self.character.matter = 1
        self.assertFalse(self.character.has_effects())
        self.character.add_effect(Effect.objects.get(name="Forces 3"))
        self.assertFalse(self.character.has_effects())
        self.character.add_effect(Effect.objects.get(name="Matter 1"))
        self.assertFalse(self.character.has_effects())
        self.character.add_effect(Effect.objects.get(name="Prime 1"))
        self.assertFalse(self.character.has_effects())
        self.character.add_effect(Effect.objects.get(name="Forces 1"))
        self.assertTrue(self.character.has_effects())

    def test_total_effects(self):
        self.character.arete = 3
        self.character.forces = 3
        self.character.prime = 2
        self.character.correspondence = 3
        r1 = Effect.objects.create(name="Fireball", forces=3, prime=2)
        r2 = Effect.objects.create(name="Teleport", correspondence=3)
        self.character.add_effect(r1)
        self.assertEqual(self.character.total_effects(), 5)
        self.character.add_effect(r2)
        self.assertEqual(self.character.total_effects(), 8)

    def test_filter_effects(self):
        self.character.arete = 5
        self.character.correspondence = 5
        self.character.time = 5
        self.character.spirit = 5
        self.character.forces = 5
        self.character.matter = 5
        self.character.life = 5
        self.character.entropy = 5
        self.character.prime = 5
        self.character.mind = 5
        self.assertEqual(len(self.character.filter_effects()), 2637)
        self.character.mind = 4
        self.assertEqual(len(self.character.filter_effects()), 2540)
        self.character.prime = 1
        self.assertEqual(len(self.character.filter_effects()), 2160)
        self.character.correspondence = 1
        self.character.time = 1
        self.character.spirit = 1
        self.character.forces = 2
        self.character.matter = 0
        self.character.life = 0
        self.character.entropy = 0
        self.character.prime = 0
        self.character.mind = 0
        self.assertEqual(len(self.character.filter_effects()), 175)

    def test_has_mage_history(self):
        self.assertFalse(self.character.has_mage_history())
        self.character.age_of_awakening = 13
        self.assertFalse(self.character.has_mage_history())
        self.character.avatar_description = "Avatar"
        self.assertTrue(self.character.has_mage_history())

    def test_set_quiet_rating(self):
        self.assertEqual(self.character.quiet, 0)
        self.character.set_quiet_rating(3)
        self.assertEqual(self.character.quiet, 3)

    def test_set_quiet_type(self):
        self.assertEqual(self.character.quiet_type, "none")
        self.character.set_quiet_type("denial")
        self.assertEqual(self.character.quiet_type, "denial")

    def test_marauders_have_quiet(self):
        top_level = MageFaction.objects.create(name="TopLevel Faction", parent=None)
        marauder = MageFaction.objects.create(name="Marauders", parent=None)
        self.assertEqual(self.character.quiet, 0)
        self.assertEqual(self.character.quiet_type, "none")
        self.character.set_faction(top_level, None, None)
        self.assertEqual(self.character.quiet, 0)
        self.assertEqual(self.character.quiet_type, "none")
        self.character.set_faction(marauder, None, None)
        self.assertNotEqual(self.character.quiet, 0)
        self.assertNotEqual(self.character.quiet_type, "none")

    def test_resonance_rating(self):
        resonance = Resonance.objects.create(name="test_resonance")
        res_rating = ResRating.objects.create(mage=self.character, resonance=resonance, rating=3)
        self.assertEqual(self.character.resonance_rating(resonance), res_rating.rating)

    def test_has_specialties(self):
        self.assertTrue(self.character.has_specialties())
        self.character.forces = 4
        self.assertFalse(self.character.has_specialties())
        self.character.add_specialty(Specialty.objects.create(stat="forces"))
        self.assertTrue(self.character.has_specialties())

    def test_has_library(self):
        self.character.library = 3
        self.assertFalse(self.character.has_library())
        Library.objects.create(name="test_library", rank=3, owned_by=self.character)
        self.assertTrue(self.character.has_library())

    def test_has_node(self):
        self.character.node = 2
        self.assertFalse(self.character.has_node())
        Node.objects.create(name="test_node", rank=2, owned_by=self.character)
        self.assertTrue(self.character.has_node())


class TestMageDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.mage = Mage.objects.create(name="Test Mage", owner=self.player, status="App")
        self.url = self.mage.get_absolute_url()

    def test_mage_detail_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_mage_detail_view_templates(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/mage/detail.html")


class TestMageCreateView(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Mage",
            "description": 0,
            "willpower": 0,
            "age": 0,
            "apparent_age": 0,
            "history": 0,
            "goals": 0,
            "notes": 0,
            "strength": 0,
            "dexterity": 0,
            "stamina": 0,
            "perception": 0,
            "intelligence": 0,
            "wits": 0,
            "charisma": 0,
            "manipulation": 0,
            "appearance": 0,
            "awareness": 0,
            "art": 0,
            "leadership": 0,
            "animal_kinship": 0,
            "blatancy": 0,
            "carousing": 0,
            "do": 0,
            "flying": 0,
            "high_ritual": 0,
            "lucid_dreaming": 0,
            "search": 0,
            "seduction": 0,
            "larceny": 0,
            "meditation": 0,
            "research": 0,
            "survival": 0,
            "technology": 0,
            "acrobatics": 0,
            "archery": 0,
            "biotech": 0,
            "energy_weapons": 0,
            "jetpack": 0,
            "riding": 0,
            "torture": 0,
            "cosmology": 0,
            "enigmas": 0,
            "finance": 0,
            "law": 0,
            "occult": 0,
            "politics": 0,
            "area_knowledge": 0,
            "belief_systems": 0,
            "cryptography": 0,
            "demolitions": 0,
            "lore": 0,
            "media": 0,
            "pharmacopeia": 0,
            "cooking": 0,
            "diplomacy": 0,
            "instruction": 0,
            "intrigue": 0,
            "intuition": 0,
            "mimicry": 0,
            "negotiation": 0,
            "newspeak": 0,
            "scan": 0,
            "scrounging": 0,
            "style": 0,
            "blind_fighting": 0,
            "climbing": 0,
            "disguise": 0,
            "elusion": 0,
            "escapology": 0,
            "fast_draw": 0,
            "fast_talk": 0,
            "fencing": 0,
            "fortune_telling": 0,
            "gambling": 0,
            "gunsmith": 0,
            "heavy_weapons": 0,
            "hunting": 0,
            "hypnotism": 0,
            "jury_rigging": 0,
            "microgravity_operations": 0,
            "misdirection": 0,
            "networking": 0,
            "pilot": 0,
            "psychology": 0,
            "security": 0,
            "speed_reading": 0,
            "swimming": 0,
            "conspiracy_theory": 0,
            "chantry_politics": 0,
            "covert_culture": 0,
            "cultural_savvy": 0,
            "helmsman": 0,
            "history_knowledge": 0,
            "power_brokering": 0,
            "propaganda": 0,
            "theology": 0,
            "unconventional_warface": 0,
            "vice": 0,
            "essence": "Dynamic",
            "correspondence": 0,
            "time": 0,
            "spirit": 0,
            "mind": 0,
            "entropy": 0,
            "prime": 0,
            "forces": 0,
            "matter": 0,
            "life": 0,
            "arete": 2,
            "corr_name": "correspondence",
            "prime_name": "prime",
            "spirit_name": "spirit",
            "age_of_awakening": 18,
            "avatar_description": "sfjgsj",
            "rote_points": 0,
            "quintessence": 0,
            "paradox": 0,
            "quiet": 0,
            "quiet_type": "none",
            "public_info": "Test Info",
        }
        self.player = User.objects.create_user(username="User1", password="12345")
        self.client.login(username="User1", password="12345")
        self.url = Mage.get_full_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/mage/form.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, Mage.objects.first().get_absolute_url())
        self.assertEqual(Mage.objects.count(), 1)
        self.assertEqual(Mage.objects.first().name, "Test Mage")


class TestMageHumanUpdateView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="User1", password="12345")
        self.client.login(username="User1", password="12345")
        self.mage = Mage.objects.create(
            name="Test Mage", description="Test", status="App", owner=self.player
        )
        self.valid_data = {
            "name": "Test Mage 2",
            "description": 0,
            "willpower": 0,
            "age": 0,
            "apparent_age": 0,
            "history": 0,
            "goals": 0,
            "notes": 0,
            "strength": 0,
            "dexterity": 0,
            "stamina": 0,
            "perception": 0,
            "intelligence": 0,
            "wits": 0,
            "charisma": 0,
            "manipulation": 0,
            "appearance": 0,
            "awareness": 0,
            "art": 0,
            "leadership": 0,
            "animal_kinship": 0,
            "blatancy": 0,
            "carousing": 0,
            "do": 0,
            "flying": 0,
            "high_ritual": 0,
            "lucid_dreaming": 0,
            "search": 0,
            "seduction": 0,
            "larceny": 0,
            "meditation": 0,
            "research": 0,
            "survival": 0,
            "technology": 0,
            "acrobatics": 0,
            "archery": 0,
            "biotech": 0,
            "energy_weapons": 0,
            "jetpack": 0,
            "riding": 0,
            "torture": 0,
            "cosmology": 0,
            "enigmas": 0,
            "finance": 0,
            "law": 0,
            "occult": 0,
            "politics": 0,
            "area_knowledge": 0,
            "belief_systems": 0,
            "cryptography": 0,
            "demolitions": 0,
            "lore": 0,
            "media": 0,
            "pharmacopeia": 0,
            "cooking": 0,
            "diplomacy": 0,
            "instruction": 0,
            "intrigue": 0,
            "intuition": 0,
            "mimicry": 0,
            "negotiation": 0,
            "newspeak": 0,
            "scan": 0,
            "scrounging": 0,
            "style": 0,
            "blind_fighting": 0,
            "climbing": 0,
            "disguise": 0,
            "elusion": 0,
            "escapology": 0,
            "fast_draw": 0,
            "fast_talk": 0,
            "fencing": 0,
            "fortune_telling": 0,
            "gambling": 0,
            "gunsmith": 0,
            "heavy_weapons": 0,
            "hunting": 0,
            "hypnotism": 0,
            "jury_rigging": 0,
            "microgravity_operations": 0,
            "misdirection": 0,
            "networking": 0,
            "pilot": 0,
            "psychology": 0,
            "security": 0,
            "speed_reading": 0,
            "swimming": 0,
            "conspiracy_theory": 0,
            "chantry_politics": 0,
            "covert_culture": 0,
            "cultural_savvy": 0,
            "helmsman": 0,
            "history_knowledge": 0,
            "power_brokering": 0,
            "propaganda": 0,
            "theology": 0,
            "unconventional_warface": 0,
            "vice": 0,
            "essence": "Dynamic",
            "correspondence": 0,
            "time": 0,
            "spirit": 0,
            "mind": 0,
            "entropy": 0,
            "prime": 0,
            "forces": 0,
            "matter": 0,
            "life": 0,
            "arete": 2,
            "corr_name": "correspondence",
            "prime_name": "prime",
            "spirit_name": "spirit",
            "age_of_awakening": 18,
            "avatar_description": "sfjgsj",
            "rote_points": 0,
            "quintessence": 0,
            "paradox": 0,
            "quiet": 0,
            "quiet_type": "none",
            "public_info": "test_infor",
        }
        self.url = self.mage.get_full_update_url()

    def test_update_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/mage/form.html")

    def test_update_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.mage.get_absolute_url())
        self.mage.refresh_from_db()
        self.assertEqual(self.mage.name, "Test Mage 2")


class TestMageBasicsView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Test", password="password")
        self.client.login(username="Test", password="password")
        self.n = Archetype.objects.create(name="Nature")
        self.d = Archetype.objects.create(name="Demeanor")
        self.affiliation = MageFaction.objects.create(name="Affiliation")
        self.faction = MageFaction.objects.create(name="factio", parent=self.affiliation)
        self.subfaction = MageFaction.objects.create(name="subfaction", parent=self.faction)
        self.valid_data = {
            "name": "Test",
            "nature": self.n.id,
            "demeanor": self.d.id,
            "concept": "Concept",
            "affiliation": self.affiliation.id,
            "faction": self.faction.id,
            "subfaction": self.subfaction.id,
            "essence": "Dynamic",
        }
        self.url = Mage.get_creation_url()

    def test_create_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/mage/mage/magebasics.html")

    def test_create_view_successful_post(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Mage.objects.count(), 1)
        self.assertEqual(Mage.objects.first().name, "Test")
        self.assertEqual(Mage.objects.first().nature, self.n)
        self.assertEqual(Mage.objects.first().demeanor, self.d)
        self.assertEqual(Mage.objects.first().concept, "Concept")
        self.assertEqual(Mage.objects.first().affiliation, self.affiliation)
        self.assertEqual(Mage.objects.first().faction, self.faction)
        self.assertEqual(Mage.objects.first().subfaction, self.subfaction)
        self.assertEqual(Mage.objects.first().essence, "Dynamic")
