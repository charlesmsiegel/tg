import datetime
import math
import random

from characters.models.core.ability_block import Ability
from characters.models.mage.effect import Effect
from characters.models.mage.focus import Instrument, Practice
from characters.models.mage.resonance import Resonance
from characters.models.mage.rote import Rote
from characters.models.mage.sphere import Sphere
from core.models import Language, Noun
from core.utils import weighted_choice
from django.db import models
from django.db.models import Q
from django.urls import reverse
from items.models.core.material import Material
from items.models.core.medium import Medium
from items.models.mage.wonder import Wonder


class Grimoire(Wonder):
    type = "grimoire"

    abilities = models.ManyToManyField(Ability, blank=True)
    spheres = models.ManyToManyField(Sphere, blank=True)
    date_written = models.IntegerField(default=-5000)
    faction = models.ForeignKey(
        "characters.MageFaction", null=True, blank=True, on_delete=models.SET_NULL
    )
    practices = models.ManyToManyField(Practice, blank=True)
    instruments = models.ManyToManyField(Instrument, blank=True)
    is_primer = models.BooleanField(default=False)
    language = models.ForeignKey(Language, null=True, blank=True, on_delete=models.SET_NULL)
    length = models.IntegerField(default=0)
    cover_material = models.ForeignKey(
        Material,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="is_cover",
    )
    inner_material = models.ForeignKey(
        Material,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="is_inner",
    )
    medium = models.ForeignKey(Medium, null=True, blank=True, on_delete=models.SET_NULL)
    rotes = models.ManyToManyField(Rote, blank=True)

    class Meta:
        verbose_name = "Grimoire"
        verbose_name_plural = "Grimoires"

    def get_update_url(self):
        return reverse("items:mage:update:grimoire", args=[str(self.id)])

    @classmethod
    def get_creation_url(cls):
        return reverse("items:mage:create:grimoire")

    def set_abilities(self, abilities):
        for ability in abilities:
            if not isinstance(ability, Ability):
                return False
            self.abilities.add(ability)
        return True

    def has_abilities(self):
        return self.abilities.exists()

    def set_date_written(self, date_written):
        self.date_written = date_written
        return True

    def has_date_written(self):
        return self.date_written != -5000

    def set_faction(self, faction):
        self.faction = faction
        return True

    def has_faction(self):
        return self.faction is not None

    def set_focus(self, practices, instruments):
        self.practices.set(practices)
        self.instruments.set(instruments)
        self.save()
        return True

    def has_focus(self):
        return self.practices.exists() and self.instruments.exists()

    def set_language(self, language):
        self.language = language
        return True

    def has_language(self):
        return self.language is not None

    def set_length(self, length):
        self.length = length
        return True

    def has_length(self):
        return self.length != 0

    def set_materials(self, cover_material, inner_material):
        self.cover_material = cover_material
        self.inner_material = inner_material
        return True

    def has_materials(self):
        return self.cover_material is not None and self.inner_material is not None

    def set_medium(self, medium):
        self.medium = medium
        return True

    def has_medium(self):
        return self.medium is not None

    def set_rank(self, rank):
        rank = min(5, rank)
        rank = max(1, rank)
        self.rank = rank
        return True

    def has_rank(self):
        return self.rank != 0

    def set_rotes(self, rotes):
        self.rotes.set(rotes)
        self.save()
        return True

    def has_rotes(self):
        tot = (
            self.rotes.count()
            + self.practices.count()
            + self.spheres.count()
            + self.abilities.count()
        )
        if self.is_primer:
            tot += 1
        return tot == self.rank + 3

    def set_spheres(self, spheres):
        for sphere in spheres:
            if not isinstance(sphere, Sphere):
                return False
            self.spheres.add(sphere)
        return True

    def has_spheres(self):
        return self.spheres.exists()

    def set_is_primer(self, is_primer):
        self.is_primer = is_primer
        return True

    def random_abilities(self, abilities=None):
        if self.practices is None:
            raise ValueError("Must have Practice before assigning abilities")
        if abilities is None:
            ability_list = Ability.objects.none()
            for practice in self.practices.all():
                ability_list = ability_list | practice.abilities.all()
            ability_list = ability_list.distinct()
            ability_dict = {x: 1 for x in ability_list}
            if len(ability_dict) > 0:
                choice = weighted_choice(ability_dict, ceiling=20)
            else:
                raise ValueError("No Abilties")
            abilities = [choice]
            while random.random() < 0.1:
                if len(ability_dict) > len(abilities):
                    abilities.append(
                        weighted_choice(
                            {k: v for k, v in ability_dict.items() if k not in abilities}
                        )
                    )
        self.set_abilities(abilities)

    def random_date_written(self, date_written=None):
        if date_written is None:
            if self.faction is not None:
                if self.faction.founded is not None:
                    date_written = random.randint(
                        self.faction.founded, datetime.datetime.now().year
                    )
            date_written = random.randint(
                datetime.datetime.now().year - 100, datetime.datetime.now().year
            )
        self.set_date_written(date_written)

    def random_faction(self, faction=None):
        if faction is None:
            faction_probs = {}
            from characters.models.mage.faction import MageFaction

            for faction in MageFaction.objects.all():
                if faction.parent is None:
                    faction_probs[faction] = 30
                elif faction.parent.parent is None:
                    faction_probs[faction] = 10
                elif faction.parent.parent.parent is None:
                    faction_probs[faction] = 1
                else:
                    faction_probs[faction] = 0
                faction = weighted_choice(faction_probs, ceiling=100)
        self.set_faction(faction)

    def random_practices(self, practices):
        if self.faction is None:
            raise ValueError("Faction must come before Practice")
        if practices is None:
            practices = self.faction.practices.all()
            if not practices.exists():
                practices = Practice.objects.all()
            num_practices = 1
            while random.random() < 0.25 and num_practices < practices.distinct().count():
                num_practices += 1
            practices = practices.order_by("?").distinct()[:num_practices]
        return practices

    def random_instruments(self, instruments, practices=None):
        if instruments is None:
            if practices is not None:
                instruments = Instrument.objects.none()
                for practice in practices:
                    instruments |= practice.instruments.all()
            else:
                instruments = Instrument.objects.all()
            if not instruments.exists():
                instruments = Instrument.objects.all()
            num_instruments = 1
            while random.random() < 0.3 and num_instruments < instruments.distinct().count():
                num_instruments += 1
            instruments = instruments.order_by("?").distinct()[:num_instruments]
        return instruments

    def random_focus(self, practices=None, instruments=None):
        practices = self.random_practices(practices)
        instruments = self.random_instruments(instruments, practices=practices)
        self.set_focus(practices, instruments)

    def random_language(self, language=None):
        if language is None:
            if self.faction is not None:
                if self.faction.languages.exists():
                    languages = self.faction.languages.all()
                    language = weighted_choice({x: x.frequency for x in languages})
                else:
                    languages = Language.objects.all()
                    language = weighted_choice({x: x.frequency for x in languages})
            else:
                languages = Language.objects.all()
                language = weighted_choice({x: x.frequency for x in languages})
        self.set_language(language)

    def random_length(self, length=None):
        if length is None:
            length = int(200 * (random.random() + random.random()) + 50)
            if self.is_primer:
                length += 50
            if self.medium is not None:
                if self.medium.length_modifier_type == "/":
                    length /= self.medium.length_modifier
                elif self.medium.length_modifier_type == "+":
                    length += self.medium.length_modifier
                elif self.medium.length_modifier_type == "*":
                    length *= self.medium.length_modifier
                elif self.medium.length_modifier_type == "-":
                    length -= self.medium.length_modifier
            length = int(length)
        self.set_length(length)

    def random_material(self, cover_material=None, inner_material=None):
        if cover_material is None:
            if self.faction is not None:
                if self.faction.materials.exists():
                    cover_material = self.faction.materials.order_by("?").first()
                else:
                    cover_material = Material.objects.order_by("?").first()
            else:
                cover_material = Material.objects.order_by("?").first()
        if inner_material is None:
            is_hard = random.random() <= 0.3
            if self.faction is not None:
                if self.faction.materials.filter(is_hard=is_hard).exists():
                    inner_material = (
                        self.faction.materials.filter(is_hard=is_hard).order_by("?").first()
                    )
                else:
                    inner_material = Material.objects.filter(is_hard=is_hard).order_by("?").first()
            else:
                inner_material = Material.objects.filter(is_hard=is_hard).order_by("?").first()
        self.set_materials(cover_material, inner_material)

    def random_medium(self, medium=None):
        if medium is None:
            if self.faction is not None:
                if self.faction.media.exists():
                    medium = self.faction.media.order_by("?").first()
                else:
                    medium = Medium.objects.order_by("?").first()
            else:
                medium = Medium.objects.order_by("?").first()
        self.set_medium(medium)

    def random_rank(self, rank=None):
        if rank is None:
            roll = 1 / random.random()
            roll = int(math.log(roll, 10))
            rank = max(min(roll, 5), 1)
        self.set_rank(rank)

    def random_rotes(self, rotes=None):
        if not self.spheres.exists():
            raise ValueError("Spheres must be determiend before rotes")
        if rotes is None:
            effects = []

            kwargs = {f"{sphere.property_name}__gt": 0 for sphere in self.spheres.all()}
            q_objects = Q()
            for key, value in kwargs.items():
                q_objects |= Q(**{key: value})
            effects = Effect.objects.filter(q_objects)

            kwargs = {f"{sphere.property_name}__lte": self.rank for sphere in Sphere.objects.all()}
            for key, value in kwargs.items():
                effects = effects.filter(Q(**{key: value}))
            num_rotes = self.rank
            if self.spheres.count() > 1:
                num_rotes -= self.spheres.count() - 1
            if self.practices.count() > 1:
                num_rotes -= self.practices.count() - 1
            if self.abilities.count() > 1:
                num_rotes -= self.abilities.count() - 1
            if self.is_primer:
                num_rotes -= 1
            while num_rotes < 0:
                options = []
                if self.spheres.count() > 1:
                    options.append("spheres")
                elif self.practices.count() > 1:
                    options.append("practices")
                elif self.abilities.count() > 1:
                    options.append("abilities")
                choice = random.choice(options)
                if choice == "spheres":
                    self.spheres.remove(self.spheres.last())
                if choice == "practices":
                    self.practices.remove(self.practices.last())
                if choice == "abilities":
                    self.practices.remove(self.practices.last())
                num_rotes = (
                    self.rank
                    + 3
                    - self.spheres.count()
                    - self.practices.count()
                    - self.abilities.count()
                )
                if self.is_primer:
                    num_rotes -= 1

            rotes = list(effects.order_by("?")[:num_rotes])
            rotes = [Rote.objects.create(effect=x) for x in rotes]
            for x in rotes:
                x.random(book=self)
        self.set_rotes(rotes)

    def random_spheres(self, spheres=None):
        if spheres is None:
            spheres = []
            sphere_dict = {x: 1 for x in Sphere.objects.all()}
            if self.faction is not None:
                for sphere in self.faction.affinities.all():
                    sphere_dict[sphere] += 5
            spheres.append(weighted_choice(sphere_dict))
            while random.random() < 0.1:
                remaining = {k: v for k, v in sphere_dict.items() if k not in spheres}
                if not remaining:
                    break
                spheres.append(weighted_choice(remaining))
        self.set_spheres(spheres)

    def random_is_primer(self, is_primer=None):
        if is_primer is None:
            is_primer = random.random() < 0.1
        self.set_is_primer(is_primer)

    def random_name(self):
        name = ""
        if not self.has_name():
            while Grimoire.objects.filter(name=name).exists() or name == "":
                sphere = random.choice(self.spheres.all())
                noun = Noun.objects.order_by("?").first().name.title()
                noun2 = Noun.objects.order_by("?").first().name.title()
                resonance = (
                    Resonance.objects.filter(Q(**{sphere.property_name: True}))
                    .order_by("?")
                    .first()
                    .name.title()
                )
                sphere = str(sphere).title()
                forms = [
                    f"Book of {resonance} {noun}",
                    f"{resonance} {sphere} Grimoire",
                    f"{resonance} {self.medium} of {sphere}",
                    f"{noun} of {resonance} {noun2}",
                ]
                name = random.choice(forms)
            return self.set_name(name)
        return False

    def random(
        self,
        rank=None,
        is_primer=None,
        faction=None,
        practices=None,
        instruments=None,
        date_written=None,
        medium=None,
        cover_material=None,
        inner_material=None,
        length=None,
        language=None,
        abilities=None,
        spheres=None,
        rotes=None,
    ):
        self.update_status("Sub")
        self.random_rank(rank)
        self.background_cost = 2 * self.rank
        self.quintessence_max = 5 * self.rank
        self.random_is_primer(is_primer)
        self.random_faction(faction)
        self.random_medium(medium)
        self.random_material(cover_material)
        self.random_material(inner_material)
        self.random_length(length)
        self.random_focus(practices, instruments)
        self.random_date_written(date_written)
        self.random_abilities(abilities)
        self.random_language(language)
        self.random_spheres(spheres)
        self.random_rotes(rotes)
        self.random_name()
        self.save()
