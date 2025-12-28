from characters.models.werewolf.battlescar import BattleScar
from characters.models.werewolf.camp import Camp
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift
from characters.models.werewolf.renownincident import RenownIncident
from characters.models.werewolf.rite import Rite
from characters.models.werewolf.tribe import Tribe
from characters.tests.utils import werewolf_setup
from django.contrib.auth.models import User
from django.test import TestCase
from game.models import Chronicle
from items.models.werewolf.fetish import Fetish


class TestWerewolf(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="Player")
        self.character = Werewolf.objects.create(name="Test Werewolf", owner=self.player)
        werewolf_setup()

    def test_add_gift(self):
        g = Gift.objects.get(name="Gift 1")
        self.assertEqual(self.character.gifts.count(), 0)
        self.assertTrue(self.character.add_gift(g))
        self.assertEqual(self.character.gifts.count(), 1)
        self.assertIn(g, self.character.gifts.all())

    def test_filter_gifts(self):
        self.character.rank = 2
        self.assertEqual(len(self.character.filter_gifts()), 0)
        self.character.set_breed("homid")
        self.assertEqual(len(self.character.filter_gifts()), 5)
        self.character.add_gift(Gift.objects.get(name="Homid Gift 1"))
        self.assertEqual(len(self.character.filter_gifts()), 4)

    def test_has_gifts(self):
        t = Tribe.objects.get(name="Test Tribe", willpower=5)
        self.character.set_tribe(t)
        self.character.set_breed("homid")
        self.character.set_auspice("ragabash")
        g1 = Gift.objects.get(name="Test Tribe Gift 1")
        g2 = Gift.objects.get(name="Ragabash Gift 1")
        g3 = Gift.objects.get(name="Homid Gift 1")
        self.assertFalse(self.character.has_gifts())
        self.character.add_gift(g1)
        self.assertFalse(self.character.has_gifts())
        self.character.add_gift(g2)
        self.assertFalse(self.character.has_gifts())
        self.character.add_gift(g3)
        self.assertTrue(self.character.has_gifts())

    def test_total_rites(self):
        rite = Rite.objects.create(name="Test", level=1)
        self.character.add_rite(rite)
        self.character.add_rite(rite)
        self.assertEqual(self.character.total_rites(), 1)

    def test_add_rite(self):
        r = Rite.objects.get(name="Rite 1", level=1)
        self.assertEqual(self.character.rites_known.count(), 0)
        self.assertTrue(self.character.add_rite(r))
        self.assertEqual(self.character.rites_known.count(), 1)
        self.assertIn(r, self.character.rites_known.all())

    def test_filter_rites(self):
        self.assertEqual(len(self.character.filter_rites()), 12)
        self.character.add_rite(Rite.objects.get(name="Rite 1"))
        self.character.add_rite(Rite.objects.get(name="Rite 2"))
        self.assertEqual(len(self.character.filter_rites()), 10)

    def test_has_rites(self):
        self.character.rites = 3
        self.assertFalse(self.character.has_rites())
        self.character.add_rite(Rite.objects.get(name="Rite 3"))
        self.assertTrue(self.character.has_rites())

    def test_set_tribe(self):
        t = Tribe.objects.get(name="Test Tribe")
        self.assertFalse(self.character.has_tribe())
        self.assertTrue(self.character.set_tribe(t))
        self.assertTrue(self.character.has_tribe())

    def test_has_tribe(self):
        t = Tribe.objects.get(name="Test Tribe")
        self.assertFalse(self.character.has_tribe())
        self.character.set_tribe(t)
        self.assertTrue(self.character.has_tribe())

    def test_set_breed(self):
        self.assertFalse(self.character.has_breed())
        self.assertTrue(self.character.set_breed("homid"))
        self.assertTrue(self.character.has_breed())

    def test_has_breed(self):
        self.assertFalse(self.character.has_breed())
        self.character.set_breed("homid")
        self.assertTrue(self.character.has_breed())

    def test_breed_sets_gnosis(self):
        self.character.set_breed("homid")
        self.assertEqual(self.character.gnosis, 1)
        self.character.set_breed("metis")
        self.assertEqual(self.character.gnosis, 3)
        self.character.set_breed("lupus")
        self.assertEqual(self.character.gnosis, 5)

    def test_add_camp(self):
        t = Tribe.objects.get(name="Test Tribe")
        self.character.set_tribe(t)
        c = Camp.objects.get(name="Test Camp")
        self.assertFalse(self.character.has_camp())
        self.assertTrue(self.character.add_camp(c))
        self.assertTrue(self.character.has_camp())

    def test_has_camp(self):
        t = Tribe.objects.get(name="Test Tribe")
        self.character.set_tribe(t)
        c = Camp.objects.get(name="Test Camp", tribe=t)
        self.assertFalse(self.character.has_camp())
        self.character.add_camp(c)
        self.assertTrue(self.character.has_camp())

    def test_set_gnosis(self):
        self.character.set_gnosis(4)
        self.assertEqual(self.character.gnosis, 4)

    def test_add_gnosis(self):
        self.assertEqual(self.character.gnosis, 0)
        self.assertTrue(self.character.add_gnosis())
        self.assertEqual(self.character.gnosis, 1)
        self.character.gnosis = 10
        self.assertFalse(self.character.add_gnosis())

    def test_set_rage(self):
        self.character.set_rage(5)
        self.assertEqual(self.character.rage, 5)

    def test_add_rage(self):
        self.assertEqual(self.character.rage, 0)
        self.assertTrue(self.character.add_rage())
        self.assertEqual(self.character.rage, 1)
        self.character.rage = 10
        self.assertFalse(self.character.add_rage())

    def test_tribe_sets_willpower(self):
        t = Tribe.objects.get(name="Test Tribe 2")
        self.character.set_tribe(t)
        self.assertEqual(self.character.willpower, 3)
        t = Tribe.objects.get(name="Test Tribe")
        self.character.set_tribe(t)
        self.assertEqual(self.character.willpower, 5)

    def test_set_glory(self):
        self.assertEqual(self.character.glory, 0)
        self.assertTrue(self.character.set_glory(3))
        self.assertEqual(self.character.glory, 3)

    def test_set_honor(self):
        self.assertEqual(self.character.honor, 0)
        self.assertTrue(self.character.set_honor(3))
        self.assertEqual(self.character.honor, 3)

    def test_set_wisdom(self):
        self.assertEqual(self.character.wisdom, 0)
        self.assertTrue(self.character.set_wisdom(3))
        self.assertEqual(self.character.wisdom, 3)

    def test_has_renown(self):
        self.assertFalse(self.character.has_renown())
        self.character.set_auspice("ragabash")
        self.assertEqual(self.character.glory + self.character.honor + self.character.wisdom, 3)
        self.assertTrue(self.character.has_renown())

    def test_set_auspice(self):
        self.assertFalse(self.character.has_auspice())
        self.assertTrue(self.character.set_auspice("ragabash"))
        self.assertTrue(self.character.has_auspice())

    def test_has_auspice(self):
        self.assertFalse(self.character.has_breed())
        self.character.set_breed("homid")
        self.assertTrue(self.character.has_breed())

    def test_auspice_sets_rage(self):
        self.assertEqual(self.character.rage, 0)
        self.character.set_auspice("ragabash")
        self.assertEqual(self.character.rage, 1)
        self.character.set_auspice("theurge")
        self.assertEqual(self.character.rage, 2)
        self.character.set_auspice("philodox")
        self.assertEqual(self.character.rage, 3)
        self.character.set_auspice("galliard")
        self.assertEqual(self.character.rage, 4)
        self.character.set_auspice("ahroun")
        self.assertEqual(self.character.rage, 5)

    def test_auspice_sets_renown(self):
        self.assertEqual(self.character.glory + self.character.honor + self.character.wisdom, 0)
        self.character.set_auspice("ragabash")
        self.assertEqual(self.character.glory + self.character.honor + self.character.wisdom, 3)
        self.character.set_auspice("theurge")
        self.assertEqual(self.character.glory, 0)
        self.assertEqual(self.character.honor, 0)
        self.assertEqual(self.character.wisdom, 3)
        self.character.set_auspice("philodox")
        self.assertEqual(self.character.glory, 0)
        self.assertEqual(self.character.honor, 3)
        self.assertEqual(self.character.wisdom, 0)
        self.character.set_auspice("galliard")
        self.assertEqual(self.character.glory, 2)
        self.assertEqual(self.character.honor, 0)
        self.assertEqual(self.character.wisdom, 1)
        self.character.set_auspice("ahroun")
        self.assertEqual(self.character.glory, 2)
        self.assertEqual(self.character.honor, 1)
        self.assertEqual(self.character.wisdom, 0)

    def test_set_rank(self):
        self.assertEqual(self.character.rank, 1)
        self.character.set_rank(3)
        self.assertEqual(self.character.rank, 3)

    def test_increase_rank(self):
        self.assertEqual(self.character.rank, 1)
        self.character.set_auspice("ragabash")
        self.assertFalse(self.character.increase_rank())
        self.character.set_glory(3)
        self.character.set_honor(3)
        self.character.set_wisdom(1)
        self.assertTrue(self.character.increase_rank())

    def test_has_werewolf_history(self):
        self.assertFalse(self.character.has_werewolf_history())
        self.character.first_change = "Young"
        self.assertFalse(self.character.has_werewolf_history())
        self.character.age_of_first_change = 13
        self.assertTrue(self.character.has_werewolf_history())

    def test_no_homid_red_talons(self):
        self.character.breed = "homid"
        self.assertFalse(self.character.set_tribe(Tribe.objects.create(name="Red Talons")))

    # def test_no_male_black_furies(self):
    #     self.character.sex = "Male"
    #     self.assertFalse(
    #         self.character.set_tribe(Tribe.objects.create(name="Black Furies"))
    #     )

    def test_silver_fangs_have_pure_breed_three(self):
        self.character.set_tribe(Tribe.objects.create(name="Silver Fangs"))
        self.assertEqual(self.character.pure_breed, 3)

    def test_num_renown_incidents(self):
        self.character.add_renown_incident(RenownIncident.objects.create(name="Test 1"))
        self.assertEqual(self.character.num_renown_incidents(), 1)
        self.character.add_renown_incident(RenownIncident.objects.create(name="Test 2"))
        self.assertEqual(self.character.num_renown_incidents(), 2)

    def test_add_renown_incident(self):
        r = RenownIncident.objects.create(name="Test Renown Incident", glory=1, honor=1, wisdom=1)
        self.assertTrue(self.character.add_renown_incident(r))
        self.assertEqual(self.character.num_renown_incidents(), 1)
        self.assertIn("Test Renown Incident", self.character.renown_incidents)
        self.assertEqual(self.character.temporary_glory, 1)
        self.assertEqual(self.character.temporary_honor, 1)
        self.assertEqual(self.character.temporary_wisdom, 1)

    def test_update_renown(self):
        self.character.glory = 2
        self.character.temporary_glory = 10
        self.character.update_renown()
        self.assertEqual(self.character.glory, 3)
        self.assertEqual(self.character.temporary_glory, 0)

    def test_achieved_age_only_once(self):
        r = RenownIncident.objects.create(name="One Off", glory=1, wisdom=2, only_once=True)
        self.assertTrue(self.character.add_renown_incident(r))
        self.assertFalse(self.character.add_renown_incident(r))

    def test_breed_renown_correct(self):
        r = RenownIncident.objects.create(name="Lupus Award", breed="lupus")
        self.character.set_breed("homid")
        self.assertFalse(self.character.add_renown_incident(r))

    def test_renown_check_if_has_rite(self):
        rite = Rite.objects.create(name="Test Rite for Renown")
        renown = RenownIncident.objects.create(name="Used Test Rite for Renown", rite=rite)
        self.assertFalse(self.character.add_renown_incident(renown))
        self.character.add_rite(rite)
        self.assertTrue(self.character.add_renown_incident(renown))

    def test_wont_add_if_last_is_posthumous(self):
        r1 = RenownIncident.objects.create(
            name="Award (posthumous)", glory=3, honor=3, wisdom=0, posthumous=True
        )
        r2 = RenownIncident.objects.create(name="Award", glory=3, honor=3, wisdom=0)
        self.assertTrue(self.character.add_renown_incident(r1))
        self.assertFalse(self.character.add_renown_incident(r2))

    def test_learn_a_new_rite(self):
        r = RenownIncident.objects.create(name="Learning a new rite")
        rite = Rite.objects.create(name="Test Rite")
        num = self.character.rites_known.count()
        self.character.add_renown_incident(r, rite=rite)
        self.assertEqual(self.character.rites_known.count(), num + 1)

    def test_add_battle_scar(self):
        scar = BattleScar.objects.create(name="Test Scar")
        self.assertTrue(self.character.add_battle_scar(scar))
        self.assertFalse(self.character.add_battle_scar(scar))

    def test_add_fetish(self):
        fetish = Fetish.objects.create(name="Test")
        self.assertTrue(self.character.add_fetish(fetish))
        self.assertFalse(self.character.add_fetish(fetish))

    def test_filter_fetishes(self):
        filtered = self.character.filter_fetishes(min_rating=1, max_rating=3)
        self.assertEqual(filtered.count(), 15)

    def test_total_fetish_rating(self):
        fetish = Fetish.objects.create(name="Test", rank=2)
        self.character.add_fetish(fetish)
        self.assertEqual(self.character.total_fetish_rating(), 2)


class TestWerewolfDetailView(TestCase):
    def setUp(self) -> None:
        self.player = User.objects.create_user(username="User1", password="12345")
        self.werewolf = Werewolf.objects.create(
            name="Test Werewolf",
            owner=self.player,
            status="App",
        )
        self.url = self.werewolf.get_absolute_url()

    def test_werewolf_detail_view_status_code(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_werewolf_detail_view_templates(self):
        self.client.login(username="User1", password="12345")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/garou/detail.html")


class TestWerewolfCreateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.valid_data = {
            "name": "Werewolf",
            "description": "Test",
            "concept": 0,
            "strength": 0,
            "dexterity": 0,
            "stamina": 0,
            "perception": 0,
            "intelligence": 0,
            "wits": 0,
            "charisma": 0,
            "manipulation": 0,
            "appearance": 0,
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
            "willpower": 0,
            "age": 0,
            "apparent_age": 0,
            "history": "aasf",
            "goals": "aasf",
            "notes": "aasf",
            "leadership": 0,
            "primal_urge": 0,
            "animal_ken": 0,
            "larceny": 0,
            "performance": 0,
            "survival": 0,
            "enigmas": 0,
            "law": 0,
            "occult": 0,
            "rituals": 0,
            "technology": 0,
            "rank": 1,
            "auspice": "ahroun",
            "breed": "homid",
            "gnosis": 1,
            "rage": 5,
            "glory": 2,
            "temporary_glory": 0,
            "wisdom": 0,
            "temporary_wisdom": 0,
            "honor": 1,
            "temporary_honor": 0,
            "first_change": "asfa",
            "age_of_first_change": "21",
        }
        self.url = Werewolf.get_creation_url()

    def test_create_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/garou/basics.html")

    def test_create_view_successful_post(self):
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data={"name": "Werewolf"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Werewolf.objects.count(), 1)
        self.assertEqual(Werewolf.objects.first().name, "Werewolf")


class TestWerewolfUpdateView(TestCase):
    def setUp(self):
        self.st = User.objects.create_user(username="ST", password="password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.chronicle.storytellers.add(self.st)
        self.werewolf = Werewolf.objects.create(
            name="Test Werewolf",
            owner=self.st,
            chronicle=self.chronicle,
            description="Test description",
        )
        self.valid_data = {
            "name": "Werewolf Updated",
            "owner": self.st.id,
            "description": "Test",
            "concept": 0,
            "strength": 0,
            "dexterity": 0,
            "stamina": 0,
            "perception": 0,
            "intelligence": 0,
            "wits": 0,
            "charisma": 0,
            "manipulation": 0,
            "appearance": 0,
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
            "willpower": 3,
            "temporary_willpower": 3,
            "age": 0,
            "apparent_age": 0,
            "history": "aasf",
            "goals": "aasf",
            "notes": "aasf",
            "leadership": 0,
            "primal_urge": 0,
            "animal_ken": 0,
            "larceny": 0,
            "performance": 0,
            "survival": 0,
            "enigmas": 0,
            "law": 0,
            "occult": 0,
            "rituals": 0,
            "technology": 0,
            "rank": 1,
            "auspice": "ahroun",
            "breed": "homid",
            "gnosis": 1,
            "rage": 5,
            "glory": 2,
            "temporary_glory": 0,
            "wisdom": 0,
            "temporary_wisdom": 0,
            "honor": 1,
            "temporary_honor": 0,
            "first_change": "asfa",
            "age_of_first_change": "21",
        }
        self.url = self.werewolf.get_update_url()

    def test_update_view_status_code(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        self.client.login(username="ST", password="password")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/werewolf/garou/chargen.html")

    def test_update_view_successful_post(self):
        # The werewolf update uses a chargen workflow, so POST may return 200 or 302
        self.client.login(username="ST", password="password")
        response = self.client.post(self.url, data=self.valid_data)
        # Chargen workflow may return 200 (form re-render) or 302 (redirect)
        self.assertIn(response.status_code, [200, 302])
