from datetime import date, timedelta

from characters.models.core.ability_block import Ability, AbilityBlock
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute, AttributeBlock
from characters.models.core.background_block import BackgroundBlock
from characters.models.core.character import Character
from characters.models.core.derangement import Derangement
from characters.models.core.health_block import HealthBlock
from characters.models.core.human_url_block import HumanUrlBlock
from characters.models.core.merit_flaw_block import MeritFlawBlock
from characters.models.core.specialty import Specialty
from core.models import Language
from core.utils import add_dot
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, F, Q


class Human(
    HumanUrlBlock,
    AbilityBlock,
    MeritFlawBlock,
    HealthBlock,
    BackgroundBlock,
    AttributeBlock,
    Character,
):
    type = "human"

    gameline = "wod"

    allowed_backgrounds = ["contacts", "mentor"]
    talents = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
    ]
    skills = ["crafts", "drive", "etiquette", "firearms", "melee", "stealth"]
    knowledges = ["academics", "computer", "investigation", "medicine", "science"]
    primary_abilities = [
        "alertness",
        "athletics",
        "brawl",
        "empathy",
        "expression",
        "intimidation",
        "streetwise",
        "subterfuge",
        "crafts",
        "drive",
        "etiquette",
        "firearms",
        "melee",
        "stealth",
        "academics",
        "computer",
        "investigation",
        "medicine",
        "science",
    ]

    nature = models.ForeignKey(
        Archetype,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="nature_of",
    )
    demeanor = models.ForeignKey(
        Archetype,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="demeanor_of",
    )

    specialties = models.ManyToManyField(Specialty, blank=True)

    languages = models.ManyToManyField(Language, blank=True)

    willpower = models.IntegerField(
        default=3, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    temporary_willpower = models.IntegerField(
        default=3, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    derangements = models.ManyToManyField("Derangement", blank=True)

    age = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(500)]
    )
    apparent_age = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    date_of_birth = models.DateField(blank=True, null=True)

    history = models.TextField(default="", blank=True, null=True)
    goals = models.TextField(default="", blank=True, null=True)

    freebies = models.IntegerField(default=15)
    # DEPRECATED: Use FreebieSpendingRecord model instead (see JSONFIELD_MIGRATION_GUIDE.md)
    spent_freebies = models.JSONField(default=list)
    background_points = 5

    class Meta:
        verbose_name = "Human"
        verbose_name_plural = "Humans"
        ordering = ["name"]
        constraints = [
            # Willpower must be between 1 and 10
            CheckConstraint(
                check=Q(willpower__gte=1, willpower__lte=10),
                name="characters_human_willpower_range",
                violation_error_message="Willpower must be between 1 and 10",
            ),
            # Temporary willpower must be between 0 and 10
            CheckConstraint(
                check=Q(temporary_willpower__gte=0, temporary_willpower__lte=10),
                name="characters_human_temp_willpower_range",
                violation_error_message="Temporary willpower must be between 0 and 10",
            ),
            # Temporary willpower cannot exceed permanent willpower
            CheckConstraint(
                check=Q(temporary_willpower__lte=F("willpower")),
                name="characters_human_temp_not_exceeds_max",
                violation_error_message="Temporary willpower cannot exceed permanent willpower",
            ),
            # Age must be reasonable if provided
            CheckConstraint(
                check=Q(age__isnull=True) | Q(age__gte=0, age__lte=500),
                name="characters_human_reasonable_age",
                violation_error_message="Age must be between 0 and 500",
            ),
            # Apparent age must be reasonable if provided
            CheckConstraint(
                check=Q(apparent_age__isnull=True)
                | Q(apparent_age__gte=0, apparent_age__lte=200),
                name="characters_human_reasonable_apparent_age",
                violation_error_message="Apparent age must be between 0 and 200",
            ),
        ]

    def total_freebies(self):
        return self.freebies + sum([x["cost"] for x in self.spent_freebies])

    # New model-based freebie spending methods (replaces JSONField usage)

    def create_freebie_spending_record(self, trait_name, trait_type, trait_value, cost):
        """Create a freebie spending record using the new model-based system.

        This replaces the JSONField-based spent_freebies system with proper database relations.

        Args:
            trait_name: Display name of the trait (e.g., 'Alertness', 'Strength')
            trait_type: Category of trait (e.g., 'attribute', 'ability', 'background')
            trait_value: Value gained
            cost: Freebie point cost

        Returns:
            FreebieSpendingRecord instance
        """
        from game.models import FreebieSpendingRecord

        return FreebieSpendingRecord.objects.create(
            character=self,
            trait_name=trait_name,
            trait_type=trait_type,
            trait_value=trait_value,
            cost=cost,
        )

    def get_freebie_spending_history(self):
        """Get all freebie spending records for this character.

        Returns:
            QuerySet of FreebieSpendingRecord instances ordered by creation date
        """
        return self.freebie_spendings.all()

    def total_freebies_from_model(self):
        """Calculate total freebies spent using the new model-based system.

        Returns:
            int: Total freebie points spent
        """
        from django.db.models import Sum

        spent = self.freebie_spendings.aggregate(total=Sum("cost"))["total"] or 0
        return self.freebies + spent

    def is_group_member(self):
        from characters.models.core.group import Group

        return Group.objects.filter(members=self).exists()

    def get_group(self):
        from characters.models.core.group import Group

        return Group.objects.filter(members=self).first()

    def get_heading(self):
        return f"{self.gameline}_heading"

    def add_willpower(self):
        add_dot(self, "willpower", 10)
        return add_dot(self, "temporary_willpower", 10)

    def has_finishing_touches(self):
        return (
            self.age is not None
            and self.date_of_birth is not None
            and self.description is not None
            and self.apparent_age is not None
        )

    def has_history(self):
        return self.history != "" and self.goals != ""

    def has_archetypes(self):
        return self.nature is not None and self.demeanor is not None

    def set_archetypes(self, nature, demeanor):
        self.nature = nature
        self.demeanor = demeanor
        return True

    def add_derangement(self, derangement):
        if derangement in self.derangements.all():
            return False
        self.derangements.add(derangement)
        return True

    def get_specialty(self, stat):
        spec = self.specialties.filter(stat=stat).first()
        if spec is None:
            return None
        return spec.name

    def filter_specialties(self, stat=None):
        if stat is None:
            return Specialty.objects.all().exclude(pk__in=self.specialties.all())
        return Specialty.objects.filter(stat=stat).exclude(
            pk__in=self.specialties.all()
        )

    def add_specialty(self, specialty):
        if getattr(self, specialty.stat) < 4 and specialty.stat not in [
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
        ]:
            return False
        if specialty in self.specialties.all():
            return False
        self.specialties.add(specialty)
        return True

    def has_specialties(self):
        # Collect all stats that require specialties
        high_attributes = list(self.filter_attributes(minimum=4))
        high_abilities = list(self.filter_abilities(minimum=4))

        specialty_required_abilities = [
            x
            for x in self.filter_abilities(minimum=1)
            if x
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
        ]

        # Combine all stats that require specialties
        required_stats = high_attributes + high_abilities + specialty_required_abilities

        if not required_stats:
            return True

        # Get all stat IDs that require specialties
        stat_ids = [stat.id for stat in required_stats]

        # Single query to get all specialty stat IDs
        specialty_stat_ids = set(
            self.specialties.filter(stat__id__in=stat_ids).values_list(
                "stat_id", flat=True
            )
        )

        # Check if all required stats have specialties
        return len(specialty_stat_ids) == len(stat_ids)

    def freebie_costs(self):
        return {
            "attribute": 5,
            "ability": 2,
            "background": 1,
            "new background": 1,
            "existing background": 1,
            "willpower": 1,
            "meritflaw": "rating",
        }

    def freebie_cost(self, trait_type):
        costs = self.freebie_costs()
        if trait_type not in costs.keys():
            return 10000
        return costs[trait_type]

    def freebie_spend_record(self, trait, trait_type, value, cost=None):
        if cost is None:
            cost = self.freebie_cost(trait_type)
        return {
            "trait": trait,
            "value": value,
            "cost": cost,
        }

    def xp_cost(self, trait_type, trait_value):
        costs = {
            "new_ability": 3,
            "attribute": 4,
            "ability": 2,
            "background": 3,
            "new background": 5,
            "willpower": 1,
            "meritflaw": 3,
        }
        if trait_type == "ability" and trait_value == 0:
            return costs["new_ability"]
        return costs[trait_type] * trait_value

    def willpower_freebies(self, form):
        trait = "Willpower"
        value = self.willpower + 1
        cost = 1
        self.add_willpower()
        self.freebies -= cost
        return trait, value, cost

    def needed_specialties(self):
        stats = list(Attribute.objects.all()) + list(
            Ability.objects.filter(
                property_name__in=self.talents + self.skills + self.knowledges
            )
        )

        stats4 = [x for x in stats if getattr(self, x.property_name, 0) >= 4]
        stats1 = [
            x
            for x in stats
            if getattr(self, x.property_name, 0) >= 1
            and x.property_name
            in [
                "arts",
                "athletics",
                "crafts",
                "firearms",
                "larceny",
                "melee",
                "academics",
                "esoterica",
                "lore",
                "politics",
                "science",
            ]
        ]

        stats = stats1 + stats4

        existing_specialties = [x.stat for x in self.specialties.all()]
        stats = [x.property_name for x in stats]
        return [x for x in stats if x not in existing_specialties]

    def spend_xp(self, trait):
        """Spend XP on common human traits (attributes, abilities, backgrounds, willpower).

        This is the base implementation that handles traits common to all character types.
        Subclasses should call super().spend_xp(trait) first, and if it returns a string
        (the trait name), then handle their own specific traits.

        Returns:
            True if spending was successful
            False if spending failed (insufficient XP, at maximum, etc.)
            trait (string) if this method doesn't handle this trait (pass to subclass)
        """
        # Check if trait is an attribute
        if hasattr(Attribute.objects, "filter"):
            try:
                attribute = Attribute.objects.filter(property_name=trait).first()
                if attribute and hasattr(self, trait):
                    current_value = getattr(self, trait)
                    cost = self.xp_cost("attribute", current_value + 1)

                    if cost <= self.xp:
                        if self.add_attribute(trait):
                            self.xp -= cost
                            self.add_to_spend(trait, getattr(self, trait), cost)
                            return True
                        return False
                    return False
            except:
                pass

        # Check if trait is an ability
        if hasattr(Ability.objects, "filter"):
            try:
                ability = Ability.objects.filter(property_name=trait).first()
                if ability and hasattr(self, trait):
                    current_value = getattr(self, trait)

                    if current_value == 0:
                        cost = self.xp_cost("new_ability", 0)
                    else:
                        cost = self.xp_cost("ability", current_value + 1)

                    if cost <= self.xp:
                        if self.add_ability(trait):
                            self.xp -= cost
                            self.add_to_spend(trait, getattr(self, trait), cost)
                            return True
                        return False
                    return False
            except:
                pass

        # Check if trait is a background
        if trait in self.allowed_backgrounds:
            current_value = getattr(self, trait)

            if current_value == 0:
                cost = self.xp_cost("new background", 0)
            else:
                cost = self.xp_cost("background", current_value + 1)

            if cost <= self.xp:
                if self.add_background(trait):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
                return False
            return False

        # Handle willpower
        if trait == "willpower":
            cost = self.xp_cost("willpower", self.willpower + 1)
            if cost <= self.xp:
                if self.add_willpower():
                    self.xp -= cost
                    self.add_to_spend(trait, self.willpower, cost)
                    return True
                return False
            return False

        # Return trait name to indicate this method doesn't handle it
        return trait

    def spend_freebies(self, trait):
        """Spend freebie points on common human traits.

        This is the base implementation that handles traits common to all character types.
        Subclasses should call super().spend_freebies(trait) first, and if it returns a string
        (the trait name), then handle their own specific traits.

        Returns:
            True if spending was successful
            False if spending failed (insufficient freebies, at maximum, etc.)
            trait (string) if this method doesn't handle this trait (pass to subclass)
        """
        # Check if trait is an attribute
        if hasattr(Attribute.objects, "filter"):
            try:
                attribute = Attribute.objects.filter(property_name=trait).first()
                if attribute and hasattr(self, trait):
                    cost = self.freebie_cost("attribute")
                    if cost <= self.freebies:
                        if self.add_attribute(trait):
                            self.freebies -= cost
                            return True
                        return False
                    return False
            except:
                pass

        # Check if trait is an ability
        if hasattr(Ability.objects, "filter"):
            try:
                ability = Ability.objects.filter(property_name=trait).first()
                if ability and hasattr(self, trait):
                    cost = self.freebie_cost("ability")
                    if cost <= self.freebies:
                        if self.add_ability(trait):
                            self.freebies -= cost
                            return True
                        return False
                    return False
            except:
                pass

        # Check if trait is a background
        if trait in self.allowed_backgrounds:
            cost = self.freebie_cost("background")
            if cost <= self.freebies:
                if self.add_background(trait):
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle willpower
        if trait == "willpower":
            cost = self.freebie_cost("willpower")
            if cost <= self.freebies:
                if self.add_willpower():
                    self.freebies -= cost
                    return True
                return False
            return False

        # Return trait name to indicate this method doesn't handle it
        return trait
