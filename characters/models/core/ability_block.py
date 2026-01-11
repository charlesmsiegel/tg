from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q

from characters.models.core.statistic import Statistic
from core.constants import AbilityFields
from core.utils import add_dot


class Ability(Statistic):
    type = "ability"


class AbilityBlock(models.Model):
    # Use constants from core.constants.AbilityFields as single source of truth
    # This eliminates duplication and makes ability lists easier to maintain
    talents = AbilityFields.TALENTS
    skills = AbilityFields.SKILLS
    knowledges = AbilityFields.KNOWLEDGES
    primary_abilities = AbilityFields.PRIMARY_ABILITIES

    alertness = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    athletics = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    brawl = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    empathy = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    expression = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    intimidation = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    streetwise = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    subterfuge = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    crafts = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    drive = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    etiquette = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    firearms = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    melee = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    stealth = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    academics = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    computer = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    investigation = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    medicine = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    science = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        abstract = True
        constraints = [
            # All abilities must be between 0 and 10
            CheckConstraint(
                check=Q(alertness__gte=0, alertness__lte=10),
                name="%(app_label)s_%(class)s_alertness_range",
                violation_error_message="Alertness must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(athletics__gte=0, athletics__lte=10),
                name="%(app_label)s_%(class)s_athletics_range",
                violation_error_message="Athletics must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(brawl__gte=0, brawl__lte=10),
                name="%(app_label)s_%(class)s_brawl_range",
                violation_error_message="Brawl must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(empathy__gte=0, empathy__lte=10),
                name="%(app_label)s_%(class)s_empathy_range",
                violation_error_message="Empathy must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(expression__gte=0, expression__lte=10),
                name="%(app_label)s_%(class)s_expression_range",
                violation_error_message="Expression must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(intimidation__gte=0, intimidation__lte=10),
                name="%(app_label)s_%(class)s_intimidation_range",
                violation_error_message="Intimidation must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(streetwise__gte=0, streetwise__lte=10),
                name="%(app_label)s_%(class)s_streetwise_range",
                violation_error_message="Streetwise must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(subterfuge__gte=0, subterfuge__lte=10),
                name="%(app_label)s_%(class)s_subterfuge_range",
                violation_error_message="Subterfuge must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(crafts__gte=0, crafts__lte=10),
                name="%(app_label)s_%(class)s_crafts_range",
                violation_error_message="Crafts must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(drive__gte=0, drive__lte=10),
                name="%(app_label)s_%(class)s_drive_range",
                violation_error_message="Drive must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(etiquette__gte=0, etiquette__lte=10),
                name="%(app_label)s_%(class)s_etiquette_range",
                violation_error_message="Etiquette must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(firearms__gte=0, firearms__lte=10),
                name="%(app_label)s_%(class)s_firearms_range",
                violation_error_message="Firearms must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(melee__gte=0, melee__lte=10),
                name="%(app_label)s_%(class)s_melee_range",
                violation_error_message="Melee must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(stealth__gte=0, stealth__lte=10),
                name="%(app_label)s_%(class)s_stealth_range",
                violation_error_message="Stealth must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(academics__gte=0, academics__lte=10),
                name="%(app_label)s_%(class)s_academics_range",
                violation_error_message="Academics must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(computer__gte=0, computer__lte=10),
                name="%(app_label)s_%(class)s_computer_range",
                violation_error_message="Computer must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(investigation__gte=0, investigation__lte=10),
                name="%(app_label)s_%(class)s_investigation_range",
                violation_error_message="Investigation must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(medicine__gte=0, medicine__lte=10),
                name="%(app_label)s_%(class)s_medicine_range",
                violation_error_message="Medicine must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(science__gte=0, science__lte=10),
                name="%(app_label)s_%(class)s_science_range",
                violation_error_message="Science must be between 0 and 10",
            ),
        ]

    def add_ability(self, ability, maximum=4):
        return add_dot(self, ability, maximum)

    def get_abilities(self):
        tmp = {}
        tmp.update(self.get_talents())
        tmp.update(self.get_skills())
        tmp.update(self.get_knowledges())
        return tmp

    def filter_abilities(self, minimum=0, maximum=5):
        return {k: v for k, v in self.get_abilities().items() if minimum <= v <= maximum}

    def get_talents(self):
        return {k: getattr(self, k) for k in self.talents}

    def get_skills(self):
        return {k: getattr(self, k) for k in self.skills}

    def get_knowledges(self):
        return {k: getattr(self, k) for k in self.knowledges}

    def total_talents(self):
        return sum(self.get_talents().values())

    def total_skills(self):
        return sum(self.get_skills().values())

    def total_knowledges(self):
        return sum(self.get_knowledges().values())

    def total_abilities(self):
        return sum(self.get_abilities().values())

    def has_abilities(self, primary=13, secondary=9, tertiary=5):
        triple = [self.total_talents(), self.total_skills(), self.total_knowledges()]
        triple.sort()
        return triple == [tertiary, secondary, primary]

    def get_secondaries_for_display(self):
        secondary_talents = {
            k: v
            for k, v in self.get_talents().items()
            if k not in self.primary_abilities and v != 0
        }
        secondary_skills = {
            k: v for k, v in self.get_skills().items() if k not in self.primary_abilities and v != 0
        }
        secondary_knowledges = {
            k: v
            for k, v in self.get_knowledges().items()
            if k not in self.primary_abilities and v != 0
        }

        if "History Knowledge" in secondary_knowledges:
            secondary_knowledges["History"] = secondary_knowledges.pop("History Knowledge")

        secondary_talents = list(secondary_talents.items())
        secondary_skills = list(secondary_skills.items())
        secondary_knowledges = list(secondary_knowledges.items())

        secondary_talents = [(k.replace("_", " ").title(), v, k) for k, v in secondary_talents]
        secondary_skills = [(k.replace("_", " ").title(), v, k) for k, v in secondary_skills]
        secondary_knowledges = [
            (k.replace("_", " ").title(), v, k) for k, v in secondary_knowledges
        ]

        secondary_talents.sort(key=lambda x: x[0])
        secondary_skills.sort(key=lambda x: x[0])
        secondary_knowledges.sort(key=lambda x: x[0])

        num_sec_tal = len(secondary_talents)
        num_sec_ski = len(secondary_skills)
        num_sec_kno = len(secondary_knowledges)
        m = max(num_sec_tal, num_sec_ski, num_sec_kno)
        for _ in range(m - num_sec_tal):
            secondary_talents.append(("", 0, ""))
        for _ in range(m - num_sec_ski):
            secondary_skills.append(("", 0, ""))
        for _ in range(m - num_sec_kno):
            secondary_knowledges.append(("", 0, ""))
        return list(zip(secondary_talents, secondary_skills, secondary_knowledges, strict=False))

    def ability_freebies(self, form):
        cost = 2
        trait = form.cleaned_data["example"]
        value = getattr(self, trait.property_name) + 1
        self.add_ability(trait.property_name)
        self.freebies -= cost
        trait = trait.name
        return trait, value, cost
