from characters.models.core.human import Human
from django.db import models
from django.urls import reverse


class CtDHuman(Human):
    type = "ctd_human"

    gameline = "ctd"

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "chimera",
        "dreamers",
        "holdings",
        "remembrance",
        "resources",
        "retinue",
        "title",
        "treasure",
    ]

    kenning = models.IntegerField(default=0)
    leadership = models.IntegerField(default=0)

    animal_ken = models.IntegerField(default=0)
    larceny = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)

    enigmas = models.IntegerField(default=0)
    gremayre = models.IntegerField(default=0)
    law = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    technology = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Human (Changeling)"
        verbose_name_plural = "Humans (Changeling)"

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:ctd_human")

    def get_update_url(self):
        return reverse("characters:changeling:update:ctd_human", kwargs={"pk": self.pk})

    def get_heading(self):
        return "ctd_heading"

    def get_talents(self):
        d = super().get_talents()
        d.update(
            {
                "kenning": self.kenning,
                "leadership": self.leadership,
            }
        )
        return d

    def get_skills(self):
        d = super().get_skills()
        d.update(
            {
                "animal_ken": self.animal_ken,
                "larceny": self.larceny,
                "performance": self.performance,
                "survival": self.survival,
            }
        )
        return d

    def get_knowledges(self):
        d = super().get_knowledges()
        d.update(
            {
                "enigmas": self.enigmas,
                "gremayre": self.gremayre,
                "law": self.law,
                "politics": self.politics,
                "technology": self.technology,
            }
        )
        return d
