from django.db import models

from characters.models.werewolf.gift import Gift, GiftPermission, gifts_by_rank
from characters.models.werewolf.rite import Rite
from characters.models.werewolf.wtahuman import WtAHuman
from core.utils import add_dot
from items.models.werewolf.fetish import Fetish


class Fera(WtAHuman):
    """
    Base class for all Changing Breeds (Fera).
    Fera are shapeshifters other than Garou, each with unique cultures,
    abilities, and relationships to Gaia.
    """

    type = "fera"

    # Character creation declarations; each Changing Breed overrides these.
    # chargen_choice_fields: fields chosen on the breed/faction step, in the
    # order their set_<field>() side effects apply.
    chargen_choice_fields = ("breed", "faction")
    optional_choice_fields = ()
    chargen_help_text = {}
    # (context key, field) pairs: rank-1 gifts permitted by the field's value.
    gift_group_fields = ()
    # (context key, condition) pairs: rank-1 gift lists every member may use.
    fixed_gift_groups = ()
    starting_gifts_help_text = "Choose 3 starting Gifts from your breed and faction/aspect/tribe."

    # Fera breed - varies by type
    breed = models.CharField(default="", max_length=100, blank=True)

    # Most Fera have some form of tribal/aspect system
    faction = models.CharField(default="", max_length=100, blank=True)

    # Fera use Rage, Gnosis, and Willpower like Garou
    gnosis = models.IntegerField(default=0)
    rage = models.IntegerField(default=0)

    # Most Fera have some form of renown, though it may differ from Garou
    renown = models.IntegerField(default=0)
    temporary_renown = models.IntegerField(default=0)

    # Gifts and supernatural abilities
    gifts = models.ManyToManyField(Gift, blank=True)
    rites_known = models.ManyToManyField(Rite, blank=True)
    fetishes_owned = models.ManyToManyField(Fetish, blank=True)

    # Story information
    first_change = models.TextField(default="", blank=True)
    age_of_first_change = models.IntegerField(default=0)

    gift_permissions = models.ManyToManyField(GiftPermission, blank=True)

    class Meta:
        verbose_name = "Fera"
        verbose_name_plural = "Fera"

    def chargen_field_help(self):
        return {"breed": "Choose your breed (birth form).", **self.chargen_help_text}

    def apply_chargen_choices(self, changed_fields):
        """Run the breed/faction setters for changed choices, in declared order.

        Setters grant gift permissions and starting Rage/Gnosis. Fields without a
        ``set_<field>`` keep the value the form already assigned.
        """
        for field in self.chargen_choice_fields:
            setter = getattr(self, f"set_{field}", None)
            if field in changed_fields and setter is not None:
                setter(getattr(self, field))

    def starting_gift_groups(self):
        """Rank-1 gift lists for the gifts step, keyed by template context name."""
        groups = {}
        conditions = [("breed_gifts", self.breed)] if self.breed else []
        conditions += list(self.fixed_gift_groups)
        conditions += [
            (key, getattr(self, field))
            for key, field in self.gift_group_fields
            if getattr(self, field)
        ]
        for key, condition in conditions:
            permission = GiftPermission.objects.filter(
                shifter=self.type, condition=condition
            ).first()
            if permission:
                groups[key] = Gift.objects.filter(rank=1, allowed=permission).order_by("name")
        return groups

    # Breed-specific renown traits (Bastet ferocity, Kitsune chie, ...), shown on the sheet.
    RENOWN_TRAITS = frozenset(
        {
            "glory", "honor", "wisdom", "ferocity", "cunning", "obligation", "obedience",
            "curiosity", "succor", "vision", "chie", "toku", "kagayaki", "valor",
            "harmony", "subtlety", "humor", "infamy", "innovation",
        }
    )  # fmt: skip

    def choice_display(self, field):
        """Display label for a breed/faction-style choice field (choices or title case)."""
        value = getattr(self, field, "") or ""
        if not value:
            return ""
        choices = dict(self._meta.get_field(field).choices or ())
        if field == "breed":
            choices = dict(getattr(self, "BREEDS", ())) or choices
        return choices.get(value, str(value).replace("_", " ").title())

    def sheet_choices(self):
        """(label, value) for the breed/faction step choices, for the sheet cover."""
        rows = []
        for field in self.chargen_choice_fields:
            value = self.choice_display(field)
            if value:
                label = str(self._meta.get_field(field).verbose_name).title()
                rows.append((label, value))
        return rows

    def gifts_by_rank(self):
        """Gifts grouped by rank, each labelled with the breed/faction choice it came from."""
        sources = {getattr(self, f): self.choice_display(f) for f in self.chargen_choice_fields}
        sources = {cond: label for cond, label in sources.items() if cond}
        return gifts_by_rank(self.gifts.all(), sources, self.type)

    def renown_tracks(self):
        """(label, permanent, temporary) for the sheet's Renown section: the breed's own
        renown traits (permanent only), plus the generic Renown pool when used."""
        tracks = [
            (str(f.verbose_name).title(), getattr(self, f.name), None)
            for f in type(self)._meta.local_concrete_fields
            if f.name in self.RENOWN_TRAITS
        ]
        if not tracks or self.renown or self.temporary_renown:
            tracks.append(("Renown", self.renown, self.temporary_renown))
        return tracks

    def starting_gift_choices(self):
        return Gift.objects.filter(rank=1, allowed__in=self.gift_permissions.all())

    def add_gift(self, gift):
        if gift in self.gifts.all():
            return False
        self.gifts.add(gift)
        self.save()
        return True

    def filter_gifts(self):
        return Gift.objects.filter(allowed__in=self.gift_permissions.all()).exclude(
            pk__in=self.gifts.all()
        )

    def add_rite(self, rite):
        self.rites_known.add(rite)
        self.save()
        return True

    def filter_rites(self):
        return Rite.objects.exclude(pk__in=self.rites_known.all())

    def add_gnosis(self):
        return add_dot(self, "gnosis", 10)

    def set_gnosis(self, gnosis):
        self.gnosis = gnosis
        self.save()
        return True

    def add_rage(self):
        return add_dot(self, "rage", 10)

    def set_rage(self, rage):
        self.rage = rage
        self.save()
        return True

    def add_fetish(self, fetish):
        if fetish in self.fetishes_owned.all():
            return False
        self.fetishes_owned.add(fetish)
        return True

    def has_breed(self):
        return self.breed != ""

    def has_faction(self):
        return self.faction != ""

    def filter_fetishes(self, min_rating=0, max_rating=5):
        return Fetish.objects.filter(rank__lte=max_rating, rank__gte=min_rating).exclude(
            pk__in=self.fetishes_owned.all()
        )

    def total_fetish_rating(self):
        return sum(x.rank for x in self.fetishes_owned.all())
