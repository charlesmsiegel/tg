from characters.models.core import Ability, Attribute
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Practice
from core.models import Model
from core.utils import weighted_choice
from django.db import models
from django.urls import reverse


class Rote(Model):
    type = "rote"
    gameline = "mta"

    effect = models.ForeignKey(Effect, on_delete=models.SET_NULL, null=True)
    practice = models.ForeignKey(
        Practice, on_delete=models.SET_NULL, null=True, blank=True
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True)
    ability = models.ForeignKey(Ability, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Rote"
        verbose_name_plural = "Rotes"
        ordering = ["practice", "name"]

    def get_absolute_url(self):
        return reverse("characters:mage:rote", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:mage:update:rote", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:rote")

    def get_heading(self):
        return "mta_heading"

    def random_name(self):
        self.name = (
            f"{self.effect.name} Rote {Rote.objects.filter(effect=self.effect).count()}"
        )
        self.save()

    def random(self, mage=None, book=None):
        self.update_status("Ran")
        self.name = (
            f"{self.effect.name} Rote {Rote.objects.filter(effect=self.effect).count()}"
        )

        if mage is not None:
            self.practice = mage.practices.order_by("?").first()
            attribute = weighted_choice(mage.get_attributes())
            ability = weighted_choice(
                {
                    k: v
                    for k, v in mage.get_abilities().items()
                    if k in [x.property_name for x in self.practice.abilities.all()]
                }
            )
            self.attribute = Attribute.objects.get(property_name=attribute)
            self.ability = Ability.objects.get(property_name=ability)
        elif book is not None:
            self.practice = book.practices.order_by("?").first()
            self.attribute = Attribute.objects.order_by("?").first()
            self.ability = book.abilities.order_by("?").first()
        else:
            self.practice = Practice.objects.order_by("?").first()
            self.attribute = Attribute.objects.order_by("?").first()
            self.ability = self.practice.abilities.order_by("?").first()
        self.save()
