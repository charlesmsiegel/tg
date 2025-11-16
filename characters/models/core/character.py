from core.models import Model
from django.db import models
from django.urls import reverse


class CharacterModel(Model):
    npc = models.BooleanField(default=False)

    gameline = "wod"

    class Meta:
        verbose_name = "Character Model"
        verbose_name_plural = "Character Models"
        ordering = ["name"]


class Character(CharacterModel):
    type = "character"

    freebie_step = -1

    gameline = "wod"

    concept = models.CharField(max_length=100)
    creation_status = models.IntegerField(default=1)

    notes = models.TextField(default="", blank=True, null=True)
    xp = models.IntegerField(default=0)
    spent_xp = models.JSONField(default=list)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def get_type(self):
        if "human" in self.type:
            return "Human"
        if "spirit_character" == self.type:
            return "Spirit"
        return self.type.title()

    def get_heading(self):
        return "wod_heading"

    def next_stage(self):
        self.creation_status += 1
        self.save()

    def prev_stage(self):
        self.creation_status -= 1
        self.save()

    def has_concept(self):
        return self.concept != ""

    def set_concept(self, concept):
        self.concept = concept
        return True

    def get_absolute_url(self):
        return reverse("characters:character", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:update:character", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:create:character")

    def xp_spend_record(self, trait, trait_type, value, cost=None):
        if cost is None:
            cost = self.xp_cost(trait_type, value)
        return {
            "index": f"{self.id}_{trait_type}_{trait}_{value}".replace(" ", "-"),
            "trait": trait,
            "value": value,
            "cost": cost,
            "approved": "Pending",
        }

    def waiting_for_xp_spend(self):
        for d in self.spent_xp:
            if d["approved"] == "Pending":
                return True
        return False

    def add_xp(self, amount):
        """Add XP to the character.

        Args:
            amount: Integer amount of XP to add.
        """
        self.xp += amount
        self.save()
