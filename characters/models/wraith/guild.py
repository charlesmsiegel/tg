from core.models import Model
from django.db import models
from django.urls import reverse


class Guild(Model):
    type = "guild"
    gameline = "wto"

    GUILD_TYPE_CHOICES = [
        ("greater", "Greater Guild"),
        ("lesser", "Lesser Guild"),
        ("banned", "Banned Guild"),
    ]

    guild_type = models.CharField(max_length=20, choices=GUILD_TYPE_CHOICES, default="greater")
    willpower = models.IntegerField(default=5)

    class Meta:
        verbose_name = "Guild"
        verbose_name_plural = "Guilds"

    def get_absolute_url(self):
        return reverse("characters:wraith:guild", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:wraith:update:guild", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:wraith:create:guild")
