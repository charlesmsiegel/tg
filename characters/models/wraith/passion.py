from django.db import models


class Passion(models.Model):
    wraith = models.ForeignKey(
        "Wraith",
        on_delete=models.CASCADE,
        related_name="passions",
    )
    emotion = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.IntegerField(default=1)
    is_dark_passion = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Passion"
        verbose_name_plural = "Passions"

    def __str__(self):
        return f"{self.emotion}: {self.description} ({self.rating})"
