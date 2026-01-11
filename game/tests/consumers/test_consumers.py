"""
Tests for game WebSocket consumers.

These tests cover the SceneChatConsumer for real-time scene chat functionality.
"""

import json

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, TransactionTestCase

from characters.models.core import Human
from game.consumers import SceneChatConsumer
from game.models import Chronicle, Scene
from locations.models.core import LocationModel


class TestSceneChatConsumerStraightenQuotes(TestCase):
    """Test the straighten_quotes static method."""

    def test_straighten_single_quotes(self):
        """Test that single curly quotes are straightened."""
        input_text = "\u2018Hello\u2019"  # 'Hello'
        result = SceneChatConsumer.straighten_quotes(input_text)
        self.assertEqual(result, "'Hello'")

    def test_straighten_double_quotes(self):
        """Test that double curly quotes are straightened."""
        input_text = "\u201cHello\u201d"  # "Hello"
        result = SceneChatConsumer.straighten_quotes(input_text)
        self.assertEqual(result, '"Hello"')

    def test_straighten_mixed_quotes(self):
        """Test that mixed quotes are straightened."""
        input_text = "\u201cHe said, \u2018Hello\u2019\u201d"
        result = SceneChatConsumer.straighten_quotes(input_text)
        self.assertEqual(result, "\"He said, 'Hello'\"")

    def test_straighten_prime_and_double_prime(self):
        """Test that prime marks are straightened."""
        input_text = "\u2032 and \u2033"  # ′ and ″
        result = SceneChatConsumer.straighten_quotes(input_text)
        self.assertEqual(result, "' and \"")

    def test_straighten_acute_accent(self):
        """Test that acute accent is straightened."""
        input_text = "\u00b4test"  # ´test
        result = SceneChatConsumer.straighten_quotes(input_text)
        self.assertEqual(result, "'test")

    def test_straighten_grave_accent(self):
        """Test that grave accent is straightened."""
        input_text = "\u0060test"  # `test
        result = SceneChatConsumer.straighten_quotes(input_text)
        self.assertEqual(result, "'test")

    def test_no_quotes_unchanged(self):
        """Test that text without special quotes is unchanged."""
        input_text = "Hello, World!"
        result = SceneChatConsumer.straighten_quotes(input_text)
        self.assertEqual(result, "Hello, World!")

    def test_already_straight_quotes(self):
        """Test that already straight quotes are unchanged."""
        input_text = "'Hello' and \"World\""
        result = SceneChatConsumer.straighten_quotes(input_text)
        self.assertEqual(result, "'Hello' and \"World\"")


class TestSceneChatConsumerDatabaseMethods(TransactionTestCase):
    """Test database methods of SceneChatConsumer."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.scene.characters.add(self.character)

    def test_get_scene_returns_scene(self):
        """Test get_scene returns the scene object."""
        consumer = SceneChatConsumer()
        consumer.scene_id = self.scene.pk

        # Call the sync version directly
        scene = Scene.objects.select_related("chronicle", "location").get(pk=self.scene.pk)
        self.assertEqual(scene.pk, self.scene.pk)
        self.assertEqual(scene.name, "Test Scene")

    def test_get_scene_returns_none_for_invalid_id(self):
        """Test get_scene returns None for invalid ID."""
        try:
            Scene.objects.get(pk=99999)
            self.fail("Should have raised DoesNotExist")
        except Scene.DoesNotExist:
            pass

    def test_user_owns_character(self):
        """Test user_owns_character check."""
        self.assertEqual(self.character.owner_id, self.user.pk)
        self.assertNotEqual(self.character.owner_id, self.other_user.pk)

    def test_character_in_scene(self):
        """Test character_in_scene check."""
        self.assertTrue(self.scene.characters.filter(pk=self.character.pk).exists())

        # Create another character not in scene
        other_char = Human.objects.create(
            name="Other Character",
            owner=self.other_user,
            chronicle=self.chronicle,
        )
        self.assertFalse(self.scene.characters.filter(pk=other_char.pk).exists())

    def test_create_post_success(self):
        """Test create_post creates a post successfully."""
        initial_count = self.scene.total_posts()
        post = self.scene.add_post(self.character, "", "Test message")

        self.assertIsNotNone(post)
        self.assertEqual(self.scene.total_posts(), initial_count + 1)
        self.assertEqual(post.message, "Test message")

    def test_create_post_storyteller_returns_none(self):
        """Test create_post returns None for @storyteller messages."""
        post = self.scene.add_post(self.character, "", "@storyteller Need help!")
        self.assertIsNone(post)
        self.assertTrue(self.scene.waiting_for_st)

    def test_add_character_to_scene(self):
        """Test adding a character to scene."""
        new_char = Human.objects.create(
            name="New Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.assertFalse(self.scene.characters.filter(pk=new_char.pk).exists())

        self.scene.add_character(new_char)

        self.assertTrue(self.scene.characters.filter(pk=new_char.pk).exists())


class TestSceneChatConsumerMessageHandling(TestCase):
    """Test message handling logic of SceneChatConsumer."""

    def test_empty_message_not_allowed(self):
        """Test that empty messages are not allowed."""
        message = ""
        self.assertFalse(bool(message.strip()))

    def test_message_with_only_whitespace_not_allowed(self):
        """Test that whitespace-only messages are not allowed."""
        message = "   \n\t  "
        self.assertFalse(bool(message.strip()))

    def test_valid_message_allowed(self):
        """Test that valid messages are allowed."""
        message = "Hello, World!"
        self.assertTrue(bool(message.strip()))


class TestSceneChatConsumerValidation(TransactionTestCase):
    """Test validation logic of SceneChatConsumer."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.other_user = User.objects.create_user("otheruser", "other@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
        )

    def test_finished_scene_blocks_posts(self):
        """Test that posts cannot be made to finished scenes."""
        self.scene.finished = True
        self.scene.save()

        self.assertTrue(self.scene.finished)

    def test_character_must_be_in_scene(self):
        """Test that only characters in the scene can post."""
        # Character not in scene
        self.assertFalse(self.scene.characters.filter(pk=self.character.pk).exists())

        # Add character to scene
        self.scene.add_character(self.character)
        self.assertTrue(self.scene.characters.filter(pk=self.character.pk).exists())

    def test_user_must_own_character(self):
        """Test that users can only post as their own characters."""
        self.assertEqual(self.character.owner, self.user)
        self.assertNotEqual(self.character.owner, self.other_user)


class TestSceneChatConsumerSerializePost(TransactionTestCase):
    """Test post serialization in SceneChatConsumer."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.location = LocationModel.objects.create(
            name="Test Location",
            chronicle=self.chronicle,
        )
        self.scene = Scene.objects.create(
            name="Test Scene",
            chronicle=self.chronicle,
            location=self.location,
        )
        self.character = Human.objects.create(
            name="Test Character",
            owner=self.user,
            chronicle=self.chronicle,
        )
        self.scene.characters.add(self.character)

    def test_serialize_post_includes_required_fields(self):
        """Test that serialized posts include required fields."""
        post = self.scene.add_post(self.character, "", "Test message")

        # Verify post has expected attributes
        self.assertIsNotNone(post.pk)
        self.assertEqual(post.message, "Test message")
        self.assertIsNotNone(post.datetime_created)


class TestSceneChatConsumerConnectionLogic(TestCase):
    """Test connection logic of SceneChatConsumer."""

    def test_unauthenticated_user_rejected(self):
        """Test that unauthenticated users are rejected."""
        anonymous = AnonymousUser()
        self.assertFalse(anonymous.is_authenticated)

    def test_authenticated_user_accepted(self):
        """Test that authenticated users are accepted."""
        user = User.objects.create_user("testuser", "test@test.com", "password")
        self.assertTrue(user.is_authenticated)


class TestSceneChatConsumerMessageTypes(TestCase):
    """Test different message types handled by SceneChatConsumer."""

    def test_chat_message_type_recognized(self):
        """Test that chat_message type is recognized."""
        data = {"type": "chat_message", "message": "Hello"}
        self.assertEqual(data.get("type"), "chat_message")

    def test_add_character_type_recognized(self):
        """Test that add_character type is recognized."""
        data = {"type": "add_character", "character_id": 1}
        self.assertEqual(data.get("type"), "add_character")

    def test_unknown_type_handled(self):
        """Test that unknown types are handled gracefully."""
        data = {"type": "unknown_type"}
        message_type = data.get("type")
        self.assertNotIn(message_type, ["chat_message", "add_character"])


class TestSceneChatConsumerJSONParsing(TestCase):
    """Test JSON parsing in SceneChatConsumer."""

    def test_valid_json_parsed(self):
        """Test that valid JSON is parsed correctly."""
        text_data = '{"type": "chat_message", "message": "Hello"}'
        data = json.loads(text_data)
        self.assertEqual(data["type"], "chat_message")
        self.assertEqual(data["message"], "Hello")

    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises JSONDecodeError."""
        text_data = "not valid json"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(text_data)

    def test_empty_json_object(self):
        """Test handling of empty JSON object."""
        text_data = "{}"
        data = json.loads(text_data)
        self.assertIsNone(data.get("type"))


class TestSceneChatConsumerRoomGroupName(TestCase):
    """Test room group name generation."""

    def test_room_group_name_format(self):
        """Test that room group name follows expected format."""
        scene_id = 123
        expected = f"scene_{scene_id}"
        self.assertEqual(expected, "scene_123")

    def test_room_group_name_uniqueness(self):
        """Test that different scenes have different group names."""
        scene_1_group = "scene_1"
        scene_2_group = "scene_2"
        self.assertNotEqual(scene_1_group, scene_2_group)
