from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from .mtr_human import MtRHuman


class Mummy(MtRHuman):
    """
    Amenti: Reborn mummies serving the cycle of Ma'at.
    Core supernatural character type for Mummy: the Resurrection.
    """

    type = "mummy"
    freebie_step = 7

    # ========================================
    # CORE MUMMY STATS
    # ========================================

    # Balance (like Humanity/Path Rating)
    balance = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Moral/ethical center (0-10). Loss leads to becoming Undying.",
    )

    # Sekhem (like Arete/Gnosis - primary power stat)
    sekhem = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Magical power rating (0-10). Determines Hekau cap and Ba pool.",
    )

    # Ba (current spiritual energy - like Quintessence/Blood Pool)
    ba = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Current spiritual energy pool",
    )

    # Ka (permanent spiritual energy - max Ba)
    ka_rating = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Permanent spiritual energy capacity (derived from Sekhem + backgrounds)",
    )

    # ========================================
    # VIRTUES (Mummy-specific)
    # ========================================

    conviction = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Strength of purpose and will",
    )

    restraint = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Self-control and temperance",
    )

    # ========================================
    # WEB (Soul Affiliation)
    # ========================================

    WEB_CHOICES = [
        ("isis", "Web of Isis (Preservers)"),
        ("osiris", "Web of Osiris (Judges)"),
        ("horus", "Web of Horus (Protectors)"),
        ("maat", "Web of Ma'at (Seers)"),
        ("thoth", "Web of Thoth (Scholars)"),
    ]

    web = models.CharField(
        max_length=10,
        choices=WEB_CHOICES,
        default="",
        blank=True,
        help_text="The Web/soul type this Amenti belongs to",
    )

    # ========================================
    # HEKAU (Egyptian Magic Paths)
    # ========================================
    # Each Hekau path is rated 0-5
    # Similar to Disciplines/Spheres pattern

    # Universal Hekau (available to all)
    alchemy = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Transform and transmute matter",
    )

    celestial = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Influence fate and fortune",
    )

    effigy = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Create servitors and vessels",
    )

    necromancy = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Command the dead and spirits",
    )

    nomenclature = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="True names and binding oaths",
    )

    # Web-Specific Hekau
    # Isis
    ushabti = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Animate and command servants (Isis)",
    )

    # Osiris
    judge = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Weigh souls and pronounce judgment (Osiris)",
    )

    # Horus
    phoenix = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Resilience and rebirth (Horus)",
    )

    # Ma'at
    vision = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Prophecy and far-sight (Ma'at)",
    )

    # Thoth
    divination = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Mystical knowledge and scrying (Thoth)",
    )

    # ========================================
    # ORGANIZATION & SOCIETY
    # ========================================

    # Dynasty affiliation
    dynasty = models.ForeignKey(
        "Dynasty",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The dynasty/lineage this mummy belongs to",
    )

    # Titles within Amenti society
    titles = models.ManyToManyField(
        "MummyTitle", blank=True, help_text="Titles and ranks held"
    )

    # ========================================
    # MEMORY & PAST LIVES
    # ========================================

    # Current incarnation number
    incarnation = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Which incarnation/rebirth is this (1st, 2nd, etc.)",
    )

    # Years since last death/rebirth
    years_since_rebirth = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="How long since this incarnation began",
    )

    # Original death (in ancient times)
    death_in_first_life = models.TextField(
        blank=True, help_text="How this person died in ancient Egypt"
    )

    # Memory of past lives
    past_lives_memory = models.TextField(
        blank=True, help_text="Key memories from previous incarnations"
    )

    # ========================================
    # RELATIONSHIPS
    # ========================================

    # The person who awakened/mentored this mummy
    mentor_mummy = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="students",
        help_text="The Amenti who awakened or trained this mummy",
    )

    # Ancient name (from first life)
    ancient_name = models.CharField(
        max_length=100, blank=True, help_text="Name from the First Life in ancient Egypt"
    )

    # ========================================
    # PHYSICAL MANIFESTATION
    # ========================================

    # Appearance of their mummified form
    MUMMIFIED_APPEARANCE_CHOICES = [
        ("preserved", "Well-Preserved (appears almost alive)"),
        ("desiccated", "Desiccated (clearly ancient and dried)"),
        ("skeletal", "Skeletal (only bones and wrappings)"),
        ("varies", "Varies (changes with circumstances)"),
    ]

    mummified_appearance = models.CharField(
        max_length=20,
        choices=MUMMIFIED_APPEARANCE_CHOICES,
        default="preserved",
        blank=True,
        help_text="How they appear when manifesting their true form",
    )

    # Can they still pass as mortal?
    can_pass_as_mortal = models.BooleanField(
        default=True, help_text="Can this mummy still appear fully human?"
    )

    # ========================================
    # HELPER METHODS
    # ========================================

    def get_hekau(self):
        """Return dict of all non-zero Hekau paths"""
        hekau_paths = {
            "Alchemy": self.alchemy,
            "Celestial": self.celestial,
            "Effigy": self.effigy,
            "Necromancy": self.necromancy,
            "Nomenclature": self.nomenclature,
            "Ushabti": self.ushabti,
            "Judge": self.judge,
            "Phoenix": self.phoenix,
            "Vision": self.vision,
            "Divination": self.divination,
        }
        return {k: v for k, v in hekau_paths.items() if v > 0}

    def is_web_hekau(self, hekau_name):
        """Check if a Hekau path is the favored one for this mummy's Web"""
        web_hekau_map = {
            "isis": "ushabti",
            "osiris": "judge",
            "horus": "phoenix",
            "maat": "vision",
            "thoth": "divination",
        }
        return hekau_name.lower() == web_hekau_map.get(self.web, "")

    def update_ka_from_sekhem(self):
        """Calculate Ka based on Sekhem (base 10 per Sekhem level)"""
        base_ka = self.sekhem * 10
        # Add Background: Ka bonus if tracked separately
        # This would need to check backgrounds when implemented
        self.ka_rating = base_ka

    def total_hekau(self):
        """Sum of all Hekau path ratings"""
        return sum(
            [
                self.alchemy,
                self.celestial,
                self.effigy,
                self.necromancy,
                self.nomenclature,
                self.ushabti,
                self.judge,
                self.phoenix,
                self.vision,
                self.divination,
            ]
        )

    def has_hekau(self):
        """Does this mummy know any Hekau?"""
        return self.total_hekau() > 0

    def xp_cost(self, trait_type, trait_value=None):
        """Calculate XP cost for raising a trait"""
        costs = {
            "hekau_web": 5,  # Web-favored Hekau
            "hekau_universal": 7,  # Universal Hekau
            "hekau_other": 10,  # Other Web's Hekau
            "sekhem": 10,  # Primary power stat
            "balance": 2,  # Humanity equivalent
            "virtue": 2,  # Conviction/Restraint
        }
        return costs.get(trait_type, 1) * (trait_value or 1)

    def freebie_cost(self, trait_type):
        """Calculate freebie point cost"""
        costs = {
            "hekau": 5,
            "sekhem": 7,
            "balance": 2,
            "virtue": 2,
            "ba": 1,  # Per point
        }
        return costs.get(trait_type, 1)

    def spend_ba(self, amount):
        """Spend Ba for magic"""
        if self.ba >= amount:
            self.ba -= amount
            self.save()
            return True
        return False

    def regain_ba(self, amount):
        """Regain Ba (capped at Ka)"""
        self.ba = min(self.ba + amount, self.ka_rating)
        self.save()

    def save(self, *args, **kwargs):
        """Auto-update Ka when Sekhem changes"""
        self.update_ka_from_sekhem()
        super().save(*args, **kwargs)

    # ========================================
    # URLS
    # ========================================

    def get_absolute_url(self):
        return reverse("characters:mummy:mummy", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mummy:update:mummy", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mummy:create:mummy")

    def get_heading(self):
        return "mtr_heading"

    class Meta:
        verbose_name = "Mummy"
        verbose_name_plural = "Mummies"
