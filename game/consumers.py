"""
WebSocket consumers for real-time scene chat.
"""

import json
import logging

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from characters.models.core import CharacterModel
from django.utils import timezone
from game.models import Post, Scene

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
        self.room_group_name = f"scene_{self.scene_id}"
        self.user = self.scope["user"]

        # Reject unauthenticated users
        if not self.user.is_authenticated:
            logger.warning(
                f"Unauthenticated WebSocket connection attempt for scene {self.scene_id}"
            )
            await self.close()
            return

        # Verify scene exists and user has access
        scene = await self.get_scene()
        if scene is None:
            logger.warning(f"Scene {self.scene_id} not found for WebSocket connection")
            await self.close()
            return

        # Check if scene is finished (read-only)
        self.scene_finished = scene.finished

        # Join the scene group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        logger.info(f"User {self.user.username} connected to scene {self.scene_id}")

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
            await self.send_error(str(e))

    async def handle_chat_message(self, data):
        """Handle incoming chat message."""
        character_id = data.get("character_id")
        message = data.get("message", "").strip()
        display_name = data.get("display_name", "")

        if not message:
            await self.send_error("Message cannot be empty")
            return

        # Check scene is not finished
        scene = await self.get_scene()
        if scene is None or scene.finished:
            await self.send_error("Cannot post to a finished scene")
            return

        # Get and validate character
        character = await self.get_character(character_id)
        if character is None:
            await self.send_error("Character not found")
            return

        # Verify user owns this character
        if not await self.user_owns_character(character):
            await self.send_error("You can only post as your own characters")
            return

        # Verify character is in the scene
        if not await self.character_in_scene(character, scene):
            await self.send_error("Character is not in this scene")
            return

        # Straighten quotes in the message (matching view behavior)
        message = self.straighten_quotes(message)

        # Create the post using the Scene.add_post method
        result = await self.create_post(scene, character, display_name, message)

        if result is None:
            # add_post returns None for @storyteller messages or errors
            await self.send(
                text_data=json.dumps(
                    {"type": "system_message", "message": "Message sent to storyteller"}
                )
            )
            return

        if result == "error":
            await self.send_error("Failed to process message command")
            return

        post = result

        # Prepare post data for broadcast
        post_data = await self.serialize_post(post, character)

        # Broadcast to all clients in the scene group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message_broadcast",
                "post": post_data,
            },
        )

    async def handle_add_character(self, data):
        """Handle adding a character to the scene."""
        character_id = data.get("character_id")

        # Get scene
        scene = await self.get_scene()
        if scene is None or scene.finished:
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

        # Add character to scene
        await self.add_character_to_scene(scene, character)

        # Broadcast character added notification
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "character_added_broadcast",
                "character": {
                    "id": character.pk,
                    "name": character.name,
                    "owner_id": self.user.pk,
                },
            },
        )

    async def chat_message_broadcast(self, event):
        """Send chat message to WebSocket."""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "new_post",
                    "post": event["post"],
                }
            )
        )

    async def character_added_broadcast(self, event):
        """Send character added notification to WebSocket."""
        await self.send(
            text_data=json.dumps(
                {
                    "type": "character_added",
                    "character": event["character"],
                }
            )
        )

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

    @staticmethod
    def straighten_quotes(s):
        """Normalize various quotation marks to standard ASCII."""
        single_quote_chars = [
            0x2018,
            0x2019,
            0x201A,
            0x201B,
            0x2032,
            0x02B9,
            0x02BB,
            0x02BC,
            0x02BD,
            0x275B,
            0x275C,
            0xFF07,
            0x00B4,
            0x0060,
        ]
        double_quote_chars = [
            0x201C,
            0x201D,
            0x201E,
            0x201F,
            0x2033,
            0x02BA,
            0x275D,
            0x275E,
            0xFF02,
        ]
        translation_table = {}
        for code_point in single_quote_chars:
            translation_table[code_point] = ord("'")
        for code_point in double_quote_chars:
            translation_table[code_point] = ord('"')
        return s.translate(translation_table)

    # Database operations (must be wrapped for async)

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
        return character.owner_id == self.user.pk

    @database_sync_to_async
    def character_in_scene(self, character, scene):
        """Check if character is in the scene."""
        return scene.characters.filter(pk=character.pk).exists()

    @database_sync_to_async
    def create_post(self, scene, character, display_name, message):
        """Create a post using Scene.add_post method."""
        try:
            post = scene.add_post(character, display_name, message)
            return post
        except ValueError:
            return "error"

    @database_sync_to_async
    def add_character_to_scene(self, scene, character):
        """Add a character to the scene."""
        scene.add_character(character)

    @database_sync_to_async
    def serialize_post(self, post, character):
        """Serialize post data for WebSocket transmission."""
        is_st = character.owner.profile.is_st() if hasattr(character.owner, "profile") else False
        return {
            "id": post.pk,
            "character_id": character.pk,
            "character_name": character.name,
            "character_url": character.get_absolute_url(),
            "display_name": post.display_name,
            "message": post.message,
            "datetime_created": post.datetime_created.isoformat(),
            "owner_id": character.owner_id,
            "is_st": is_st,
        }
