from django.db import models
from django.urls import reverse

from characters.models.core.ability_block import Ability
from characters.models.mage.resonance import Resonance
from core.models import Model


class Instrument(Model):
    type = "instrument"
    gameline = "mta"

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


class Practice(Model):
    type = "practice"
    gameline = "mta"

    abilities = models.ManyToManyField(Ability, blank=True)
    instruments = models.ManyToManyField(Instrument, blank=True)
    common_resonance_traits = models.ManyToManyField(Resonance, blank=True)
    benefit = models.TextField(default="", blank=True)
    penalty = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "Practice"
        verbose_name_plural = "Practices"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:mage:practice", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:practice", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:practice")

    def add_ability(self, ability):
        self.abilities.add(ability)
        return True

    def add_abilities(self, list_of_abilities):
        for ab in list_of_abilities:
            self.add_ability(ab)
        return True

    def get_rotes(self):
        from characters.models.mage.rote import Rote

        return Rote.objects.filter(practice=self)


class SpecializedPractice(Practice):
    type = "specialized_practice"

    parent_practice = models.ForeignKey(
        Practice,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="specialization",
    )
    faction = models.ForeignKey(
        "characters.MageFaction", blank=True, null=True, on_delete=models.SET_NULL
    )
    extra_benefit = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "Specialized Practice"
        verbose_name_plural = "Specialized Practices"

    def get_absolute_url(self):
        return reverse("characters:mage:specialized_practice", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:specialized_practice", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:specialized_practice")

    def get_rotes(self):
        if self.parent_practice is None:
            from characters.models.mage.rote import Rote

            return Rote.objects.none()
        return self.parent_practice.get_rotes()


class CorruptedPractice(Practice):
    type = "corrupted_practice"

    parent_practice = models.ForeignKey(
        Practice,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="corruption",
    )
    extra_benefit = models.TextField(default="", blank=True)
    price = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = "Corrupted Practice"
        verbose_name_plural = "Corrupted Practices"

    def get_absolute_url(self):
        return reverse("characters:mage:corrupted_practice", args=[str(self.id)])

    def get_update_url(self):
        return reverse("characters:mage:update:corrupted_practice", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mage:create:corrupted_practice")

    def get_rotes(self):
        if self.parent_practice is None:
            from characters.models.mage.rote import Rote

            return Rote.objects.none()
        return self.parent_practice.get_rotes()


class Tenet(Model):
    type = "tenet"
    gameline = "mta"

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


class Paradigm(Model):
    type = "paradigm"
    gameline = "mta"

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

    def get_associated_practices(self):
        associated_practices = Practice.objects.none()

        for tenet in self.tenets.all():
            associated_practices = associated_practices | tenet.associated_practices.all()

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
            associated_practices = associated_practices | tenet.associated_practices.all()
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
