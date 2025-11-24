from characters.models.werewolf.wtahuman import WtAHuman
from django.db import models
from django.urls import reverse


class Drone(WtAHuman):
    """
    Drone - Bane-possessed humans
    Mortals possessed by Banes (evil spirits of the Wyrm). Unlike Fomori
    who are internally corrupted, Drones are externally controlled by
    a possessing entity. They serve as minions and antagonists.
    """

    type = "drone"

    # Bane name/type
    bane_name = models.CharField(default="", max_length=100)
    bane_type = models.CharField(default="", max_length=100)

    # Spiritual stats
    rage = models.IntegerField(default=0)
    gnosis = models.IntegerField(default=0)
    willpower_per_turn = models.IntegerField(default=1)

    # Drones have very limited backgrounds
    allowed_backgrounds = ["contacts", "resources"]

    background_points = 2

    class Meta:
        verbose_name = "Drone"
        verbose_name_plural = "Drones"

    def get_absolute_url(self):
        return reverse("characters:werewolf:drone", kwargs={"pk": self.pk})

    def has_bane(self):
        return self.bane_name != ""

    def set_bane(self, bane_name, bane_type=""):
        self.bane_name = bane_name
        if bane_type:
            self.bane_type = bane_type
        self.save()
        return True
