"""Scene chat consumer: the quote alias and the Step 0 audience pins.

The HTML protocol itself is covered in ``test_scene_chat_socket``.
"""

import json

from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, TransactionTestCase

from characters.models.core import Human
from game.consumers import CLOSE_DENIED, CLOSE_OUTDATED, SceneChatConsumer
from game.models import Chronicle, Post, Scene


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


class TestSceneSocketAuthorization(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user("scene-owner")
        self.other = User.objects.create_user("other-player")
        self.chronicle = Chronicle.objects.create(name="Socket chronicle")
        self.scene = Scene.objects.create(name="Private scene", chronicle=self.chronicle)
        self.character = Human.objects.create(
            name="Participant", owner=self.owner, chronicle=self.chronicle
        )
        self.scene.characters.add(self.character)

    def exchange(self, user, *messages, query="?v=2"):
        """Connect as ``user``, send ``messages``; return (close code or None, texts)."""

        async def attempt():
            communicator = WebsocketCommunicator(
                SceneChatConsumer.as_asgi(), f"/ws/scene/{self.scene.pk}/{query}"
            )
            communicator.scope["user"] = user
            communicator.scope["url_route"] = {"kwargs": {"scene_id": str(self.scene.pk)}}
            await communicator.connect()
            for message in messages:
                await communicator.send_to(text_data=json.dumps(message))
            code, texts = None, []
            while not await communicator.receive_nothing(0.2):
                output = await communicator.receive_output()
                if output["type"] == "websocket.close":
                    code = output.get("code")
                    break
                texts.append(output["text"])
            await communicator.disconnect()
            return code, texts

        return async_to_sync(attempt)()

    def test_private_scene_rejects_unrelated_and_anonymous_readers(self):
        self.assertEqual(self.exchange(AnonymousUser())[0], CLOSE_DENIED)
        self.assertEqual(self.exchange(self.other)[0], CLOSE_DENIED)
        self.assertIsNone(self.exchange(self.owner)[0])

    def test_public_scene_allows_anonymous_reader_but_no_ownerless_post(self):
        self.scene.visibility = Scene.Visibility.PUBLIC
        self.scene.save(update_fields=["visibility"])
        ownerless = Human.objects.create(name="Ownerless", chronicle=self.chronicle)
        self.scene.characters.add(ownerless)
        code, texts = self.exchange(
            AnonymousUser(),
            {"action": "post", "character": str(ownerless.pk), "message": "Forged post"},
        )
        self.assertIsNone(code)
        self.assertIn("You can only post as your own characters", "".join(texts))
        self.assertEqual(Post.objects.filter(scene=self.scene).count(), 0)

    def test_character_from_other_chronicle_cannot_join(self):
        """Adding characters is an HTTP action (AddCharForm); the socket has no such action."""
        other_chronicle = Chronicle.objects.create(name="Other socket chronicle")
        other_character = Human.objects.create(
            name="Other character", owner=self.owner, chronicle=other_chronicle
        )
        for message in (
            {"action": "add_character", "character_id": other_character.pk},
            {"type": "add_character", "character_id": other_character.pk},
        ):
            code, texts = self.exchange(self.owner, message)
            self.assertIsNone(code)
            self.assertIn("Unknown action.", "".join(texts))
        self.assertFalse(self.scene.characters.filter(pk=other_character.pk).exists())

    def test_json_protocol_is_closed_as_outdated(self):
        """Tabs from before Step 11 connect without ?v=2; their script then posts over HTTP."""
        for query in ("", "?v=1", "?v=3"):
            with self.subTest(query=query):
                code, texts = self.exchange(
                    self.owner,
                    {"type": "chat_message", "character_id": self.character.pk, "message": "Hi"},
                    query=query,
                )
                self.assertEqual(code, CLOSE_OUTDATED)
                self.assertEqual(texts, [])
        self.assertFalse(Post.objects.filter(scene=self.scene).exists())
