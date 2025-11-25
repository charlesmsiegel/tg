from django.db import models
from django.urls import reverse


class Edge(models.Model):
    """Individual Edge power definition"""

    name = models.CharField(max_length=100)

    VIRTUE_CHOICES = [
        ("conviction", "Conviction - Judgement"),
        ("vision", "Vision - Defense"),
        ("zeal", "Zeal - Redemption"),
    ]

    virtue = models.CharField(
        max_length=20,
        choices=VIRTUE_CHOICES,
    )

    level = models.IntegerField(default=1)  # 1-5 typically

    # Mechanics
    cost = models.CharField(max_length=200, blank=True)  # e.g., "1 Conviction"
    duration = models.CharField(max_length=200, blank=True)
    system = models.TextField(blank=True)
    description = models.TextField(blank=True)

    # Source book reference
    book = models.ForeignKey(
        "core.Book",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Edge"
        verbose_name_plural = "Edges"
        ordering = ["virtue", "level", "name"]
        unique_together = ["name", "level"]

    def __str__(self):
        return f"{self.name} ({self.get_virtue_display()}, Level {self.level})"

    def get_absolute_url(self):
        return reverse("characters:hunter:edge", kwargs={"pk": self.pk})
