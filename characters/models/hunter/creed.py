from django.db import models


class Creed(models.Model):
    """Hunter's moral path and philosophical approach to the imbuing"""

    name = models.CharField(max_length=100, unique=True)

    # Primary Virtue associated with this creed
    VIRTUE_CHOICES = [
        ("conviction", "Conviction"),
        ("vision", "Vision"),
        ("zeal", "Zeal"),
    ]

    primary_virtue = models.CharField(
        max_length=20,
        choices=VIRTUE_CHOICES,
        default="conviction",
    )

    # Creed philosophy and description
    philosophy = models.TextField(blank=True)
    nickname = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    # Preferred Edges (edges this creed commonly uses)
    favored_edges = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Creed"
        verbose_name_plural = "Creeds"
        ordering = ["name"]

    def __str__(self):
        return self.name
