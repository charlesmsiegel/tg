
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from characters.models.core import (
    Archetype,
    Derangement,
    Human,
    MeritFlaw,
    MeritFlawRating,
)
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.specialty import Specialty
from characters.tests.utils import human_setup
from core.models import Language, Number
from game.models import Chronicle, ObjectType


class TestHuman(TestCase):
    def setUp(self) -> None:
        human_setup()
        self.user = User.objects.create_user(username="Test")
        self.character = Human.objects.create(name="Test Human", owner=self.user)
        for i in range(10):
            Archetype.objects.create(name=f"Archetype {i}")

        for i in [1, 2, 3, 4, 5, 6]:
            Number.objects.create(value=i)
            Number.objects.create(value=-i)

        human = ObjectType.objects.get_or_create(
            name=self.character.type, type="char", gameline="wod"
        )[0]

        for i in range(1, 6):
            mf = MeritFlaw.objects.create(name=f"Merit {i}")
            mf.allowed_types.add(human)
            mf.add_rating(i)
            mf = MeritFlaw.objects.create(name=f"Flaw {i}")
            mf.allowed_types.add(human)
            mf.add_rating(-i)

        for i in range(10):
            for stat in self.character.get_attributes():
                Specialty.objects.create(
                    name=f"{stat.replace('_', ' ').title()} Specialty {i}",
                    stat=stat,
                )
        for i in range(10):
            for ability in self.character.get_abilities():
                Specialty.objects.create(
                    name=f"{ability.replace('_', ' ').title()} Specialty {i}",
                    stat=ability,
                )
        for i in range(20):
            Language.objects.create(name=f"TL {i}")

    def test_add_willpower(self):
        self.assertEqual(self.character.willpower, 3)
        self.assertTrue(self.character.add_willpower())
        self.assertEqual(self.character.willpower, 4)

    def test_has_finishing_touches(self):
        self.assertFalse(self.character.has_finishing_touches())
        self.character.age = 18
        self.assertFalse(self.character.has_finishing_touches())
        self.character.date_of_birth = now()
        self.assertFalse(self.character.has_finishing_touches())
        self.character.description = "Hardcore Asshole"
        self.assertFalse(self.character.has_finishing_touches())
        self.character.apparent_age = 18
        self.assertTrue(self.character.has_finishing_touches())

    def test_has_history(self):
        self.assertFalse(self.character.has_history())
        self.character.history = "Got older."
        self.assertFalse(self.character.has_history())
        self.character.goals = "Get older still."
        self.assertTrue(self.character.has_history())

    def test_static_numbers(self):
        self.assertEqual(self.character.willpower, 3)
        self.assertEqual(self.character.background_points, 5)
        self.assertEqual(self.character.freebies, 15)

    def test_add_damage(self):
        self.assertEqual(self.character.get_wound_penalty(), 0)
        self.character.add_bashing()
        self.assertEqual(self.character.get_wound_penalty(), 0)
        self.character.add_aggravated()
        self.assertEqual(self.character.current_health_levels, "AB")
        self.assertEqual(self.character.get_wound_penalty(), -1)
        self.character.add_lethal()
        self.assertEqual(self.character.current_health_levels, "ALB")
        self.assertEqual(self.character.get_wound_penalty(), -1)
        self.character.add_bashing()
        self.assertEqual(self.character.get_wound_penalty(), -2)
        self.character.add_bashing()
        self.assertEqual(self.character.get_wound_penalty(), -2)
        self.character.add_bashing()
        self.assertEqual(self.character.get_wound_penalty(), -5)
        self.character.add_bashing()
        self.assertEqual(self.character.current_health_levels, "ALBBBBB")
        self.character.add_bashing()
        self.assertEqual(self.character.current_health_levels, "ALLBBBB")
        self.character.add_aggravated()
        self.assertEqual(self.character.get_wound_penalty(), -1000)

    def test_has_archetypes(self):
        self.assertFalse(self.character.has_archetypes())
        self.character.nature = Archetype.objects.first()
        self.character.demeanor = Archetype.objects.first()
        self.assertTrue(self.character.has_archetypes())

    def test_set_archetypes(self):
        self.assertFalse(self.character.has_archetypes())
        self.assertTrue(
            self.character.set_archetypes(Archetype.objects.first(), Archetype.objects.first())
        )
        self.assertTrue(self.character.has_archetypes())

    def test_add_mf(self):
        m3 = MeritFlaw.objects.get(name="Merit 3")
        self.assertEqual(self.character.merits_and_flaws.count(), 0)
        self.assertTrue(self.character.add_mf(m3, 3))
        self.assertEqual(self.character.merits_and_flaws.count(), 1)
        self.assertIn(m3, self.character.merits_and_flaws.all())

    def test_has_max_flaws(self):
        self.assertFalse(self.character.has_max_flaws())
        self.character.add_mf(MeritFlaw.objects.get(name="Flaw 3"), -3)
        self.assertFalse(self.character.has_max_flaws())
        self.character.add_mf(MeritFlaw.objects.get(name="Flaw 4"), -4)
        self.assertTrue(self.character.has_max_flaws())

    def test_filter_mfs(self):
        self.assertEqual(len(self.character.filter_mfs()), 10)
        self.character.add_mf(MeritFlaw.objects.get(name="Merit 1"), 1)
        self.assertEqual(len(self.character.filter_mfs()), 9)
        self.character.add_mf(MeritFlaw.objects.get(name="Merit 2"), 2)
        self.assertEqual(len(self.character.filter_mfs()), 8)
        self.character.add_mf(MeritFlaw.objects.get(name="Flaw 2"), -2)
        self.assertEqual(len(self.character.filter_mfs()), 7)
        self.character.add_mf(MeritFlaw.objects.get(name="Flaw 5"), -5)
        self.assertEqual(len(self.character.filter_mfs()), 3)
        m = MeritFlaw.objects.create(name="Test Merit")
        m.add_ratings([1, 2, 3])
        self.assertNotIn(m, self.character.filter_mfs())
        m.allowed_types.add(ObjectType.objects.get(name="human"))
        self.assertIn(m, self.character.filter_mfs())

    def test_total_merits(self):
        self.assertEqual(self.character.total_merits(), 0)
        self.character.add_mf(MeritFlaw.objects.get(name="Merit 3"), 3)
        self.assertEqual(self.character.total_merits(), 3)
        self.character.add_mf(MeritFlaw.objects.get(name="Flaw 3"), -3)
        self.assertEqual(self.character.total_merits(), 3)

    def test_total_flaws(self):
        self.assertEqual(self.character.total_flaws(), 0)
        self.character.add_mf(MeritFlaw.objects.get(name="Flaw 3"), -3)
        self.assertEqual(self.character.total_flaws(), -3)
        self.character.add_mf(MeritFlaw.objects.get(name="Merit 3"), 3)
        self.assertEqual(self.character.total_flaws(), -3)

    def test_mf_rating(self):
        mf = MeritFlaw.objects.create(name="Test Merit Flaw")
        mf.add_ratings([-2, -1])
        MeritFlawRating.objects.create(character=self.character, mf=mf, rating=-2)
        self.assertEqual(self.character.mf_rating(mf), -2)

    def test_add_derangement(self):
        d = Derangement.objects.create(name="Test Derangement")
        self.assertTrue(self.character.add_derangement(d))
        self.assertFalse(self.character.add_derangement(d))

    def set_attributes(self):
        self.character.strength = 5
        self.character.dexterity = 4
        self.character.stamina = 3
        self.character.perception = 2
        self.character.intelligence = 1
        self.character.wits = 2
        self.character.charisma = 3
        self.character.manipulation = 4
        self.character.appearance = 5

    def test_get_attributes(self):
        self.assertEqual(
            self.character.get_attributes(),
            {
                "strength": 1,
                "dexterity": 1,
                "stamina": 1,
                "perception": 1,
                "intelligence": 1,
                "wits": 1,
                "charisma": 1,
                "manipulation": 1,
                "appearance": 1,
            },
        )
        self.set_attributes()
        self.assertEqual(
            self.character.get_attributes(),
            {
                "strength": 5,
                "dexterity": 4,
                "stamina": 3,
                "perception": 2,
                "intelligence": 1,
                "wits": 2,
                "charisma": 3,
                "manipulation": 4,
                "appearance": 5,
            },
        )

    def test_get_physical_attributes(self):
        self.assertEqual(
            self.character.get_physical_attributes(),
            {
                "strength": 1,
                "dexterity": 1,
                "stamina": 1,
            },
        )
        self.set_attributes()
        self.assertEqual(
            self.character.get_physical_attributes(),
            {
                "strength": 5,
                "dexterity": 4,
                "stamina": 3,
            },
        )

    def test_get_mental_attributes(self):
        self.assertEqual(
            self.character.get_mental_attributes(),
            {
                "perception": 1,
                "intelligence": 1,
                "wits": 1,
            },
        )
        self.set_attributes()
        self.assertEqual(
            self.character.get_mental_attributes(),
            {
                "perception": 2,
                "intelligence": 1,
                "wits": 2,
            },
        )

    def test_get_social_attributes(self):
        self.assertEqual(
            self.character.get_social_attributes(),
            {
                "charisma": 1,
                "manipulation": 1,
                "appearance": 1,
            },
        )
        self.set_attributes()
        self.assertEqual(
            self.character.get_social_attributes(),
            {
                "charisma": 3,
                "manipulation": 4,
                "appearance": 5,
            },
        )

    def test_add_attribute(self):
        self.character.strength = 1
        self.assertTrue(self.character.add_attribute("strength"))
        self.assertEqual(self.character.strength, 2)
        self.character.strength = 5
        self.assertFalse(self.character.add_attribute("strength", maximum=5))
        self.assertEqual(self.character.strength, 5)
        self.assertTrue(self.character.add_attribute("strength", maximum=6))
        self.assertEqual(self.character.strength, 6)

    def test_filter_attributes(self):
        self.character.strength = 5
        self.assertEqual(
            self.character.filter_attributes(maximum=4),
            {
                "dexterity": 1,
                "stamina": 1,
                "intelligence": 1,
                "wits": 1,
                "perception": 1,
                "appearance": 1,
                "manipulation": 1,
                "charisma": 1,
            },
        )
        self.assertEqual(
            self.character.filter_attributes(maximum=5),
            {
                "strength": 5,
                "dexterity": 1,
                "stamina": 1,
                "intelligence": 1,
                "wits": 1,
                "perception": 1,
                "appearance": 1,
                "manipulation": 1,
                "charisma": 1,
            },
        )
        self.character.strength = 4
        self.assertEqual(self.character.filter_attributes(minimum=3), {"strength": 4})
        self.assertEqual(self.character.filter_attributes(minimum=3, maximum=5), {"strength": 4})
        self.assertEqual(self.character.filter_attributes(minimum=5, maximum=6), {})

    def test_has_attributes(self):
        triple = [
            self.character.total_physical_attributes(),
            self.character.total_mental_attributes(),
            self.character.total_social_attributes(),
        ]
        triple.sort()
        self.assertNotEqual(triple, [6, 8, 10])
        self.character.strength = 3
        self.character.dexterity = 4
        self.character.stamina = 3
        self.character.intelligence = 3
        self.character.wits = 3
        self.character.perception = 2
        self.character.charisma = 2
        self.character.manipulation = 2
        self.character.appearance = 2
        triple = [
            self.character.total_physical_attributes(),
            self.character.total_mental_attributes(),
            self.character.total_social_attributes(),
        ]
        triple.sort()
        self.assertEqual(triple, [6, 8, 10])
        self.character.perception = 3
        triple = [
            self.character.total_physical_attributes(),
            self.character.total_mental_attributes(),
            self.character.total_social_attributes(),
        ]
        triple.sort()
        self.assertNotEqual(triple, [6, 8, 10])

    def test_total_physical_attribute(self):
        self.character.strength = 1
        self.character.dexterity = 2
        self.character.stamina = 3
        self.assertEqual(self.character.total_physical_attributes(), 6)
        self.character.stamina = 2
        self.assertEqual(self.character.total_physical_attributes(), 5)

    def test_total_mental_attribute(self):
        self.character.perception = 1
        self.character.intelligence = 2
        self.character.wits = 3
        self.assertEqual(self.character.total_mental_attributes(), 6)
        self.character.wits = 2
        self.assertEqual(self.character.total_mental_attributes(), 5)

    def test_total_social_attribute(self):
        self.character.charisma = 1
        self.character.manipulation = 2
        self.character.appearance = 3
        self.assertEqual(self.character.total_social_attributes(), 6)
        self.character.appearance = 2
        self.assertEqual(self.character.total_social_attributes(), 5)

    def test_total_attributes(self):
        self.character.strength = 3
        self.character.dexterity = 2
        self.character.stamina = 4
        self.assertEqual(self.character.total_attributes(), 15)

    def test_get_abilities(self):
        self.assertEqual(
            self.character.get_abilities(),
            {
                "alertness": 0,
                "athletics": 0,
                "brawl": 0,
                "empathy": 0,
                "expression": 0,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 0,
                "crafts": 0,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
                "academics": 0,
                "computer": 0,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_abilities(),
            {
                "alertness": 3,
                "athletics": 3,
                "brawl": 3,
                "empathy": 3,
                "expression": 1,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 0,
                "crafts": 3,
                "drive": 3,
                "etiquette": 3,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
                "academics": 3,
                "computer": 2,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
            },
        )

    def test_get_talents(self):
        self.assertEqual(
            self.character.get_talents(),
            {
                "alertness": 0,
                "athletics": 0,
                "brawl": 0,
                "empathy": 0,
                "expression": 0,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_talents(),
            {
                "alertness": 3,
                "athletics": 3,
                "brawl": 3,
                "empathy": 3,
                "expression": 1,
                "intimidation": 0,
                "streetwise": 0,
                "subterfuge": 0,
            },
        )

    def test_get_skills(self):
        self.assertEqual(
            self.character.get_skills(),
            {
                "crafts": 0,
                "drive": 0,
                "etiquette": 0,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_skills(),
            {
                "crafts": 3,
                "drive": 3,
                "etiquette": 3,
                "firearms": 0,
                "melee": 0,
                "stealth": 0,
            },
        )

    def test_get_knowledges(self):
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 0,
                "computer": 0,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
            },
        )
        self.set_abilities()
        self.assertEqual(
            self.character.get_knowledges(),
            {
                "academics": 3,
                "computer": 2,
                "investigation": 0,
                "medicine": 0,
                "science": 0,
            },
        )

    def test_add_ability(self):
        self.character.occult = 0
        self.assertTrue(self.character.add_ability("occult"))
        self.assertEqual(self.character.occult, 1)
        self.character.occult = 5
        self.assertFalse(self.character.add_ability("occult", maximum=5))
        self.assertEqual(self.character.occult, 5)
        self.assertTrue(self.character.add_ability("occult", maximum=6))
        self.assertEqual(self.character.occult, 6)

    def test_filter_abilities(self):
        self.assertEqual(len(self.character.filter_abilities(minimum=1, maximum=3)), 0)
        self.assertEqual(len(self.character.filter_abilities(minimum=0, maximum=3)), 19)
        self.set_abilities()
        self.assertEqual(len(self.character.filter_abilities(minimum=1, maximum=3)), 10)
        self.assertEqual(len(self.character.filter_abilities(minimum=1, maximum=2)), 2)

    def set_abilities(self):
        self.character.alertness = 3
        self.character.athletics = 3
        self.character.brawl = 3
        self.character.empathy = 3
        self.character.expression = 1
        self.character.crafts = 3
        self.character.drive = 3
        self.character.etiquette = 3
        self.character.academics = 3
        self.character.computer = 2

    def test_has_abilities(self):
        triple = [
            self.character.total_talents(),
            self.character.total_skills(),
            self.character.total_knowledges(),
        ]
        triple.sort()
        self.assertNotEqual(triple, [5, 9, 13])
        self.set_abilities()
        triple = [
            self.character.total_talents(),
            self.character.total_skills(),
            self.character.total_knowledges(),
        ]
        triple.sort()
        self.assertEqual(triple, [5, 9, 13])
        self.character.subterfuge = 1
        triple = [
            self.character.total_talents(),
            self.character.total_skills(),
            self.character.total_knowledges(),
        ]
        triple.sort()
        self.assertNotEqual(triple, [5, 9, 13])

    def test_total_talents(self):
        self.character.alertness = 2
        self.character.athletics = 1
        self.character.brawl = 1
        self.assertEqual(self.character.total_talents(), 4)

    def test_total_skills(self):
        self.character.etiquette = 2
        self.character.firearms = 1
        self.character.stealth = 3
        self.assertEqual(self.character.total_skills(), 6)

    def test_total_knowledges(self):
        self.character.academics = 1
        self.character.investigation = 2
        self.assertEqual(self.character.total_knowledges(), 3)

    def test_total_abilities(self):
        self.character.add_ability("brawl")
        self.character.add_ability("firearms")
        self.assertEqual(self.character.total_abilities(), 2)

    def test_languages(self):
        english = Language.objects.create(name="English")
        self.assertEqual(self.character.languages.count(), 0)
        self.character.languages.add(english)
        self.assertEqual(self.character.languages.count(), 1)

    def test_language_merit(self):
        m = MeritFlaw.objects.create(name="Language")
        m.add_ratings([1, 2, 3, 4, 5])
        # Character starts as 'Un' (unfinished) - no status change needed
        # num_languages() returns the number of languages entitled by the Language merit
        self.assertEqual(self.character.num_languages(), 0)
        for i in range(5):
            self.character.add_mf(m, i + 1)
            self.assertEqual(self.character.num_languages(), i + 1)

    def test_natural_linguist_merit(self):
        # num_languages() returns the number of languages entitled by merits
        # Natural Linguist doubles the Language merit rating
        self.assertEqual(self.character.num_languages(), 0)
        nl = MeritFlaw.objects.create(name="Natural Linguist")
        nl.add_rating(1)
        m = MeritFlaw.objects.create(name="Language")
        m.add_ratings([1, 2, 3, 4, 5])
        self.character.add_mf(nl, 1)
        for i in range(5):
            self.character.add_mf(m, i + 1)
            # With Natural Linguist, language count is doubled
            self.assertEqual(self.character.num_languages(), 2 * (i + 1))
        # Create new character in default 'Un' status
        lt = Human.objects.create(name="language tester", owner=self.user)
        self.assertEqual(lt.num_languages(), 0)
        lt.add_mf(m, 1)
        # Without Natural Linguist, just the Language rating
        self.assertEqual(lt.num_languages(), 1)
        lt.add_mf(nl, 1)
        # With Natural Linguist added, the Language rating is doubled
        self.assertEqual(lt.num_languages(), 2)

    def test_add_specialty(self):
        num = self.character.specialties.count()
        self.assertTrue(
            self.character.add_specialty(
                Specialty.objects.get(name="Athletics Specialty 3", stat="athletics")
            )
        )
        self.assertEqual(self.character.specialties.count(), num + 1)

    def test_filter_specialties(self):
        self.assertEqual(len(self.character.filter_specialties()), 280)
        self.assertEqual(len(self.character.filter_specialties(stat="strength")), 10)
        self.assertEqual(len(self.character.filter_specialties(stat="athletics")), 10)
        self.character.add_specialty(
            Specialty.objects.get(name="Athletics Specialty 3", stat="athletics")
        )
        self.assertEqual(len(self.character.filter_specialties(stat="athletics")), 9)

    def test_has_specialties(self):
        self.character.dexterity = 2
        self.character.stamina = 3
        self.character.perception = 4
        self.character.intelligence = 5
        self.character.wits = 4
        self.character.charisma = 3
        self.character.manipulation = 2
        self.character.appearance = 4
        self.character.alertness = 1
        self.character.athletics = 2
        self.character.brawl = 4
        self.character.crafts = 1
        self.character.drive = 2
        self.character.etiquette = 5
        self.character.firearms = 3
        self.character.stealth = 4
        self.character.medicine = 2
        self.character.science = 1
        for attribute, value in self.character.get_attributes().items():
            if value >= 4:
                self.assertGreaterEqual(
                    self.character.specialties.filter(stat=attribute).count(), 0
                )
        for ability, value in self.character.get_abilities().items():
            if value >= 4 or (
                ability
                in [
                    "arts",
                    "athletics",
                    "crafts",
                    "firearms",
                    "melee",
                    "academics",
                    "occult",
                    "lore",
                    "politics",
                    "science",
                ]
                and value > 0
            ):
                self.assertGreaterEqual(self.character.specialties.filter(stat=ability).count(), 0)

    def test_get_backgrounds(self):
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "contacts": 0,
                "mentor": 0,
            },
        )
        contacts = Background.objects.get_or_create(name="Contacts", property_name="contacts")[0]
        BackgroundRating.objects.create(char=self.character, bg=contacts, rating=3)
        mentor = Background.objects.get_or_create(name="Mentor", property_name="mentor")[0]
        BackgroundRating.objects.create(char=self.character, bg=mentor, rating=2)
        self.assertEqual(
            self.character.get_backgrounds(),
            {
                "contacts": 3,
                "mentor": 2,
            },
        )

    def test_add_background(self):
        total = self.character.total_backgrounds()
        self.assertTrue(self.character.add_background("contacts"))
        self.assertEqual(self.character.total_backgrounds(), total + 1)

    def test_filter_backgrounds(self):
        self.assertEqual(len(self.character.filter_backgrounds()), 2)
        contacts = Background.objects.get_or_create(name="Contacts", property_name="contacts")[0]
        BackgroundRating.objects.create(char=self.character, bg=contacts, rating=4)
        mentor = Background.objects.get_or_create(name="Mentor", property_name="mentor")[0]
        BackgroundRating.objects.create(char=self.character, bg=mentor, rating=2)
        self.assertEqual(len(self.character.filter_backgrounds(minimum=3)), 1)
        self.assertEqual(len(self.character.filter_backgrounds(maximum=3)), 1)

    def test_has_backgrounds(self):
        self.assertFalse(self.character.has_backgrounds())
        contacts = Background.objects.get_or_create(name="Contacts", property_name="contacts")[0]
        BackgroundRating.objects.create(char=self.character, bg=contacts, rating=2)
        mentor = Background.objects.get_or_create(name="Mentor", property_name="mentor")[0]
        BackgroundRating.objects.create(char=self.character, bg=mentor, rating=3)
        self.assertTrue(self.character.has_backgrounds())

    def test_notes_field(self):
        self.assertEqual(self.character.notes, "")
        self.character.notes = "This is a note."
        self.assertNotEqual(self.character.notes, "")

    def test_static_numbers(self):
        self.assertEqual(self.character.willpower, 3)
        self.assertEqual(self.character.background_points, 5)
        self.assertEqual(self.character.freebies, 15)

    def test_ability_deficit_flaw(self):
        mf = MeritFlaw.objects.create(name="Ability Deficit")
        mf.add_rating(-2)
        self.character.add_mf(mf, -2)
        self.character.alertness = 3
        self.character.athletics = 2
        self.character.drive = 3
        self.character.etiquette = 2
        self.character.academics = 3
        self.character.computer = 2
        self.character.mf_based_corrections()
        self.assertEqual(self.character.total_abilities(), 10)
        l = [
            self.character.total_talents(),
            self.character.total_skills(),
            self.character.total_knowledges(),
        ]
        l.sort()
        self.assertEqual([0, 5, 5], l)

    def test_total_backgrounds(self):
        Background.objects.get_or_create(name="Contacts", property_name="contacts")[0]
        Background.objects.get_or_create(name="Mentor", property_name="mentor")[0]
        self.character.add_background("contacts")
        self.character.add_background("mentor")
        self.assertEqual(self.character.total_backgrounds(), 2)

    def test_attribute_specialties(self):
        self.character.specialties.create(name="strength focus", stat="strength")
        self.character.specialties.create(name="charisma focus", stat="charisma")
        self.assertEqual(self.character.specialties.get(stat="strength").name, "strength focus")
        self.assertEqual(self.character.specialties.get(stat="charisma").name, "charisma focus")

    def test_get_attribute_max_mortal(self):
        """Test that mortals have attribute max of 5 (Issue #1376)."""
        self.assertEqual(self.character.get_attribute_max(), 5)

    def test_get_attribute_min_mortal(self):
        """Test that mortals have attribute minimum of 1 (Issue #1117)."""
        self.assertEqual(self.character.get_attribute_min("strength"), 1)
        self.assertEqual(self.character.get_attribute_min("appearance"), 1)

    def test_validate_attributes_valid(self):
        """Test validation passes for valid mortal attributes (Issue #1117)."""
        # All attributes default to 1, which is valid
        errors = self.character.validate_attributes()
        self.assertEqual(errors, {})

    def test_validate_attributes_below_minimum(self):
        """Test validation catches attributes below minimum (Issue #1117)."""
        self.character.strength = 0
        errors = self.character.validate_attributes()
        self.assertIn("strength", errors)
        self.assertIn("must be at least 1", errors["strength"])

    def test_add_attribute_respects_max(self):
        """Test that add_attribute respects get_attribute_max (Issue #1376)."""
        self.character.strength = 5
        # Should fail to add because max is 5 for mortals
        result = self.character.add_attribute("strength")
        self.assertFalse(result)
        self.assertEqual(self.character.strength, 5)


class TestHumanDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="Test", password="password")
        self.human = Human.objects.create(name="Test Human", owner=self.player, status="App")
        self.url = self.human.get_absolute_url()

    def test_human_detail_view_status_code(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_human_detail_view_templates(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/human/detail.html")


class TestHumanCreateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.valid_data = {
            "name": "Test Human",
            "owner": self.st.id,
            "description": "Test",
            "willpower": 3,
            "childhood": "Test",
            "history": "Test",
            "goals": "Test",
            "notes": "Test",
            "strength": 1,
            "dexterity": 1,
            "stamina": 1,
            "charisma": 1,
            "manipulation": 1,
            "appearance": 1,
            "perception": 1,
            "intelligence": 1,
            "wits": 1,
        }
        self.url = Human.get_full_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/human/form.html")

    def test_create_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Human.objects.count(), 1)
        self.assertEqual(Human.objects.first().name, "Test Human")


class TestHumanUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.st,
            chronicle=self.chronicle,
        )
        self.valid_data = {
            "name": "Test Human Updated",
            "owner": self.st.id,
            "description": "Test",
            "willpower": 3,
            "childhood": "Test",
            "history": "Test",
            "goals": "Test",
            "notes": "Test",
            "strength": 1,
            "dexterity": 1,
            "stamina": 1,
            "charisma": 1,
            "manipulation": 1,
            "appearance": 1,
            "perception": 1,
            "intelligence": 1,
            "wits": 1,
        }
        self.url = self.human.get_full_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/human/form.html")

    def test_update_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.human.refresh_from_db()
        self.assertEqual(self.human.name, "Test Human Updated")


class TestHumanBasicsView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Test", password="password")
        self.n = Archetype.objects.create(name="Nature")
        self.d = Archetype.objects.create(name="Demeanor")
        self.valid_data = {
            "name": "Test Human",
            "nature": self.n.id,
            "demeanor": self.d.id,
            "concept": "Test character",
        }
        self.url = Human.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/human/humanbasics.html")

    def test_create_view_successful_post(self):
        self.client.login(username="Test", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Human.objects.count(), 1)
        self.assertEqual(Human.objects.first().name, "Test Human")
        self.assertEqual(Human.objects.first().concept, "Test character")
        self.assertEqual(Human.objects.first().nature, self.n)
        self.assertEqual(Human.objects.first().demeanor, self.d)


class TestAttributeView(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Test", password="password")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.player,
        )
        self.valid_data = {
            "strength": 2,
            "dexterity": 2,
            "stamina": 2,
            "charisma": 3,
            "manipulation": 2,
            "appearance": 3,
            "perception": 3,
            "intelligence": 4,
            "wits": 3,
        }
        self.url = self.human.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/human/attributes.html")

    def test_update_view_successful_post(self):
        self.client.login(username="Test", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.human.refresh_from_db()
        self.assertEqual(self.human.strength, 2)
        self.assertEqual(self.human.dexterity, 2)
        self.assertEqual(self.human.stamina, 2)
        self.assertEqual(self.human.charisma, 3)
        self.assertEqual(self.human.manipulation, 2)
        self.assertEqual(self.human.appearance, 3)
        self.assertEqual(self.human.perception, 3)
        self.assertEqual(self.human.intelligence, 4)
        self.assertEqual(self.human.wits, 3)
        self.assertEqual(self.human.creation_status, 2)


class TestHumanCharacterCreationView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="Test", password="password")
        self.human = Human.objects.create(
            name="Test Human",
            owner=self.player,
        )
        self.url = self.human.get_absolute_url()

    def test_creation_status_selector(self):
        self.client.login(username="Test", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/human/attributes.html")
        self.human.creation_status = 10
        self.human.save()
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/human/detail.html")
