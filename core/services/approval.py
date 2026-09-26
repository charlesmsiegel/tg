"""Service for handling object and image approvals."""

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404

from characters.models.changeling.chimera import Chimera
from characters.models.core.character import Character
from characters.models.core.group import Group
from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from core.models import CharacterTemplate
from core.permissions import Permission, PermissionManager
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
        "group": Group,
        "chimera": Chimera,
        "effect": Effect,
        "location": LocationModel,
        "item": ItemModel,
        "rote": Rote,
        "template": CharacterTemplate,
    }

    # Model type to class mapping for image approvals
    IMAGE_MODEL_MAP = {
        "character": Character,
        "location": LocationModel,
        "item": ItemModel,
    }

    @classmethod
    def approve_object(cls, model_type: str, object_id: int, approver=None) -> tuple:
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
            obj = get_object_or_404(model_class.objects.select_for_update(), pk=object_id)
            if approver is None or not PermissionManager.user_has_permission(
                approver, obj, Permission.APPROVE
            ):
                raise PermissionDenied("Approval requires a scoped storyteller")
            if obj.status != "Sub":
                raise ValidationError("Only submitted objects can be approved")
            obj.status = "App"
            obj.save(update_fields=["status"])

            # Handle character-specific group pooled background updates
            if model_type == "character" and hasattr(obj, "group_set"):
                groups = obj.group_set.select_related().all()
                for g in groups:
                    g.update_pooled_backgrounds()

        type_display = model_type.title()
        return obj, f"{type_display} '{obj.name}' approved successfully!"

    @classmethod
    def transition_object(cls, model_type, object_id, user, target_status):
        """Submit a draft or return a submitted object for revisions."""
        model_class = cls.OBJECT_MODEL_MAP.get(model_type)
        if model_class is None or target_status not in {"Sub", "Rev"}:
            raise ValueError("Unsupported object transition")
        with transaction.atomic():
            obj = get_object_or_404(model_class.objects.select_for_update(), pk=object_id)
            if target_status == "Sub":
                if obj.status not in {"Un", "Rev"}:
                    raise ValidationError("Only drafts can be submitted")
                if not PermissionManager.user_has_permission(
                    user, obj, Permission.EDIT_FULL
                ):
                    raise PermissionDenied("Cannot submit this object")
                # Opt-in hook: a model lists what still blocks submission.
                submission_errors = getattr(obj, "submission_errors", None)
                if submission_errors is not None:
                    errors = submission_errors()
                    if errors:
                        raise ValidationError("; ".join(errors))
            else:
                if obj.status != "Sub":
                    raise ValidationError("Only submitted objects can be returned")
                if not PermissionManager.user_has_permission(
                    user, obj, Permission.APPROVE
                ):
                    raise PermissionDenied("Matching chronicle ST required")
            update_fields = ["status"]
            if target_status == "Rev":
                # Opt-in hook: a model resets its own state and names the fields.
                on_returned = getattr(obj, "on_returned_for_revision", None)
                if on_returned is not None:
                    update_fields.extend(on_returned())
            obj.status = target_status
            obj.save(update_fields=update_fields)
            return obj

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
