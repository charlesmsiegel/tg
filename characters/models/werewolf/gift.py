from django.db import models
from django.urls import reverse

from core.models import Model


class GiftPermission(models.Model):
    shifter = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.shifter}/{self.condition}"


class Gift(Model):
    type = "gift"
    gameline = "wta"

    rank = models.IntegerField(default=0)
    allowed = models.ManyToManyField(GiftPermission, blank=True)

    class Meta:
        verbose_name = "Gift"
        verbose_name_plural = "Gifts"

    def get_absolute_url(self):
        return reverse("characters:werewolf:gift", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:werewolf:update:gift", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:werewolf:create:gift")


def gifts_by_rank(gifts, sources, shifter):
    """Group a character's gifts by rank for the sheet, each with the source it came from.

    ``sources`` maps a GiftPermission condition to its label, in priority order (e.g.
    {"Uktena": "Uktena", "theurge": "Theurge", "homid": "Homid"}); a gift's source is the
    first of those that its ``allowed`` permissions for ``shifter`` grant. Returns
    ``[(rank, [(gift, source), ...]), ...]`` in ascending rank, gifts by name.
    """
    groups = {}
    for gift in gifts.prefetch_related("allowed").order_by("rank", "name"):
        conditions = {p.condition for p in gift.allowed.all() if p.shifter == shifter}
        source = next((label for cond, label in sources.items() if cond in conditions), "")
        groups.setdefault(gift.rank, []).append((gift, source))
    return sorted(groups.items(), key=lambda item: item[0])
