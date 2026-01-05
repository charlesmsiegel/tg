from core.models import Model
from django.db import models
from django.urls import reverse


class ApocalypticFormTrait(Model):
    """Represents a specific ability/trait available in apocalyptic form."""

    type = "apocalyptic_form_trait"
    gameline = "dtf"

    # Description of what this trait does
    description = models.TextField(default="", blank=True)

    # Point cost for this trait (1-5, typically 1-3)
    cost = models.IntegerField(default=1)

    # Associated house (optional - some traits might be universal)
    house = models.ForeignKey(
        "DemonHouse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apocalyptic_traits",
    )

    # Some traits can ONLY be used as high torment traits
    high_torment_only = models.BooleanField(
        default=False,
        help_text="If True, this trait can only be placed in the high torment column",
    )

    class Meta:
        verbose_name = "Apocalyptic Form Trait"
        verbose_name_plural = "Apocalyptic Form Traits"
        ordering = ["cost", "name"]

    def __str__(self):
        suffix = " (High Torment Only)" if self.high_torment_only else ""
        return f"{self.name} ({self.cost} pts){suffix}"

    def get_absolute_url(self):
        return reverse("characters:demon:apocalyptic_trait", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:apocalyptic_trait", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:apocalyptic_trait")


class ApocalypticForm(Model):
    """
    Represents a complete apocalyptic form configuration.

    Must have exactly 4 low torment traits and 4 high torment traits,
    with total point cost not exceeding 16.
    """

    type = "apocalyptic_form"
    gameline = "dtf"

    # The 4 low torment traits (cannot include high_torment_only traits)
    low_torment_traits = models.ManyToManyField(
        ApocalypticFormTrait,
        blank=True,
        related_name="forms_as_low_torment",
    )

    # The 4 high torment traits (can include any trait)
    high_torment_traits = models.ManyToManyField(
        ApocalypticFormTrait,
        blank=True,
        related_name="forms_as_high_torment",
    )

    class Meta:
        verbose_name = "Apocalyptic Form"
        verbose_name_plural = "Apocalyptic Forms"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:demon:apocalyptic_form", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:apocalyptic_form", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:apocalyptic_form")

    def low_torment_count(self):
        """Count of low torment traits."""
        return self.low_torment_traits.count()

    def high_torment_count(self):
        """Count of high torment traits."""
        return self.high_torment_traits.count()

    def total_traits(self):
        """Total number of traits."""
        return self.low_torment_count() + self.high_torment_count()

    def low_torment_points(self):
        """Total points spent on low torment traits."""
        return sum(trait.cost for trait in self.low_torment_traits.all())

    def high_torment_points(self):
        """Total points spent on high torment traits."""
        return sum(trait.cost for trait in self.high_torment_traits.all())

    def total_points(self):
        """Total points spent on all traits."""
        return self.low_torment_points() + self.high_torment_points()

    def points_remaining(self):
        """Points remaining (out of 16)."""
        return 16 - self.total_points()

    def is_valid(self):
        """Check if form has exactly 4 low + 4 high traits and total points <= 16."""
        return (
            self.low_torment_count() == 4
            and self.high_torment_count() == 4
            and self.total_points() <= 16
        )

    def is_complete(self):
        """Check if form has exactly 8 traits (4 low + 4 high)."""
        return self.low_torment_count() == 4 and self.high_torment_count() == 4

    def can_add_low_torment_trait(self, trait):
        """Check if a trait can be added to low torment list."""
        # high_torment_only traits cannot be in low torment list
        if trait.high_torment_only:
            return False
        if self.low_torment_count() >= 4:
            return False
        if trait in self.low_torment_traits.all():
            return False
        # Can't have same trait in both lists
        if trait in self.high_torment_traits.all():
            return False
        if self.total_points() + trait.cost > 16:
            return False
        return True

    def can_add_high_torment_trait(self, trait):
        """Check if a trait can be added to high torment list."""
        if self.high_torment_count() >= 4:
            return False
        if trait in self.high_torment_traits.all():
            return False
        # Can't have same trait in both lists
        if trait in self.low_torment_traits.all():
            return False
        if self.total_points() + trait.cost > 16:
            return False
        return True

    def add_low_torment_trait(self, trait):
        """Add a trait to the low torment list if valid."""
        if self.can_add_low_torment_trait(trait):
            self.low_torment_traits.add(trait)
            return True
        return False

    def add_high_torment_trait(self, trait):
        """Add a trait to the high torment list if valid."""
        if self.can_add_high_torment_trait(trait):
            self.high_torment_traits.add(trait)
            return True
        return False

    def remove_low_torment_trait(self, trait):
        """Remove a trait from the low torment list."""
        if trait in self.low_torment_traits.all():
            self.low_torment_traits.remove(trait)
            return True
        return False

    def remove_high_torment_trait(self, trait):
        """Remove a trait from the high torment list."""
        if trait in self.high_torment_traits.all():
            self.high_torment_traits.remove(trait)
            return True
        return False

    def copy_from(self, other_form):
        """Copy traits from another ApocalypticForm."""
        self.low_torment_traits.set(other_form.low_torment_traits.all())
        self.high_torment_traits.set(other_form.high_torment_traits.all())
