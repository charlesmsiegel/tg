from characters.models.changeling.ctdhuman import CtDHuman
from django.db import models
from django.urls import reverse


class Inanimae(CtDHuman):
    """
    Inanimae - Elemental fae bound to the natural world.
    Unlike Changelings who are tied to human dreams, Inanimae are
    connected to the elements themselves (earth, water, air, fire, wood).
    """

    type = "inanimae"

    # Inanimae kingdoms (elemental types)
    KINGDOMS = [
        ("kubera", "Kubera"),  # Earth elementals
        ("ondine", "Ondine"),  # Water elementals
        ("paroseme", "Paroseme"),  # Wood/plant elementals
        ("sylph", "Sylph"),  # Air elementals
        ("salamander", "Salamander"),  # Fire elementals
        ("solimond", "Solimond"),  # Crystal/mineral elementals (rare)
        ("mannikin", "Mannikin"),  # Artificial/crafted elementals (rare)
    ]

    # Inanimae "seemings" (life stages, different from changeling seemings)
    INANIMAE_SEEMINGS = [
        ("glimmer", "Glimmer"),  # Newly awakened, young
        ("naturae", "Naturae"),  # Mature, in balance
        ("ancient", "Ancient"),  # Old, powerful, possibly detached
    ]

    kingdom = models.CharField(
        default="",
        max_length=20,
        choices=KINGDOMS,
        help_text="The elemental kingdom of this Inanimae",
    )

    inanimae_seeming = models.CharField(
        default="",
        max_length=15,
        choices=INANIMAE_SEEMINGS,
        help_text="Life stage of the Inanimae",
    )

    # Inanimae use Seasons instead of Courts
    SEASONS = [
        ("spring", "Spring"),  # Growth and renewal
        ("summer", "Summer"),  # Passion and action
        ("autumn", "Autumn"),  # Harvest and wisdom
        ("winter", "Winter"),  # Rest and death
    ]

    season = models.CharField(
        default="",
        max_length=10,
        choices=SEASONS,
        help_text="The Season this Inanimae aligns with",
    )

    # Inanimae use Mana instead of Glamour
    mana = models.IntegerField(
        default=4, help_text="Elemental power (equivalent to Glamour)"
    )

    # Inanimae are less affected by Banality but have Anchors
    anchor_description = models.TextField(
        default="",
        blank=True,
        help_text="The natural location or element this Inanimae is anchored to",
    )

    # Elemental affinity - grants bonus to certain actions
    elemental_strength = models.TextField(
        default="",
        blank=True,
        help_text="What this Inanimae excels at due to their element",
    )

    elemental_weakness = models.TextField(
        default="",
        blank=True,
        help_text="What this Inanimae is vulnerable to due to their element",
    )

    # Inanimae can use Arts but have their own traditions
    # They use the same Arts as Changelings but favor different ones
    # (This is inherited from CtDHuman/Changeling)

    class Meta:
        verbose_name = "Inanimae"
        verbose_name_plural = "Inanimae"

    def get_absolute_url(self):
        return reverse("characters:changeling:inanimae", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:changeling:update:inanimae", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:inanimae")

    def has_kingdom(self):
        return self.kingdom != ""

    def set_kingdom(self, kingdom):
        """Set the elemental kingdom of this Inanimae"""
        self.kingdom = kingdom
        return True

    def has_season(self):
        return self.season != ""

    def set_season(self, season):
        """Set the seasonal alignment"""
        self.season = season
        return True

    def has_inanimae_seeming(self):
        return self.inanimae_seeming != ""

    def set_inanimae_seeming(self, seeming):
        """Set the life stage of this Inanimae"""
        self.inanimae_seeming = seeming
        # Adjust starting Mana by seeming
        if seeming == "glimmer":
            self.mana = 5  # Young and full of elemental energy
        elif seeming == "ancient":
            self.mana = 3  # Less energy but more wisdom
        else:
            self.mana = 4  # Naturae
        return True

    def add_mana(self):
        """Add a dot of Mana (like Glamour for Changelings)"""
        from core.utils import add_dot

        return add_dot(self, "mana", 10)

    def set_anchor(self, description):
        """Set the Inanimae's anchor description"""
        self.anchor_description = description
        return True

    def has_anchor(self):
        return self.anchor_description != ""
