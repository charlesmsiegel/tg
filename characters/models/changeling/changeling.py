from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.changeling.house import House
from characters.models.changeling.kith import Kith
from characters.models.changeling.legacy import Legacy
from core.utils import add_dot, weighted_choice
from django.db import models
from django.utils.timezone import now


class Changeling(CtDHuman):
    type = "changeling"

    freebie_step = 6

    court = models.CharField(
        default="",
        max_length=20,
        choices=[("seelie", "Seelie"), ("unseelie", "Unseelie")],
    )
    seelie_legacy = models.ForeignKey(
        Legacy,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="seelie_legacy_of",
    )
    unseelie_legacy = models.ForeignKey(
        Legacy,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="unseelie_legacy_of",
    )

    kith = models.ForeignKey(Kith, null=True, blank=True, on_delete=models.SET_NULL)
    seeming = models.CharField(
        default="",
        max_length=15,
        choices=[("childling", "Childling"), ("wilder", "Wilder"), ("grump", "Grump")],
    )
    house = models.ForeignKey(House, null=True, blank=True, on_delete=models.SET_NULL)

    autumn = models.IntegerField(default=0)
    chicanery = models.IntegerField(default=0)
    chronos = models.IntegerField(default=0)
    contract = models.IntegerField(default=0)
    dragons_ire = models.IntegerField(default=0)
    legerdemain = models.IntegerField(default=0)
    metamorphosis = models.IntegerField(default=0)
    naming = models.IntegerField(default=0)
    oneiromancy = models.IntegerField(default=0)
    primal = models.IntegerField(default=0)
    pyretics = models.IntegerField(default=0)
    skycraft = models.IntegerField(default=0)
    soothsay = models.IntegerField(default=0)
    sovereign = models.IntegerField(default=0)
    spring = models.IntegerField(default=0)
    summer = models.IntegerField(default=0)
    wayfare = models.IntegerField(default=0)
    winter = models.IntegerField(default=0)

    actor = models.IntegerField(default=0)
    fae = models.IntegerField(default=0)
    nature_realm = models.IntegerField(default=0)
    prop = models.IntegerField(default=0)
    scene = models.IntegerField(default=0)
    time = models.IntegerField(default=0)

    banality = models.IntegerField(default=3)
    glamour = models.IntegerField(default=4)

    MUSING_THRESHOLDS = [
        ("inspire_creativity", "Inspire Creativity"),
        ("create_hope", "Create Hope"),
        ("create_love", "Create Love"),
        ("create_calm", "Create Calm"),
        ("foster_trust", "Foster Trust"),
        ("help_those_in_need", "Help Those In Need"),
        ("foster_dreams", "Foster Dreams"),
    ]

    RAVAGING_THRESHOLDS = [
        ("exhaust_creativity", "Exhaust Creativity"),
        ("destroy_hope", "Destroy Hope"),
        ("destroy_love", "Destroy Love"),
        ("create_anger", "Create Anger"),
        ("break_trust", "Break Trust"),
        ("exploit_dependence", "Exploit Dependence"),
        ("destroy_illusions", "Destroy Illusions"),
    ]

    musing_threshold = models.CharField(
        default="",
        max_length=20,
        choices=MUSING_THRESHOLDS,
    )
    ravaging_threshold = models.CharField(
        default="",
        max_length=20,
        choices=RAVAGING_THRESHOLDS,
    )

    antithesis = models.TextField(default="")

    true_name = models.TextField(default="")
    date_ennobled = models.DateField(blank=True, null=True)
    crysalis = models.TextField(default="")
    date_of_crysalis = models.DateField(blank=True, null=True)
    fae_mien = models.TextField(default="")

    class Meta:
        verbose_name = "Changeling"
        verbose_name_plural = "Changelings"

    def has_court(self):
        return self.court != ""

    def set_court(self, court):
        self.court = court
        return True

    def eligible_for_house(self):
        if self.kith:
            return self.title > 0 or "Sidhe" in self.kith.name
        return self.title > 0

    def has_house(self):
        if self.eligible_for_house():
            return self.house is not None
        return self.house is None

    def set_house(self, house):
        if self.eligible_for_house() and house.court == self.court:
            self.house = house
            return True
        return False

    def has_seelie_legacy(self):
        return self.seelie_legacy is not None

    def set_seelie_legacy(self, legacy):
        if legacy.court == "seelie":
            self.seelie_legacy = legacy
            return True
        return False

    def has_unseelie_legacy(self):
        return self.unseelie_legacy is not None

    def set_unseelie_legacy(self, legacy):
        if legacy.court == "unseelie":
            self.unseelie_legacy = legacy
            return True
        return False

    def has_seeming(self):
        return self.seeming != ""

    def set_seeming(self, seeming):
        self.willpower = 4
        self.seeming = seeming
        if self.seeming == "childling":
            self.add_glamour()
        if self.seeming == "grump":
            self.add_willpower()
        return True

    def has_kith(self):
        return self.kith is not None

    def set_kith(self, kith):
        self.kith = kith
        return True

    def add_art(self, art):
        return add_dot(self, art, 5)

    def get_arts(self):
        return {
            "autumn": self.autumn,
            "chicanery": self.chicanery,
            "chronos": self.chronos,
            "contract": self.contract,
            "dragons_ire": self.dragons_ire,
            "legerdemain": self.legerdemain,
            "metamorphosis": self.metamorphosis,
            "naming": self.naming,
            "oneiromancy": self.oneiromancy,
            "primal": self.primal,
            "pyretics": self.pyretics,
            "skycraft": self.skycraft,
            "soothsay": self.soothsay,
            "sovereign": self.sovereign,
            "spring": self.spring,
            "summer": self.summer,
            "wayfare": self.wayfare,
            "winter": self.winter,
        }

    def filter_arts(self, minimum=0, maximum=5):
        return [k for k, v in self.get_arts().items() if minimum <= v <= maximum]

    def has_arts(self):
        return self.total_arts() == 3

    def total_arts(self):
        return sum(v for v in self.get_arts().values())

    def add_realm(self, realm):
        return add_dot(self, realm, 5)

    def get_realms(self):
        return {
            "actor": self.actor,
            "fae": self.fae,
            "nature_realm": self.nature_realm,
            "prop": self.prop,
            "scene": self.scene,
            "time": self.time,
        }

    def filter_realms(self, minimum=0, maximum=5):
        return [k for k, v in self.get_realms().items() if minimum <= v <= maximum]

    def has_realms(self):
        return self.total_realms() == 5

    def total_realms(self):
        return sum(v for v in self.get_realms().values())

    def add_banality(self):
        return add_dot(self, "banality", 10)

    def add_glamour(self):
        return add_dot(self, "glamour", 10)

    def has_musing_threshold(self):
        return self.musing_threshold != ""

    def set_musing_threshold(self, threshold):
        self.musing_threshold = threshold
        return True

    def has_ravaging_threshold(self):
        return self.ravaging_threshold != ""

    def set_ravaging_threshold(self, threshold):
        self.ravaging_threshold = threshold
        return True

    def set_antithesis(self, antithesis):
        self.antithesis = antithesis
        return True

    def has_antithesis(self):
        return self.antithesis != ""

    def has_changeling_history(self):
        b = True
        b = b and (self.true_name != "")
        b = b and (self.date_ennobled != "")
        b = b and (self.crysalis != "")
        b = b and (self.date_of_crysalis != "")
        return b

    def set_changeling_history(
        self, true_name, date_ennobled, crysalis, date_of_crysalis
    ):
        self.true_name = true_name
        self.date_ennobled = date_ennobled
        self.crysalis = crysalis
        self.date_of_crysalis = date_of_crysalis
        return True

    def has_changeling_appearance(self):
        return self.fae_mien != ""

    def set_changeling_appearance(self, fae_mien):
        self.fae_mien = fae_mien
        return True

    def birthright_correction(self):
        if self.kith.name == "Troll":
            self.add_attribute("strength", maximum=10)
            self.max_health_levels += 1
            self.save()
        if self.kith.name == "Satyr":
            self.add_attribute("stamina", maximum=10)
        if self.kith.name == "Piskey":
            self.add_attribute("dexterity", maximum=10)
        if "Sidhe" in self.kith.name:
            self.add_attribute("appearance", maximum=10)
            self.add_attribute("appearance", maximum=10)

    def art_freebies(self, form):
        """Spend freebies to increase an art"""
        trait = form.cleaned_data["example"]
        value = getattr(self, trait.property_name, 0) + 1
        cost = 5
        self.add_art(trait.property_name)
        self.freebies -= cost
        self.spent_freebies.append(self.freebie_spend_record(trait.name, trait.property_name, value, cost))
        return True

    def realm_freebies(self, form):
        """Spend freebies to increase a realm"""
        trait = form.cleaned_data["example"]
        value = getattr(self, trait.property_name, 0) + 1
        cost = 3
        self.add_realm(trait.property_name)
        self.freebies -= cost
        self.spent_freebies.append(self.freebie_spend_record(trait.name, trait.property_name, value, cost))
        return True

    def glamour_freebies(self, form):
        """Spend freebies to increase glamour"""
        trait = "Glamour"
        value = self.glamour + 1
        cost = 3
        self.add_glamour()
        self.freebies -= cost
        self.spent_freebies.append(self.freebie_spend_record(trait, "glamour", value, cost))
        return True

    def xp_frequencies(self):
        """Return frequency distribution for XP spending (for random character generation)."""
        return {
            "attribute": 16,
            "ability": 20,
            "background": 13,
            "willpower": 1,
            "art": 30,
            "realm": 15,
            "glamour": 3,
            "banality": 1,
        }

    def xp_cost(self, trait_type, trait_value=None):
        """Return XP cost for changeling-specific traits."""
        from collections import defaultdict

        costs = defaultdict(
            lambda: super().xp_cost(trait_type, trait_value) if trait_value is not None else 10000,
            {
                "art": 8,
                "realm": 5,
                "glamour": 3,
                "banality": 2,
            },
        )

        if trait_type in ["art", "realm", "glamour", "banality"]:
            if trait_value is not None:
                return costs[trait_type] * trait_value
            return costs[trait_type]

        return costs[trait_type]

    def spend_xp(self, trait):
        """Spend XP on a trait."""
        output = super().spend_xp(trait)
        if output in [True, False]:
            return output

        # Check if trait is an art
        arts_list = list(self.get_arts().keys())

        if trait in arts_list:
            current_value = getattr(self, trait)
            cost = self.xp_cost("art", current_value + 1)

            if cost <= self.xp:
                if self.add_art(trait):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
                return False
            return False

        # Check if trait is a realm
        realms_list = list(self.get_realms().keys())

        if trait in realms_list:
            current_value = getattr(self, trait)
            cost = self.xp_cost("realm", current_value + 1)

            if cost <= self.xp:
                if self.add_realm(trait):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
                return False
            return False

        # Handle glamour
        if trait == "glamour":
            cost = self.xp_cost("glamour", self.glamour + 1)
            if cost <= self.xp:
                if self.add_glamour():
                    self.xp -= cost
                    self.add_to_spend(trait, self.glamour, cost)
                    return True
                return False
            return False

        # Handle banality
        if trait == "banality":
            cost = self.xp_cost("banality", self.banality + 1)
            if cost <= self.xp:
                if self.add_banality():
                    self.xp -= cost
                    self.add_to_spend(trait, self.banality, cost)
                    return True
                return False
            return False

        return trait

    def freebie_frequencies(self):
        """Return frequency distribution for freebie spending (for random character generation)."""
        return {
            "attribute": 15,
            "ability": 8,
            "background": 10,
            "willpower": 1,
            "meritflaw": 20,
            "art": 25,
            "realm": 15,
            "glamour": 5,
            "banality": 1,
        }

    def freebie_costs(self):
        """Return a dictionary of freebie costs for changeling traits."""
        costs = super().freebie_costs()
        costs.update({
            "art": 5,
            "realm": 3,
            "glamour": 3,
            "banality": 2,
        })
        return costs

    def freebie_cost(self, trait_type):
        """Return freebie cost for changeling-specific traits."""
        changeling_costs = {
            "art": 5,
            "realm": 3,
            "glamour": 3,
            "banality": 2,
        }
        if trait_type in changeling_costs.keys():
            return changeling_costs[trait_type]
        return super().freebie_cost(trait_type)

    def spend_freebies(self, trait):
        """Spend freebie points on a trait."""
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output

        # Check if trait is an art
        arts_list = list(self.get_arts().keys())

        if trait in arts_list:
            cost = self.freebie_cost("art")
            if cost <= self.freebies:
                if self.add_art(trait):
                    self.freebies -= cost
                    return True
                return False
            return False

        # Check if trait is a realm
        realms_list = list(self.get_realms().keys())

        if trait in realms_list:
            cost = self.freebie_cost("realm")
            if cost <= self.freebies:
                if self.add_realm(trait):
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle glamour
        if trait == "glamour":
            cost = self.freebie_cost("glamour")
            if cost <= self.freebies:
                if self.add_glamour():
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle banality
        if trait == "banality":
            cost = self.freebie_cost("banality")
            if cost <= self.freebies:
                if self.add_banality():
                    self.freebies -= cost
                    return True
                return False
            return False

        return trait
