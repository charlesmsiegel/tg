from characters.models.core.ability import Ability
from characters.models.mage.resonance import Resonance
from core.models import Model
from django.db import models
from django.urls import reverse


# Create your models here.
class Instrument(Model):
    type = "instrument"

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"

    def get_absolute_url(self):
        return reverse("characters:mage:instrument", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:instrument", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:instrument")

    def get_heading(self):
        return "mtas_heading"


class Practice(Model):
    type = "practice"

    abilities = models.ManyToManyField(Ability, blank=True)
    instruments = models.ManyToManyField(Instrument, blank=True)
    common_resonance_traits = models.ManyToManyField(Resonance, blank=True)
    benefit = models.TextField(default="")
    penalty = models.TextField(default="")

    class Meta:
        verbose_name = "Practice"
        verbose_name_plural = "Practices"

    def get_absolute_url(self):
        return reverse("characters:mage:practice", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:practice", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:practice")

    def get_heading(self):
        return "mtas_heading"

    def add_ability(self, ability):
        self.abilities.add(ability)
        return True

    def add_abilities(self, list_of_abilities):
        for ab in list_of_abilities:
            self.add_ability(ab)
        return True


class SpecializedPractice(Practice):
    type = "specialized_practice"

    parent_practice = models.ForeignKey(Practice, blank=True, null=True, on_delete=models.SET_NULL)
    faction = models.ForeignKey(
        "characters.MageFaction", blank=True, null=True, on_delete=models.SET_NULL
    )
    extra_benefit = models.TextField(default="")

    def get_update_url(self):
        return reverse(
            "characters:mage:update:specialized_practice", kwargs={"pk": self.pk}
        )

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:specialized_practice")


class CorruptedPractice(Practice):
    type = "corrupted_practice"

    parent_practice = models.ForeignKey(Practice, blank=True, null=True, on_delete=models.SET_NULL)
    extra_benefit = models.TextField(default="")
    price = models.TextField(default="")

    def get_update_url(self):
        return reverse(
            "characters:mage:update:corrupted_practice", kwargs={"pk": self.pk}
        )

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:corrupted_practice")


class Tenet(Model):
    type = "tenet"

    tenet_type = models.CharField(
        max_length=3,
        choices=[
            ("met", "Metaphysical"),
            ("per", "Personal"),
            ("asc", "Ascension"),
            ("oth", "Other"),
        ],
        default="oth",
    )

    associated_practices = models.ManyToManyField(
        Practice,
        blank=True,
        related_name="associated_of",
    )
    limited_practices = models.ManyToManyField(
        Practice,
        blank=True,
        related_name="limited_of",
    )

    class Meta:
        verbose_name = "Tenet"
        verbose_name_plural = "Tenets"

    def get_absolute_url(self):
        return reverse("characters:mage:tenet", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:tenet", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:tenet")

    def get_heading(self):
        return "mtas_heading"


class Paradigm(Model):
    type = "paradigm"

    tenets = models.ManyToManyField(Tenet, blank=True)

    class Meta:
        verbose_name = "Paradigm"
        verbose_name_plural = "Paradigms"

    def get_absolute_url(self):
        return reverse("characters:mage:paradigm", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:paradigm", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:paradigm")

    def get_heading(self):
        return "mtas_heading"

    def get_associated_practices(self):
        associated_practices = Practice.objects.none()

        for tenet in self.tenets.all():
            associated_practices = (
                associated_practices | tenet.associated_practices.all()
            )

        return associated_practices.distinct().exclude(
            id__in=self.get_intersection_practices().values("id")
        )

    def get_limited_practices(self):
        limited_practices = Practice.objects.none()

        for tenet in self.tenets.all():
            limited_practices = limited_practices | tenet.limited_practices.all()

        return limited_practices.distinct().exclude(
            id__in=self.get_intersection_practices().values("id")
        )

    def get_intersection_practices(self):
        associated_practices = Practice.objects.none()
        limited_practices = Practice.objects.none()
        for tenet in self.tenets.all():
            associated_practices = (
                associated_practices | tenet.associated_practices.all()
            )
            limited_practices = limited_practices | tenet.limited_practices.all()

        return associated_practices & limited_practices

    def set_tenets(self, t1, t2, t3):
        types = set([t1.tenet_type, t2.tenet_type, t3.tenet_type])
        if types != {"met", "per", "asc"}:
            return False
        self.add_tenet(t1)
        self.add_tenet(t2)
        self.add_tenet(t3)
        return True

    def add_tenet(self, tenet):
        self.tenets.add(tenet)
        return True

    def has_tenets(self):
        tenet_types = self.tenets.values_list("tenet_type", flat=True)
        if "met" in tenet_types and "asc" in tenet_types and "per" in tenet_types:
            return True
        return False
