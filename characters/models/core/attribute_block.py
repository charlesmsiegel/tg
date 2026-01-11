from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q

from characters.models.core.statistic import Statistic
from core.utils import add_dot


class Attribute(Statistic):
    type = "attribute"


class AttributeBlock(models.Model):
    strength = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    dexterity = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    stamina = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    perception = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    intelligence = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    wits = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    charisma = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    manipulation = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    appearance = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        abstract = True
        constraints = [
            # All attributes must be between 0 and 10
            CheckConstraint(
                check=Q(strength__gte=0, strength__lte=10),
                name="%(app_label)s_%(class)s_strength_range",
                violation_error_message="Strength must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(dexterity__gte=0, dexterity__lte=10),
                name="%(app_label)s_%(class)s_dexterity_range",
                violation_error_message="Dexterity must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(stamina__gte=0, stamina__lte=10),
                name="%(app_label)s_%(class)s_stamina_range",
                violation_error_message="Stamina must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(perception__gte=0, perception__lte=10),
                name="%(app_label)s_%(class)s_perception_range",
                violation_error_message="Perception must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(intelligence__gte=0, intelligence__lte=10),
                name="%(app_label)s_%(class)s_intelligence_range",
                violation_error_message="Intelligence must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(wits__gte=0, wits__lte=10),
                name="%(app_label)s_%(class)s_wits_range",
                violation_error_message="Wits must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(charisma__gte=0, charisma__lte=10),
                name="%(app_label)s_%(class)s_charisma_range",
                violation_error_message="Charisma must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(manipulation__gte=0, manipulation__lte=10),
                name="%(app_label)s_%(class)s_manipulation_range",
                violation_error_message="Manipulation must be between 0 and 10",
            ),
            CheckConstraint(
                check=Q(appearance__gte=0, appearance__lte=10),
                name="%(app_label)s_%(class)s_appearance_range",
                violation_error_message="Appearance must be between 0 and 10",
            ),
        ]

    def add_attribute(self, attribute, maximum=None):
        """Add a dot to an attribute, respecting the character's maximum.

        Args:
            attribute: The attribute property name to increase
            maximum: Override maximum (if None, uses get_attribute_max())
        """
        if maximum is None:
            maximum = self.get_attribute_max()
        return add_dot(self, attribute, maximum)

    def get_attribute_max(self):
        """Return the maximum value for attributes.

        Default is 5 for mortals. Subclasses should override this
        to implement supernatural exceptions (e.g., low-generation vampires).
        """
        return 5

    def get_attribute_min(self, attribute_name=None):
        """Return the minimum value for an attribute.

        Default is 1 for mortals. Subclasses should override this
        to implement supernatural exceptions (e.g., Nosferatu Appearance 0).

        Args:
            attribute_name: Optional attribute name for attribute-specific minimums
        """
        return 1

    def validate_attributes(self):
        """Validate that all attributes meet minimum requirements.

        Returns:
            dict: Validation errors keyed by attribute name, empty if valid
        """
        errors = {}
        attributes = self.get_attributes()
        for attr_name, value in attributes.items():
            minimum = self.get_attribute_min(attr_name)
            if value < minimum:
                errors[attr_name] = (
                    f"{attr_name.title()} must be at least {minimum} (currently {value})"
                )
        return errors

    def get_attributes(self):
        return {
            "strength": self.strength,
            "dexterity": self.dexterity,
            "stamina": self.stamina,
            "perception": self.perception,
            "intelligence": self.intelligence,
            "wits": self.wits,
            "charisma": self.charisma,
            "manipulation": self.manipulation,
            "appearance": self.appearance,
        }

    def get_physical_attributes(self, attribute_dict=None):
        if attribute_dict is None:
            attribute_dict = self.get_attributes()
        return {
            k: v for k, v in attribute_dict.items() if k in ["strength", "dexterity", "stamina"]
        }

    def get_social_attributes(self, attribute_dict=None):
        if attribute_dict is None:
            attribute_dict = self.get_attributes()
        return {
            k: v
            for k, v in attribute_dict.items()
            if k in ["charisma", "manipulation", "appearance"]
        }

    def get_mental_attributes(self, attribute_dict=None):
        if attribute_dict is None:
            attribute_dict = self.get_attributes()
        return {
            k: v for k, v in attribute_dict.items() if k in ["perception", "intelligence", "wits"]
        }

    def total_physical_attributes(self, attribute_dict=None):
        return sum(self.get_physical_attributes(attribute_dict=attribute_dict).values())

    def total_social_attributes(self, attribute_dict=None):
        return sum(self.get_social_attributes(attribute_dict=attribute_dict).values())

    def total_mental_attributes(self, attribute_dict=None):
        return sum(self.get_mental_attributes(attribute_dict=attribute_dict).values())

    def total_attributes(self):
        return sum(self.get_attributes().values())

    def has_attributes(self, primary=7, secondary=5, tertiary=3, max_value=5, attribute_dict=None):
        triple = [
            self.total_physical_attributes(attribute_dict=attribute_dict),
            self.total_mental_attributes(attribute_dict=attribute_dict),
            self.total_social_attributes(attribute_dict=attribute_dict),
        ]
        triple.sort()
        return triple == [3 + tertiary, 3 + secondary, 3 + primary]

    def filter_attributes(self, minimum=0, maximum=5):
        return {k: v for k, v in self.get_attributes().items() if minimum <= v <= maximum}

    def attribute_freebies(self, form):
        cost = 5
        trait = form.cleaned_data["example"]
        value = getattr(self, trait.property_name) + 1
        self.add_attribute(trait.property_name)
        self.freebies -= cost
        trait = trait.name
        return trait, value, cost
