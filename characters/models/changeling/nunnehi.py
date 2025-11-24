from characters.models.changeling.ctdhuman import CtDHuman
from core.utils import add_dot
from django.db import models
from django.urls import reverse


class Nunnehi(CtDHuman):
    """
    Nunnehi - Native American fae spirits.
    Unlike European Changelings, Nunnehi are more closely tied to the spirit world
    and natural places. They are protectors of their lands and peoples.
    """

    type = "nunnehi"

    # Nunnehi tribes (families)
    TRIBES = [
        ("may_may_gway_shi", "May-May-Gway-Shi"),  # Water dwellers
        ("yunwi_tsundi", "Yunwi Tsundi"),  # Little People of Cherokee
        ("canotina", "Canotina"),  # Tree spirits
        ("kachina", "Kachina"),  # Spirit dancers of the Southwest
        ("nanehi", "Nanehi"),  # Pathfinders and guides
        ("nunnehi_proper", "Nunnehi"),  # Cherokee immortals
        ("other", "Other"),  # Other tribal spirits
    ]

    # Nunnehi "seemings" - different from European changelings
    NUNNEHI_SEEMINGS = [
        ("katchina", "Katchina"),  # Young, playful
        ("kohedan", "Kohedan"),  # Mature, balanced
        ("kurganegh", "Kurganegh"),  # Elder, wise
    ]

    tribe = models.CharField(
        default="",
        max_length=30,
        choices=TRIBES,
        help_text="The family/tribe of this Nunnehi",
    )

    nunnehi_seeming = models.CharField(
        default="",
        max_length=20,
        choices=NUNNEHI_SEEMINGS,
        help_text="Life stage of the Nunnehi",
    )

    # Nunnehi use Medicine instead of Glamour
    medicine = models.IntegerField(
        default=4, help_text="Spiritual power (equivalent to Glamour)"
    )

    # Nunnehi are less affected by Banality in natural places
    # They have connections to the land
    sacred_place = models.TextField(
        default="",
        blank=True,
        help_text="The sacred location this Nunnehi is connected to",
    )

    # Nunnehi have spirit guides
    spirit_guide = models.CharField(
        max_length=100,
        default="",
        blank=True,
        help_text="The spirit animal or guide that aids this Nunnehi",
    )

    # Nunnehi have duties to their people
    tribal_duty = models.TextField(
        default="",
        blank=True,
        help_text="The responsibility this Nunnehi has to their people or land",
    )

    # Path instead of European court/legacy system
    PATH_CHOICES = [
        ("warrior", "Path of the Warrior"),
        ("healer", "Path of the Healer"),
        ("sage", "Path of the Sage"),
        ("trickster", "Path of the Trickster"),
    ]

    path = models.CharField(
        default="",
        max_length=20,
        choices=PATH_CHOICES,
        help_text="The spiritual path this Nunnehi follows",
    )

    class Meta:
        verbose_name = "Nunnehi"
        verbose_name_plural = "Nunnehi"

    def get_absolute_url(self):
        return reverse("characters:changeling:nunnehi", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:changeling:update:nunnehi", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:changeling:create:nunnehi")

    def has_tribe(self):
        return self.tribe != ""

    def set_tribe(self, tribe):
        """Set the Nunnehi tribe/family"""
        self.tribe = tribe
        return True

    def has_path(self):
        return self.path != ""

    def set_path(self, path):
        """Set the spiritual path"""
        self.path = path
        return True

    def has_nunnehi_seeming(self):
        return self.nunnehi_seeming != ""

    def set_nunnehi_seeming(self, seeming):
        """Set the life stage of this Nunnehi"""
        self.nunnehi_seeming = seeming
        # Adjust starting Medicine by seeming
        if seeming == "katchina":
            self.medicine = 5  # Young and energetic
        elif seeming == "kurganegh":
            self.medicine = 3  # Elder, less raw power but more wisdom
        else:
            self.medicine = 4  # Kohedan
        return True

    def add_medicine(self):
        """Add a dot of Medicine (like Glamour for Changelings)"""
        return add_dot(self, "medicine", 10)

    def set_sacred_place(self, place):
        """Set the sacred place connection"""
        self.sacred_place = place
        return True

    def has_sacred_place(self):
        return self.sacred_place != ""

    def set_spirit_guide(self, guide):
        """Set the spirit guide"""
        self.spirit_guide = guide
        return True

    def has_spirit_guide(self):
        return self.spirit_guide != ""

    def set_tribal_duty(self, duty):
        """Set the tribal duty"""
        self.tribal_duty = duty
        return True

    def has_tribal_duty(self):
        return self.tribal_duty != ""
