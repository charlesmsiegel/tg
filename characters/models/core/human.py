from datetime import date, timedelta

from characters.managers import BackgroundManager, MeritFlawManager
from characters.models.core.ability_block import Ability, AbilityBlock
from characters.models.core.archetype import Archetype
from characters.models.core.attribute_block import Attribute, AttributeBlock
from characters.models.core.character import Character
from characters.models.core.derangement import Derangement
from characters.models.core.health_block import HealthBlock
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
from core.models import Language
from core.utils import add_dot, get_short_gameline_name
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import CheckConstraint, F, Q
from django.urls import reverse


class Human(
    AbilityBlock,
    HealthBlock,
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

    # Merit/Flaw management (formerly from MeritFlawBlock)
    merits_and_flaws = models.ManyToManyField(
        MeritFlaw,
        blank=True,
        through="MeritFlawRating",
        related_name="flawed",
    )

    # Background management (formerly from BackgroundBlock)
    # Note: backgrounds are managed dynamically through BackgroundRating model
    # No direct fields needed here - see background_manager property

    willpower = models.IntegerField(
        default=3, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    temporary_willpower = models.IntegerField(
        default=3, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    derangements = models.ManyToManyField("Derangement", blank=True)

    age = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5000)]
    )
    apparent_age = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    date_of_birth = models.DateField(blank=True, null=True)

    history = models.TextField(default="", blank=True, null=True)
    goals = models.TextField(default="", blank=True, null=True)

    freebies = models.IntegerField(default=15)
    # DEPRECATED: Use FreebieSpendingRecord model instead (see JSONFIELD_MIGRATION_GUIDE.md)
    spent_freebies = models.JSONField(default=list, blank=True)  # list is callable - safe
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
                check=Q(age__isnull=True) | Q(age__gte=0, age__lte=5000),
                name="characters_human_reasonable_age",
                violation_error_message="Age must be between 0 and 5000",
            ),
            # Apparent age must be reasonable if provided
            CheckConstraint(
                check=Q(apparent_age__isnull=True) | Q(apparent_age__gte=0, apparent_age__lte=200),
                name="characters_human_reasonable_apparent_age",
                violation_error_message="Apparent age must be between 0 and 200",
            ),
        ]

    # ========================================================================
    # Manager Properties (Composition over Inheritance)
    # ========================================================================

    @property
    def merit_flaw_manager(self):
        """
        Lazy-loaded manager for merit/flaw operations.

        This replaces direct inheritance from MeritFlawBlock with composition.

        Returns:
            MeritFlawManager: Manager instance for this character
        """
        if not hasattr(self, "_merit_flaw_manager"):
            self._merit_flaw_manager = MeritFlawManager(self)
        return self._merit_flaw_manager

    @property
    def background_manager(self):
        """
        Lazy-loaded manager for background operations.

        This replaces direct inheritance from BackgroundBlock with composition.

        Returns:
            BackgroundManager: Manager instance for this character
        """
        if not hasattr(self, "_background_manager"):
            self._background_manager = BackgroundManager(self)
        return self._background_manager

    # ========================================================================
    # URL Methods (formerly from HumanUrlBlock)
    # ========================================================================

    @staticmethod
    def get_gameline_for_url(gameline):
        """
        Get formatted gameline prefix for URL generation.

        Args:
            gameline: Gameline code (e.g., 'vtm', 'wta')

        Returns:
            str: Formatted gameline prefix with colon, or empty string
        """
        g = get_short_gameline_name(gameline)
        if g:
            g += ":"
        return g

    def get_full_update_url(self):
        """
        Get URL for full character update view.

        Returns:
            str: URL path for full update view
        """
        return reverse(
            f"characters:{self.get_gameline_for_url(self.gameline)}update:{self.type}_full",
            kwargs={"pk": self.pk},
        )

    def get_update_url(self):
        """
        Get URL for character update view.

        Returns:
            str: URL path for update view
        """
        return reverse(
            f"characters:{self.get_gameline_for_url(self.gameline)}update:{self.type}",
            kwargs={"pk": self.pk},
        )

    @classmethod
    def get_full_creation_url(cls):
        """
        Get URL for full character creation view.

        Returns:
            str: URL path for full creation view
        """
        return reverse(f"characters:{cls.get_gameline_for_url(cls.gameline)}create:{cls.type}_full")

    @classmethod
    def get_creation_url(cls):
        """
        Get URL for character creation view.

        Returns:
            str: URL path for creation view
        """
        return reverse(f"characters:{cls.get_gameline_for_url(cls.gameline)}create:{cls.type}")

    # ========================================================================
    # Freebie and XP Methods
    # ========================================================================

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

    @transaction.atomic
    def award_backstory_freebies(self, amount):
        """Award backstory freebies to this character.

        This method awards bonus freebie points (typically for backstory) and
        marks the character's freebies as approved. This operation is atomic.

        Args:
            amount: Number of freebie points to award (0-15 typically)

        Raises:
            ValidationError: If freebies have already been approved or amount is invalid
        """
        from django.core.exceptions import ValidationError

        # Lock the character to prevent concurrent awards
        character = Human.objects.select_for_update().get(pk=self.pk)

        if character.freebies_approved:
            raise ValidationError(
                "Freebies have already been approved for this character",
                code="freebies_already_approved",
            )

        if amount < 0 or amount > 15:
            raise ValidationError(
                "Backstory freebies must be between 0 and 15",
                code="invalid_amount",
            )

        # Award the freebies
        character.freebies += amount
        character.freebies_approved = True
        character.save(update_fields=["freebies", "freebies_approved"])

        return character

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

    def set_willpower(self, value):
        if self.temporary_willpower >= value:
            self.temporary_willpower = value
        self.willpower = value
        self.save()

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
        return Specialty.objects.filter(stat=stat).exclude(pk__in=self.specialties.all())

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
            self.specialties.filter(stat__id__in=stat_ids).values_list("stat_id", flat=True)
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
            Ability.objects.filter(property_name__in=self.talents + self.skills + self.knowledges)
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

    # ========================================================================
    # Backward Compatibility Delegates
    # These methods delegate to the manager classes for backward compatibility.
    # New code should use character.merit_flaw_manager or character.background_manager
    # ========================================================================

    # MeritFlawBlock backward compatibility
    def num_languages(self):
        """DEPRECATED: Use character.merit_flaw_manager.num_languages()"""
        return self.merit_flaw_manager.num_languages()

    def get_mf_and_rating_list(self):
        """DEPRECATED: Use character.merit_flaw_manager.get_mf_and_rating_list()"""
        return self.merit_flaw_manager.get_mf_and_rating_list()

    def add_mf(self, mf, rating):
        """DEPRECATED: Use character.merit_flaw_manager.add_mf()"""
        return self.merit_flaw_manager.add_mf(mf, rating)

    def filter_mfs(self):
        """DEPRECATED: Use character.merit_flaw_manager.filter_mfs()"""
        return self.merit_flaw_manager.filter_mfs()

    def mf_rating(self, mf):
        """DEPRECATED: Use character.merit_flaw_manager.mf_rating()"""
        return self.merit_flaw_manager.mf_rating(mf)

    def has_max_flaws(self):
        """DEPRECATED: Use character.merit_flaw_manager.has_max_flaws()"""
        return self.merit_flaw_manager.has_max_flaws()

    def total_flaws(self):
        """DEPRECATED: Use character.merit_flaw_manager.total_flaws()"""
        return self.merit_flaw_manager.total_flaws()

    def total_merits(self):
        """DEPRECATED: Use character.merit_flaw_manager.total_merits()"""
        return self.merit_flaw_manager.total_merits()

    def meritflaw_freebies(self, form):
        """DEPRECATED: Use character.merit_flaw_manager.meritflaw_freebies()"""
        return self.merit_flaw_manager.meritflaw_freebies(form)

    # BackgroundBlock backward compatibility
    def total_background_rating(self, bg_name):
        """DEPRECATED: Use character.background_manager.total_background_rating()"""
        return self.background_manager.total_background_rating(bg_name)

    def get_backgrounds(self):
        """DEPRECATED: Use character.background_manager.get_backgrounds()"""
        return self.background_manager.get_backgrounds()

    def add_background(self, background, maximum=5):
        """DEPRECATED: Use character.background_manager.add_background()"""
        return self.background_manager.add_background(background, maximum)

    def total_backgrounds(self):
        """DEPRECATED: Use character.background_manager.total_backgrounds()"""
        return self.background_manager.total_backgrounds()

    def filter_backgrounds(self, minimum=0, maximum=5):
        """DEPRECATED: Use character.background_manager.filter_backgrounds()"""
        return self.background_manager.filter_backgrounds(minimum, maximum)

    def has_backgrounds(self):
        """DEPRECATED: Use character.background_manager.has_backgrounds()"""
        return self.background_manager.has_backgrounds()

    def new_background_freebies(self, form):
        """DEPRECATED: Use character.background_manager.new_background_freebies()"""
        return self.background_manager.new_background_freebies(form)

    def existing_background_freebies(self, form):
        """DEPRECATED: Use character.background_manager.existing_background_freebies()"""
        return self.background_manager.existing_background_freebies(form)

    # Dynamic background properties (for backward compatibility with old property system)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create dynamic properties for all allowed backgrounds
        for bg in self.allowed_backgrounds:
            if not hasattr(self.__class__, bg):
                setattr(
                    self.__class__,
                    bg,
                    property(
                        lambda self, bg_name=bg: self.background_manager.get_background_property(
                            bg_name
                        ),
                        lambda self, value, bg_name=bg: self.background_manager.set_background_property(
                            bg_name, value
                        ),
                    ),
                )

    # ========================================================================
    # XP and Freebie Spending Methods
    # ========================================================================

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
