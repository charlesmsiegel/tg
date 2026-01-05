from core.models import Model
from django.urls import reverse


class SeptPosition(Model):
    """
    SeptPosition - Formal roles within a Sept
    Represents the various leadership and functional positions in a
    Werewolf sept. Each position has specific responsibilities and duties.
    """

    type = "septposition"

    # Common sept positions
    POSITION_TYPES = [
        ("master_of_challenge", "Master of the Challenge"),
        ("keeper_of_land", "Keeper of the Land"),
        ("warder", "Warder"),
        ("guardian", "Guardian"),
        ("gatekeeper", "Gatekeeper"),
        ("den_parent", "Den Parent"),
        ("truthcatcher", "Truthcatcher"),
        ("caller_of_wyld", "Caller of the Wyld"),
        ("master_of_rites", "Master of the Rites"),
        ("talesinger", "Talesinger"),
        ("wyrmfoe", "Wyrmfoe"),
        ("elder", "Elder"),
        ("sept_leader", "Sept Leader"),
        ("other", "Other"),
    ]

    class Meta:
        verbose_name = "Sept Position"
        verbose_name_plural = "Sept Positions"

    def get_absolute_url(self):
        return reverse("characters:werewolf:septposition", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:septposition", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:septposition")
