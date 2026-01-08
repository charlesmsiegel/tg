from characters.models.werewolf.battlescar import BattleScar
from characters.models.werewolf.camp import Camp
from characters.models.werewolf.gift import Gift, GiftPermission
from characters.models.werewolf.renownincident import RenownIncident
from characters.models.werewolf.rite import Rite
from characters.models.werewolf.tribe import Tribe
from characters.models.werewolf.wtahuman import WtAHuman
from core.linked_stat import linked_stat_fields
from core.utils import add_dot
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from items.models.werewolf.fetish import Fetish


class Werewolf(WtAHuman):
    type = "werewolf"

    rank_names = {
        1: "Cliath",
        2: "Fostern",
        3: "Adren",
        4: "Athro",
        5: "Elder",
    }

    AUSPICES = [
        ("ragabash", "Ragabash"),
        ("theurge", "Theurge"),
        ("philodox", "Philodox"),
        ("galliard", "Galliard"),
        ("ahroun", "Ahroun"),
    ]

    rank = models.IntegerField(default=1)
    auspice = models.CharField(
        default="",
        max_length=100,
        choices=AUSPICES,
        blank=True,
    )

    BREEDS = [
        ("homid", "Homid"),
        ("metis", "Metis"),
        ("lupus", "Lupus"),
    ]

    breed = models.CharField(
        default="",
        max_length=100,
        choices=BREEDS,
        blank=True,
    )
    tribe = models.ForeignKey(Tribe, blank=True, null=True, on_delete=models.SET_NULL)
    camps = models.ManyToManyField(Camp, blank=True)

    # All Garou must have at least 1 Gnosis and 1 Rage (W20 Core Rulebook)
    gnosis = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message="All werewolves must have at least 1 Gnosis"),
            MaxValueValidator(10),
        ],
    )
    rage = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message="All werewolves must have at least 1 Rage"),
            MaxValueValidator(10),
        ],
    )

    glory, temporary_glory, glory_renown = linked_stat_fields(
        "glory", default=0, cap_temporary=False
    )
    wisdom, temporary_wisdom, wisdom_renown = linked_stat_fields(
        "wisdom", default=0, cap_temporary=False
    )
    honor, temporary_honor, honor_renown = linked_stat_fields(
        "honor", default=0, cap_temporary=False
    )

    renown_incidents = models.JSONField(default=list, blank=True)  # list is callable - safe

    gifts = models.ManyToManyField(Gift, blank=True)
    rites_known = models.ManyToManyField(Rite, blank=True)
    fetishes_owned = models.ManyToManyField(Fetish, blank=True)

    first_change = models.TextField(default="", blank=True)
    battle_scars = models.ManyToManyField("BattleScar", blank=True)
    age_of_first_change = models.IntegerField(default=0)

    gift_permissions = models.ManyToManyField(GiftPermission, blank=True)

    requirements = {
        "ragabash": {
            1: {"total": 3},
            2: {"total": 7},
            3: {"total": 13},
            4: {"total": 19},
            5: {"total": 25},
        },
        "theurge": {
            1: {"glory": 0, "honor": 0, "wisdom": 3},
            2: {"glory": 1, "honor": 0, "wisdom": 5},
            3: {"glory": 2, "honor": 1, "wisdom": 7},
            4: {"glory": 4, "honor": 2, "wisdom": 9},
            5: {"glory": 4, "honor": 9, "wisdom": 10},
        },
        "philodox": {
            1: {"glory": 0, "honor": 3, "wisdom": 0},
            2: {"glory": 1, "honor": 4, "wisdom": 1},
            3: {"glory": 2, "honor": 6, "wisdom": 2},
            4: {"glory": 3, "honor": 8, "wisdom": 4},
            5: {"glory": 4, "honor": 10, "wisdom": 9},
        },
        "galliard": {
            1: {"glory": 2, "honor": 0, "wisdom": 1},
            2: {"glory": 4, "honor": 0, "wisdom": 2},
            3: {"glory": 4, "honor": 2, "wisdom": 4},
            4: {"glory": 7, "honor": 2, "wisdom": 6},
            5: {"glory": 9, "honor": 5, "wisdom": 9},
        },
        "ahroun": {
            1: {"glory": 2, "honor": 1, "wisdom": 0},
            2: {"glory": 4, "honor": 1, "wisdom": 1},
            3: {"glory": 6, "honor": 3, "wisdom": 1},
            4: {"glory": 9, "honor": 4, "wisdom": 2},
            5: {"glory": 10, "honor": 9, "wisdom": 4},
        },
    }

    class Meta:
        verbose_name = "Werewolf"
        verbose_name_plural = "Werewolves"
        constraints = [
            CheckConstraint(
                check=Q(gnosis__gte=1, gnosis__lte=10),
                name="characters_werewolf_gnosis_range",
                violation_error_message="Gnosis must be between 1 and 10",
            ),
            CheckConstraint(
                check=Q(rage__gte=1, rage__lte=10),
                name="characters_werewolf_rage_range",
                violation_error_message="Rage must be between 1 and 10",
            ),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()
        errors = {}
        if self.gnosis < 1:
            errors["gnosis"] = "All werewolves must have at least 1 Gnosis."
        if self.rage < 1:
            errors["rage"] = "All werewolves must have at least 1 Rage."
        if errors:
            raise ValidationError(errors)

    def get_rank_name(self):
        return self.rank_names[self.rank]

    def has_breed(self):
        return self.breed != ""

    def set_breed(self, breed):
        for b in self.BREEDS:
            self.gift_permissions.remove(
                GiftPermission.objects.get_or_create(shifter="werewolf", condition=b)[0]
            )
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="werewolf", condition=breed)[0]
        )

        self.breed = breed
        if breed == "homid":
            self.set_gnosis(1)
        elif breed == "metis":
            self.set_gnosis(3)
        elif breed == "lupus":
            self.set_gnosis(5)
        self.save()
        return True

    def has_auspice(self):
        return self.auspice != ""

    def set_auspice(self, auspice, ragabash_renown=(1, 1, 1)):
        for a in self.AUSPICES:
            self.gift_permissions.remove(
                GiftPermission.objects.get_or_create(shifter="werewolf", condition=a)[0]
            )
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="werewolf", condition=auspice)[0]
        )

        self.auspice = auspice
        if auspice == "ragabash":
            self.set_glory(ragabash_renown[0])
            self.set_honor(ragabash_renown[1])
            self.set_wisdom(ragabash_renown[2])
            self.set_rage(1)
        elif auspice == "theurge":
            self.set_glory(0)
            self.set_honor(0)
            self.set_wisdom(3)
            self.set_rage(2)
        elif auspice == "philodox":
            self.set_glory(0)
            self.set_honor(3)
            self.set_wisdom(0)
            self.set_rage(3)
        elif auspice == "galliard":
            self.set_glory(2)
            self.set_honor(0)
            self.set_wisdom(1)
            self.set_rage(4)
        elif auspice == "ahroun":
            self.set_glory(2)
            self.set_honor(1)
            self.set_wisdom(0)
            self.set_rage(5)
        self.save()
        return True

    def has_tribe(self):
        return self.tribe is not None

    def set_tribe(self, tribe):
        for t in Tribe.objects.all():
            self.gift_permissions.remove(
                GiftPermission.objects.get_or_create(shifter="werewolf", condition=t.name)[0]
            )
        self.gift_permissions.add(
            GiftPermission.objects.get_or_create(shifter="werewolf", condition=tribe.name)[0]
        )

        if tribe.name == "Red Talons" and self.breed == "homid":
            return False
        # if tribe.name == "Black Furies" and self.sex == "Male":
        #     return False
        self.tribe = tribe
        self.willpower = tribe.willpower
        if self.tribe.name == "Silver Fangs" and self.pure_breed < 3:
            self.pure_breed = 3
        self.save()
        return True

    def has_camp(self):
        return self.camps.exists()

    def add_camp(self, camp):
        if camp is None:
            return False
        if GiftPermission.objects.filter(shifter="werewolf", condition=camp.name).count() == 1:
            self.gift_permissions.add(
                GiftPermission.objects.filter(shifter="werewolf", condition=camp.name)
            )
        self.camps.add(camp)
        self.save()
        return True

    def add_gift(self, gift):
        if gift in self.gifts.all():
            return False
        self.gifts.add(gift)
        self.save()
        return True

    def filter_gifts(self):
        return Gift.objects.filter(
            rank__lte=self.rank, allowed__in=self.gift_permissions.all()
        ).exclude(pk__in=self.gifts.all())

    def has_gifts(self):
        b = self.gifts.count() >= 3
        breed = GiftPermission.objects.get_or_create(shifter="werewolf", condition=self.breed)[0]
        auspice = GiftPermission.objects.get_or_create(shifter="werewolf", condition=self.auspice)[
            0
        ]
        if self.tribe is not None:
            tribe = GiftPermission.objects.get_or_create(
                shifter="werewolf", condition=self.tribe.name
            )[0]
        else:
            b = False

        b = b and self.gifts.filter(allowed=breed).exists()
        b = b and self.gifts.filter(allowed=auspice).exists()
        b = b and self.gifts.filter(allowed=tribe).exists()

        return b

    def add_rite(self, rite):
        self.rites_known.add(rite)
        self.save()
        return True

    def filter_rites(self):
        return Rite.objects.exclude(pk__in=self.rites_known.all())

    def has_rites(self):
        return self.rites == self.total_rites()

    def total_rites(self):
        return (
            sum(x.level for x in self.rites_known.all())
            + self.rites_known.filter(level=0).count() / 2
        )

    def set_glory(self, glory):
        self.glory = glory
        self.save()
        return True

    def set_honor(self, honor):
        self.honor = honor
        self.save()
        return True

    def set_wisdom(self, wisdom):
        self.wisdom = wisdom
        self.save()
        return True

    def has_renown(self):
        return (self.glory + self.honor + self.wisdom) == 3

    def update_renown(self):
        if self.temporary_glory >= 10:
            self.glory += 1
            self.temporary_glory -= 10
        if self.temporary_honor >= 10:
            self.honor += 1
            self.temporary_honor -= 10
        if self.temporary_wisdom >= 10:
            self.wisdom += 1
            self.temporary_wisdom -= 10

    def num_renown_incidents(self):
        return len(self.renown_incidents)

    def add_renown_incident(self, r, rite=None):
        if r.breed != "":
            if r.breed != self.breed:
                return False
        if r.rite is not None:
            if r.rite not in self.rites_known.all():
                return False
        if r.only_once and r.name in self.renown_incidents:
            return False
        if len(self.renown_incidents) != 0:
            if RenownIncident.objects.get(name=self.renown_incidents[-1]).posthumous:
                return False
        self.renown_incidents.append(r.name)
        self.temporary_glory += r.glory
        self.temporary_honor += r.honor
        self.temporary_wisdom += r.wisdom
        self.temporary_glory = max(0, self.temporary_glory)
        self.temporary_honor = max(0, self.temporary_honor)
        self.temporary_wisdom = max(0, self.temporary_wisdom)
        if rite is not None:
            self.rites_known.add(rite)
        return True

    def add_gnosis(self):
        return add_dot(self, "gnosis", 10)

    def set_gnosis(self, gnosis):
        self.gnosis = gnosis
        self.save()
        return True

    def add_rage(self):
        return add_dot(self, "rage", 10)

    def set_rage(self, rage):
        self.rage = rage
        self.save()
        return True

    def set_rank(self, rank):
        self.rank = rank
        self.save()
        return True

    def increase_rank(self):
        if self.rank < 5:
            requirements = self.requirements[self.auspice][self.rank + 1]
            if "total" in requirements.keys():
                allowed = self.glory + self.honor + self.wisdom >= requirements["total"]
            else:
                allowed = (
                    (self.glory >= requirements["glory"])
                    and (self.honor >= requirements["honor"])
                    and (self.wisdom >= requirements["wisdom"])
                )
            if allowed:
                self.set_rank(self.rank + 1)
                self.save()
                return True
        return False

    def has_werewolf_history(self):
        return (self.first_change != "") and (self.age_of_first_change != 0)

    def add_battle_scar(self, scar):
        if scar not in self.battle_scars.all():
            self.battle_scars.add(scar)
            self.temporary_glory += scar.glory
            self.update_renown()
            self.save()
            return True
        return False

    def add_fetish(self, fetish):
        if fetish in self.fetishes_owned.all():
            return False
        self.fetishes_owned.add(fetish)
        return True

    def filter_fetishes(self, min_rating=0, max_rating=5):
        return Fetish.objects.filter(rank__lte=max_rating, rank__gte=min_rating).exclude(
            pk__in=self.fetishes_owned.all()
        )

    def total_fetish_rating(self):
        return sum(x.rank for x in self.fetishes_owned.all())

    def xp_frequencies(self):
        """Return frequency distribution for XP spending (for random character generation)."""
        return {
            "attribute": 16,
            "ability": 20,
            "background": 13,
            "willpower": 1,
            "gift": 30,
            "rite": 5,
            "rage": 2,
            "gnosis": 3,
            "renown": 10,
        }

    def xp_cost(self, trait_type, trait_value=None):
        """Return XP cost for werewolf-specific traits."""
        from collections import defaultdict

        costs = defaultdict(
            lambda: super().xp_cost(trait_type, trait_value) if trait_value is not None else 10000,
            {
                "gift": 3,
                "rite": 1,
                "rage": 1,
                "gnosis": 2,
                "glory": 1,
                "honor": 1,
                "wisdom": 1,
            },
        )

        if trait_type in ["gift", "rite", "rage", "gnosis", "glory", "honor", "wisdom"]:
            if trait_value is not None:
                return costs[trait_type] * trait_value
            return costs[trait_type]

        return costs[trait_type]

    def spend_xp(self, trait):
        """Spend XP on a trait."""
        output = super().spend_xp(trait)
        if output in [True, False]:
            return output

        # Handle gifts
        if trait == "gift":
            # This would require a gift object to be passed,
            # so we'll just return trait for now
            return trait

        # Handle rites
        if trait == "rite":
            # This would require a rite object to be passed,
            # so we'll just return trait for now
            return trait

        # Handle rage
        if trait == "rage":
            cost = self.xp_cost("rage", self.rage + 1)
            if cost <= self.xp:
                if self.add_rage():
                    self.xp -= cost
                    self.add_to_spend(trait, self.rage, cost)
                    return True
                return False
            return False

        # Handle gnosis
        if trait == "gnosis":
            cost = self.xp_cost("gnosis", self.gnosis + 1)
            if cost <= self.xp:
                if self.add_gnosis():
                    self.xp -= cost
                    self.add_to_spend(trait, self.gnosis, cost)
                    return True
                return False
            return False

        # Handle renown (glory, honor, wisdom)
        if trait in ["glory", "honor", "wisdom"]:
            cost = self.xp_cost(trait, getattr(self, trait) + 1)
            if cost <= self.xp:
                current = getattr(self, trait)
                setattr(self, trait, current + 1)
                self.xp -= cost
                self.add_to_spend(trait, getattr(self, trait), cost)
                self.save()
                return True
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
            "gift": 25,
            "rite": 3,
            "rage": 5,
            "gnosis": 8,
            "renown": 5,
        }

    def freebie_costs(self):
        """Return a dictionary of freebie costs for werewolf traits."""
        costs = super().freebie_costs()
        costs.update(
            {
                "gift": 5,
                "rite": 1,
                "rage": 1,
                "gnosis": 2,
                "glory": 1,
                "honor": 1,
                "wisdom": 1,
            }
        )
        return costs

    def freebie_cost(self, trait_type):
        """Return freebie cost for werewolf-specific traits."""
        werewolf_costs = {
            "gift": 5,
            "rite": 1,
            "rage": 1,
            "gnosis": 2,
            "glory": 1,
            "honor": 1,
            "wisdom": 1,
        }
        if trait_type in werewolf_costs.keys():
            return werewolf_costs[trait_type]
        return super().freebie_cost(trait_type)

    def spend_freebies(self, trait):
        """Spend freebie points on a trait."""
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output

        # Handle gifts (would need Gift object)
        if trait == "gift":
            return trait

        # Handle rites (would need Rite object)
        if trait == "rite":
            return trait

        # Handle rage
        if trait == "rage":
            cost = self.freebie_cost("rage")
            if cost <= self.freebies:
                if self.add_rage():
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle gnosis
        if trait == "gnosis":
            cost = self.freebie_cost("gnosis")
            if cost <= self.freebies:
                if self.add_gnosis():
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle renown (glory, honor, wisdom)
        if trait in ["glory", "honor", "wisdom"]:
            cost = self.freebie_cost(trait)
            if cost <= self.freebies:
                current = getattr(self, trait)
                setattr(self, trait, current + 1)
                self.freebies -= cost
                self.save()
                return True
            return False

        return trait
