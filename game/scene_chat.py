"""Scene chat: the one posting path and the live broadcasts (Step 11).

The WebSocket consumer and the HTTP fallback (``game.actions.ScenePostView``)
both authorize with ``can_post``, validate with ``PostForm`` and persist with
``create_post``. Scene actions announce their changes with ``broadcast``; each
connected consumer renders the event for its own viewer.
"""

import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction

from characters.services.result import ServiceResult
from core.actions import ActionFailed
from game.text import straighten_quotes

logger = logging.getLogger(__name__)

STORYTELLER_PREFIX = "@storyteller"

# Group event types; Channels calls the consumer method with "." replaced by "_".
POST_CREATED = "scene.post"
CHARACTER_JOINED = "scene.characters"
SCENE_CLOSED = "scene.closed"


def group_name(scene_id):
    return f"scene_{scene_id}"


# Post ids are 64-bit; a larger cursor would overflow the database parameter.
MAX_POST_ID = 2**63 - 1


def post_cursor(value):
    """A post id cursor from a query string or JSON, or ``None`` if it is junk.

    Only ASCII digits count: ``str.isdigit()`` accepts characters such as "²"
    that ``int()`` rejects.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        if not (value.isascii() and value.isdigit() and len(value) <= 19):
            return None
        value = int(value)
    if isinstance(value, int) and 0 <= value <= MAX_POST_ID:
        return value
    return None


def can_post(user, scene):
    """Players post as one of their own characters in an open scene (Step 0)."""
    return bool(
        user.is_authenticated and not scene.finished and scene.characters.owned_by(user).exists()
    )


def create_post(scene, form):
    """Post a valid ``PostForm``'s message; call inside the caller's transaction.

    Returns ``ServiceResult`` whose ``object`` is the new post, or ``None`` for
    a message addressed to the storyteller. Raises ``ActionFailed`` when a dice
    command is malformed; nothing is posted then.
    """
    own = form.character_queryset
    character = own.first() if own.count() == 1 else form.cleaned_data["character"]
    if character is None:
        raise ActionFailed("You need a character in this scene to post.")
    message = straighten_quotes(form.cleaned_data["message"])
    try:
        post = scene.add_post(character, form.cleaned_data["display_name"], message)
    except ValueError as exc:
        raise ActionFailed("Command does not match the expected format.") from exc
    if post is None:
        # add_post returns None both for storyteller messages and for commands
        # it could not parse; only the first is a success.
        if message.lower().startswith(STORYTELLER_PREFIX):
            return ServiceResult.ok("Message sent to the storyteller.")
        raise ActionFailed("Command does not match the expected format.")
    broadcast(scene.pk, POST_CREATED, post_id=post.pk)
    return ServiceResult.ok("Post added successfully!", obj=post)


def broadcast(scene_id, event_type, **data):
    """Tell the scene's connections about a committed change.

    Sent after commit so no one renders a row that may still roll back; a
    channel layer failure is logged on this module's logger (not on
    ``django.db.backends``, where ``on_commit(robust=True)`` would put it and
    the production settings discard it) and never fails the change itself.
    """
    event = {"type": event_type, **data}

    def send():
        try:
            layer = get_channel_layer()
            if layer is not None:
                async_to_sync(layer.group_send)(group_name(scene_id), event)
        except Exception:
            logger.exception("Scene %s broadcast of %s failed", scene_id, event_type)

    transaction.on_commit(send)
