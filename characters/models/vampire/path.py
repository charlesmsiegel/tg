from core.models import Model
from django.db import models
from django.urls import reverse


class Path(Model):
    """
    Represents a Path of Enlightenment (alternative to Humanity).
    Examples: Path of Caine, Path of Death and the Soul, Path of Honorable Accord
    """

    type = "path"
    gameline = "vtm"

    # Path attributes - which virtues this path requires
    requires_conviction = models.BooleanField(
        default=True, help_text="If True, uses Conviction; if False, uses Conscience"
    )
    requires_instinct = models.BooleanField(
        default=True, help_text="If True, uses Instinct; if False, uses Self-Control"
    )

    # Path description and ethics
    ethics = models.TextField(blank=True, help_text="The moral code of this Path")

    class Meta:
        verbose_name = "Path of Enlightenment"
        verbose_name_plural = "Paths of Enlightenment"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:vampire:path", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:vampire:update:path", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:vampire:create:path")

    def get_heading(self):
        return "vtm_heading"

    def check_character_virtues(self, character):
        """
        Check if a character has the correct virtues for this path.
        Returns True if character's virtue booleans match this path's requirements.
        """
        return (
            character.has_conviction == self.requires_conviction
            and character.has_instinct == self.requires_instinct
        )

    def update_character_virtues(self, character):
        """
        Update a character's virtue booleans to match this path's requirements.
        Resets the values of virtues that are being switched away from.
        Returns True if any changes were made.
        """
        changed = False

        # Update first virtue (Conviction vs Conscience)
        if character.has_conviction != self.requires_conviction:
            character.has_conviction = self.requires_conviction
            # Reset the virtue we're switching away from
            if self.requires_conviction:
                character.conscience = 0
            else:
                character.conviction = 0
            changed = True

        # Update second virtue (Instinct vs Self-Control)
        if character.has_instinct != self.requires_instinct:
            character.has_instinct = self.requires_instinct
            # Reset the virtue we're switching away from
            if self.requires_instinct:
                character.self_control = 0
            else:
                character.instinct = 0
            changed = True

        return changed

    def get_virtues_display(self):
        """Return a string describing which virtues this path requires."""
        first_virtue = "Conviction" if self.requires_conviction else "Conscience"
        second_virtue = "Instinct" if self.requires_instinct else "Self-Control"
        return f"{first_virtue} and {second_virtue}"
