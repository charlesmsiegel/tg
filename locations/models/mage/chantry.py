from django.db import models
from django.db.models import CheckConstraint, Q

from characters.models.core.background_block import BackgroundBlock
from characters.models.core.character import CharacterModel
from characters.models.core.human import Human
from characters.models.mage.effect import Effect
from core.models import BaseBackgroundRating
from core.utils import CharacterOrganizationRegistry
from locations.models.core.location import LocationModel


class Chantry(BackgroundBlock, LocationModel):
    allowed_backgrounds = [
        "allies",
        "arcane",
        "backup",
        "cult",
        "elders",
        "retainers",
        "spies",
        "resources",
        "enhancement",
        "requisitions",
        "sanctum",
        "node",
        "library",
    ]

    INTEGRATED_EFFECTS_NUMBERS = {
        0: 0,
        1: 4,
        2: 8,
        3: 15,
        4: 20,
        5: 25,
        6: 35,
        7: 45,
        8: 55,
        9: 70,
        10: 90,
    }

    LIBRARY_TYPE_FREE_DOTS = 3

    type = "chantry"
    gameline = "mta"

    faction = models.ForeignKey(
        "characters.MageFaction", blank=True, null=True, on_delete=models.SET_NULL
    )

    LEADERSHIP_CHOICES = [
        ("panel", "Panel of Cabal Leaders"),
        ("teachers", "Teachers"),
        ("triumvirate", "Triumvirate"),
        ("democracy", "Democracy"),
        ("anarchy", "Anarchy"),
        ("single_deacon", "Single Deacon"),
        ("council_of_elders", "Council of Elders"),
        ("meritocracy", "Meritocracy"),
    ]

    leadership_type = models.CharField(
        max_length=20, null=True, blank=True, choices=LEADERSHIP_CHOICES
    )
    leaders = models.ManyToManyField(Human, blank=True, related_name="chantry_leader_at")

    SEASONS = [
        ("spring", "Spring"),
        ("winter", "Winter"),
        ("summer", "Summer"),
        ("autumn", "Autumn"),
    ]

    season = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=SEASONS,
    )

    CHANTRY_TYPES = [
        ("exploration", "Exploration"),
        ("ancestral", "Ancestral"),
        ("hereditary", "Hereditary"),
        ("college", "College"),
        ("squatter", "Squatter"),
        ("war", "War"),
        ("library", "Library"),
        ("healing", "Healing"),
        ("research", "Research"),
        ("fortress", "Fortress"),
        ("diplomatic", "Diplomatic"),
    ]

    chantry_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=CHANTRY_TYPES,
    )

    total_points = models.IntegerField(default=0)

    integrated_effects = models.ManyToManyField(Effect, blank=True)
    integrated_effects_score = models.IntegerField(default=0)

    # Chantry-specific resources
    nodes = models.ManyToManyField("locations.Node", blank=True, related_name="chantry_nodes")
    chantry_library = models.ForeignKey(
        "locations.Library",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="chantry",
    )

    members = models.ManyToManyField(Human, blank=True, related_name="member_of")
    cabals = models.ManyToManyField("characters.Cabal", blank=True)

    ambassador = models.ForeignKey(
        Human,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="ambassador_from",
    )
    node_tender = models.ForeignKey(
        Human,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="tends_node_at",
    )
    investigator = models.ManyToManyField(Human, blank=True, related_name="investigator_at")
    guardian = models.ManyToManyField(Human, blank=True, related_name="guardian_of")
    teacher = models.ManyToManyField(Human, blank=True, related_name="teacher_at")

    factional_names = {
        "Akashayana": [
            "Monastery",
            "Torii",
            "Pagoda",
            "Bodhimandala",
            "Tao Chang",
            "Dojo",
            "Dojang",
            "Xiudaoyuan",
        ],
        "Celestial Chorus": ["Chapel", "Covenant", "Sanctuary", "Adytum", "Temple"],
        "Cult of Ecstasy": ["Pleasuredome"],
        "Dreamspeakers": ["Lodge"],
        "Euthanatos": ["Marabout"],
        "Order of Hermes": ["Covenant", "Chantry"],
        "Hollow Ones": ["Hideout", "Hole", "Crashspace", "Haunt"],
        "Society of Ether": ["Laboratory"],
        "Verbena": ["Covenhouse", "Circle", "Great Hall"],
        "Virtual Adepts": ["Epicenter", "Fortress", "Net"],
        "Traditions": ["Chantry"],
        "Technocratic Union": ["Construct"],
        "Kopa Loei": ["He'iau"],
    }

    class Meta:
        verbose_name = "Chantry"
        verbose_name_plural = "Chantries"

    @property
    def points(self):
        return self.total_points - self.total_cost()

    def free_dots(self, property_name):
        """Dots of a background this chantry holds at no cost.

        A library-type chantry gets ``LIBRARY_TYPE_FREE_DOTS`` free Library dots,
        which also act as a floor that cannot be removed.
        """
        if property_name == "library" and self.chantry_type == "library":
            return self.LIBRARY_TYPE_FREE_DOTS
        return 0

    def bg_cost(self, background_rating):
        if background_rating.bg is None:
            return 0
        property_name = background_rating.bg.property_name
        paid_dots = max(0, background_rating.rating - self.free_dots(property_name))
        return self.trait_cost(property_name) * paid_dots

    def total_cost(self):
        tot = 0
        for bgr in self.backgrounds.select_related("bg"):
            tot += self.bg_cost(bgr)
        tot += self.integrated_effects_score * 2
        return tot

    def integrated_effects_number(self):
        return self.INTEGRATED_EFFECTS_NUMBERS[self.integrated_effects_score]

    def spent_integrated_effect_points(self):
        return sum([x.rote_cost for x in self.integrated_effects.all()])

    def current_ie_points(self):
        return self.integrated_effects_number() - self.spent_integrated_effect_points()

    @property
    def rank(self):
        if self.total_points < 11:
            return 1
        elif self.total_points < 21:
            return 2
        elif self.total_points < 31:
            return 3
        elif self.total_points < 71:
            return 4
        return 5

    def has_season(self):
        return self.season is not None

    def set_season(self, season):
        self.season = season
        self.save()
        return True

    def has_chantry_type(self):
        return self.chantry_type is not None

    def set_chantry_type(self, chantry_type):
        self.chantry_type = chantry_type
        if chantry_type == "library":
            self.library = 3
        self.save()
        return True

    def trait_cost(self, trait):
        if trait in [
            "allies",
            "arcane",
            "backup",
            "cult",
            "elders",
            "integrated_effects",
            "library",
            "retainers",
            "spies",
        ]:
            return 2
        if trait in ["node", "resources"]:
            return 3
        if trait in ["enhancement", "requisitions"]:
            return 4
        if trait in ["sanctum"]:
            return 5
        return 1000

    def points_spent(self):
        return (
            2
            * (
                self.allies
                + self.arcane
                + self.backup
                + self.cult
                + self.elders
                + self.integrated_effects
                + self.library
                + self.retainers
                + self.spies
            )
            + 3 * (self.node + self.resources)
            + 4 * (self.enhancement + self.requisitions)
            + 5 * (self.sanctum)
        )

    def has_node(self):
        return self.total_node() == self.node

    def add_node(self, node):
        self.nodes.add(node)
        self.save()

    def total_node(self):
        return sum(x.rank for x in self.nodes.all())

    def has_library(self):
        if self.chantry_library is not None:
            return self.chantry_library.rank == self.chantry_library.num_books()
        return False

    def set_library(self, library):
        self.chantry_library = library
        library.contained_within.add(self)
        return True

    def set_rank(self, rank):
        self.rank = rank
        return True

    def get_traits(self):
        return {
            "allies": self.allies,
            "arcane": self.arcane,
            "backup": self.backup,
            "cult": self.cult,
            "elders": self.elders,
            "integrated_effects": self.integrated_effects,
            "retainers": self.retainers,
            "spies": self.spies,
            "resources": self.resources,
            "enhancement": self.enhancement,
            "requisitions": self.requisitions,
            "reality_zone": self.sanctum,
            "node": self.node,
            "library": self.library,
        }

    def set_faction(self, faction):
        self.faction = faction
        return True

    def has_faction(self):
        return self.faction is not None

    # Ratings for these backgrounds are finished by creating an object in wizard steps 3-6.
    WIZARD_RESOURCES = ("node", "library", "allies", "sanctum")
    FINAL_WIZARD_STEP = 6

    def submission_errors(self):
        """Reasons this chantry cannot be submitted yet; empty when it can."""
        from locations.services.chantry_points import (
            has_affordable_effect,
            has_affordable_purchase,
        )

        def plural(count, word):
            return f"{count} {word}{'' if count == 1 else 's'}"

        errors = []
        if self.creation_status <= self.FINAL_WIZARD_STEP:
            errors.append(
                f"Finish every creation step (the chantry is on step "
                f"{self.creation_status} of {self.FINAL_WIZARD_STEP})."
            )
        if self.points < 0:
            errors.append(f"{plural(-self.points, 'more point')} spent than the chantry has.")
        if has_affordable_purchase(self):
            errors.append(
                f"{plural(self.points, 'unspent point')} can still buy a background "
                "or Integrated Effects dot."
            )
        ie_points = self.current_ie_points()
        if ie_points < 0:
            errors.append(
                f"Integrated effects cost {plural(-ie_points, 'more point')} than the "
                "Integrated Effects score allows."
            )
        if has_affordable_effect(self):
            errors.append(
                f"{plural(ie_points, 'Integrated Effects point')} can still buy an effect."
            )
        for rating in self.backgrounds.select_related("bg"):
            name = rating.bg.name if rating.bg else "A deleted background"
            if rating.bg is None or rating.bg.property_name not in self.allowed_backgrounds:
                errors.append(f"{name} is not a chantry background.")
            elif not 1 <= rating.rating <= 5:
                errors.append(f"{name} must be rated 1 to 5.")
            if (
                rating.bg is not None
                and rating.bg.property_name in self.WIZARD_RESOURCES
                and not rating.complete
            ):
                errors.append(f"{name} has not been set up yet.")
        return errors

    def on_returned_for_revision(self):
        """ApprovalService hook: a returned chantry re-enters the wizard at step 1."""
        self.creation_status = 1
        return ["creation_status"]

    def get_independent_members(self):
        """Returns members who aren't part of any cabals in this chantry."""
        cabal_member_ids = set()
        for cabal in self.cabals.all():
            cabal_member_ids.update(cabal.members.values_list("id", flat=True))
        return self.members.exclude(id__in=cabal_member_ids)

    @staticmethod
    def cleanup_character_organizations(character):
        """Remove character from all Chantry organizational structures."""
        # Only process if character is a Human (or subclass) with Chantry relationships
        if not hasattr(character, "member_of"):
            return

        # Remove from Chantry memberships
        for chantry in character.member_of.all():
            chantry.members.remove(character)

        # Remove from Chantry leadership
        for chantry in character.chantry_leader_at.all():
            chantry.leaders.remove(character)

        # Remove from ambassador positions
        for chantry in character.ambassador_from.all():
            chantry.ambassador = None
            chantry.save()

        # Remove from node tender positions
        for chantry in character.tends_node_at.all():
            chantry.node_tender = None
            chantry.save()

        # Remove from investigator roles
        for chantry in character.investigator_at.all():
            chantry.investigator.remove(character)

        # Remove from guardian roles
        for chantry in character.guardian_of.all():
            chantry.guardian.remove(character)

        # Remove from teacher roles
        for chantry in character.teacher_at.all():
            chantry.teacher.remove(character)


class ChantryBackgroundRating(BaseBackgroundRating):
    """Background rating for a chantry."""

    chantry = models.ForeignKey(
        Chantry,
        on_delete=models.SET_NULL,
        null=True,
        related_name="backgrounds",
    )
    display_alt_name = models.BooleanField(default=False)

    # The object realised for this rating in the chantry wizard: a Node, Library
    # or Sanctum (a location) or an Allies NPC (a character). ``core.Model`` is
    # abstract, so one FK per polymorphic tree; use ``linked_object`` to read or
    # write. Columns added to legacy databases by tg_schema 0002.
    linked_location = models.ForeignKey(
        "locations.LocationModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    linked_character = models.ForeignKey(
        "characters.CharacterModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        ordering = ["bg__name"]
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=0, rating__lte=10),
                name="locations_chantrybackgroundrating_rating_range",
                violation_error_message="Chantry background rating must be between 0 and 10",
            ),
        ]

    @property
    def linked_object(self):
        """The concrete linked Node, Library, Sanctum or character, or None."""
        linked = self.linked_location or self.linked_character
        return linked.get_real_instance() if linked is not None else None

    @linked_object.setter
    def linked_object(self, obj):
        if obj is not None and not isinstance(obj, LocationModel | CharacterModel):
            raise TypeError(f"Cannot link {type(obj).__name__} to a chantry background")
        self.linked_location = obj if isinstance(obj, LocationModel) else None
        self.linked_character = obj if isinstance(obj, CharacterModel) else None

    def display_name(self):
        if self.bg.alternate_name == "":
            return self.bg.name
        elif self.display_alt_name:
            return self.bg.alternate_name
        return self.bg.name


# Register the cleanup handler with the registry
CharacterOrganizationRegistry.register(Chantry.cleanup_character_organizations)
