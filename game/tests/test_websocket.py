"""
Tests for WebSocket-based real-time scene chat.

These tests cover:
- SceneChatConsumer connection/disconnection
- Authentication and authorization
- Chat message handling
- Post creation and broadcasting
- Fallback behavior
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from characters.models.core.human import Human
from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase, override_settings
from game.consumers import SceneChatConsumer
from game.models import Chronicle, Gameline, Post, Scene, STRelationship
from locations.models.core import LocationModel

# Test channel layer settings
TEST_CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}


class SceneChatConsumerUnitTests(TestCase):
    """Unit tests for SceneChatConsumer helper methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.add_character(self.character)

    def test_straighten_quotes_single_quotes(self):
        """Test that various single quote characters are normalized."""
        consumer = SceneChatConsumer()
        # Test various single quote characters
        test_strings = [
            ("\u2018test\u2019", "'test'"),  # LEFT/RIGHT SINGLE QUOTATION MARK
            ("\u201atest\u201b", "'test'"),  # SINGLE LOW-9/HIGH-REVERSED-9
            ("\u2032test\u02b9", "'test'"),  # PRIME/MODIFIER LETTER PRIME
        ]
        for input_str, expected in test_strings:
            result = consumer.straighten_quotes(input_str)
            self.assertEqual(result, expected)

    def test_straighten_quotes_double_quotes(self):
        """Test that various double quote characters are normalized."""
        consumer = SceneChatConsumer()
        # Test various double quote characters
        test_strings = [
            ("\u201ctest\u201d", '"test"'),  # LEFT/RIGHT DOUBLE QUOTATION MARK
            ("\u201etest\u201f", '"test"'),  # DOUBLE LOW-9/HIGH-REVERSED-9
            ("\u2033test\u02ba", '"test"'),  # DOUBLE PRIME/MODIFIER
        ]
        for input_str, expected in test_strings:
            result = consumer.straighten_quotes(input_str)
            self.assertEqual(result, expected)

    def test_straighten_quotes_mixed(self):
        """Test normalizing mixed quote types."""
        consumer = SceneChatConsumer()
        input_str = "\u201cHe said \u2018hello\u2019\u201d"
        expected = "\"He said 'hello'\""
        result = consumer.straighten_quotes(input_str)
        self.assertEqual(result, expected)

    def test_straighten_quotes_no_quotes(self):
        """Test that strings without special quotes are unchanged."""
        consumer = SceneChatConsumer()
        input_str = "Regular text without special quotes"
        result = consumer.straighten_quotes(input_str)
        self.assertEqual(result, input_str)


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class SceneChatConsumerConnectionTests(TransactionTestCase):
    """Test WebSocket connection handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.add_character(self.character)

    async def test_unauthenticated_connection_rejected(self):
        """Test that unauthenticated users cannot connect."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        # Don't set user (anonymous)
        connected, _ = await communicator.connect()
        self.assertFalse(connected)
        await communicator.disconnect()

    async def test_authenticated_connection_accepted(self):
        """Test that authenticated users can connect."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_nonexistent_scene_rejected(self):
        """Test that connection to nonexistent scene is rejected."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, "/ws/scene/99999/")
        communicator.scope["user"] = self.user
        connected, _ = await communicator.connect()
        self.assertFalse(connected)
        await communicator.disconnect()


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class SceneChatConsumerMessageTests(TransactionTestCase):
    """Test chat message handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="test2@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.character2 = Human.objects.create(
            name="Other Character",
            owner=self.user2,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.add_character(self.character)

    async def test_send_chat_message(self):
        """Test sending a chat message via WebSocket."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        # Send a chat message
        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": "Hello, world!",
            }
        )

        # Receive the broadcast
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "new_post")
        self.assertEqual(response["post"]["message"], "Hello, world!")
        self.assertEqual(response["post"]["character_name"], "Test Character")

        await communicator.disconnect()

    async def test_message_saved_to_database(self):
        """Test that messages are saved to the database."""
        from tg.asgi import application

        initial_post_count = await database_sync_to_async(
            lambda: Post.objects.filter(scene=self.scene).count()
        )()

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": "Test message for database",
            }
        )

        # Wait for response
        await communicator.receive_json_from()
        await communicator.disconnect()

        # Check database
        final_post_count = await database_sync_to_async(
            lambda: Post.objects.filter(scene=self.scene).count()
        )()
        self.assertEqual(final_post_count, initial_post_count + 1)

        # Verify post content
        post = await database_sync_to_async(
            lambda: Post.objects.filter(scene=self.scene).latest("datetime_created")
        )()
        self.assertEqual(post.message, "Test message for database")

    async def test_cannot_post_as_other_user_character(self):
        """Test that users cannot post as characters they don't own."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        # Try to post as user2's character
        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character2.pk,
                "display_name": "",
                "message": "Trying to impersonate",
            }
        )

        # Should receive an error
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "error")
        self.assertIn("own characters", response["message"])

        await communicator.disconnect()

    async def test_cannot_post_to_finished_scene(self):
        """Test that posts to finished scenes are rejected."""
        from tg.asgi import application

        # Close the scene
        await database_sync_to_async(self.scene.close)()

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": "Post to finished scene",
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "error")
        self.assertIn("finished", response["message"].lower())

        await communicator.disconnect()

    async def test_empty_message_rejected(self):
        """Test that empty messages are rejected."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": "   ",  # Whitespace only
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "error")
        self.assertIn("empty", response["message"].lower())

        await communicator.disconnect()

    async def test_character_not_in_scene_rejected(self):
        """Test that posting as character not in scene is rejected."""
        from tg.asgi import application

        # Add character to scene for user2 but not for user
        await database_sync_to_async(self.scene.add_character)(self.character2)

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user2
        await communicator.connect()

        # Character2 is in scene, so this should work
        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character2.pk,
                "display_name": "",
                "message": "Valid message",
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "new_post")

        await communicator.disconnect()


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class SceneChatConsumerBroadcastTests(TransactionTestCase):
    """Test message broadcasting to multiple clients."""

    def setUp(self):
        """Set up test fixtures."""
        self.user1 = User.objects.create_user(
            username="user1", email="user1@test.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.char1 = Human.objects.create(
            name="Character 1",
            owner=self.user1,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.char2 = Human.objects.create(
            name="Character 2",
            owner=self.user2,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.add_character(self.char1)
        self.scene.add_character(self.char2)

    async def test_message_broadcast_to_all_clients(self):
        """Test that messages are broadcast to all connected clients."""
        from tg.asgi import application

        # Connect two clients
        comm1 = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        comm1.scope["user"] = self.user1
        await comm1.connect()

        comm2 = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        comm2.scope["user"] = self.user2
        await comm2.connect()

        # User1 sends a message
        await comm1.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.char1.pk,
                "display_name": "",
                "message": "Hello from user1",
            }
        )

        # Both clients should receive the broadcast
        response1 = await comm1.receive_json_from()
        response2 = await comm2.receive_json_from()

        self.assertEqual(response1["type"], "new_post")
        self.assertEqual(response2["type"], "new_post")
        self.assertEqual(response1["post"]["message"], "Hello from user1")
        self.assertEqual(response2["post"]["message"], "Hello from user1")

        await comm1.disconnect()
        await comm2.disconnect()


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class SceneChatConsumerDiceRollTests(TransactionTestCase):
    """Test dice roll and command processing via WebSocket."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            dexterity=3,
            firearms=2,
        )
        self.scene.add_character(self.character)

    async def test_dice_roll_command(self):
        """Test that dice roll commands are processed."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": "Rolling dice /roll 5 difficulty 6",
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "new_post")
        # The message should contain roll results
        self.assertIn("roll of 5 dice", response["post"]["message"])
        self.assertIn("difficulty 6", response["post"]["message"])

        await communicator.disconnect()

    async def test_stat_roll_command(self):
        """Test that stat-based roll commands are processed."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": "Shooting /stat Dexterity + Firearms",
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "new_post")
        # Should show stat values
        self.assertIn("Dexterity (3)", response["post"]["message"])
        self.assertIn("Firearms (2)", response["post"]["message"])
        self.assertIn("= 5 dice", response["post"]["message"])

        await communicator.disconnect()


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class SceneChatConsumerAddCharacterTests(TransactionTestCase):
    """Test adding characters to scene via WebSocket."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="test2@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.character2 = Human.objects.create(
            name="Other Character",
            owner=self.user2,
            chronicle=self.chronicle,
            concept="Test",
        )

    async def test_add_own_character_to_scene(self):
        """Test adding own character to scene via WebSocket."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        await communicator.send_json_to(
            {
                "type": "add_character",
                "character_id": self.character.pk,
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "character_added")
        self.assertEqual(response["character"]["name"], "Test Character")

        # Verify in database
        in_scene = await database_sync_to_async(
            lambda: self.scene.characters.filter(pk=self.character.pk).exists()
        )()
        self.assertTrue(in_scene)

        await communicator.disconnect()

    async def test_cannot_add_other_user_character(self):
        """Test that users cannot add characters they don't own."""
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        await communicator.send_json_to(
            {
                "type": "add_character",
                "character_id": self.character2.pk,
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "error")
        self.assertIn("own characters", response["message"])

        await communicator.disconnect()


class SceneDetailViewIntegrationTests(TestCase):
    """Integration tests for Scene detail view with WebSocket support."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.add_character(self.character)

    def test_scene_detail_includes_websocket_config(self):
        """Test that scene detail page includes WebSocket configuration."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.pk}")

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # Check for WebSocket JavaScript
        self.assertIn("WebSocket", content)
        self.assertIn(f"SCENE_ID = {self.scene.pk}", content)
        self.assertIn("initWebSocket", content)

    def test_scene_detail_includes_fallback_form(self):
        """Test that scene detail page includes fallback form."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.pk}")

        content = response.content.decode()

        # Check for standard form elements
        self.assertIn('id="post-form"', content)
        self.assertIn('name="message"', content)
        self.assertIn('method="post"', content)

    def test_posts_displayed_on_page_load(self):
        """Test that existing posts are displayed on page load."""
        # Create some posts
        self.scene.add_post(self.character, "", "First post")
        self.scene.add_post(self.character, "", "Second post")

        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.pk}")

        content = response.content.decode()
        self.assertIn("First post", content)
        self.assertIn("Second post", content)

    def test_standard_form_submission_still_works(self):
        """Test that standard form submission (fallback) still works."""
        self.client.login(username="testuser", password="password")

        initial_count = Post.objects.filter(scene=self.scene).count()

        response = self.client.post(
            f"/game/scene/{self.scene.pk}",
            {
                "character": self.character.pk,
                "display_name": "",
                "message": "Standard form post",
            },
        )

        self.assertEqual(response.status_code, 302)  # Redirect after post
        self.assertEqual(Post.objects.filter(scene=self.scene).count(), initial_count + 1)

        post = Post.objects.filter(scene=self.scene).latest("datetime_created")
        self.assertEqual(post.message, "Standard form post")

    def test_finished_scene_hides_form(self):
        """Test that finished scenes don't show the post form."""
        self.scene.close()

        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.pk}")

        content = response.content.decode()
        # The form should not be present for finished scenes
        self.assertNotIn('id="post-form"', content)

    def test_connection_status_element_present(self):
        """Test that connection status element is in the page."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(f"/game/scene/{self.scene.pk}")

        content = response.content.decode()
        self.assertIn('id="connection-status"', content)
        self.assertIn('id="status-indicator"', content)


class PostModelIntegrationTests(TestCase):
    """Test that Post model works correctly with the WebSocket flow."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            temporary_willpower=5,
        )
        self.scene.add_character(self.character)

    def test_add_post_creates_post_object(self):
        """Test that add_post creates a Post object."""
        post = self.scene.add_post(self.character, "", "Test message")

        self.assertIsInstance(post, Post)
        self.assertEqual(post.message, "Test message")
        self.assertEqual(post.scene, self.scene)
        self.assertEqual(post.character, self.character)

    def test_add_post_with_display_name(self):
        """Test that add_post respects display name."""
        post = self.scene.add_post(self.character, "Custom Name", "Test")

        self.assertEqual(post.display_name, "Custom Name")

    def test_add_post_default_display_name(self):
        """Test that add_post uses character name as default."""
        post = self.scene.add_post(self.character, "", "Test")

        self.assertEqual(post.display_name, self.character.name)

    def test_add_post_processes_wp_command(self):
        """Test that willpower spending commands are processed."""
        initial_wp = self.character.temporary_willpower
        post = self.scene.add_post(self.character, "", "Spending willpower #WP")

        self.character.refresh_from_db()
        self.assertEqual(self.character.temporary_willpower, initial_wp - 1)
        self.assertIn("WP", post.message)

    def test_add_post_storyteller_message(self):
        """Test that @storyteller messages work correctly."""
        result = self.scene.add_post(self.character, "", "@storyteller Please help!")

        # @storyteller messages return None
        self.assertIsNone(result)
        self.assertTrue(self.scene.waiting_for_st)


@override_settings(CHANNEL_LAYERS=TEST_CHANNEL_LAYERS)
class SceneChatConsumerXSSTests(TransactionTestCase):
    """Test XSS prevention in WebSocket message handling.

    These tests verify that potentially malicious content is handled safely.
    The server transmits messages as-is (for flexibility), and the client-side
    JavaScript uses escapeHtml() to prevent XSS when rendering.

    See issue #1094 for details on the vulnerability and fix.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="password"
        )
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(name="Test Location", chronicle=self.chronicle)
        self.scene = Scene.objects.create(
            name="Test Scene", chronicle=self.chronicle, location=self.location
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
        )
        self.scene.add_character(self.character)

    async def test_xss_payload_in_message_transmitted_unmodified(self):
        """Test that XSS payloads in messages are transmitted as-is.

        The server does not sanitize messages - this is intentional so that
        legitimate angle brackets and HTML entities in game text are preserved.
        The client-side JavaScript MUST escape all user content before rendering
        with innerHTML using the escapeHtml() function.
        """
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        # Send a message with XSS payload
        xss_payload = "<img src=x onerror=\"alert('XSS')\">"
        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": xss_payload,
            }
        )

        # Receive the broadcast - message should be transmitted as-is
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "new_post")
        self.assertEqual(response["post"]["message"], xss_payload)

        await communicator.disconnect()

    async def test_script_tag_in_message_transmitted_unmodified(self):
        """Test that script tags in messages are transmitted as-is.

        Client-side escaping handles this - see test above for explanation.
        """
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        xss_payload = '<script>alert("XSS")</script>'
        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": xss_payload,
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "new_post")
        self.assertEqual(response["post"]["message"], xss_payload)

        await communicator.disconnect()

    async def test_legitimate_angle_brackets_preserved(self):
        """Test that legitimate angle brackets in game text are preserved.

        Players often use angle brackets for actions, e.g., <waves hand>.
        These should be transmitted and then escaped on the client side.
        """
        from tg.asgi import application

        communicator = WebsocketCommunicator(application, f"/ws/scene/{self.scene.pk}/")
        communicator.scope["user"] = self.user
        await communicator.connect()

        message = "The mage says <mystically> you shall not pass!"
        await communicator.send_json_to(
            {
                "type": "chat_message",
                "character_id": self.character.pk,
                "display_name": "",
                "message": message,
            }
        )

        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "new_post")
        self.assertEqual(response["post"]["message"], message)

        await communicator.disconnect()

    def test_xss_payload_stored_in_database(self):
        """Test that XSS payloads in posts are stored as-is in database.

        Database stores raw content. Client-side rendering handles escaping.
        """
        xss_payload = "<img src=x onerror=\"alert('XSS')\">"
        post = self.scene.add_post(self.character, "", xss_payload)

        post.refresh_from_db()
        self.assertEqual(post.message, xss_payload)
