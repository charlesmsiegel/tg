from characters.models.changeling.ctdhuman import CtDHuman
from django.db import models
from django.urls import reverse


class AutumnPerson(CtDHuman):
    """
    Autumn People - Mortals who embody and spread Banality.
    These are the enemies of the Dreaming, those who suppress wonder,
    imagination, and magic. They are often authority figures, bureaucrats,
    or anyone who crushes dreams and enforces cold reality.
    """

    type = "autumn_person"

    # Autumn People archetypes (their role in suppressing the Dreaming)
    ARCHETYPES = [
        ("authority", "Authority Figure"),  # Police, judges, enforcers of order
        ("bureaucrat", "Bureaucrat"),  # Paper-pushers, rule-followers
        ("cynic", "Cynic"),  # Those who mock and destroy belief
        ("fundamentalist", "Fundamentalist"),  # Rigid believers in one truth
        ("corporate", "Corporate Climber"),  # Money over magic
        ("scientist", "Rigid Scientist"),  # Only cold facts matter
        ("debunker", "Debunker"),  # Actively destroys wonder
        ("other", "Other"),
    ]

    archetype = models.CharField(
        default="",
        max_length=30,
        choices=ARCHETYPES,
        help_text="How this person suppresses the Dreaming",
    )

    # Banality level - Autumn People have HIGH Banality
    banality_rating = models.IntegerField(
        default=8, help_text="Banality level (typically 7-10 for Autumn People)"
    )

    # Awareness of fae - most don't know, some hunt consciously
    AWARENESS_LEVELS = [
        ("unaware", "Unaware"),  # Suppresses dreams unknowingly
        ("suspicious", "Suspicious"),  # Senses something "off"
        ("aware", "Aware"),  # Knows fae exist
        ("hunter", "Active Hunter"),  # Actively hunts changelings
    ]

    awareness = models.CharField(
        default="unaware",
        max_length=20,
        choices=AWARENESS_LEVELS,
        help_text="How aware they are of the fae world",
    )

    # Organization affiliation (if any)
    organization = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="Organization they belong to (govt agency, corp, etc.)",
    )

    # What drives them to suppress wonder
    motivation = models.TextField(
        default="",
        blank=True,
        help_text="Why they suppress imagination and the Dreaming",
    )

    # Their sphere of influence
    sphere_of_influence = models.TextField(
        default="",
        blank=True,
        help_text="Where they hold power (jurisdiction, company, institution)",
    )

    # Special abilities against fae
    anti_fae_abilities = models.JSONField(
        default=list,
        blank=True,
        help_text="Special abilities for hunting or suppressing fae",
    )

    # Dauntain - the most dangerous Autumn People who were once fae
    is_dauntain = models.BooleanField(
        default=False,
        help_text="True if this is a Dauntain (ex-changeling consumed by Banality)",
    )

    former_kith = models.CharField(
        max_length=50,
        default="",
        blank=True,
        help_text="If Dauntain, what kith they once were",
    )

    class Meta:
        verbose_name = "Autumn Person"
        verbose_name_plural = "Autumn People"

    def get_absolute_url(self):
        return reverse("characters:changeling:autumn_person", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse(
            "characters:changeling:update:autumn_person", kwargs={"pk": self.pk}
        )

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:autumn_person")

    def has_archetype(self):
        return self.archetype != ""

    def set_archetype(self, archetype):
        """Set the Autumn Person's archetype"""
        self.archetype = archetype
        return True

    def set_awareness(self, awareness):
        """Set how aware they are of the fae"""
        self.awareness = awareness
        return True

    def set_organization(self, org):
        """Set their organizational affiliation"""
        self.organization = org
        return True

    def has_organization(self):
        return self.organization != ""

    def set_motivation(self, motivation):
        """Set why they suppress the Dreaming"""
        self.motivation = motivation
        return True

    def has_motivation(self):
        return self.motivation != ""

    def set_sphere_of_influence(self, sphere):
        """Set their area of control"""
        self.sphere_of_influence = sphere
        return True

    def has_sphere_of_influence(self):
        return self.sphere_of_influence != ""

    def make_dauntain(self, former_kith=""):
        """Convert this character to a Dauntain"""
        self.is_dauntain = True
        self.former_kith = former_kith
        self.banality_rating = 10  # Dauntain have maximum Banality
        return True

    def add_anti_fae_ability(self, ability):
        """Add a special ability against fae"""
        if ability not in self.anti_fae_abilities:
            self.anti_fae_abilities.append(ability)
        return True
