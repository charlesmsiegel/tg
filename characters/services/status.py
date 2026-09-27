"""Character status transitions requested from the character sheet."""

from characters.services.result import ServiceResult

STATUS_VERBS = {"Ret": "retired", "Dec": "deceased"}


def change_character_status(character, target):
    """Move ``character`` to ``target`` when its state machine allows it.

    The caller holds a row lock on ``character``, so the transition is checked
    against the committed status. ``Character.save`` removes a retired or
    deceased character from its organizations, as it did for the old handler.
    """
    verb = STATUS_VERBS.get(target, target)
    if target not in character.STATUS_TRANSITIONS.get(character.status, ()):
        return ServiceResult.fail(
            f"'{character.name}' cannot be marked {verb} from its current status."
        )
    character.status = target
    character.save()
    return ServiceResult.ok(f"'{character.name}' marked {verb}.", obj=character)
