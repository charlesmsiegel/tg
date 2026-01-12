from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.urls import reverse

from characters.costs import get_freebie_cost, get_xp_cost
from core.constants import CharacterStatus
from core.linked_stat import LinkedStat

from .clan import VampireClan
from .path import Path
from .sect import VampireSect
from .title import VampireTitle
from .vtmhuman import VtMHuman


class Vampire(VtMHuman):
    """
    Represents a Vampire character (embraced undead).
    """

    type = "vampire"
    freebie_step = 7

    # Minimum starting values for morality traits (V20 rules)
    MIN_STARTING_PATH_RATING = 4
    MIN_STARTING_HUMANITY = 4

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "alternate_identity",
        "black_hand_membership",
        "domain",
        "fame",
        "generation",
        "herd",
        "influence",
        "resources",
        "retainers",
        "rituals",
        "status_background",
    ]

    # Clan and Sect
    clan = models.ForeignKey(
        VampireClan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vampires",
    )

    sect = models.ForeignKey(
        VampireSect,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vampires",
    )

    # Sire
    sire = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="childer",
    )

    # Generation (3rd - 15th typically)
    generation_rating = models.IntegerField(default=13)

    # Blood Pool
    blood_pool = models.IntegerField(default=10)
    max_blood_pool = models.IntegerField(default=10)
    blood_per_turn = models.IntegerField(default=1)
    blood = LinkedStat("max_blood_pool", "blood_pool", cap_temporary=False)

    # Physical Disciplines
    celerity = models.IntegerField(default=0)
    fortitude = models.IntegerField(default=0)
    potence = models.IntegerField(default=0)

    # Mental Disciplines
    auspex = models.IntegerField(default=0)
    dominate = models.IntegerField(default=0)
    dementation = models.IntegerField(default=0)

    # Social Disciplines
    presence = models.IntegerField(default=0)

    # Animalistic Disciplines
    animalism = models.IntegerField(default=0)
    protean = models.IntegerField(default=0)

    # Stealth Disciplines
    obfuscate = models.IntegerField(default=0)

    # Unique Clan Disciplines
    chimerstry = models.IntegerField(default=0)
    necromancy = models.IntegerField(default=0)
    obtenebration = models.IntegerField(default=0)
    quietus = models.IntegerField(default=0)
    serpentis = models.IntegerField(default=0)
    thaumaturgy = models.IntegerField(default=0)
    vicissitude = models.IntegerField(default=0)

    # Bloodline Unique Disciplines
    daimoinon = models.IntegerField(default=0)
    melpominee = models.IntegerField(default=0)
    mytherceria = models.IntegerField(default=0)
    obeah = models.IntegerField(default=0)
    temporis = models.IntegerField(default=0)
    thanatosis = models.IntegerField(default=0)
    valeren = models.IntegerField(default=0)
    visceratika = models.IntegerField(default=0)

    # Virtue selection - determines which virtues are active
    has_conviction = models.BooleanField(
        default=False, help_text="If True, uses Conviction; if False, uses Conscience"
    )
    has_instinct = models.BooleanField(
        default=False, help_text="If True, uses Instinct; if False, uses Self-Control"
    )

    # Virtues (Camarilla) - Can be 0 when using alternative virtues (Conviction/Instinct)
    conscience = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    self_control = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    courage = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    # Virtues (Sabbat alternative) - Can be 0 when using standard virtues (Conscience/Self-Control)
    conviction = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    instinct = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    # Morality
    humanity = models.IntegerField(default=7)
    path = models.ForeignKey(
        Path,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="followers",
    )
    path_rating = models.IntegerField(default=0)

    # Titles
    titles = models.ManyToManyField(VampireTitle, blank=True, related_name="holders")

    class Meta:
        verbose_name = "Vampire"
        verbose_name_plural = "Vampires"
        constraints = [
            # Virtue pairs can be 0 when using alternative (Conviction vs Conscience, Instinct vs Self-Control)
            CheckConstraint(
                check=Q(conscience__gte=0, conscience__lte=5),
                name="characters_vampire_conscience_range",
                violation_error_message="Conscience must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(self_control__gte=0, self_control__lte=5),
                name="characters_vampire_self_control_range",
                violation_error_message="Self-Control must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(courage__gte=1, courage__lte=5),
                name="characters_vampire_courage_range",
                violation_error_message="Courage must be between 1 and 5",
            ),
            CheckConstraint(
                check=Q(conviction__gte=0, conviction__lte=5),
                name="characters_vampire_conviction_range",
                violation_error_message="Conviction must be between 0 and 5",
            ),
            CheckConstraint(
                check=Q(instinct__gte=0, instinct__lte=5),
                name="characters_vampire_instinct_range",
                violation_error_message="Instinct must be between 0 and 5",
            ),
            # Humanity/Path can be 0-10 (degeneration allows going below 4)
            CheckConstraint(
                check=Q(humanity__gte=0, humanity__lte=10),
                name="characters_vampire_humanity_range",
                violation_error_message="Humanity must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(path_rating__gte=0, path_rating__lte=10),
                name="characters_vampire_path_rating_range",
                violation_error_message="Path rating must be between 0 and 10",
            ),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()
        errors = {}

        # Validate virtue minimums based on which virtues the character uses
        # Courage is always required
        if self.courage < 1:
            errors["courage"] = "Courage must be at least 1."

        # Validate first virtue pair (Conviction vs Conscience)
        if self.has_conviction:
            if self.conviction < 1:
                errors["conviction"] = "Conviction must be at least 1."
        else:
            if self.conscience < 1:
                errors["conscience"] = "Conscience must be at least 1."

        # Validate second virtue pair (Instinct vs Self-Control)
        if self.has_instinct:
            if self.instinct < 1:
                errors["instinct"] = "Instinct must be at least 1."
        else:
            if self.self_control < 1:
                errors["self_control"] = "Self Control must be at least 1."

        # Validate Humanity/Path during character creation (UNAPPROVED or SUBMITTED)
        # Once approved, characters can have lower humanity due to degeneration
        if self.status in [CharacterStatus.UNAPPROVED, CharacterStatus.SUBMITTED]:
            # Validate humanity (if on humanity, not a path)
            if not self.path:
                if self.humanity < self.MIN_STARTING_HUMANITY:
                    errors["humanity"] = (
                        f"Starting Humanity must be at least {self.MIN_STARTING_HUMANITY}."
                    )
                elif self.humanity > 10:
                    errors["humanity"] = "Starting Humanity cannot exceed 10."
            # Validate path_rating (if on a path)
            else:
                if self.path_rating < self.MIN_STARTING_PATH_RATING:
                    errors["path_rating"] = (
                        f"Starting Path rating must be at least "
                        f"{self.MIN_STARTING_PATH_RATING}."
                    )
                elif self.path_rating > 10:
                    errors["path_rating"] = "Starting Path rating cannot exceed 10."

        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse("characters:vampire:vampire", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:vampire", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:vampire")

    # Generation table for trait maximums (V20 rules)
    # Format: generation: (max_trait, max_blood_pool, blood_per_turn)
    GENERATION_TABLE = {
        3: (10, 50, 10),
        4: (9, 50, 10),
        5: (8, 40, 8),
        6: (7, 30, 6),
        7: (6, 20, 4),
        8: (5, 15, 3),
        9: (5, 14, 2),
        10: (5, 13, 1),
        11: (5, 12, 1),
        12: (5, 11, 1),
        13: (5, 10, 1),
        14: (5, 10, 1),
        15: (5, 10, 1),
    }

    def update_generation_values(self):
        """Update max blood pool and blood per turn based on generation."""
        if self.generation_rating in self.GENERATION_TABLE:
            _, self.max_blood_pool, self.blood_per_turn = self.GENERATION_TABLE[
                self.generation_rating
            ]

    def get_trait_max(self):
        """Return the maximum value for traits based on generation.

        Per V20 rules:
        - Generation 3: Max 10
        - Generation 4: Max 9
        - Generation 5: Max 8
        - Generation 6: Max 7
        - Generation 7: Max 6
        - Generation 8+: Max 5
        """
        if self.generation_rating in self.GENERATION_TABLE:
            return self.GENERATION_TABLE[self.generation_rating][0]
        return 5  # Default for unknown generations

    def get_attribute_max(self):
        """Return the maximum value for attributes based on generation."""
        return self.get_trait_max()

    def get_discipline_max(self):
        """Return the maximum value for disciplines based on generation."""
        return self.get_trait_max()

    def get_attribute_min(self, attribute_name=None):
        """Return the minimum value for an attribute.

        Nosferatu have Appearance 0 as their clan weakness.
        """
        if attribute_name == "appearance" and self.clan and self.clan.name == "Nosferatu":
            return 0
        return 1

    def spend_blood(self, amount):
        """Spend blood points from the blood pool.

        Args:
            amount: Number of blood points to spend

        Returns:
            True if successful, False if insufficient blood

        Raises:
            ValueError: If amount exceeds per-turn spending limit
        """
        if amount > self.blood_per_turn:
            raise ValueError(
                f"Cannot spend {amount} blood points per turn. "
                f"Maximum per turn is {self.blood_per_turn} (Generation {self.generation_rating})."
            )
        if amount > self.blood_pool:
            return False
        self.blood_pool -= amount
        self.save()
        return True

    def restore_blood(self, amount):
        """Restore blood points to the blood pool.

        Args:
            amount: Number of blood points to restore

        Returns:
            int: Actual amount restored (may be less if at max)
        """
        old_pool = self.blood_pool
        self.blood_pool = min(self.blood_pool + amount, self.max_blood_pool)
        self.save()
        return self.blood_pool - old_pool

    def validate_blood_pool(self):
        """Validate blood pool is within valid range.

        Returns:
            dict: Validation errors, empty if valid
        """
        errors = {}
        if self.blood_pool < 0:
            errors["blood_pool"] = "Blood pool cannot be negative"
        if self.blood_pool > self.max_blood_pool:
            errors["blood_pool"] = (
                f"Blood pool ({self.blood_pool}) exceeds maximum "
                f"({self.max_blood_pool}) for Generation {self.generation_rating}"
            )
        return errors

    def save(self, *args, **kwargs):
        """Override save to update generation-dependent values and handle path changes."""
        self.update_generation_values()

        # If a path is set, ensure virtues match the path's requirements
        if self.path:
            self.path.update_character_virtues(self)

        super().save(*args, **kwargs)

    def get_disciplines(self):
        """Return a dictionary of all disciplines with their ratings."""
        disciplines = {
            "Celerity": self.celerity,
            "Fortitude": self.fortitude,
            "Potence": self.potence,
            "Auspex": self.auspex,
            "Dominate": self.dominate,
            "Dementation": self.dementation,
            "Presence": self.presence,
            "Animalism": self.animalism,
            "Protean": self.protean,
            "Obfuscate": self.obfuscate,
            "Chimerstry": self.chimerstry,
            "Necromancy": self.necromancy,
            "Obtenebration": self.obtenebration,
            "Quietus": self.quietus,
            "Serpentis": self.serpentis,
            "Thaumaturgy": self.thaumaturgy,
            "Vicissitude": self.vicissitude,
            "Daimoinon": self.daimoinon,
            "Melpominee": self.melpominee,
            "Mytherceria": self.mytherceria,
            "Obeah": self.obeah,
            "Temporis": self.temporis,
            "Thanatosis": self.thanatosis,
            "Valeren": self.valeren,
            "Visceratika": self.visceratika,
        }
        return {k: v for k, v in disciplines.items() if v > 0}

    def get_clan_disciplines(self):
        """Return list of in-clan disciplines."""
        if self.clan:
            return list(self.clan.disciplines.all())
        return []

    def is_clan_discipline(self, discipline):
        """Check if a discipline is in-clan."""
        if not self.clan:
            return False
        clan_disciplines = [d.property_name for d in self.clan.disciplines.all()]
        if isinstance(discipline, str):
            return discipline in clan_disciplines
        return discipline.property_name in clan_disciplines

    def discipline_freebies(self, form):
        """Spend freebies on disciplines."""
        discipline = form.cleaned_data["example"]
        is_clan = self.is_clan_discipline(discipline)
        cost = 7 if is_clan else 10

        # Get current rating and increment
        current_rating = getattr(self, discipline.property_name, 0)
        setattr(self, discipline.property_name, current_rating + 1)
        self.freebies -= cost

        trait = discipline.name
        value = current_rating + 1
        return trait, value, cost

    def virtue_freebies(self, form):
        """Spend freebies on virtues."""
        # Virtues cost 2 freebies per dot
        cost = 2
        virtue_name = form.cleaned_data["example"].lower()

        # Get current rating and increment
        current_rating = getattr(self, virtue_name, 1)
        setattr(self, virtue_name, current_rating + 1)
        self.freebies -= cost

        trait = virtue_name.title()
        value = current_rating + 1
        return trait, value, cost

    def humanity_freebies(self, form):
        """Spend freebies on Humanity."""
        cost = 1
        self.humanity += 1
        self.freebies -= cost
        return "Humanity", self.humanity, cost

    def path_rating_freebies(self, form):
        """Spend freebies on Path rating."""
        cost = 1
        self.path_rating += 1
        self.freebies -= cost
        return "Path Rating", self.path_rating, cost

    @property
    def active_virtue_1(self):
        """Return the rating of the first active virtue (Conviction or Conscience)."""
        return self.conviction if self.has_conviction else self.conscience

    @property
    def active_virtue_1_name(self):
        """Return the name of the first active virtue."""
        return "Conviction" if self.has_conviction else "Conscience"

    @property
    def active_virtue_2(self):
        """Return the rating of the second active virtue (Instinct or Self-Control)."""
        return self.instinct if self.has_instinct else self.self_control

    @property
    def active_virtue_2_name(self):
        """Return the name of the second active virtue."""
        return "Instinct" if self.has_instinct else "Self-Control"

    def get_active_virtues(self):
        """Return a dict of active virtues with their ratings."""
        return {
            self.active_virtue_1_name: self.active_virtue_1,
            self.active_virtue_2_name: self.active_virtue_2,
            "Courage": self.courage,
        }

    def set_virtue_by_name(self, virtue_name, value):
        """Set a virtue value by name (case-insensitive)."""
        virtue_name = virtue_name.lower()
        if virtue_name in [
            "conscience",
            "conviction",
            "self_control",
            "instinct",
            "courage",
        ]:
            setattr(self, virtue_name, value)
        else:
            raise ValueError(f"Unknown virtue: {virtue_name}")

    def xp_frequencies(self):
        """Return frequency distribution for XP spending (for random character generation)."""
        return {
            "attribute": 16,
            "ability": 20,
            "background": 13,
            "willpower": 1,
            "discipline": 35,
            "virtue": 3,
            "humanity": 1,
            "path_rating": 1,
        }

    def spend_xp(self, trait):
        """Spend XP on a trait."""
        output = super().spend_xp(trait)
        if output in [True, False]:
            return output

        # Check if trait is a discipline
        discipline_fields = [
            "celerity",
            "fortitude",
            "potence",
            "auspex",
            "dominate",
            "dementation",
            "presence",
            "animalism",
            "protean",
            "obfuscate",
            "chimerstry",
            "necromancy",
            "obtenebration",
            "quietus",
            "serpentis",
            "thaumaturgy",
            "vicissitude",
            "daimoinon",
            "melpominee",
            "mytherceria",
            "obeah",
            "temporis",
            "thanatosis",
            "valeren",
            "visceratika",
        ]

        if trait in discipline_fields:
            current_value = getattr(self, trait)

            # Determine if it's clan or out-of-clan
            from characters.models.vampire.discipline import Discipline

            try:
                discipline_obj = Discipline.objects.get(property_name=trait)
                is_clan = self.is_clan_discipline(discipline_obj)

                if current_value == 0:
                    cost = get_xp_cost("new_discipline")
                elif is_clan:
                    cost = get_xp_cost("clan_discipline") * (current_value + 1)
                else:
                    cost = get_xp_cost("out_of_clan_discipline") * (current_value + 1)

                if cost <= self.xp:
                    from core.utils import add_dot

                    # Use generation-based maximum for disciplines
                    if add_dot(self, trait, self.get_discipline_max()):
                        self.xp -= cost
                        self.add_to_spend(trait, getattr(self, trait), cost)
                        return True
                    return False
                return False
            except Discipline.DoesNotExist:
                return False

        # Handle virtues
        if trait in ["conscience", "conviction", "self_control", "instinct", "courage"]:
            current_value = getattr(self, trait)
            cost = get_xp_cost("virtue") * (current_value + 1)
            if cost <= self.xp:
                from core.utils import add_dot

                if add_dot(self, trait, 5):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
                return False
            return False

        # Handle humanity
        if trait == "humanity":
            cost = get_xp_cost("humanity") * (self.humanity + 1)
            if cost <= self.xp:
                from core.utils import add_dot

                if add_dot(self, "humanity", 10):
                    self.xp -= cost
                    self.add_to_spend(trait, self.humanity, cost)
                    return True
                return False
            return False

        # Handle path rating
        if trait == "path_rating":
            cost = get_xp_cost("path_rating") * (self.path_rating + 1)
            if cost <= self.xp:
                from core.utils import add_dot

                if add_dot(self, "path_rating", 10):
                    self.xp -= cost
                    self.add_to_spend(trait, self.path_rating, cost)
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
            "discipline": 30,
            "virtue": 8,
            "humanity": 4,
            "path_rating": 4,
        }

    def spend_freebies(self, trait):
        """Spend freebie points on a trait."""
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output

        # Check if trait is a discipline
        discipline_fields = [
            "celerity",
            "fortitude",
            "potence",
            "auspex",
            "dominate",
            "dementation",
            "presence",
            "animalism",
            "protean",
            "obfuscate",
            "chimerstry",
            "necromancy",
            "obtenebration",
            "quietus",
            "serpentis",
            "thaumaturgy",
            "vicissitude",
            "daimoinon",
            "melpominee",
            "mytherceria",
            "obeah",
            "temporis",
            "thanatosis",
            "valeren",
            "visceratika",
        ]

        if trait in discipline_fields:
            from characters.models.vampire.discipline import Discipline

            try:
                discipline_obj = Discipline.objects.get(property_name=trait)
                is_clan = self.is_clan_discipline(discipline_obj)
                cost = 7 if is_clan else 10

                if cost <= self.freebies:
                    from core.utils import add_dot

                    # Use generation-based maximum for disciplines
                    if add_dot(self, trait, self.get_discipline_max()):
                        self.freebies -= cost
                        return True
                    return False
                return False
            except Discipline.DoesNotExist:
                return False

        # Handle virtues
        if trait in ["conscience", "conviction", "self_control", "instinct", "courage"]:
            cost = get_freebie_cost("virtue")
            if cost <= self.freebies:
                from core.utils import add_dot

                if add_dot(self, trait, 5):
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle humanity
        if trait == "humanity":
            cost = get_freebie_cost("humanity")
            if cost <= self.freebies:
                from core.utils import add_dot

                if add_dot(self, "humanity", 10):
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle path rating
        if trait == "path_rating":
            cost = get_freebie_cost("path_rating")
            if cost <= self.freebies:
                from core.utils import add_dot

                if add_dot(self, "path_rating", 10):
                    self.freebies -= cost
                    return True
                return False
            return False

        return trait
