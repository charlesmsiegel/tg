from django.db import models
from django.urls import reverse


class HunterOrganization(models.Model):
    """Hunter groups and networks (cells, compacts, conspiracies)"""

    name = models.CharField(max_length=200)

    ORGANIZATION_TYPE_CHOICES = [
        ("cell", "Independent Cell"),
        ("network", "Hunter Network"),
        ("compact", "Compact"),
        ("conspiracy", "Conspiracy"),
    ]

    organization_type = models.CharField(
        max_length=100,
        choices=ORGANIZATION_TYPE_CHOICES,
        default="cell",
    )

    # Organization details
    philosophy = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    resources = models.IntegerField(default=1)  # 1-5

    # Membership
    members = models.ManyToManyField(
        "Hunter",
        blank=True,
        related_name="organizations",
    )

    leader = models.ForeignKey(
        "Hunter",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="led_organizations",
    )

    class Meta:
        verbose_name = "Hunter Organization"
        verbose_name_plural = "Hunter Organizations"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("characters:hunter:organization", kwargs={"pk": self.pk})
