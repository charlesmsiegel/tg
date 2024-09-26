from characters.models.core.statistic import Statistic
from django.db import models


class Background(Statistic):
    type = "background"

    multiplier = models.IntegerField(default=1)


class BackgroundRating(models.Model):
    bg = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True)
    char = models.ForeignKey(
        "characters.Human",
        on_delete=models.SET_NULL,
        null=True,
        related_name="backgrounds",
    )
    rating = models.IntegerField(default=0)
    note = models.CharField(default="", max_length=100)
    complete = models.BooleanField(default=True)

    class Meta:
        ordering = ["bg__name"]

    def __str__(self):
        return f"{self.bg} ({self.note})"
