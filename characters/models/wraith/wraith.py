from characters.models.wraith.arcanos import Arcanos
from characters.models.wraith.faction import WraithFaction
from characters.models.wraith.guild import Guild
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wtohuman import WtOHuman
from core.utils import add_dot
from django.db import models


class Wraith(WtOHuman):
    type = "wraith"

    freebie_step = 7

    allowed_backgrounds = [
        "contacts",
        "mentor",
        "allies",
        "artifact",
        "eidolon",
        "haunt",
        "legacy",
        "memoriam",
        "notoriety",
        "relic",
        "status_background",
    ]

    # Guild and Faction
    guild = models.ForeignKey(
        Guild,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )
    legion = models.ForeignKey(
        WraithFaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="legion_members",
    )
    faction = models.ForeignKey(
        WraithFaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faction_members",
    )

    # Core Wraith Stats
    corpus = models.IntegerField(default=10)
    pathos = models.IntegerField(default=5)
    pathos_permanent = models.IntegerField(default=5)

    # Shadow Stats
    angst = models.IntegerField(default=0)
    angst_permanent = models.IntegerField(default=0)

    # Arcanoi (Standard - 13 Greater Guilds)
    argos = models.IntegerField(default=0)
    castigate = models.IntegerField(default=0)
    embody = models.IntegerField(default=0)
    fatalism = models.IntegerField(default=0)
    flux = models.IntegerField(default=0)
    inhabit = models.IntegerField(default=0)
    keening = models.IntegerField(default=0)
    lifeweb = models.IntegerField(default=0)
    moliate = models.IntegerField(default=0)
    mnemosynis = models.IntegerField(default=0)
    outrage = models.IntegerField(default=0)
    pandemonium = models.IntegerField(default=0)
    phantasm = models.IntegerField(default=0)
    usury = models.IntegerField(default=0)
    intimation = models.IntegerField(default=0)  # Banned

    # Dark Arcanoi (for Spectres)
    blighted_insight = models.IntegerField(default=0)
    collogue = models.IntegerField(default=0)
    corruptor = models.IntegerField(default=0)
    false_life = models.IntegerField(default=0)
    tempestos = models.IntegerField(default=0)
    osseum = models.IntegerField(default=0)
    connaissance = models.IntegerField(default=0)

    # Character Type
    CHARACTER_TYPE_CHOICES = [
        ("wraith", "Wraith"),
        ("spectre", "Spectre"),
        ("doppelganger", "Doppelganger"),
        ("chosen", "Chosen"),
        ("dark_spirit", "Dark Spirit"),
        ("risen", "Risen"),
    ]

    character_type = models.CharField(
        max_length=20, choices=CHARACTER_TYPE_CHOICES, default="wraith"
    )

    # Shadow
    shadow_archetype = models.ForeignKey(
        ShadowArchetype,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wraiths",
    )
    thorns = models.ManyToManyField(Thorn, blank=True, through="ThoronRating")

    # History
    death_description = models.TextField(default="")
    age_at_death = models.IntegerField(default=0)

    background_points = 7
    passion_points = 10
    fetter_points = 10

    class Meta:
        verbose_name = "Wraith"
        verbose_name_plural = "Wraiths"
        ordering = ["name"]

    def has_guild(self):
        return self.guild is not None

    def set_guild(self, guild):
        self.guild = guild
        if guild:
            self.willpower = guild.willpower
        self.save()
        return True

    def has_legion(self):
        return self.legion is not None

    def set_legion(self, legion):
        self.legion = legion
        self.save()
        return True

    def has_faction(self):
        return self.faction is not None

    def set_faction(self, faction):
        self.faction = faction
        self.save()
        return True

    def get_arcanoi(self):
        return {
            "argos": self.argos,
            "castigate": self.castigate,
            "embody": self.embody,
            "fatalism": self.fatalism,
            "flux": self.flux,
            "inhabit": self.inhabit,
            "keening": self.keening,
            "lifeweb": self.lifeweb,
            "moliate": self.moliate,
            "mnemosynis": self.mnemosynis,
            "outrage": self.outrage,
            "pandemonium": self.pandemonium,
            "phantasm": self.phantasm,
            "usury": self.usury,
            "intimation": self.intimation,
        }

    def get_dark_arcanoi(self):
        return {
            "blighted_insight": self.blighted_insight,
            "collogue": self.collogue,
            "corruptor": self.corruptor,
            "false_life": self.false_life,
            "tempestos": self.tempestos,
            "osseum": self.osseum,
            "connaissance": self.connaissance,
        }

    def total_arcanoi(self):
        return sum(self.get_arcanoi().values())

    def total_dark_arcanoi(self):
        return sum(self.get_dark_arcanoi().values())

    def add_arcanos(self, arcanos):
        return add_dot(self, arcanos, 5)

    def filter_arcanoi(self, minimum=0, maximum=5):
        return {k: v for k, v in self.get_arcanoi().items() if minimum <= v <= maximum}

    def has_arcanoi(self):
        return self.total_arcanoi() == 5

    def add_passion(self, emotion, description, rating=1, is_dark=False):
        from characters.models.wraith.passion import Passion
        passion = Passion.objects.create(
            wraith=self,
            emotion=emotion,
            description=description,
            rating=rating,
            is_dark_passion=is_dark,
        )
        return True

    def total_passion_rating(self):
        from characters.models.wraith.passion import Passion
        return sum(p.rating for p in Passion.objects.filter(wraith=self))

    def has_passions(self):
        return self.total_passion_rating() == self.passion_points

    def add_fetter(self, fetter_type, description, rating=1):
        from characters.models.wraith.fetter import Fetter
        fetter = Fetter.objects.create(
            wraith=self,
            fetter_type=fetter_type,
            description=description,
            rating=rating,
        )
        return True

    def total_fetter_rating(self):
        from characters.models.wraith.fetter import Fetter
        return sum(f.rating for f in Fetter.objects.filter(wraith=self))

    def has_fetters(self):
        return self.total_fetter_rating() == self.fetter_points

    def add_thorn(self, thorn):
        tr, _ = ThoronRating.objects.get_or_create(thorn=thorn, wraith=self)
        if tr.rating == 0:
            tr.rating = 1
            tr.save()
            return True
        return False

    def has_shadow(self):
        return self.shadow_archetype is not None

    def set_shadow_archetype(self, archetype):
        self.shadow_archetype = archetype
        self.save()
        return True

    def add_corpus(self):
        return add_dot(self, "corpus", 10)

    def add_pathos(self):
        return add_dot(self, "pathos_permanent", 10)

    def add_angst(self):
        return add_dot(self, "angst_permanent", 10)

    def has_wraith_history(self):
        return self.death_description != "" and self.age_at_death != 0

    def xp_frequencies(self):
        return {
            "attribute": 16,
            "ability": 20,
            "background": 13,
            "willpower": 1,
            "arcanos": 37,
            "pathos": 2,
        }

    def freebie_frequencies(self):
        return {
            "attribute": 15,
            "ability": 8,
            "background": 10,
            "willpower": 1,
            "meritflaw": 20,
            "arcanos": 25,
            "pathos": 5,
            "passion": 5,
            "fetter": 5,
            "corpus": 5,
        }

    def freebie_costs(self):
        costs = super().freebie_costs()
        costs.update(
            {
                "arcanos": 7,
                "pathos": 1,
                "passion": 2,
                "fetter": 1,
                "corpus": 1,
            }
        )
        return costs


class ThoronRating(models.Model):
    wraith = models.ForeignKey(Wraith, on_delete=models.CASCADE)
    thorn = models.ForeignKey(Thorn, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Thorn Rating"
        verbose_name_plural = "Thorn Ratings"

    def __str__(self):
        return f"{self.wraith.name}: {self.thorn.name} ({self.rating})"
