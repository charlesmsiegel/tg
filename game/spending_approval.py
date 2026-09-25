"""One guarded transaction for approving or denying character spending."""

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404

from characters.services.freebie_spending import FreebieSpendingServiceFactory
from characters.services.xp_spending import XPSpendingServiceFactory
from core.permissions import Permission, PermissionManager, Role
from game.models import FreebieSpendingRecord, XPSpendingRequest


class SpendingDecisionError(Exception):
    """The spending service rejected an attempted decision."""


def can_approve_spending(user, character):
    """Return the same scoped decision used by all spending endpoints."""
    if character is None or not PermissionManager.user_has_permission(
        user, character, Permission.APPROVE
    ):
        return False
    if character.owner_id == user.pk:
        roles = PermissionManager.get_user_roles(user, character)
        if not getattr(character, "npc", False) or not roles & {
            Role.CHRONICLE_HEAD_ST,
            Role.CHRONICLE_ST,
        }:
            return False
    return True


def require_spending_approver(user, character):
    if not can_approve_spending(user, character):
        raise PermissionDenied("Approval requires a scoped storyteller and no PC self-approval")


def decide_spending_request(record_model, character, record_id, approver, decision):
    """Lock a pending request, check scope, and apply its service exactly once."""
    if record_model not in {XPSpendingRequest, FreebieSpendingRecord}:
        raise ValueError("Unsupported spending record")
    if decision not in {"approve", "deny"}:
        raise ValueError("Unsupported spending decision")

    with transaction.atomic():
        try:
            record = (
                record_model.objects.select_for_update()
                .select_related("character")
                .get(pk=record_id, character_id=character.pk, approved="Pending")
            )
        except record_model.DoesNotExist as exc:
            raise Http404("Spending request not found") from exc

        # ForeignKey dereferencing returns the CharacterModel base row. XP and
        # freebie services need the concrete polymorphic character methods.
        subject = record.character.get_real_instance()
        if not PermissionManager.user_has_permission(approver, subject, Permission.VIEW_FULL):
            raise Http404("Spending request not found")
        require_spending_approver(approver, subject)

        if record_model is XPSpendingRequest:
            service = XPSpendingServiceFactory.get_service(subject)
        else:
            service = FreebieSpendingServiceFactory.get_service(subject)

        result = (
            service.apply(record, approver)
            if decision == "approve"
            else service.deny(record, approver)
        )
        if not result.success:
            raise SpendingDecisionError(result.error or "Spending decision failed")
        return result
