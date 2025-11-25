"""
Merit and Flaw Manager for Character models.

Extracts merit/flaw management logic from MeritFlawBlock mixin to
implement composition over inheritance.
"""

from django.db.models import F, Q, Sum


class MeritFlawManager:
    """
    Manages merit and flaw operations for a character.

    This manager encapsulates all merit/flaw-related business logic,
    allowing the Human model to use composition instead of inheriting
    from MeritFlawBlock.

    Usage:
        character.merit_flaw_manager.add_mf(merit, rating)
        character.merit_flaw_manager.total_merits()
    """

    def __init__(self, character):
        """
        Initialize manager with a character instance.

        Args:
            character: A character model instance (Human or subclass)
        """
        self.character = character

    def num_languages(self):
        """
        Calculate number of language merits.

        Takes into account the "Natural Linguist" merit which doubles
        the effective rating of the "Language" merit.

        Returns:
            int: Number of languages the character knows
        """
        from characters.models.core.merit_flaw_block import MeritFlaw

        mf_list = self.character.merits_and_flaws.all().values_list("name", flat=True)
        if "Language" not in mf_list:
            return 0
        language_rating = self.mf_rating(MeritFlaw.objects.get(name="Language"))
        if "Natural Linguist" in mf_list:
            language_rating *= 2
        return language_rating

    def get_mf_and_rating_list(self):
        """
        Get list of all merits/flaws with their ratings.

        Returns:
            list: List of tuples (MeritFlaw instance, rating)
        """
        return [
            (x, self.mf_rating(x)) for x in self.character.merits_and_flaws.all()
        ]

    def add_mf(self, mf, rating):
        """
        Add a merit or flaw with specified rating to the character.

        Args:
            mf: MeritFlaw instance
            rating: Integer rating (positive for merits, negative for flaws)

        Returns:
            bool: True if successfully added, False if rating is invalid
        """
        from characters.models.core.merit_flaw_block import MeritFlawRating

        if rating in mf.get_ratings():
            mfr, _ = MeritFlawRating.objects.get_or_create(
                character=self.character, mf=mf
            )
            mfr.rating = rating
            mfr.save()
            return True
        return False

    def filter_mfs(self):
        """
        Filter available merits/flaws for this character.

        Returns merits and flaws that:
        - Haven't been taken yet, OR
        - Have been taken but not at maximum rating
        - Are allowed for this character type
        - Respects the maximum flaws limit (-7)

        Returns:
            QuerySet: Filtered MeritFlaw queryset
        """
        from characters.models.core.merit_flaw_block import (
            MeritFlaw,
            MeritFlawRating,
        )
        from game.models import ObjectType

        character_type = self.character.type
        if character_type in ["fomor"]:
            character_type = "human"

        # Get merits/flaws not yet taken
        new_mfs = MeritFlaw.objects.exclude(
            pk__in=self.character.merits_and_flaws.all()
        )

        # Get merits/flaws taken but not at max rating
        non_max_mf = MeritFlawRating.objects.filter(
            character=self.character
        ).exclude(Q(rating=F("mf__max_rating")))

        had_mfs = MeritFlaw.objects.filter(pk__in=non_max_mf)
        mf = new_mfs | had_mfs

        # If at max flaws, only show merits (positive ratings)
        if self.has_max_flaws():
            mf = mf.filter(max_rating__gt=0)

        # Filter by character type
        character_type_object = ObjectType.objects.get(name=character_type)
        return mf.filter(allowed_types=character_type_object)

    def mf_rating(self, mf):
        """
        Get rating for a specific merit/flaw on this character.

        Args:
            mf: MeritFlaw instance

        Returns:
            int: Rating value, or 0 if not taken
        """
        from characters.models.core.merit_flaw_block import MeritFlawRating

        try:
            return MeritFlawRating.objects.get(
                character=self.character, mf=mf
            ).rating
        except MeritFlawRating.DoesNotExist:
            return 0

    def has_max_flaws(self):
        """
        Check if character has reached maximum flaw limit.

        Returns:
            bool: True if total flaws <= -7
        """
        return self.total_flaws() <= -7

    def total_flaws(self):
        """
        Calculate total flaw points (negative ratings).

        Returns:
            int: Sum of all negative merit/flaw ratings
        """
        from characters.models.core.merit_flaw_block import MeritFlawRating

        result = MeritFlawRating.objects.filter(
            character=self.character, rating__lt=0
        ).aggregate(Sum("rating"))
        return result["rating__sum"] or 0

    def total_merits(self):
        """
        Calculate total merit points (positive ratings).

        Returns:
            int: Sum of all positive merit/flaw ratings
        """
        from characters.models.core.merit_flaw_block import MeritFlawRating

        result = MeritFlawRating.objects.filter(
            character=self.character, rating__gt=0
        ).aggregate(Sum("rating"))
        return result["rating__sum"] or 0

    def meritflaw_freebies(self, form):
        """
        Spend freebie points on a merit or flaw.

        Args:
            form: Django form with cleaned_data containing merit/flaw info

        Returns:
            tuple: (trait_name, value, cost)
        """
        trait = form.cleaned_data["example"]
        value = int(form.data["value"])
        cost = value
        self.add_mf(trait, value)
        self.character.freebies -= cost
        trait = trait.name
        return trait, value, cost
