"""
Generic Rating Model - Consolidates 12+ similar rating classes into one.

This is a PROTOTYPE implementation. Do NOT use in production without:
1. Creating proper migrations
2. Migrating data from existing rating tables
3. Updating all code that references old rating classes
4. Thorough testing

See REFACTORING_ANALYSIS.md for full details.
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class GenericRating(models.Model):
    """
    Generic rating model that can relate any two models with a rating value.

    This replaces 12 similar rating classes:
    - WonderResonanceRating
    - NodeResonanceRating
    - ResRating (Mage)
    - NodeMeritFlawRating
    - MeritFlawRating
    - ChantryBackgroundRating
    - BackgroundRating
    - PooledBackgroundRating
    - PracticeRating
    - ZoneRating
    - PathRating (needs special handling)
    - AdvantageRating

    Usage:
        # Create a rating
        rating = GenericRating.create_rating(wonder, resonance, 3)

        # Get a rating
        value = GenericRating.get_rating(wonder, resonance)

        # Update a rating
        rating.rating = 5
        rating.save()
    """

    # The object being rated (e.g., Wonder, Node, Mage, Human)
    parent_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="ratings_as_parent",
    )
    parent_object_id = models.PositiveIntegerField()
    parent_object = GenericForeignKey("parent_content_type", "parent_object_id")

    # The rating subject (e.g., Resonance, MeritFlaw, Background)
    subject_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="ratings_as_subject",
    )
    subject_object_id = models.PositiveIntegerField()
    subject_object = GenericForeignKey("subject_content_type", "subject_object_id")

    # The rating value
    rating = models.IntegerField(default=0)

    # Optional fields for specific use cases
    display_alt_name = models.BooleanField(default=False)  # For BackgroundRating
    display_preference = models.CharField(
        max_length=100, blank=True
    )  # For BackgroundRating
    note = models.TextField(blank=True)  # General purpose notes

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        indexes = [
            models.Index(fields=["parent_content_type", "parent_object_id"]),
            models.Index(fields=["subject_content_type", "subject_object_id"]),
        ]
        # Ensure uniqueness of parent-subject pairs
        unique_together = [
            [
                "parent_content_type",
                "parent_object_id",
                "subject_content_type",
                "subject_object_id",
            ]
        ]

    def __str__(self):
        return f"{self.parent_object}: {self.subject_object} = {self.rating}"

    @classmethod
    def create_rating(cls, parent, subject, rating_value, **kwargs):
        """
        Create or update a rating.

        Args:
            parent: The object being rated (e.g., a Wonder instance)
            subject: The subject of the rating (e.g., a Resonance instance)
            rating_value: The rating value (integer)
            **kwargs: Additional fields (display_alt_name, note, etc.)

        Returns:
            The GenericRating instance
        """
        parent_ct = ContentType.objects.get_for_model(parent)
        subject_ct = ContentType.objects.get_for_model(subject)

        rating, created = cls.objects.update_or_create(
            parent_content_type=parent_ct,
            parent_object_id=parent.pk,
            subject_content_type=subject_ct,
            subject_object_id=subject.pk,
            defaults={"rating": rating_value, **kwargs},
        )
        return rating

    @classmethod
    def get_rating_value(cls, parent, subject):
        """
        Get the rating value for a parent-subject pair.

        Returns 0 if no rating exists.
        """
        parent_ct = ContentType.objects.get_for_model(parent)
        subject_ct = ContentType.objects.get_for_model(subject)

        try:
            rating = cls.objects.get(
                parent_content_type=parent_ct,
                parent_object_id=parent.pk,
                subject_content_type=subject_ct,
                subject_object_id=subject.pk,
            )
            return rating.rating
        except cls.DoesNotExist:
            return 0

    @classmethod
    def get_ratings_for_parent(cls, parent, subject_model=None):
        """
        Get all ratings for a parent object.

        Args:
            parent: The parent object
            subject_model: Optional model class to filter by subject type

        Returns:
            QuerySet of GenericRating instances
        """
        parent_ct = ContentType.objects.get_for_model(parent)

        filters = {
            "parent_content_type": parent_ct,
            "parent_object_id": parent.pk,
        }

        if subject_model:
            subject_ct = ContentType.objects.get_for_model(subject_model)
            filters["subject_content_type"] = subject_ct

        return cls.objects.filter(**filters)

    @classmethod
    def total_rating(cls, parent, subject_model=None):
        """
        Get the sum of all ratings for a parent.

        Args:
            parent: The parent object
            subject_model: Optional model class to filter by subject type

        Returns:
            Integer sum of all ratings
        """
        ratings = cls.get_ratings_for_parent(parent, subject_model)
        return sum(r.rating for r in ratings)


class RatingMixin(models.Model):
    """
    Mixin to add rating functionality to any model.

    Usage:
        class Wonder(RatingMixin, ItemModel):
            ...

    Then use:
        wonder.add_rating(resonance, 3)
        rating_value = wonder.get_rating(resonance)
        rated_items = wonder.get_rated_objects(Resonance)
        total = wonder.total_ratings()
    """

    class Meta:
        abstract = True

    def add_rating(self, subject, rating_value, **kwargs):
        """
        Add or update a rating for a subject.

        Args:
            subject: The object being rated
            rating_value: The rating value (integer)
            **kwargs: Additional fields

        Returns:
            The GenericRating instance
        """
        return GenericRating.create_rating(self, subject, rating_value, **kwargs)

    def get_rating(self, subject):
        """
        Get the rating value for a subject.

        Returns 0 if not rated.
        """
        return GenericRating.get_rating_value(self, subject)

    def get_rated_objects(self, model_class):
        """
        Get all objects of a certain type that this object has rated.

        Returns:
            List of tuples: [(object, rating_value), ...]
        """
        ratings = GenericRating.get_ratings_for_parent(self, model_class)

        return [(r.subject_object, r.rating) for r in ratings]

    def get_all_ratings(self):
        """
        Get all ratings for this object.

        Returns:
            QuerySet of GenericRating instances
        """
        return GenericRating.get_ratings_for_parent(self)

    def total_ratings(self, subject_model=None):
        """
        Get total of all ratings (optionally filtered by subject type).

        Args:
            subject_model: Optional model class to filter by

        Returns:
            Integer sum of all ratings
        """
        return GenericRating.total_rating(self, subject_model)

    def filter_rated_objects(
        self, model_class, minimum=None, maximum=None, exclude_rated=False
    ):
        """
        Get objects of a certain type filtered by rating.

        Args:
            model_class: The model class to filter
            minimum: Minimum rating to include (None = no minimum)
            maximum: Maximum rating to include (None = no maximum)
            exclude_rated: If True, exclude objects already rated

        Returns:
            QuerySet of objects matching the criteria
        """
        all_objects = model_class.objects.all()

        if exclude_rated:
            # Get IDs of objects already rated
            ratings = GenericRating.get_ratings_for_parent(self, model_class)
            rated_ids = [r.subject_object_id for r in ratings]
            all_objects = all_objects.exclude(pk__in=rated_ids)
        else:
            # Filter by rating range
            ratings = GenericRating.get_ratings_for_parent(self, model_class)

            if minimum is not None:
                # Include only objects with rating >= minimum
                include_ids = [r.subject_object_id for r in ratings if r.rating >= minimum]
                all_objects = all_objects.filter(pk__in=include_ids)

            if maximum is not None:
                # Exclude objects with rating > maximum
                exclude_ids = [r.subject_object_id for r in ratings if r.rating > maximum]
                all_objects = all_objects.exclude(pk__in=exclude_ids)

        return all_objects


# Example usage and migration helpers


def migrate_resonance_ratings():
    """
    EXAMPLE migration function to convert old ResonanceRating classes
    to GenericRating.

    This should be adapted and run as a Django data migration.
    DO NOT RUN THIS DIRECTLY - use Django migrations!
    """
    # Example for WonderResonanceRating
    from items.models.mage.wonder import WonderResonanceRating

    for old_rating in WonderResonanceRating.objects.all():
        GenericRating.create_rating(
            parent=old_rating.wonder,
            subject=old_rating.resonance,
            rating_value=old_rating.rating,
        )

    # Repeat for NodeResonanceRating, ResRating, etc.
    # from locations.models.mage.node import NodeResonanceRating
    # for old_rating in NodeResonanceRating.objects.all():
    #     GenericRating.create_rating(
    #         parent=old_rating.node,
    #         subject=old_rating.resonance,
    #         rating_value=old_rating.rating,
    #     )


def example_usage():
    """Example of how to use the new GenericRating system."""
    from items.models.mage.wonder import Wonder
    from characters.models.mage.resonance import Resonance

    # Get a wonder and resonance
    wonder = Wonder.objects.first()
    resonance = Resonance.objects.first()

    # Add a rating (old way: WonderResonanceRating.objects.create(...))
    GenericRating.create_rating(wonder, resonance, 3)

    # Get a rating value (old way: wonder.resonance_rating(resonance))
    rating = GenericRating.get_rating_value(wonder, resonance)
    print(f"Wonder has resonance rating: {rating}")

    # Get all resonance ratings for this wonder
    resonance_ratings = GenericRating.get_ratings_for_parent(wonder, Resonance)
    for rating_obj in resonance_ratings:
        print(f"  {rating_obj.subject_object}: {rating_obj.rating}")

    # Using the mixin (if Wonder inherits from RatingMixin)
    # wonder.add_rating(resonance, 3)
    # rating = wonder.get_rating(resonance)
    # total = wonder.total_ratings(Resonance)
