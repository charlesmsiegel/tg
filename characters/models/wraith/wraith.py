from characters.models.wraith.arcanos import Arcanos
from characters.models.wraith.faction import WraithFaction
from characters.models.wraith.guild import Guild
from characters.models.wraith.shadow_archetype import ShadowArchetype
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wtohuman import WtOHuman
from core.utils import add_dot
from django.db import models
from django.db.models import Q, CheckConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


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
    thorns = models.ManyToManyField(Thorn, blank=True, through="ThornRating")

    # Catharsis and Harrowing Tracking
    in_catharsis = models.BooleanField(default=False)
    catharsis_count = models.IntegerField(default=0)
    harrowing_count = models.IntegerField(default=0)
    last_harrowing_result = models.CharField(
        max_length=20,
        choices=[
            ("none", "None"),
            ("success", "Success"),
            ("failure", "Failure"),
            ("catharsis", "Catharsis"),
        ],
        default="none",
    )

    # Spectre Transition
    is_shadow_dominant = models.BooleanField(default=False)
    spectrehood_date = models.DateTimeField(null=True, blank=True)
    redemption_attempts = models.IntegerField(default=0)

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

    def get_absolute_url(self):
        return reverse("characters:wraith:wraith", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:wraith:update:wraith", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:wraith:create:wraith")

    def get_heading(self):
        return "wto_heading"

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
        tr, _ = ThornRating.objects.get_or_create(thorn=thorn, wraith=self)
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

    # Catharsis and Harrowing Mechanics

    def check_catharsis_trigger(self):
        """
        Check if Catharsis should trigger.
        Catharsis triggers when Shadow's temporary Angst exceeds Psyche's permanent Willpower.
        """
        return self.angst > self.willpower

    def trigger_catharsis(self):
        """
        Trigger a Catharsis event where Shadow takes temporary control.
        Returns True if successfully triggered.
        """
        if not self.check_catharsis_trigger():
            return False

        self.in_catharsis = True
        self.catharsis_count += 1
        self.is_shadow_dominant = True
        self.save()
        return True

    def resolve_catharsis(self, shadow_won=False):
        """
        Resolve a Catharsis event.
        shadow_won: True if Shadow maintained control, False if Psyche regained it.
        """
        self.in_catharsis = False
        if not shadow_won:
            self.is_shadow_dominant = False
        self.save()
        return True

    def check_harrowing_trigger(self):
        """
        Check if Harrowing should trigger.
        Triggers on:
        - Loss of all Willpower
        - Loss of a Fetter
        - Corpus reduced to 0
        - Angst reaches 10 (permanent Spectrehood threshold)
        """
        from characters.models.wraith.fetter import Fetter

        triggers = []

        # Check Willpower
        if self.willpower == 0:
            triggers.append("zero_willpower")

        # Check Corpus
        if self.corpus <= 0:
            triggers.append("zero_corpus")

        # Check for lost Fetters (this would need to be tracked separately)
        if Fetter.objects.filter(wraith=self).count() == 0:
            triggers.append("no_fetters")

        # Check permanent Angst
        if self.angst_permanent >= 10:
            triggers.append("max_angst")

        return triggers

    def trigger_harrowing(self, trigger_type="unknown"):
        """
        Trigger a Harrowing - the Psyche enters the Labyrinth to face the Shadow.
        This is a contested roll between Psyche and Shadow.
        """
        self.harrowing_count += 1
        self.save()
        return {
            "count": self.harrowing_count,
            "trigger": trigger_type,
            "message": f"Harrowing #{self.harrowing_count} triggered due to: {trigger_type}",
        }

    def resolve_harrowing(self, result="success"):
        """
        Resolve a Harrowing.
        result: 'success' (Psyche wins), 'failure' (becomes Spectre), or 'catharsis' (extraordinary success)
        """
        self.last_harrowing_result = result

        if result == "failure":
            # Psyche loses to Shadow - becomes Spectre
            return self.become_spectre()
        elif result == "catharsis":
            # Extraordinary success - reduce Angst
            self.angst_permanent = max(0, self.angst_permanent - 1)
            self.angst = max(0, self.angst - 3)
        # Success - just survive

        self.save()
        return True

    def become_spectre(self):
        """
        Transform a Wraith into a Spectre.
        Shadow becomes dominant, Psyche is suppressed.
        Changes character type and converts Passions to Dark Passions.
        """
        from characters.models.wraith.passion import Passion
        from django.utils import timezone

        if self.character_type == "spectre":
            return False  # Already a Spectre

        # Change character type
        self.character_type = "spectre"
        self.is_shadow_dominant = True
        self.spectrehood_date = timezone.now()

        # Convert all normal Passions to Dark Passions
        passions = Passion.objects.filter(wraith=self, is_dark_passion=False)
        for passion in passions:
            passion.is_dark_passion = True
            passion.save()

        # Reduce connection to Fetters (optional - makes them weaker)
        from characters.models.wraith.fetter import Fetter
        fetters = Fetter.objects.filter(wraith=self)
        for fetter in fetters:
            fetter.rating = max(1, fetter.rating // 2)  # Halve fetter strength
            fetter.save()

        # Shadow gains any Eidolon background points
        if self.eidolon > 0:
            self.angst_permanent = min(10, self.angst_permanent + self.eidolon)
            self.eidolon = 0

        self.save()
        return True

    def attempt_redemption(self):
        """
        Attempt to redeem a Spectre back to Wraith status.
        This is a difficult process requiring intervention (Pardoners, Darksiders, etc.)
        Returns success/failure and requirements.
        """
        if self.character_type != "spectre":
            return {
                "success": False,
                "message": "Character is not a Spectre - redemption not needed",
            }

        self.redemption_attempts += 1

        # Requirements for redemption (these would be checked externally):
        # - Must have at least 1 remaining Fetter
        # - Angst must be reduced below 10
        # - Requires Castigate Arcanos or Pardoner assistance
        # - Willpower contest between restored Psyche and Shadow

        from characters.models.wraith.fetter import Fetter

        fetters = Fetter.objects.filter(wraith=self).count()
        can_attempt = fetters > 0 and self.angst_permanent < 10

        if not can_attempt:
            return {
                "success": False,
                "message": f"Redemption requirements not met. Fetters: {fetters}, Permanent Angst: {self.angst_permanent}",
                "requirements": {
                    "fetters": "At least 1 Fetter required",
                    "angst": "Permanent Angst must be below 10",
                    "assistance": "Pardoner or Darksider assistance required",
                },
            }

        return {
            "success": True,
            "can_attempt": True,
            "message": "Redemption requirements met - ready for contested roll",
            "roll_info": {
                "psyche_pool": f"Willpower ({self.willpower}) + Eidolon (if any)",
                "shadow_pool": f"Permanent Angst ({self.angst_permanent})",
                "difficulty": 6,
            },
        }

    def complete_redemption(self, psyche_successes, shadow_successes):
        """
        Complete a redemption attempt based on contested rolls.
        psyche_successes: Number of successes on Psyche's roll
        shadow_successes: Number of successes on Shadow's roll
        """
        from characters.models.wraith.passion import Passion
        from django.utils import timezone

        if psyche_successes > shadow_successes:
            # Redemption successful - Psyche regains control
            self.character_type = "wraith"
            self.is_shadow_dominant = False

            # Convert Dark Passions back to normal (some may remain dark)
            dark_passions = Passion.objects.filter(wraith=self, is_dark_passion=True)
            redeemed_count = max(1, psyche_successes - shadow_successes)
            for i, passion in enumerate(dark_passions[:redeemed_count]):
                passion.is_dark_passion = False
                passion.save()

            # Reduce Angst
            self.angst_permanent = max(0, self.angst_permanent - (psyche_successes - shadow_successes))
            self.angst = max(0, self.angst - (psyche_successes - shadow_successes) * 2)

            self.save()
            return {
                "success": True,
                "message": f"Redemption successful! Psyche regained control. {redeemed_count} Passion(s) redeemed.",
                "passions_redeemed": redeemed_count,
                "angst_reduced": psyche_successes - shadow_successes,
            }
        else:
            # Redemption failed - remains Spectre
            return {
                "success": False,
                "message": "Redemption failed. Shadow maintained control.",
                "consequence": "Shadow grows stronger from the failed attempt",
            }

    def get_catharsis_info(self):
        """Return information about current Catharsis state."""
        return {
            "in_catharsis": self.in_catharsis,
            "catharsis_count": self.catharsis_count,
            "can_trigger": self.check_catharsis_trigger(),
            "shadow_dominant": self.is_shadow_dominant,
            "angst": self.angst,
            "willpower": self.willpower,
        }

    def get_harrowing_info(self):
        """Return information about Harrowing status and triggers."""
        triggers = self.check_harrowing_trigger()
        return {
            "harrowing_count": self.harrowing_count,
            "last_result": self.last_harrowing_result,
            "active_triggers": triggers,
            "at_risk": len(triggers) > 0,
            "angst_permanent": self.angst_permanent,
            "corpus": self.corpus,
            "willpower": self.willpower,
        }

    def xp_cost(self, trait_type, trait_value=None):
        """Return XP cost for wraith-specific traits."""
        from collections import defaultdict

        costs = defaultdict(
            lambda: super().xp_cost(trait_type, trait_value) if trait_value is not None else 10000,
            {
                "arcanos": 10,
                "pathos": 2,
                "corpus": 1,
                "angst": 1,
            },
        )

        if trait_type in ["arcanos", "pathos", "corpus", "angst"]:
            if trait_value is not None:
                return costs[trait_type] * trait_value
            return costs[trait_type]

        return costs[trait_type]

    def spend_xp(self, trait):
        """Spend XP on a trait."""
        output = super().spend_xp(trait)
        if output in [True, False]:
            return output

        # Check if trait is an arcanos
        arcanoi_list = list(self.get_arcanoi().keys()) + list(self.get_dark_arcanoi().keys())

        if trait in arcanoi_list:
            current_value = getattr(self, trait)
            cost = self.xp_cost("arcanos", current_value + 1)

            if cost <= self.xp:
                if self.add_arcanos(trait):
                    self.xp -= cost
                    self.add_to_spend(trait, getattr(self, trait), cost)
                    return True
                return False
            return False

        # Handle pathos
        if trait == "pathos_permanent" or trait == "pathos":
            cost = self.xp_cost("pathos", self.pathos_permanent + 1)
            if cost <= self.xp:
                if self.add_pathos():
                    self.xp -= cost
                    self.pathos = self.pathos_permanent
                    self.add_to_spend(trait, self.pathos_permanent, cost)
                    return True
                return False
            return False

        # Handle corpus
        if trait == "corpus":
            cost = self.xp_cost("corpus", self.corpus + 1)
            if cost <= self.xp:
                if self.add_corpus():
                    self.xp -= cost
                    self.add_to_spend(trait, self.corpus, cost)
                    return True
                return False
            return False

        # Handle angst
        if trait == "angst_permanent" or trait == "angst":
            cost = self.xp_cost("angst", self.angst_permanent + 1)
            if cost <= self.xp:
                if self.add_angst():
                    self.xp -= cost
                    self.angst = self.angst_permanent
                    self.add_to_spend(trait, self.angst_permanent, cost)
                    return True
                return False
            return False

        return trait

    def freebie_cost(self, trait_type):
        """Return freebie cost for wraith-specific traits."""
        wraith_costs = {
            "arcanos": 7,
            "pathos": 1,
            "passion": 2,
            "fetter": 1,
            "corpus": 1,
        }
        if trait_type in wraith_costs.keys():
            return wraith_costs[trait_type]
        return super().freebie_cost(trait_type)

    def spend_freebies(self, trait):
        """Spend freebie points on a trait."""
        output = super().spend_freebies(trait)
        if output in [True, False]:
            return output

        # Check if trait is an arcanos
        arcanoi_list = list(self.get_arcanoi().keys()) + list(self.get_dark_arcanoi().keys())

        if trait in arcanoi_list:
            cost = self.freebie_cost("arcanos")
            if cost <= self.freebies:
                if self.add_arcanos(trait):
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle pathos
        if trait == "pathos_permanent" or trait == "pathos":
            cost = self.freebie_cost("pathos")
            if cost <= self.freebies:
                if self.add_pathos():
                    self.freebies -= cost
                    self.pathos = self.pathos_permanent
                    return True
                return False
            return False

        # Handle corpus
        if trait == "corpus":
            cost = self.freebie_cost("corpus")
            if cost <= self.freebies:
                if self.add_corpus():
                    self.freebies -= cost
                    return True
                return False
            return False

        # Handle passion (would need Passion object)
        if trait == "passion":
            return trait

        # Handle fetter (would need Fetter object)
        if trait == "fetter":
            return trait

        return trait

    # Freebie spending methods

    def arcanos_freebies(self, form):
        """Spend freebies to increase an arcanos."""
        arcanos_name = form.cleaned_data["example"]
        cost = 7
        value = getattr(self, arcanos_name, 0) + 1

        # Add the arcanos
        self.add_arcanos(arcanos_name)
        self.freebies -= cost

        # Record the spend
        self.spent_freebies.append(
            self.freebie_spend_record(
                arcanos_name.replace("_", " ").title(), arcanos_name, value, cost
            )
        )
        return True

    def pathos_freebies(self, form):
        """Spend freebies to increase permanent pathos."""
        trait = "Pathos"
        cost = 1
        value = self.pathos_permanent + 1

        # Add pathos
        self.add_pathos()
        self.freebies -= cost

        # Update current pathos to match permanent
        self.pathos = self.pathos_permanent

        # Record the spend
        self.spent_freebies.append(
            self.freebie_spend_record(trait, "pathos", value, cost)
        )
        return True

    def passion_freebies(self, form):
        """Spend freebies to add a new passion."""
        # Passions cost 2 freebies per dot
        cost = 2
        rating = 1  # New passions start at rating 1

        # This is handled via the passion form, so we just decrement freebies
        self.freebies -= cost

        # Record the spend
        self.spent_freebies.append(
            self.freebie_spend_record("New Passion", "passion", rating, cost)
        )
        return True

    def fetter_freebies(self, form):
        """Spend freebies to add a new fetter."""
        # Fetters cost 1 freebie per dot
        cost = 1
        rating = 1  # New fetters start at rating 1

        # This is handled via the fetter form, so we just decrement freebies
        self.freebies -= cost

        # Record the spend
        self.spent_freebies.append(
            self.freebie_spend_record("New Fetter", "fetter", rating, cost)
        )
        return True

    def corpus_freebies(self, form):
        """Spend freebies to increase corpus."""
        trait = "Corpus"
        cost = 1
        value = self.corpus + 1

        # Add corpus
        self.add_corpus()
        self.freebies -= cost

        # Record the spend
        self.spent_freebies.append(
            self.freebie_spend_record(trait, "corpus", value, cost)
        )
        return True


class ThornRating(models.Model):
    wraith = models.ForeignKey(Wraith, on_delete=models.CASCADE)
    thorn = models.ForeignKey(Thorn, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = "Thorn Rating"
        verbose_name_plural = "Thorn Ratings"
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name='characters_wraith_thornrating_rating_range',
                violation_error_message="Thorn rating must be between 0 and 10"
            ),
        ]

    def __str__(self):
        return f"{self.wraith.name}: {self.thorn.name} ({self.rating})"
