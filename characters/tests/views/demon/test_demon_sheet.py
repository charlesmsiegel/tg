"""Rendering tests for the Demon-family character sheets (Spread design)."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.demon import Demon
from characters.models.demon.apocalyptic_form import ApocalypticForm, ApocalypticFormTrait
from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.earthbound import Earthbound
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.lore import Lore
from characters.models.demon.thrall import Thrall
from characters.models.demon.visage import Visage
from game.models import Chronicle


class DemonSheetTestBase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.chronicle = Chronicle.objects.create(name="The Burning Year")
        self.house = DemonHouse.objects.create(name="Devils", celestial_name="Namaru")
        self.visage = Visage.objects.create(name="Bel", description="A figure of blinding glory.")
        self.client.login(username="owner", password="password")

    def get(self, obj, **params):
        response = self.client.get(obj.get_absolute_url(), params)
        self.assertEqual(response.status_code, 200)
        return response


class TestDemonSheet(DemonSheetTestBase):
    def setUp(self):
        super().setUp()
        self.faction = DemonFaction.objects.create(name="Reconcilers")
        self.flame = Lore.objects.create(name="Lore of Flame", property_name="flame")
        low = ApocalypticFormTrait.objects.create(name="Wings", cost=2, description="Flight.")
        high = ApocalypticFormTrait.objects.create(
            name="Searing Light", cost=4, high_torment_only=True
        )
        form = ApocalypticForm.objects.create(name="Form")
        form.low_torment_traits.add(low)
        form.high_torment_traits.add(high)
        self.demon = Demon.objects.create(
            name="Ahrimel",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            house=self.house,
            faction=self.faction,
            visage=self.visage,
            apocalyptic_form=form,
            celestial_name="Ahrimel of the Flame",
            lore_of_flame=2,
            lore_of_the_celestials=1,
            faith=5,
            temporary_faith=3,
            torment=4,
            willpower=6,
            conviction=3,
            conscience=2,
            courage=1,
            age_of_fall=4000,
            abyss_duration="Six thousand years.",
        )
        self.thrall = Thrall.objects.create(name="Marcy", owner=self.owner, master=self.demon)
        self.demon.add_pact(self.thrall, terms="Protection for her son.", faith_payment=2)

    def test_uses_spread_shell_without_bootstrap(self):
        response = self.get(self.demon)
        self.assertTemplateUsed(response, "core/tl_base.html")
        self.assertTemplateUsed(response, "characters/demon/display_includes/lore_block.html")
        self.assertNotContains(response, "tg-card")
        self.assertNotContains(response, 'class="row')

    def test_cover_basics(self):
        response = self.get(self.demon)
        for label in ("House", "Faction", "Visage", "Host"):
            self.assertContains(response, f'<span class="tl-facts__k">{label}</span>', html=False)
        self.assertContains(response, self.house.get_absolute_url())
        self.assertContains(response, self.faction.get_absolute_url())
        # C19: the celestial name titles the cover; the name is the mortal host's.
        title = response.content.decode().split('class="tl-cover__name', 1)[1].split("</h1>", 1)[0]
        self.assertIn("Ahrimel of the Flame", title)
        self.assertContains(response, f"Host: {self.demon.name}")

    def test_lores_are_the_power_section(self):
        response = self.get(self.demon)
        self.assertContains(response, 'class="tl-section tl-section--power tl-span-7" id="lores"')
        # Linked to the Lore record where one exists, computed label otherwise.
        self.assertContains(
            response, f'<a href="{self.flame.get_absolute_url()}">Lore of Flame</a>'
        )
        self.assertContains(response, "Lore of the Celestials")
        self.assertNotContains(response, "Lore of Storms")

    def test_advantage_tracks(self):
        content = self.get(self.demon).content.decode()
        for label in ("Faith", "Torment", "Willpower"):
            self.assertIn(f'<span class="tl-track__label">{label}</span>', content)
        self.assertIn('aria-label="5 of 10"', content)  # permanent Faith
        self.assertIn('aria-label="3 of 10"', content)  # temporary Faith

    def test_virtues_block(self):
        response = self.get(self.demon)
        self.assertContains(response, 'id="virtues"')
        for label in ("Conviction", "Conscience", "Courage"):
            self.assertContains(response, label)

    def test_apocalyptic_form_columns(self):
        response = self.get(self.demon)
        self.assertContains(response, 'id="apocalyptic-form"')
        self.assertContains(response, "Low Torment traits · 1/4")
        self.assertContains(response, "High Torment traits · 1/4")
        self.assertContains(response, "Wings")
        self.assertContains(response, "High Torment only · 4 pts")
        self.assertContains(response, "6/16 points spent")
        self.assertContains(response, "A figure of blinding glory.")

    def test_pacts_and_history(self):
        response = self.get(self.demon)
        self.assertContains(response, 'id="pacts"')
        self.assertContains(response, "Protection for her son.")
        self.assertContains(response, "Age of Fall")
        self.assertContains(response, "Six thousand years.")

    def test_empty_sections_hidden(self):
        self.demon.visage = None
        self.demon.apocalyptic_form = None
        self.demon.save()
        self.demon.get_pacts().delete()
        response = self.get(self.demon)
        self.assertNotContains(response, 'id="apocalyptic-form"')
        self.assertNotContains(response, 'id="pacts"')
        self.assertNotContains(response, 'id="rituals"')


class TestEarthboundSheet(DemonSheetTestBase):
    def test_earthbound_sections(self):
        earthbound = Earthbound.objects.create(
            name="Ruination",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            house=self.house,
            visage=self.visage,
            reliquary_type="location",
            reliquary_description="The flooded church.",
            manifestation_range=12,
            urge_flesh=2,
            lore_of_flame=4,
            cult_size="Forty fishermen",
            date_summoned="1791",
        )
        response = self.get(earthbound)
        self.assertTemplateUsed(response, "core/tl_base.html")
        self.assertNotContains(response, "tg-card")
        for section in ("lores", "advantages", "virtues", "urges", "reliquary", "cult", "history"):
            self.assertContains(response, f'id="{section}"')
        self.assertContains(response, "12 yards")
        self.assertContains(response, "The flooded church.")
        self.assertContains(response, "Lore of Flame")
        self.assertContains(response, "1791")
        self.assertContains(response, "No apocalyptic form selected.")


class TestThrallSheet(DemonSheetTestBase):
    def test_thrall_sections(self):
        demon = Demon.objects.create(name="Master Demon", owner=self.owner)
        thrall = Thrall.objects.create(
            name="Marcy",
            owner=self.owner,
            chronicle=self.chronicle,
            status="App",
            master=demon,
            faith_potential=3,
            daily_faith_offered=2,
            enhancements=["Immune to fear"],
        )
        demon.add_pact(thrall, terms="Protection.", faith_payment=1)
        response = self.get(thrall)
        self.assertTemplateUsed(response, "core/tl_base.html")
        self.assertNotContains(response, "tg-card")
        self.assertContains(response, '<span class="tl-facts__k">Master</span>', html=False)
        self.assertContains(response, 'id="enhancements"')
        self.assertContains(response, "Immune to fear")
        self.assertContains(response, "Faith Potential")
        self.assertContains(response, "Daily Faith")
        self.assertContains(response, "Active Pacts")
        self.assertContains(response, 'id="virtues"')


class TestDtFHumanSheet(DemonSheetTestBase):
    def test_human_sheet(self):
        human = DtFHuman.objects.create(
            name="Mortal", owner=self.owner, chronicle=self.chronicle, status="App", enigmas=2
        )
        response = self.get(human)
        self.assertTemplateUsed(response, "core/tl_base.html")
        self.assertNotContains(response, "tg-card")
        self.assertContains(response, "Enigmas")
        self.assertContains(response, 'id="health"')
