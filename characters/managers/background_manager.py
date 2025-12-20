"""
Background Manager for Character models.

Extracts background management logic from BackgroundBlock mixin to
implement composition over inheritance.
"""


class BackgroundManager:
    """
    Manages background operations for a character.

    This manager encapsulates all background-related business logic,
    allowing the Human model to use composition instead of inheriting
    from BackgroundBlock.

    Backgrounds in WoD are special - they're not direct fields on the character
    but are managed through the BackgroundRating model. This manager provides
    a clean interface to interact with backgrounds.

    Usage:
        character.background_manager.add_background('contacts')
        character.background_manager.total_backgrounds()
    """

    def __init__(self, character):
        """
        Initialize manager with a character instance.

        Args:
            character: A character model instance (Human or subclass)
        """
        self.character = character

    def total_background_rating(self, bg_name):
        """
        Get total rating for a specific background.

        Characters can have multiple instances of the same background
        (e.g., multiple Contacts with different specializations).

        Args:
            bg_name: Property name of the background (e.g., 'contacts')

        Returns:
            int: Sum of all ratings for this background type
        """
        from characters.models.core.background_block import BackgroundRating

        return sum(
            [
                x.rating
                for x in BackgroundRating.objects.filter(
                    bg__property_name=bg_name, char=self.character
                )
            ]
        )

    def get_backgrounds(self):
        """
        Get dictionary of all backgrounds and their total ratings.

        Returns:
            dict: {bg_name: total_rating} for all allowed backgrounds
        """
        return {bg: self.total_background_rating(bg) for bg in self.character.allowed_backgrounds}

    def add_background(self, background, maximum=5):
        """
        Add a dot to a background.

        This method handles both creating new background instances and
        increasing existing ones.

        Args:
            background: Either a string (property name), Background instance,
                       or BackgroundRating instance
            maximum: Maximum rating for a single background instance (default 5)

        Returns:
            bool: True if successfully added, False if at maximum
        """
        from characters.models.core.background_block import Background, BackgroundRating

        if isinstance(background, str):
            bg, _ = Background.objects.get_or_create(
                property_name=background,
                defaults={"name": background.replace("_", " ").title()},
            )
            ratings = BackgroundRating.objects.filter(char=self.character, bg=bg)
            if ratings.filter(rating__lt=5).count() > 0:
                background = ratings.filter(rating__lt=5).first()
            else:
                background = BackgroundRating.objects.create(char=self.character, bg=bg)
        elif isinstance(background, Background):
            ratings = BackgroundRating.objects.filter(char=self.character, bg=background)
            if ratings.filter(rating__lt=5).count() > 0:
                background = ratings.filter(rating__lt=5).first()
            else:
                background = BackgroundRating.objects.create(char=self.character, bg=background)
        else:
            raise ValueError(
                "Must be a background name, Background object, or BackgroundRating object"
            )

        if background.rating == 5:
            return False
        background.rating += 1
        background.save()
        return True

    def total_backgrounds(self):
        """
        Calculate total background points spent.

        Returns:
            int: Sum of all background ratings
        """
        return sum(self.get_backgrounds().values())

    def filter_backgrounds(self, minimum=0, maximum=5):
        """
        Filter backgrounds by rating range.

        Args:
            minimum: Minimum rating to include (default 0)
            maximum: Maximum rating to include (default 5)

        Returns:
            dict: Filtered {bg_name: rating} dictionary
        """
        return {k: v for k, v in self.get_backgrounds().items() if minimum <= v <= maximum}

    def has_backgrounds(self):
        """
        Check if character has enough backgrounds for creation.

        If character has spent more than their background_points allowance,
        the extra cost is deducted from freebie points.

        Returns:
            bool: True if character has at least background_points worth
        """
        if self.total_backgrounds() > self.character.background_points:
            self.character.freebies -= self.total_backgrounds() - self.character.background_points
        return self.total_backgrounds() >= self.character.background_points

    def new_background_freebies(self, form):
        """
        Spend freebie points on a new background.

        Args:
            form: Django form with cleaned_data containing background info

        Returns:
            tuple: (trait_name, value, cost)
        """
        from characters.models.core.background_block import (
            Background,
            BackgroundRating,
            PooledBackgroundRating,
        )

        trait = form.cleaned_data["example"]
        cost = trait.multiplier
        value = 1
        trait = Background.objects.get(pk=form.data["example"])

        if "pooled" in form.data.keys():
            pbgr = PooledBackgroundRating.objects.get_or_create(
                bg=trait, group=self.character.get_group(), note=form.data["note"]
            )[0]
            pbgr.rating += 1
            pbgr.save()
            BackgroundRating.objects.create(
                bg=trait,
                rating=1,
                char=self.character,
                note=form.data["note"],
                complete=True,
                pooled=True,
            )
        else:
            BackgroundRating.objects.create(
                bg=trait,
                rating=1,
                char=self.character,
                note=form.data["note"],
                pooled=False,
            )

        self.character.freebies -= cost
        trait = str(trait)
        if form.data["note"]:
            trait += f" ({form.data['note']})"
        return trait, value, cost

    def existing_background_freebies(self, form):
        """
        Spend freebie points to increase an existing background.

        Args:
            form: Django form with cleaned_data containing background info

        Returns:
            tuple: (trait_name, value, cost)
        """
        from characters.models.core.background_block import PooledBackgroundRating

        trait = form.cleaned_data["example"]
        cost = trait.bg.multiplier

        if trait.pooled:
            pbgr = PooledBackgroundRating.objects.get(
                bg=trait.bg, group=self.character.get_group(), note=trait.note
            )
            pbgr.rating += 1
            pbgr.save()

        value = trait.rating + 1
        trait.rating += 1
        trait.save()
        self.character.freebies -= cost
        trait = str(trait)
        return trait, value, cost

    def get_background_property(self, bg_name):
        """
        Get the total rating for a background (property-style access).

        This provides backward compatibility with the old dynamic property system.

        Args:
            bg_name: Property name of the background

        Returns:
            int: Total rating for this background
        """
        return self.total_background_rating(bg_name)

    def set_background_property(self, bg_name, value):
        """
        Set the rating for a background (property-style access).

        This provides backward compatibility with the old dynamic property system.
        If value is 0, deletes all background ratings. Otherwise, creates a new one.

        Args:
            bg_name: Property name of the background
            value: New rating value
        """
        from characters.models.core.background_block import Background, BackgroundRating

        if value != 0:
            bg, _ = Background.objects.get_or_create(
                property_name=bg_name,
                defaults={"name": bg_name.replace("_", " ").title()},
            )
            BackgroundRating.objects.create(
                char=self.character,
                bg=bg,
                rating=value,
            )
        else:
            BackgroundRating.objects.filter(char=self.character, bg__property_name=bg_name).delete()
