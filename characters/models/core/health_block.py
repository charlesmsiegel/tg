from django.db import models


class HealthBlock(models.Model):
    current_health_levels = models.CharField(default="", max_length=100, blank=True)
    max_health_levels = models.IntegerField(default=7)

    class Meta:
        abstract = True

    def get_health_levels(self):
        damage = list(self.current_health_levels)
        health_levels = damage + ["-"] * (self.max_health_levels - len(damage))
        return health_levels

    def get_health_level_names(self):
        defaults = [
            "Bruised",
            "Hurt",
            "Injured",
            "Wounded",
            "Mauled",
            "Crippled",
            "Incapacitated",
        ]
        difference = self.max_health_levels - len(defaults)
        if difference != 0:
            return ["Bruised"] * difference + defaults
        return defaults

    def get_wound_penalty_list(self):
        defaults = ["-0", "-1", "-1", "-2", "-2", "-5"]
        difference = self.max_health_levels - len(defaults)
        if difference != 0:
            return ["-0"] * difference + defaults
        return defaults

    def get_health_table(self):
        return zip(
            self.get_health_level_names(),
            self.get_wound_penalty_list(),
            self.get_health_levels(), strict=False,
        )

    def get_wound_penalty(self):
        health_levels = len(self.current_health_levels)
        if health_levels <= self.max_health_levels - 6:
            return 0
        if health_levels <= self.max_health_levels - 4:
            return -1
        if health_levels <= self.max_health_levels - 2:
            return -2
        if health_levels <= self.max_health_levels - 1:
            return -5
        return -1000

    def add_bashing(self):
        if len(self.current_health_levels) < self.max_health_levels:
            self.current_health_levels += "B"
        elif "B" in self.current_health_levels:
            self.current_health_levels = self.current_health_levels.replace("B", "L", 1)
        self.current_health_levels = "".join(
            sorted(self.current_health_levels, key=self.sort_damage)
        )

    @staticmethod
    def sort_damage(damage_type):
        if damage_type == "B":
            return 2
        if damage_type == "L":
            return 1
        return 0

    def add_aggravated(self):
        if len(self.current_health_levels) < self.max_health_levels:
            self.current_health_levels += "A"
        self.current_health_levels = "".join(
            sorted(self.current_health_levels, key=self.sort_damage)
        )

    def add_lethal(self):
        if len(self.current_health_levels) < self.max_health_levels:
            self.current_health_levels += "L"
        self.current_health_levels = "".join(
            sorted(self.current_health_levels, key=self.sort_damage)
        )
