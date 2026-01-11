from django.db import models
from django.urls import reverse

from locations.models.core.location import LocationModel
from locations.models.mage.reality_zone import RealityZone


class Sector(LocationModel):
    type = "sector"
    gameline = "mta"

    SECTOR_CLASS = [
        ("virgin", "Virgin Web"),
        ("grid", "Grid"),
        ("c_sector", "C-Sector (Constrained)"),
        ("corrupted", "Corrupted Web"),
        ("junklands", "Junklands"),
        ("haunts", "Haunts"),
        ("trash", "Trash"),
        ("streamland", "Streamland"),
        ("warzone", "Warzone"),
    ]

    ACCESS_LEVEL = [
        ("free", "Free Sector"),
        ("restricted", "Restricted Sector"),
    ]

    sector_class = models.CharField(max_length=15, choices=SECTOR_CLASS, default="grid")
    access_level = models.CharField(max_length=10, choices=ACCESS_LEVEL, default="free")

    # Power and Security
    power_rating = models.IntegerField(
        default=5,
        help_text="Forces/Prime Effects exceeding this generate Paradox (Warzones: 7, Corrupted: 5+)",
    )
    security_level = models.IntegerField(
        default=0, help_text="Difficulty to hack/breach (0=open, 10=maximum)"
    )

    # Access Control
    requires_password = models.BooleanField(default=False)
    password_hint = models.CharField(max_length=200, blank=True)
    approved_users = models.TextField(
        blank=True, help_text="List of approved user types/credentials (one per line)"
    )

    # Constraint Protocols
    constraints = models.TextField(
        blank=True,
        help_text="Custom physics/rules for this sector (genre enforcement, tech requirements, etc.)",
    )
    genre_theme = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., 'Film Noir Detective', 'Medieval Fantasy', 'Cyberpunk', etc.",
    )

    # Size and Structure
    size_rating = models.IntegerField(
        default=1,
        help_text="1=Room, 2=Building, 3=Block, 4=Neighborhood, 5=City, 6=Region",
    )

    # Administrator
    administrator = models.CharField(
        max_length=200,
        blank=True,
        help_text="Who controls this sector (Convention, Tradition, individual, etc.)",
    )

    # Reality Zone effects
    reality_zone = models.ForeignKey(RealityZone, blank=True, null=True, on_delete=models.SET_NULL)
    difficulty_modifier = models.IntegerField(
        default=0,
        help_text="Modifier to Arete rolls for compatible/incompatible paradigms",
    )

    # Special Properties
    has_lag = models.BooleanField(
        default=False, help_text="Sector showing signs of impending Whiteout"
    )
    paradox_risk_modifier = models.IntegerField(
        default=0, help_text="Additional Paradox points generated in this sector"
    )

    # Corrupted/Junklands specific
    is_reformattable = models.BooleanField(
        default=True,
        help_text="Can this sector be reformatted? (False for Corrupted Web)",
    )
    corruption_level = models.IntegerField(default=0, help_text="0=none, 10=completely corrupted")

    # Temporal effects
    time_dilation = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        help_text="Time flow ratio (1.0=normal, 2.0=twice as fast, 0.5=half speed)",
    )
    temporal_instability = models.BooleanField(
        default=False, help_text="Time flows unpredictably (Hung Sectors)"
    )

    # ARO Information
    aro_count = models.IntegerField(
        default=0, help_text="Number of Augmented Reality Objects in this sector"
    )
    aro_density = models.CharField(
        max_length=20,
        choices=[
            ("none", "None"),
            ("sparse", "Sparse"),
            ("moderate", "Moderate"),
            ("dense", "Dense"),
            ("overwhelming", "Overwhelming"),
        ],
        default="moderate",
    )

    # Streamland specific
    data_flow_rate = models.CharField(
        max_length=20,
        choices=[
            ("trickle", "Trickle"),
            ("steady", "Steady"),
            ("high", "High"),
            ("torrent", "Torrent"),
        ],
        blank=True,
    )

    # Population
    estimated_users = models.IntegerField(
        default=0, help_text="Approximate number of regular users/visitors"
    )

    # Connections
    connected_sectors = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="conduits_from",
        help_text="Sectors this one has conduits/hot links to",
    )

    # Notes
    hazards = models.TextField(
        blank=True,
        help_text="Environmental hazards, hostile entities, security measures, etc.",
    )
    notable_features = models.TextField(
        blank=True, help_text="Landmarks, AROs, unique properties, etc."
    )

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"

    def get_update_url(self):
        return reverse("locations:mage:update:sector", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("locations:mage:create:sector")

    def get_effective_difficulty(self, paradigm_match=True):
        """
        Calculate the effective difficulty for Arete/Enlightenment rolls in this sector.
        Based on Reality Zone and constraint protocol compatibility.
        """
        base_difficulty = 6  # Standard Mage difficulty

        if self.reality_zone:
            # Reality zones can modify difficulty
            base_difficulty += self.difficulty_modifier

        if not paradigm_match and self.constraints:
            # Incompatible paradigms face additional penalties
            base_difficulty += 1

        return max(3, min(10, base_difficulty))  # Cap between 3-10

    def generates_paradox_for_power(self, effect_power_level):
        """
        Check if an effect's power level exceeds the sector's rating,
        generating additional Paradox.
        """
        if effect_power_level > self.power_rating:
            return effect_power_level - self.power_rating
        return 0

    def is_accessible_to(self, user_credentials=None):
        """
        Check if a user can access this sector.
        """
        if self.access_level == "free":
            return True

        if self.access_level == "restricted":
            if not user_credentials:
                return False

            # Check if user credentials match approved users
            if self.approved_users:
                approved_list = [u.strip() for u in self.approved_users.split("\n") if u.strip()]
                return any(cred in user_credentials for cred in approved_list)

        return False

    def get_whiteout_risk(self, paradox_pool_size):
        """
        Determine Whiteout risk based on Paradox pool size.
        Per sourcebook: lag occurs with pool of 11+
        """
        if paradox_pool_size >= 11:
            return "critical"
        elif paradox_pool_size >= 6:
            return "high"
        elif paradox_pool_size >= 3:
            return "moderate"
        return "low"

    def calculate_base_paradox(self, is_vulgar=False, has_witnesses=False):
        """
        Calculate base Paradox for an effect in this sector.
        """
        paradox = 0

        if is_vulgar:
            if has_witnesses or self.access_level == "restricted":
                paradox += 1

        # Add sector-specific modifiers
        paradox += self.paradox_risk_modifier

        # Corrupted sectors generate Paradox for all effects
        if self.sector_class == "corrupted":
            paradox += 1

        return paradox

    def get_navigation_difficulty(self):
        """
        Get the difficulty for navigating TO this sector through conduits.
        """
        base_difficulty = 6

        # Restricted sectors are harder to find
        if self.access_level == "restricted":
            base_difficulty += 2

        # Security adds to difficulty
        if self.security_level > 0:
            base_difficulty += min(2, self.security_level // 3)

        # Corrupted sectors are unpredictable
        if self.sector_class in ["corrupted", "junklands"]:
            base_difficulty += 1

        return min(10, base_difficulty)

    def get_de_rez_type(self, violation_severity="minor"):
        """
        Determine what type of De-Rez occurs for protocol violations.
        """
        if self.sector_class == "corrupted":
            return "hard"  # Corrupted sectors always hard de-rez

        if self.access_level == "restricted" and violation_severity == "major":
            return "hard"

        if violation_severity in ["major", "critical"]:
            return "hard"

        return "soft"

    def time_in_sector(self, real_world_minutes):
        """
        Calculate how much time passes in this sector for a given real-world time.
        """
        return float(real_world_minutes) * float(self.time_dilation)

    def __str__(self):
        return f"{self.name} ({self.get_sector_class_display()})"
