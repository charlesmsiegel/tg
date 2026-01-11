# game/signals.py
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from characters.models.core.character import CharacterModel
from game.models import Journal


@receiver(post_save)
def create_journal_for_character(sender, instance, created, **kwargs):
    """Create a Journal for a newly created Character.

    Uses get_or_create to prevent race conditions. This runs within the same
    database transaction as the Character save, ensuring consistency.
    If a race condition occurs (duplicate key), we handle it gracefully.
    """
    if created and isinstance(instance, CharacterModel):
        try:
            Journal.objects.get_or_create(character=instance)
        except IntegrityError:
            # Race condition: another process already created the Journal.
            # This is fine - the Journal exists, which is what we want.
            pass
