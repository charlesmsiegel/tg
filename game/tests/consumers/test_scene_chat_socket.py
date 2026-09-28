"""The scene chat socket's HTML protocol (Step 11), end to end through Channels."""

import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import TransactionTestCase
from django.urls import reverse

from characters.models.core.human import Human
from core.tests.action_audience import ActionAudienceMixin
from game import scene_chat
from game.consumers import CLOSE_DENIED, CLOSE_NORMAL, SceneChatConsumer
from game.models import Post, Scene
from game.selectors import SCENE_POST_WINDOW, scene_post


class SocketTestBase(ActionAudienceMixin, TransactionTestCase):
    """Owner and ST each play a character in an open scene of their chronicle."""

    def setUp(self):
        super().setUp()
        async_to_sync(get_channel_layer().flush)()
        self.character = Human.objects.create(
            name="Scene Hero", owner=self.users["owner"], chronicle=self.chronicle
        )
        self.st_character = Human.objects.create(
            name="Narrator", owner=self.users["st"], chronicle=self.chronicle
        )
        # A chronicle member who is not in the scene.
        self.bystander = Human.objects.create(
            name="Bystander", owner=self.users["player"], chronicle=self.chronicle
        )
        self.scene = Scene.objects.create(name="Opening", chronicle=self.chronicle)
        self.scene.characters.add(self.character, self.st_character)

    def run_async(self, coroutine_function):
        return async_to_sync(coroutine_function)()

    async def open(self, who, query="?v=2"):
        communicator = WebsocketCommunicator(
            SceneChatConsumer.as_asgi(), f"/ws/scene/{self.scene.pk}/{query}"
        )
        communicator.scope["user"] = self.users.get(who) or AnonymousUser()
        communicator.scope["url_route"] = {"kwargs": {"scene_id": str(self.scene.pk)}}
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        return communicator

    async def drain(self, communicator, timeout=0.3):
        """Every frame sent until the socket goes quiet (or closes).

        ``receive_nothing`` waits without cancelling the application, which a
        timed-out ``receive_output`` would do.
        """
        frames = []
        while not await communicator.receive_nothing(timeout):
            output = await communicator.receive_output()
            frames.append(output)
            if output["type"] == "websocket.close":
                break
        return frames

    @staticmethod
    def text(frames):
        return "".join(frame.get("text", "") for frame in frames)

    @staticmethod
    def close_code(frames):
        closes = [frame for frame in frames if frame["type"] == "websocket.close"]
        return closes[-1].get("code", CLOSE_NORMAL) if closes else None

    async def send(self, communicator, **data):
        await communicator.send_to(text_data=json.dumps(data))

    def posts(self):
        return list(Post.objects.filter(scene=self.scene).order_by("pk"))

    def expected_post_html(self, post, viewer):
        post = scene_post(self.scene, post.pk)
        return render_to_string(
            "game/scene/ws/_posts.html",
            {"posts": [post], "viewer_id": getattr(self.users.get(viewer), "pk", None)},
        )


class ConnectTests(SocketTestBase):
    def test_audience_matrix(self):
        expected = {
            "owner": True,
            "player": True,  # has a character in the chronicle
            "st": True,
            "other_line_st": True,
            "other_chronicle_st": False,
            "staff": True,
            "anonymous": False,
        }

        async def attempt(who):
            communicator = await self.open(who)
            frames = await self.drain(communicator, timeout=0.1)
            await communicator.disconnect()
            return self.close_code(frames)

        for who, allowed in expected.items():
            with self.subTest(who=who):
                code = async_to_sync(attempt)(who)
                self.assertEqual(code, None if allowed else CLOSE_DENIED)

    def test_missing_and_hidden_scenes_close_alike(self):
        hidden = Scene.objects.create(
            name="Secret", chronicle=self.chronicle, visibility=Scene.Visibility.PARTICIPANTS
        )

        async def attempt(scene_id):
            communicator = WebsocketCommunicator(
                SceneChatConsumer.as_asgi(), f"/ws/scene/{scene_id}/?v=2"
            )
            communicator.scope["user"] = self.users["player"]
            communicator.scope["url_route"] = {"kwargs": {"scene_id": str(scene_id)}}
            await communicator.connect()
            return await self.drain(communicator, timeout=0.1)

        self.assertEqual(self.close_code(async_to_sync(attempt)(hidden.pk)), CLOSE_DENIED)
        self.assertEqual(self.close_code(async_to_sync(attempt)(999999)), CLOSE_DENIED)

    def test_public_scene_admits_anonymous_readers(self):
        self.scene.visibility = Scene.Visibility.PUBLIC
        self.scene.save()

        async def attempt():
            communicator = await self.open("anonymous")
            frames = await self.drain(communicator, timeout=0.1)
            await communicator.disconnect()
            return frames

        self.assertIsNone(self.close_code(self.run_async(attempt)))


class PostTests(SocketTestBase):
    def test_post_is_rendered_for_each_recipient(self):
        async def scenario():
            owner = await self.open("owner")
            st = await self.open("st")
            await self.send(owner, action="post", character="", display_name="", message="Hi")
            return await self.drain(owner), await self.drain(st)

        owner_frames, st_frames = self.run_async(scenario)
        [post] = self.posts()
        owner_text, st_text = self.text(owner_frames), self.text(st_frames)
        # The sender gets fresh fields (autofocused) and a cleared notice.
        self.assertIn('id="post-message-fields" hx-swap-oob="true"', owner_text)
        self.assertIn("autofocus", owner_text)
        self.assertIn('<div id="scene-chat-notice" hx-swap-oob="innerHTML"></div>', owner_text)
        self.assertNotIn("post-message-fields", st_text)
        # Each connection gets the partial rendered for its own viewer.
        self.assertIn(self.expected_post_html(post, "owner"), owner_text)
        self.assertEqual(st_text, self.expected_post_html(post, "st"))
        self.assertIn('class="highlight"', owner_text)
        self.assertNotIn('class="highlight"', st_text)

    def test_quotes_are_straightened_and_the_chosen_character_used(self):
        second = Human.objects.create(
            name="Sidekick", owner=self.users["owner"], chronicle=self.chronicle
        )
        self.scene.characters.add(second)

        async def scenario():
            owner = await self.open("owner")
            await self.send(
                owner,
                action="post",
                character=str(second.pk),
                display_name="",
                message="“Hi”",
            )
            return await self.drain(owner)

        self.run_async(scenario)
        [post] = self.posts()
        self.assertEqual((post.character_id, post.message), (second.pk, '"Hi"'))

    def test_refused_posts_write_nothing_and_keep_the_typed_text(self):
        self.scene.visibility = Scene.Visibility.PUBLIC
        self.scene.save()
        cases = [
            (
                "owner",
                {"character": str(self.st_character.pk), "message": "Forged"},
                "Character: Select a valid choice.",
            ),
            ("player", {"message": "Not in the scene"}, "You can only post as your own"),
            ("staff", {"message": "Staff without a character"}, "You can only post as your own"),
            (
                "anonymous",
                {"character": str(self.character.pk), "message": "Hi"},
                "You can only post as your own",
            ),
            ("owner", {"message": "   "}, "Message: This field is required."),
            (
                "owner",
                {"message": "Hi", "display_name": "x" * 101},
                "Display name: Ensure this value has at most 100 characters",
            ),
            (
                "owner",
                {"message": "Leap /extended nonsense"},
                "Command does not match the expected format.",
            ),
        ]

        async def attempt(who, fields):
            sender = await self.open(who)
            witness = await self.open("st")
            await self.send(sender, action="post", **fields)
            return await self.drain(sender), await self.drain(witness)

        for who, fields, error in cases:
            with self.subTest(who=who, fields=fields):
                sent, seen = async_to_sync(attempt)(who, fields)
                text = self.text(sent)
                self.assertIn('class="tg-message error"', text)
                self.assertIn(error, text)
                self.assertNotIn("post-message-fields", text)
                self.assertEqual(seen, [])
                self.assertEqual(self.posts(), [])

    def test_finished_scene_refuses_posts(self):
        async def scenario():
            owner = await self.open("owner")
            await database_sync_to_async(Scene.objects.filter(pk=self.scene.pk).update)(
                finished=True
            )
            await self.send(owner, action="post", message="Too late")
            return await self.drain(owner)

        self.assertIn("This scene is closed.", self.text(self.run_async(scenario)))
        self.assertEqual(self.posts(), [])

    def test_storyteller_message_is_acknowledged_without_a_post(self):
        async def scenario():
            owner = await self.open("owner")
            st = await self.open("st")
            await self.send(owner, action="post", message="@storyteller help")
            return await self.drain(owner), await self.drain(st)

        sent, seen = self.run_async(scenario)
        self.assertIn("Message sent to the storyteller.", self.text(sent))
        self.assertIn("post-message-fields", self.text(sent))
        self.assertEqual(seen, [])
        self.assertEqual(self.posts(), [])

    def test_http_post_reaches_open_sockets(self):
        async def scenario():
            st = await self.open("st")

            def post_over_http():
                self.client.force_login(self.users["owner"])
                self.client.post(
                    reverse("game:scene_post", kwargs={"pk": self.scene.pk}),
                    {"message": "Via HTTP"},
                )

            await database_sync_to_async(post_over_http)()
            return await self.drain(st)

        text = self.text(self.run_async(scenario))
        [post] = self.posts()
        self.assertEqual(text, self.expected_post_html(post, "st"))

    def test_bad_frames_get_a_notice_and_keep_the_connection(self):
        async def scenario():
            owner = await self.open("owner")
            replies = []
            for frame in ("not json", "[1, 2]", json.dumps({"action": "dance"})):
                await owner.send_to(text_data=frame)
                replies.append(self.text(await self.drain(owner)))
            await self.send(owner, action="post", message="Still here")
            replies.append(self.text(await self.drain(owner)))
            return replies

        bad_json, not_object, unknown, ok = self.run_async(scenario)
        self.assertIn("Invalid message format.", bad_json)
        self.assertIn("Invalid message format.", not_object)
        self.assertIn("Unknown action.", unknown)
        self.assertIn("Still here", ok)

    def test_oversized_frame_is_refused(self):
        async def scenario():
            owner = await self.open("owner")
            with self.settings(DATA_UPLOAD_MAX_MEMORY_SIZE=100):
                await self.send(owner, action="post", message="x" * 200)
                return await self.drain(owner)

        self.assertIn("Message too large.", self.text(self.run_async(scenario)))
        self.assertEqual(self.posts(), [])


class SyncTests(SocketTestBase):
    def make_posts(self, count):
        return [
            Post.objects.create(
                scene=self.scene,
                character=self.character,
                display_name="Hero",
                message=f"Post {n}",
            )
            for n in range(count)
        ]

    def test_sync_sends_the_posts_after_the_last_seen(self):
        posts = self.make_posts(3)

        async def scenario():
            owner = await self.open("owner")
            await self.send(owner, action="sync", after=posts[0].pk)
            first = self.text(await self.drain(owner))
            await self.send(owner, action="sync", after=posts[2].pk)
            return first, await self.drain(owner)

        text, nothing = self.run_async(scenario)
        self.assertTrue(text.startswith('<div hx-swap-oob="beforeend:#posts-container">'))
        self.assertNotIn(f'id="post-{posts[0].pk}"', text)
        self.assertIn(f'id="post-{posts[1].pk}"', text)
        self.assertIn(f'id="post-{posts[2].pk}"', text)
        self.assertLess(text.index(f"post-{posts[1].pk}"), text.index(f"post-{posts[2].pk}"))
        self.assertEqual(nothing, [])

    def test_too_many_missed_posts_ask_for_a_reload(self):
        self.make_posts(SCENE_POST_WINDOW + 1)

        async def scenario():
            owner = await self.open("owner")
            await self.send(owner, action="sync", after=0)
            return self.text(await self.drain(owner))

        text = self.run_async(scenario)
        self.assertIn("You missed more posts than can be shown here.", text)
        self.assertIn(f'href="{self.scene.get_absolute_url()}"', text)
        self.assertNotIn("post-item", text)

    def test_invalid_cursor(self):
        async def scenario():
            owner = await self.open("owner")
            replies = []
            for after in ("5", -1, True, None):
                await self.send(owner, action="sync", after=after)
                replies.append(self.text(await self.drain(owner)))
            return replies

        for reply in self.run_async(scenario):
            self.assertIn("Invalid message format.", reply)


class SceneEventTests(SocketTestBase):
    def test_character_joining_updates_each_viewers_own_regions(self):
        self.scene.visibility = Scene.Visibility.PUBLIC
        self.scene.save()
        newcomer = Human.objects.create(
            name="Newcomer", owner=self.users["owner"], chronicle=self.chronicle
        )

        def add_over_http():
            self.client.force_login(self.users["owner"])
            self.client.post(
                reverse("game:scene_add_character", kwargs={"pk": self.scene.pk}),
                {"character_to_add": newcomer.pk},
            )

        async def scenario():
            sockets = {who: await self.open(who) for who in ("owner", "st", "anonymous")}
            await database_sync_to_async(add_over_http)()
            return {who: self.text(await self.drain(socket)) for who, socket in sockets.items()}

        seen = self.run_async(scenario)
        for text in seen.values():
            self.assertIn("Newcomer joined the scene.", text)
        # The owner can now post as Newcomer too, so their choice becomes a select.
        self.assertIn(
            '<div id="post-character-field" class="mb-3" hx-swap-oob="true">', seen["owner"]
        )
        self.assertIn(f'<option value="{newcomer.pk}">Newcomer</option>', seen["owner"])
        self.assertNotIn("post-character-field", seen["st"])
        # Nobody is offered the newcomer any more.
        self.assertIn('id="add-char-field" hx-swap-oob="true"', seen["st"])
        self.assertNotIn(f'value="{newcomer.pk}"', seen["st"])
        self.assertIn(f'value="{self.bystander.pk}"', seen["st"])
        # Anonymous readers have no forms, so no regions to update.
        self.assertNotIn("add-char-field", seen["anonymous"])

    def test_closing_replaces_the_actions_and_ends_the_connection(self):
        def close_over_http():
            self.client.force_login(self.users["st"])
            self.client.post(reverse("game:scene_close", kwargs={"pk": self.scene.pk}))

        async def scenario():
            owner = await self.open("owner")
            await database_sync_to_async(close_over_http)()
            return await self.drain(owner)

        frames = self.run_async(scenario)
        self.assertIn('<div id="scene-actions" hx-swap-oob="true">', self.text(frames))
        self.assertIn("This scene has been closed.", self.text(frames))
        self.assertEqual(self.close_code(frames), CLOSE_NORMAL)

    def test_viewer_who_loses_access_is_disconnected(self):
        async def scenario():
            player = await self.open("player")
            await database_sync_to_async(Scene.objects.filter(pk=self.scene.pk).update)(
                visibility=Scene.Visibility.PARTICIPANTS
            )
            owner = await self.open("owner")
            await self.send(owner, action="post", message="Secret now")
            return await self.drain(player)

        frames = self.run_async(scenario)
        self.assertNotIn("Secret now", self.text(frames))
        self.assertEqual(self.close_code(frames), CLOSE_DENIED)

    def test_events_for_other_scenes_are_not_seen(self):
        other = Scene.objects.create(name="Elsewhere", chronicle=self.chronicle)
        other.characters.add(self.character)

        async def scenario():
            owner = await self.open("owner")
            await database_sync_to_async(
                lambda: scene_chat.broadcast(other.pk, scene_chat.SCENE_CLOSED)
            )()
            return await self.drain(owner)

        self.assertEqual(self.run_async(scenario), [])
