"""Tests for the Werewolf-family character sheets (Spread C13)."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.werewolf.bastet import Bastet
from characters.models.werewolf.charm import SpiritCharm
from characters.models.werewolf.drone import Drone
from characters.models.werewolf.fomor import Fomor
from characters.models.werewolf.fomoripower import FomoriPower
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift, GiftPermission
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.renownincident import RenownIncident
from characters.models.werewolf.rite import Rite
from characters.models.werewolf.septposition import SeptPosition
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.tribe import Tribe
from items.models.werewolf.fetish import Fetish


def permission(condition, shifter="werewolf"):
    return GiftPermission.objects.get_or_create(shifter=shifter, condition=condition)[0]


class TestGarouSheet(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="player", password="pw")
        self.tribe = Tribe.objects.create(name="Uktena")
        self.werewolf = Werewolf.objects.create(
            name="Aurelio",
            owner=self.player,
            status="App",
            tribe=self.tribe,
            auspice="theurge",
            breed="homid",
            rank=2,
            concept="Lore-keeper",
            glory=2,
            temporary_glory=4,
            age_of_first_change=17,
            first_change="On the ice of Wolf Lake.",
        )
        self.sense_wyrm = Gift.objects.create(name="Sense Wyrm", rank=1)
        self.sense_wyrm.allowed.add(permission("theurge"))
        self.sense_magic = Gift.objects.create(name="Sense Magic", rank=1)
        self.sense_magic.allowed.add(permission("Uktena"), permission("theurge"))
        self.bird = Gift.objects.create(name="Spirit of the Bird", rank=2)
        self.bird.allowed.add(permission("Uktena"))
        self.werewolf.gifts.add(self.sense_wyrm, self.sense_magic, self.bird)
        self.rite = Rite.objects.create(name="Rite of Cleansing", level=1)
        self.werewolf.rites_known.add(self.rite)
        self.fetish = Fetish.objects.create(name="Crow-Feather Knife", rank=2)
        self.werewolf.fetishes_owned.add(self.fetish)
        self.client.login(username="player", password="pw")

    def test_gifts_by_rank_labels_the_source(self):
        groups = self.werewolf.gifts_by_rank()
        self.assertEqual([rank for rank, _ in groups], [1, 2])
        rank_one = {gift.name: source for gift, source in groups[0][1]}
        # The tribe wins when a gift is open to both the tribe and the auspice.
        self.assertEqual(rank_one, {"Sense Magic": "Uktena", "Sense Wyrm": "Theurge"})
        self.assertEqual(groups[1][1], [(self.bird, "Uktena")])

    def test_sheet_shows_cover_basics_and_gift_columns(self):
        response = self.client.get(self.werewolf.get_absolute_url())
        self.assertContains(response, '<span class="tl-facts__k">Tribe</span>', html=False)
        self.assertContains(response, '<span class="tl-facts__k">Auspice</span>', html=False)
        self.assertContains(response, "Fostern")
        self.assertContains(response, 'id="gifts"')
        self.assertContains(response, "Rank 2")
        self.assertContains(response, '<span class="tl-gift__src">Uktena</span>', html=False)
        self.assertContains(response, self.rite.get_absolute_url())
        self.assertContains(response, self.fetish.get_absolute_url())

    def test_sheet_shows_advantages_beside_renown(self):
        response = self.client.get(self.werewolf.get_absolute_url())
        self.assertContains(response, 'class="tl-section tl-span-6" id="advantages"')
        self.assertContains(response, 'class="tl-section tl-section--power tl-span-6" id="renown"')
        self.assertContains(response, 'class="tl-track tl-track--wide"')
        self.assertContains(response, 'aria-label="4 of 10"')  # temporary Glory squares
        for label in ("Willpower", "Gnosis", "Rage", "Glory", "Honor", "Wisdom"):
            self.assertContains(response, f'<span class="tl-track__label">{label}</span>')

    def test_sheet_three_columns_and_first_change(self):
        response = self.client.get(self.werewolf.get_absolute_url())
        self.assertContains(response, 'class="tl-section tl-span-4" id="backgrounds"')
        self.assertContains(response, 'class="tl-section tl-span-4" id="health"')
        self.assertContains(response, "Age of First Change")
        self.assertContains(response, "On the ice of Wolf Lake.")
        self.assertNotContains(response, 'class="tg-card')

    def test_experience_tab_lists_renown_incidents(self):
        incident = RenownIncident.objects.create(name="Performed a rite")
        self.werewolf.renown_incidents = ["Performed a rite", "Unrecorded deed"]
        self.werewolf.save()
        response = self.client.get(self.werewolf.get_absolute_url() + "?tab=experience")
        self.assertContains(response, 'id="renown-incidents"')
        self.assertContains(response, incident.get_absolute_url())
        self.assertContains(response, "Unrecorded deed")
        self.assertContains(response, "Spent XP")
        sheet = self.client.get(self.werewolf.get_absolute_url())
        self.assertNotContains(sheet, 'id="renown-incidents"')


class TestWerewolfFamilySheets(TestCase):
    def setUp(self):
        self.player = User.objects.create_user(username="player", password="pw")
        self.client.login(username="player", password="pw")

    def test_kinfolk_sheet(self):
        tribe = Tribe.objects.create(name="Fianna")
        kin = Kinfolk.objects.create(
            name="Ruth", owner=self.player, status="App", tribe=tribe, relation="Aunt", gnosis=1
        )
        gift = Gift.objects.create(name="Persuasion", rank=1)
        gift.allowed.add(permission("Kinfolk"))
        kin.gifts.add(gift)
        response = self.client.get(kin.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/kinfolk/detail.html")
        self.assertContains(response, "Aunt")
        self.assertContains(response, '<span class="tl-gift__src">Kinfolk</span>', html=False)
        self.assertContains(response, 'id="renown"')
        self.assertContains(response, '<span class="tl-track__label">Gnosis</span>')

    def test_kinfolk_edit_page_is_a_form(self):
        staff = User.objects.create_user(username="staff", password="pw", is_staff=True)
        kin = Kinfolk.objects.create(name="Ruth", owner=self.player)
        self.client.force_login(staff)
        response = self.client.get(kin.get_update_url())
        self.assertTemplateUsed(response, "characters/werewolf/kinfolk/form.html")
        self.assertTemplateUsed(response, "core/form.html")
        self.assertContains(response, 'method="post"')

    def test_fomor_sheet(self):
        fomor = Fomor.objects.create(name="Dale", owner=self.player, status="App", rage=3)
        power = FomoriPower.objects.create(name="Berserker")
        fomor.powers.add(power)
        response = self.client.get(fomor.get_absolute_url())
        self.assertContains(response, "Fomor Powers")
        self.assertContains(response, power.get_absolute_url())
        self.assertContains(response, '<span class="tl-track__label">Rage</span>')
        self.assertNotContains(response, '<span class="tl-track__label">Gnosis</span>')

    def test_drone_sheet_is_a_full_human_sheet(self):
        drone = Drone.objects.create(
            name="Tess", owner=self.player, status="App", bane_name="Scrag", willpower_per_turn=2
        )
        response = self.client.get(drone.get_absolute_url())
        self.assertContains(response, "Possessing Bane")
        self.assertContains(response, "Scrag")
        self.assertContains(response, 'id="attributes"')
        self.assertContains(response, "Willpower per turn")

    def test_fera_sheet_uses_breed_choices_and_renown(self):
        bastet = Bastet.objects.create(
            name="Nadia",
            owner=self.player,
            status="App",
            breed="homid",
            tribe="simba",
            pryio="midnight",
            ferocity=2,
            cunning=3,
        )
        gift = Gift.objects.create(name="Sense Prey", rank=1)
        gift.allowed.add(permission("simba", "bastet"))
        bastet.gifts.add(gift)
        self.assertIn(("Tribe", "Simba"), bastet.sheet_choices())
        self.assertEqual(
            [label for label, _, _ in bastet.renown_tracks()], ["Ferocity", "Honor", "Cunning"]
        )
        response = self.client.get(bastet.get_absolute_url())
        self.assertTemplateUsed(response, "characters/werewolf/fera/detail.html")
        self.assertContains(response, "Midnight")
        self.assertContains(response, '<span class="tl-gift__src">Simba</span>', html=False)
        self.assertContains(response, '<span class="tl-track__label">Ferocity</span>')

    def test_spirit_sheet(self):
        spirit = SpiritCharacter.objects.create(
            name="Lake Wind", owner=self.player, status="App", essence=15, description="Cold."
        )
        charm = SpiritCharm.objects.create(name="Airt Sense", essence_cost=1)
        spirit.charms.add(charm)
        response = self.client.get(spirit.get_absolute_url())
        self.assertContains(response, '<span class="tl-facts__k">Essence</span>', html=False)
        self.assertContains(response, 'id="charms"')
        self.assertContains(response, charm.get_absolute_url())
        self.assertContains(response, "Cold.")

    def test_sept_position_uses_the_object_page(self):
        staff = User.objects.create_user(username="staff", password="pw", is_staff=True)
        position = SeptPosition.objects.create(name="Warder", description="Guards the caern.")
        self.client.force_login(staff)
        response = self.client.get(position.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/object.html")
        self.assertContains(response, "Guards the caern.")
