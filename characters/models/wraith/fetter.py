from django.db import models


class Fetter(models.Model):
    wraith = models.ForeignKey(
        "Wraith",
        on_delete=models.CASCADE,
        related_name="fetters",
    )

    FETTER_TYPE_CHOICES = [
        ("object", "Object"),
        ("location", "Location"),
        ("person", "Person"),
    ]

    fetter_type = models.CharField(max_length=20, choices=FETTER_TYPE_CHOICES, default="object")
    description = models.TextField()
    rating = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Fetter"
        verbose_name_plural = "Fetters"

    def __str__(self):
        return f"{self.description} ({self.rating})"
