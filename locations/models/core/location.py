from django.core.exceptions import ValidationError
from django.db import models, router, transaction

from core.models import Model, ModelManager, ModelQuerySet
from core.registry_urls import RegistryURLMixin


class LocationQuerySet(ModelQuerySet):
    """Custom queryset for LocationModel with chainable query patterns."""

    def top_level(self):
        """Top-level locations (not contained within any other location)"""
        return self.filter(contained_within__isnull=True)


# Create LocationModelManager from ModelManager to inherit polymorphic_ctype optimization
LocationModelManager = ModelManager.from_queryset(LocationQuerySet)


class LocationModel(RegistryURLMixin, Model):
    type = "location"

    parent = models.ForeignKey(
        "LocationModel",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    contained_within = models.ManyToManyField(
        "LocationModel",
        blank=True,
        related_name="contains",
    )
    owned_by = models.ForeignKey(
        "characters.CharacterModel", blank=True, null=True, on_delete=models.SET_NULL
    )

    gauntlet = models.IntegerField(default=7)
    shroud = models.IntegerField(default=7)
    dimension_barrier = models.IntegerField(default=6)
    creation_status = models.IntegerField(default=1)

    objects = LocationModelManager()

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Location"

    def get_scenes(self):
        return self.scene_set.all()

    def containment_chains(self, max_depth=10):
        """Where this place sits: one chain per direct container, innermost first.

        Each chain climbs through the first container of every step ("Newberry Library ›
        Near North Side") and stops at a top-level place, at ``max_depth``, or when the
        containment graph loops back on itself.
        """
        chains = []
        for container in self.contained_within.all():
            chain, seen, current = [], {self.pk}, container
            while current is not None and current.pk not in seen and len(chain) < max_depth:
                chain.append(current)
                seen.add(current.pk)
                current = current.contained_within.first()
            chains.append(chain)
        return chains

    def owned_by_list(self):
        if self.owned_by:
            return [self.owned_by]
        else:
            return []

    def clean(self):
        """Validate location data before saving."""
        super().clean()
        errors = {}

        # Validate gauntlet is in valid range (0-10)
        if self.gauntlet < 0 or self.gauntlet > 10:
            errors["gauntlet"] = "Gauntlet must be between 0 and 10"

        # Validate shroud is in valid range (0-10)
        if self.shroud < 0 or self.shroud > 10:
            errors["shroud"] = "Shroud must be between 0 and 10"

        # Validate dimension_barrier is in valid range (0-10)
        if self.dimension_barrier < 0 or self.dimension_barrier > 10:
            errors["dimension_barrier"] = "Dimension barrier must be between 0 and 10"

        # Validate creation_status is non-negative
        if self.creation_status < 0:
            errors["creation_status"] = "Creation status cannot be negative"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        zone_id = getattr(self, "reality_zone_id", None)
        update_fields = kwargs.get("update_fields", args[3] if len(args) > 3 else None)
        if update_fields is not None:
            # Django also accepts generators and (on 5.2) positional arguments.
            # Inspect once without consuming an iterator before the actual save.
            update_fields = frozenset(update_fields)
            if "update_fields" in kwargs:
                kwargs["update_fields"] = update_fields
            elif len(args) > 3:
                args = (*args[:3], update_fields, *args[4:])
        if zone_id is None or (
            update_fields is not None
            and not {"reality_zone", "reality_zone_id"}.intersection(update_fields)
        ):
            return super().save(*args, **kwargs)
        using = kwargs.get("using", args[2] if len(args) > 2 else None) or router.db_for_write(
            type(self), instance=self
        )
        # Commit the link and its sticky classification together. A failed place
        # save must not turn a staff standalone reference into a player zone.
        with transaction.atomic(using=using):
            result = super().save(*args, **kwargs)
            zone_model = self._meta.get_field("reality_zone").remote_field.model
            zone_model.objects.using(using).filter(pk=zone_id, is_player_zone=False).update(
                is_player_zone=True
            )
            return result
