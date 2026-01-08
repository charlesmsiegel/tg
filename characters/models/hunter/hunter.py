from django.db import models
from django.urls import reverse

from core.linked_stat import linked_stat_fields

from .creed import Creed
from .htrhuman import HtRHuman


# Factory-created linked stat fields for Hunter virtues
_conviction_fields = linked_stat_fields("conviction", default=1, min_permanent=1, max_permanent=5)
_vision_fields = linked_stat_fields("vision", default=1, min_permanent=1, max_permanent=5)
_zeal_fields = linked_stat_fields("zeal", default=1, min_permanent=1, max_permanent=5)


class Hunter(HtRHuman):
    """
    Represents an Imbued Hunter character.
    Hunters are mortals chosen by mysterious entities called the Messengers
    and granted supernatural powers (Edges) fueled by their Virtues.
    """

    type = "hunter"
    freebie_step = 7

    # ===== CREED =====
    creed = models.ForeignKey(
        Creed,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="hunters",
    )

    # ===== VIRTUES (Hunter-specific trinity) =====
    # These replace Conscience/Self-Control/Courage from other gamelines
    conviction, temporary_conviction, conviction_stat = _conviction_fields  # Justice/Judgement
    vision, temporary_vision, vision_stat = _vision_fields  # Defense/Mercy
    zeal, temporary_zeal, zeal_stat = _zeal_fields  # Zeal/Vengeance

    # ===== EDGES (Supernatural Powers) =====
    # Conviction Edges (Judgement) - 7 edges
    discern = models.IntegerField(default=0)
    burden = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    expose = models.IntegerField(default=0)
    investigate = models.IntegerField(default=0)
    witness = models.IntegerField(default=0)
    prosecute = models.IntegerField(default=0)

    # Vision Edges (Defense) - 7 edges
    illuminate = models.IntegerField(default=0)
    ward = models.IntegerField(default=0)
    cleave = models.IntegerField(default=0)
    hide = models.IntegerField(default=0)
    blaze = models.IntegerField(default=0)
    radiate = models.IntegerField(default=0)
    vengeance = models.IntegerField(default=0)

    # Zeal Edges (Redemption) - 7 edges
    demand = models.IntegerField(default=0)
    confront = models.IntegerField(default=0)
    donate = models.IntegerField(default=0)
    becalm = models.IntegerField(default=0)
    respire = models.IntegerField(default=0)
    rejuvenate = models.IntegerField(default=0)
    redeem = models.IntegerField(default=0)

    # ===== ADDITIONAL HUNTER TRAITS =====
    imbuing_date = models.DateField(blank=True, null=True)  # When they were chosen

    PRIMARY_VIRTUE_CHOICES = [
        ("conviction", "Conviction"),
        ("vision", "Vision"),
        ("zeal", "Zeal"),
    ]

    primary_virtue = models.CharField(
        max_length=20,
        choices=PRIMARY_VIRTUE_CHOICES,
        default="conviction",
    )

    # Safehouse relationship
    safehouse = models.ForeignKey(
        "locations.Safehouse",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="members",
    )

    # Cell members (many-to-many relationship)
    # symmetrical=True means if A is in B's cell, B is automatically in A's cell
    cell_members = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=True,
    )

    class Meta:
        verbose_name = "Hunter"
        verbose_name_plural = "Hunters"

    # ===== METHODS =====
    def get_edges(self):
        """Return dictionary of all learned edges by virtue"""
        edges = {"conviction": {}, "vision": {}, "zeal": {}}

        # Conviction Edges
        conviction_edges = [
            "discern",
            "burden",
            "balance",
            "expose",
            "investigate",
            "witness",
            "prosecute",
        ]
        for edge in conviction_edges:
            rating = getattr(self, edge, 0)
            if rating > 0:
                edges["conviction"][edge] = rating

        # Vision Edges
        vision_edges = [
            "illuminate",
            "ward",
            "cleave",
            "hide",
            "blaze",
            "radiate",
            "vengeance",
        ]
        for edge in vision_edges:
            rating = getattr(self, edge, 0)
            if rating > 0:
                edges["vision"][edge] = rating

        # Zeal Edges
        zeal_edges = [
            "demand",
            "confront",
            "donate",
            "becalm",
            "respire",
            "rejuvenate",
            "redeem",
        ]
        for edge in zeal_edges:
            rating = getattr(self, edge, 0)
            if rating > 0:
                edges["zeal"][edge] = rating

        return edges

    def primary_edges(self):
        """Return edges associated with the primary virtue"""
        if self.creed:
            return self.creed.primary_virtue
        return self.primary_virtue

    def freebie_cost(self, trait_type):
        """Override for Hunter-specific freebie costs"""
        costs = {
            "attribute": 5,
            "ability": 2,
            "background": 1,
            "virtue": 2,  # Conviction/Vision/Zeal
            "edge": 3,  # All Edges cost 3 freebies per dot
            "willpower": 1,
        }
        if trait_type in costs:
            return costs[trait_type]
        return super().freebie_cost(trait_type)

    def xp_cost(self, trait_type, value):
        """Override for Hunter-specific XP costs"""
        costs = {
            "new ability": 3,
            "ability": value * 2,
            "new background": 3,
            "background": value * 2,
            "virtue": value * 2,  # Conviction/Vision/Zeal
            "edge": value * 3,  # Edges cost current rating x3
            "willpower": value,
        }
        if trait_type in costs:
            return costs[trait_type]
        return super().xp_cost(trait_type, value)

    def spend_xp(self, trait):
        """Handle Hunter-specific XP spending"""
        result = super().spend_xp(trait)

        # Custom logic for Edges
        edge_names = [
            "discern",
            "burden",
            "balance",
            "expose",
            "investigate",
            "witness",
            "prosecute",
            "illuminate",
            "ward",
            "cleave",
            "hide",
            "blaze",
            "radiate",
            "vengeance",
            "demand",
            "confront",
            "donate",
            "becalm",
            "respire",
            "rejuvenate",
            "redeem",
        ]

        if trait in edge_names:
            current_value = getattr(self, trait, 0)
            cost = self.xp_cost("edge", current_value + 1)
            return {"success": True, "cost": cost, "trait": trait}

        return result

    def spend_freebies(self, trait):
        """Handle Hunter-specific freebie spending"""
        result = super().spend_freebies(trait)

        # Custom logic for Virtues
        if trait in ["conviction", "vision", "zeal"]:
            return {"success": True, "cost": self.freebie_cost("virtue")}

        # Custom logic for Edges
        edge_names = [
            "discern",
            "burden",
            "balance",
            "expose",
            "investigate",
            "witness",
            "prosecute",
            "illuminate",
            "ward",
            "cleave",
            "hide",
            "blaze",
            "radiate",
            "vengeance",
            "demand",
            "confront",
            "donate",
            "becalm",
            "respire",
            "rejuvenate",
            "redeem",
        ]

        if trait in edge_names:
            return {"success": True, "cost": self.freebie_cost("edge")}

        return result

    def get_absolute_url(self):
        return reverse("characters:hunter:hunter", kwargs={"pk": self.pk})
