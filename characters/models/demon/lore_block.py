from django.db import models

from core.utils import add_dot


class LoreBlock(models.Model):
    """Mixin for characters with Demon lores (23 different lores)."""

    # All 23 Lores (0-5 rating each)
    lore_of_awakening = models.IntegerField(default=0)
    lore_of_the_beast = models.IntegerField(default=0)
    lore_of_the_celestials = models.IntegerField(default=0)
    lore_of_death = models.IntegerField(default=0)
    lore_of_the_earth = models.IntegerField(default=0)
    lore_of_flame = models.IntegerField(default=0)
    lore_of_the_firmament = models.IntegerField(default=0)
    lore_of_the_flesh = models.IntegerField(default=0)
    lore_of_the_forge = models.IntegerField(default=0)
    lore_of_the_fundament = models.IntegerField(default=0)
    lore_of_humanity = models.IntegerField(default=0)
    lore_of_light = models.IntegerField(default=0)
    lore_of_longing = models.IntegerField(default=0)
    lore_of_paths = models.IntegerField(default=0)
    lore_of_patterns = models.IntegerField(default=0)
    lore_of_portals = models.IntegerField(default=0)
    lore_of_radiance = models.IntegerField(default=0)
    lore_of_the_realms = models.IntegerField(default=0)
    lore_of_the_spirit = models.IntegerField(default=0)
    lore_of_storms = models.IntegerField(default=0)
    lore_of_transfiguration = models.IntegerField(default=0)
    lore_of_the_wild = models.IntegerField(default=0)
    lore_of_the_winds = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def get_lores(self):
        """Return a dictionary of all lore ratings."""
        return {
            "lore_of_awakening": self.lore_of_awakening,
            "lore_of_the_beast": self.lore_of_the_beast,
            "lore_of_the_celestials": self.lore_of_the_celestials,
            "lore_of_death": self.lore_of_death,
            "lore_of_the_earth": self.lore_of_the_earth,
            "lore_of_flame": self.lore_of_flame,
            "lore_of_the_firmament": self.lore_of_the_firmament,
            "lore_of_the_flesh": self.lore_of_the_flesh,
            "lore_of_the_forge": self.lore_of_the_forge,
            "lore_of_the_fundament": self.lore_of_the_fundament,
            "lore_of_humanity": self.lore_of_humanity,
            "lore_of_light": self.lore_of_light,
            "lore_of_longing": self.lore_of_longing,
            "lore_of_paths": self.lore_of_paths,
            "lore_of_patterns": self.lore_of_patterns,
            "lore_of_portals": self.lore_of_portals,
            "lore_of_radiance": self.lore_of_radiance,
            "lore_of_the_realms": self.lore_of_the_realms,
            "lore_of_the_spirit": self.lore_of_the_spirit,
            "lore_of_storms": self.lore_of_storms,
            "lore_of_transfiguration": self.lore_of_transfiguration,
            "lore_of_the_wild": self.lore_of_the_wild,
            "lore_of_the_winds": self.lore_of_the_winds,
        }

    def total_lores(self):
        """Return total dots spent in lores."""
        return sum(self.get_lores().values())

    def add_lore(self, lore_name, maximum=5):
        """Add a dot to a specific lore."""
        return add_dot(self, lore_name, maximum)

    def filter_lores(self, minimum=0, maximum=5):
        """Return lores within a specific rating range."""
        return {k: v for k, v in self.get_lores().items() if minimum <= v <= maximum}
