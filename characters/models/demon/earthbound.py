from characters.models.demon.dtf_human import DtFHuman
from characters.models.demon.house import DemonHouse
from characters.models.demon.lore_block import LoreBlock
from django.db import models
from django.urls import reverse


class Earthbound(LoreBlock, DtFHuman):
    """
    Earthbound Demon - ancient demons trapped in reliquaries.

    Earthbound have fundamentally different mechanics from regular fallen demons.
    They exist in reliquaries (objects or locations) and have vast power but are
    immobile without mortal hosts.
    """

    type = "earthbound"

    freebie_step = 7

    # Earthbound-specific backgrounds
    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "influence",
        "resources",
        # Earthbound-specific backgrounds
        "codex",  # Knowledge of True Names
        "cult",  # Size of worship cult
        "hoard",  # Maximum Faith capacity
        "mastery",  # Extra Faith for enhancing evocations
        "thralls",  # Powerful servants (replaces followers)
        "worship",  # Faith gained from rituals
    ]

    # House (original angelic house)
    house = models.ForeignKey(
        DemonHouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="earthbound",
    )

    # URGES - replace/augment Physical, Social, Mental attributes when manifested
    # These distribute dots to host Attributes when possessing or manifesting
    urge_flesh = models.IntegerField(
        default=1,
        help_text="Physical urges - distribute among Strength, Dexterity, Stamina (1-5)",
    )
    urge_thought = models.IntegerField(
        default=1,
        help_text="Mental urges - distribute among Perception, Intelligence, Wits (1-5)",
    )
    urge_emotion = models.IntegerField(
        default=1,
        help_text="Social urges - distribute among Charisma, Manipulation, Appearance (1-5)",
    )

    # FAITH AND TORMENT
    faith = models.IntegerField(default=3, help_text="Permanent Faith rating (1-10)")
    temporary_faith = models.IntegerField(
        default=10,
        help_text="Temporary Faith pool (max determined by Hoard background)",
    )
    max_faith = models.IntegerField(
        default=10, help_text="Maximum Faith pool from Hoard (10-35 for Earthbound)"
    )

    torment = models.IntegerField(
        default=6, help_text="Permanent Torment rating (becomes 10 at Final Damnation)"
    )
    temporary_torment = models.IntegerField(default=0)

    # VIRTUES (Earthbound still have these)
    conviction = models.IntegerField(default=1)
    courage = models.IntegerField(default=1)
    conscience = models.IntegerField(default=1)

    # RELIQUARY INFORMATION
    RELIQUARY_TYPES = [
        ("perfect", "Perfect Reliquary"),
        ("improvised", "Improvised Reliquary"),
        ("location", "Location"),
    ]

    reliquary_type = models.CharField(
        max_length=20,
        choices=RELIQUARY_TYPES,
        default="perfect",
        help_text="Type of reliquary the Earthbound inhabits",
    )

    reliquary_description = models.TextField(
        blank=True, help_text="Description of the reliquary's appearance and nature"
    )

    # For perfect reliquaries
    reliquary_materials = models.TextField(
        blank=True,
        help_text="Materials and affinity (e.g., 'rubies and volcanic stone for fire affinity')",
    )

    # Health levels (for tracking reliquary damage)
    reliquary_max_health = models.IntegerField(
        default=10,
        help_text="Maximum health levels (= permanent Faith for perfect/improvised, (Faith+Willpower)x2 for locations)",
    )

    reliquary_current_health = models.IntegerField(
        default=10, help_text="Current health levels of reliquary"
    )

    reliquary_soak = models.IntegerField(
        default=0,
        help_text="Soak rating (= permanent Willpower for perfect/location, temp Willpower for improvised)",
    )

    # APOCALYPTIC FORM - Earthbound design custom visages
    # They get 16 form points to spend on 8 features
    visage_features = models.JSONField(
        default=list,
        blank=True,
        help_text="List of 8 visage features with point costs, e.g., [{'name': 'Claws/Teeth', 'cost': 2}, ...]",
    )

    visage_grotesqueries = models.JSONField(
        default=list,
        blank=True,
        help_text="List of 8 grotesqueries (cosmetic deformities), e.g., ['Decaying', 'Multiple Eyes', ...]",
    )

    total_form_points = models.IntegerField(
        default=16, help_text="Total form points available (default 16)"
    )

    # MANIFESTATION
    can_manifest = models.BooleanField(
        default=True,
        help_text="Can manifest apocalyptic form (perfect reliquary & location: 2 Faith/turn, improvised: 1 Faith/turn)",
    )

    manifestation_range = models.IntegerField(
        default=0,
        help_text="Range in yards for location reliquaries (= permanent Faith)",
    )

    # CULT INFORMATION
    cult_size = models.CharField(
        max_length=500,
        blank=True,
        help_text="Description of cult size and organization",
    )

    worship_ritual_frequency = models.CharField(
        max_length=200,
        blank=True,
        help_text="How often worship rituals are performed (e.g., 'once per week')",
    )

    # THRALLS (powerful servants)
    # Note: Earthbound use Thralls background, not Followers
    # Thralls can be empowered mortals or enslaved demons

    # TRUE NAMES KNOWN (Codex background)
    known_celestial_names = models.JSONField(
        default=list, blank=True, help_text="List of Celestial Names known"
    )

    known_true_names = models.JSONField(
        default=list, blank=True, help_text="List of True Names known"
    )

    # LORE MASTERY
    # Earthbound can spend extra Faith to enhance evocations (Mastery background)
    mastery_rating = models.IntegerField(
        default=0,
        help_text="How much extra Faith can be spent on enhancing evocations (0-5)",
    )

    # EARTHBOUND-SPECIFIC ABILITIES
    indoctrination = models.IntegerField(default=0)  # Brainwashing skill
    recall = models.IntegerField(default=0)  # Memory of mortal history (Earthbound only)
    tactics = models.IntegerField(default=0)  # Military strategy
    torture = models.IntegerField(default=0)  # Interrogation through pain

    # SPECIAL LORES
    # Earthbound have access to Lore of Chaos, Contamination, and Violation

    # Learned rituals (including Earthbound rituals)
    rituals = models.ManyToManyField("Ritual", blank=True, related_name="earthbound_who_know")

    # CELESTIAL IDENTITY
    celestial_name = models.CharField(
        max_length=200, default="", help_text="The demon's Celestial Name"
    )

    # HISTORY
    date_summoned = models.CharField(
        max_length=200,
        blank=True,
        help_text="When the Earthbound was first summoned from Hell",
    )

    time_in_stasis = models.TextField(
        blank=True,
        help_text="Periods when the Earthbound was in dreaming stasis due to low Faith",
    )

    class Meta:
        verbose_name = "Earthbound"
        verbose_name_plural = "Earthbound"

    def get_absolute_url(self):
        return reverse("characters:demon:earthbound", kwargs={"pk": self.pk})

    def get_heading(self):
        return "dtf_heading"

    def is_final_damnation(self):
        """Check if Earthbound has reached Final Damnation (Torment 10)"""
        return self.torment >= 10

    def get_faith_per_manifestation_turn(self):
        """Get Faith cost per turn to manifest apocalyptic form"""
        if self.reliquary_type == "improvised":
            return 1
        else:  # perfect or location
            return 2

    def get_max_faith_from_hoard(self):
        """Calculate max Faith based on Hoard background"""
        # This would reference the Hoard background rating
        # 0=10, 1=15, 2=20, 3=25, 4=30, 5=35
        # For now, return the stored value
        return self.max_faith

    def calculate_reliquary_health(self):
        """Calculate reliquary health levels based on type"""
        if self.reliquary_type == "location":
            return (self.faith + self.willpower) * 2
        else:  # perfect or improvised
            return self.faith

    def can_regenerate_reliquary(self):
        """Check if can spend Faith to heal reliquary"""
        return (
            self.temporary_faith > 0 and self.reliquary_current_health < self.reliquary_max_health
        )

    def get_total_visage_feature_cost(self):
        """Calculate total form points spent on visage features"""
        total = 0
        for feature in self.visage_features:
            if isinstance(feature, dict) and "cost" in feature:
                total += feature.get("cost", 0)
        return total

    def has_valid_visage(self):
        """Check if visage has 8 features totaling 16 points or less"""
        return (
            len(self.visage_features) == 8
            and len(self.visage_grotesqueries) == 8
            and self.get_total_visage_feature_cost() <= self.total_form_points
        )
