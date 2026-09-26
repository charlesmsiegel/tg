"""Authorized navigation. Predicates are pure; only POST-driven transitions write."""

from django.core.exceptions import PermissionDenied
from django.db import transaction

from core.permissions import Permission, PermissionManager

from . import get_workflow


def _skip_effect(character, step):
    if step.key == "languages":
        from core.models import Language

        english, _ = Language.objects.get_or_create(name="English")
        character.languages.add(english)


@transaction.atomic
def advance(character, *, user):
    """Complete the current task and skip consecutive inapplicable tasks.

    The caller saves form data using its existing lifecycle. Only the position
    and explicit skip effects are persisted here; terminal views submit as before.
    """
    if character.status not in {"Un", "Rev"} or not PermissionManager.user_has_permission(
        user, character, Permission.EDIT_FULL
    ):
        raise PermissionDenied("Cannot advance this character")
    workflow = get_workflow(character.type)
    if workflow is None:
        raise ValueError(f"No chargen workflow for {character.type}")
    current = workflow.step(character.creation_status)
    position = character.creation_status + 1
    if position > len(workflow.steps):
        raise ValueError("The final step must submit the character")
    if current.should_skip(character):
        _skip_effect(character, current)
    while position < len(workflow.steps):
        step = workflow.step(position)
        if not step.should_skip(character):
            break
        _skip_effect(character, step)
        position += 1
    character.creation_status = position
    character.save(update_fields=["creation_status"])
    return position


def previous_position(character):
    """Find an applicable predecessor without applying effects or writing rows."""
    workflow = get_workflow(character.type)
    if workflow is None:
        return max(1, character.creation_status - 1)
    workflow.step(character.creation_status)
    position = max(1, character.creation_status - 1)
    while position > 1 and workflow.step(position).should_skip(character):
        position -= 1
    return position
