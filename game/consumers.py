"""
WebSocket consumers for real-time scene chat.
"""

import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import transaction

from characters.models.core import CharacterModel
from core.actions import ActionFailed
from core.templatetags.sanitize_text import render_post_html
from game import scene_chat
from game.forms import PostForm
from game.models import Scene
from game.security import can_view_scene
from game.selectors import scene_post
from game.text import straighten_quotes

logger = logging.getLogger(__name__)


class SceneChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time scene chat.

    Handles:
    - Connection/disconnection to scene-specific chat rooms
    - Broadcasting new posts to all connected clients
    - Saving posts to database via Scene.add_post()
    - Authentication and authorization checks
    """

    async def connect(self):
        """Handle WebSocket connection."""
        self.scene_id = self.scope["url_route"]["kwargs"]["scene_id"]
        self.room_group_name = scene_chat.group_name(self.scene_id)
        self.user = self.scope["user"]

        # Public scenes admit anonymous readers; every other audience is
        # checked before joining the broadcast group.
        scene = await self.get_scene()
        if scene is None or not await self.user_can_view_scene(scene):
            await self.close()
            return

        # Check if scene is finished (read-only)
        self.scene_finished = scene.finished

        # Join the scene group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        logger.info(f"User {self.user} connected to scene {self.scene_id}")

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave the scene group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"User {self.user.username} disconnected from scene {self.scene_id}")

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get("type")

            if message_type == "chat_message":
                await self.handle_chat_message(data)
            elif message_type == "add_character":
                await self.handle_add_character(data)
            else:
                logger.warning(f"Unknown message type: {message_type}")
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            await self.send_error("Invalid message format")
        except Exception as e:
            logger.error(f"Error processing WebSocket message: {e}", exc_info=True)
            await self.send_error("Could not process message")

    async def handle_chat_message(self, data):
        """Handle incoming chat message through the shared posting path."""
        fields = {
            "character": data.get("character_id"),
            "display_name": data.get("display_name", ""),
            "message": data.get("message", ""),
        }
        ok, outcome = await self.submit_post(fields)
        if not ok:
            await self.send_error(outcome)
        elif outcome.object is None:
            await self.send(
                text_data=json.dumps({"type": "system_message", "message": outcome.message})
            )

    async def handle_add_character(self, data):
        """Handle adding a character to the scene."""
        character_id = data.get("character_id")

        # Get scene
        scene = await self.get_scene()
        if scene is None or scene.finished or not await self.user_can_view_scene(scene):
            await self.send_error("Cannot add character to finished scene")
            return

        # Get and validate character
        character = await self.get_character(character_id)
        if character is None:
            await self.send_error("Character not found")
            return

        # Verify user owns this character
        if not await self.user_owns_character(character):
            await self.send_error("You can only add your own characters")
            return
        if character.chronicle_id != scene.chronicle_id:
            await self.send_error("Character cannot join this scene")
            return

        # Add character to scene; the broadcast follows the commit.
        await self.add_character_to_scene(scene, character)

    async def scene_post(self, event):
        """A post was committed: send it to this connection's viewer."""
        payload = await self.post_payload(event["post_id"])
        if payload is False:
            await self.close()
        elif payload:
            await self.send(text_data=json.dumps({"type": "new_post", "post": payload}))

    async def scene_characters(self, event):
        """A character joined the scene."""
        payload = await self.character_payload(event["character_id"])
        if payload is False:
            await self.close()
        elif payload:
            await self.send(text_data=json.dumps({"type": "character_added", "character": payload}))

    async def scene_closed(self, event):
        """The scene was closed; the old client has nothing to update."""
        await self.close()

    async def send_error(self, message):
        """Send error message to client."""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "error",
                    "message": message,
                }
            )
        )

    straighten_quotes = staticmethod(straighten_quotes)

    @database_sync_to_async
    def get_scene(self):
        """Get scene by ID."""
        try:
            return Scene.objects.select_related("chronicle", "location").get(pk=self.scene_id)
        except Scene.DoesNotExist:
            return None

    @database_sync_to_async
    def get_character(self, character_id):
        """Get character by ID."""
        try:
            return CharacterModel.objects.select_related("owner").get(pk=character_id)
        except CharacterModel.DoesNotExist:
            return None

    @database_sync_to_async
    def user_owns_character(self, character):
        """Check if current user owns the character."""
        return self.user.is_authenticated and character.owner_id == self.user.pk

    @database_sync_to_async
    def user_can_view_scene(self, scene):
        return can_view_scene(self.user, scene)

    @database_sync_to_async
    def character_in_scene(self, character, scene):
        """Check if character is in the scene."""
        return scene.characters.filter(pk=character.pk).exists()

    @database_sync_to_async
    def submit_post(self, fields):
        """Authorize, validate and post like ``ScenePostView``; ``(ok, result or error)``."""
        scene = self.visible_scene()
        if scene is None or scene.finished:
            return False, "Cannot post to a finished scene"
        if not scene_chat.can_post(self.user, scene):
            return False, "You can only post as your own characters in this scene"
        form = PostForm(data=fields, user=self.user, scene=scene)
        if not form.is_valid():
            return False, next(iter(form.errors.values()))[0]
        try:
            with transaction.atomic():
                return True, scene_chat.create_post(scene, form)
        except ActionFailed as exc:
            return False, str(exc)

    def visible_scene(self):
        scene = (
            Scene.objects.select_related("chronicle", "location").filter(pk=self.scene_id).first()
        )
        if scene is None or not can_view_scene(self.user, scene):
            return None
        return scene

    @database_sync_to_async
    def add_character_to_scene(self, scene, character):
        """Add a character to the scene and announce it after commit."""
        with transaction.atomic():
            scene.add_character(character)
            scene_chat.broadcast(scene.pk, scene_chat.CHARACTER_JOINED, character_id=character.pk)

    @database_sync_to_async
    def post_payload(self, post_id):
        """The old JSON shape of a post; ``False`` if the viewer lost access."""
        scene = self.visible_scene()
        if scene is None:
            return False
        post = scene_post(scene, post_id)
        if post is None:
            return None
        character = post.character
        return {
            "id": post.pk,
            "character_id": character.pk if character else None,
            "character_name": character.name if character else "",
            "character_url": character.get_absolute_url() if character else "",
            "display_name": post.display_name,
            "message": post.message,
            "message_html": render_post_html(post.message),
            "datetime_created": post.datetime_created.isoformat(),
            "owner_id": character.owner_id if character else None,
            "is_st": post.author_is_st,
        }

    @database_sync_to_async
    def character_payload(self, character_id):
        if self.visible_scene() is None:
            return False
        character = CharacterModel.objects.filter(pk=character_id).first()
        if character is None:
            return None
        return {"id": character.pk, "name": character.name, "owner_id": character.owner_id}
