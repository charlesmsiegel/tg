"""Service for handling object and image approvals."""

from django.db import transaction
from django.shortcuts import get_object_or_404

from characters.models.core.character import Character
from characters.models.mage.rote import Rote
from items.models.core import ItemModel
from locations.models.core.location import LocationModel


class ApprovalService:
    """
    Service class for managing approval workflows.

    Consolidates duplicated approval logic from ProfileView.post() into
    a single, testable service class.
    """

    # Model type to class mapping for object approvals
    OBJECT_MODEL_MAP = {
        "character": Character,
        "location": LocationModel,
        "item": ItemModel,
        "rote": Rote,
    }

    # Model type to class mapping for image approvals
    IMAGE_MODEL_MAP = {
        "character": Character,
        "location": LocationModel,
        "item": ItemModel,
    }

    @classmethod
    def approve_object(cls, model_type: str, object_id: int) -> tuple:
        """
        Approve an object (character, location, item, or rote).

        Args:
            model_type: One of 'character', 'location', 'item', 'rote'
            object_id: Primary key of the object to approve

        Returns:
            Tuple of (object, success_message)

        Raises:
            ValueError: If model_type is not valid
            Http404: If object with given ID does not exist
        """
        model_class = cls.OBJECT_MODEL_MAP.get(model_type)
        if not model_class:
            raise ValueError(f"Invalid model type: {model_type}")

        with transaction.atomic():
            obj = get_object_or_404(model_class, pk=object_id)
            obj.status = "App"
            obj.save()

            # Handle character-specific group pooled background updates
            if model_type == "character" and hasattr(obj, "group_set"):
                groups = obj.group_set.select_related().all()
                for g in groups:
                    g.update_pooled_backgrounds()

        type_display = model_type.title()
        return obj, f"{type_display} '{obj.name}' approved successfully!"

    @classmethod
    def approve_image(cls, model_type: str, object_id: int) -> tuple:
        """
        Approve an image for an object (character, location, or item).

        Args:
            model_type: One of 'character', 'location', 'item'
            object_id: Primary key of the object whose image to approve

        Returns:
            Tuple of (object, success_message)

        Raises:
            ValueError: If model_type is not valid
            Http404: If object with given ID does not exist
        """
        model_class = cls.IMAGE_MODEL_MAP.get(model_type)
        if not model_class:
            raise ValueError(f"Invalid model type for image approval: {model_type}")

        obj = get_object_or_404(model_class, pk=object_id)
        obj.image_status = "app"
        obj.save()

        return obj, f"Image for '{obj.name}' approved successfully!"

    @classmethod
    def parse_image_id(cls, raw_id: str) -> str:
        """
        Parse image approval ID from form submission.

        The form submits IDs like "image-123", this extracts "123".

        Args:
            raw_id: The raw ID string from form submission

        Returns:
            The parsed object ID
        """
        if raw_id and "-" in raw_id:
            return raw_id.split("-")[-1]
        return raw_id
