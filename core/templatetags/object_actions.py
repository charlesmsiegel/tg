"""Render only the actions the current actor can take on a full object view."""

from django import template

from characters.models.changeling.chimera import Chimera
from characters.models.core.character import Character
from characters.models.core.group import Group
from characters.models.mage.effect import Effect
from characters.models.mage.rote import Rote
from core.models import CharacterTemplate
from core.permissions import Permission, PermissionManager
from items.models.core import ItemModel
from locations.models.core import LocationModel

register = template.Library()


@register.inclusion_tag("core/object_actions.html", takes_context=True)
def object_actions(context):
    obj = context.get("object")
    user = context["request"].user
    if isinstance(obj, Character):
        object_type = "character"
    elif isinstance(obj, Group):
        object_type = "group"
    elif isinstance(obj, Chimera):
        object_type = "chimera"
    elif isinstance(obj, Effect):
        object_type = "effect"
    elif isinstance(obj, Rote):
        object_type = "rote"
    elif isinstance(obj, ItemModel):
        object_type = "item"
    elif isinstance(obj, LocationModel):
        object_type = "location"
    elif isinstance(obj, CharacterTemplate):
        object_type = "template"
    else:
        return {}
    can_edit = PermissionManager.user_has_permission(user, obj, Permission.EDIT_FULL)
    can_approve = PermissionManager.user_has_permission(user, obj, Permission.APPROVE)
    can_submit = can_edit and obj.status in {"Un", "Rev"}
    # Models may opt in to listing what blocks submission (see ApprovalService).
    submission_errors = []
    if can_submit and hasattr(obj, "submission_errors"):
        submission_errors = obj.submission_errors()
    return {
        "object_type": object_type,
        "object_pk": obj.pk,
        "can_submit": can_submit and not submission_errors,
        "submission_errors": submission_errors,
        "can_review": can_approve and obj.status == "Sub",
    }
