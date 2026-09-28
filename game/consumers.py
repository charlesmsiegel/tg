"""WebSocket consumer for live scene chat (Step 11).

Protocol v2 (``/ws/scene/<id>/?v=2``): the page's htmx ``ws`` extension sends
JSON objects built by ``ws-send`` (``{"action": "post", <PostForm fields>}``)
or by ``scene-chat.js`` (``{"action": "sync", "after": <post id>}``), and
receives HTML whose top-level elements it swaps out of band. Any other URL is
a tab from before the switch and is closed with 4400.

Group events carry ids, never markup: each connection re-checks its viewer's
access and renders the event for that viewer, so one viewer's rendering never
reaches another connection. Posting goes through ``game.scene_chat``, the same
path as the HTTP fallback. Posts delivered to a signed-in viewer count as read:
their scene read marker moves up to the newest one (``mark_read``), unless an
unread backlog before them has not been loaded on the page yet.
"""

import json
import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string

from characters.models.core import CharacterModel
from core.actions import ActionFailed
from game import scene_chat
from game.forms import AddCharForm, PostForm
from game.models import Scene, UserSceneReadStatus
from game.security import can_view_scene
from game.selectors import scene_cast, scene_post, scene_posts_after
from game.text import straighten_quotes

logger = logging.getLogger(__name__)

PROTOCOL = "2"  # /ws/scene/<id>/?v=2; the JSON protocol (v1) was removed in Step 11

# Close codes outside the htmx ws extension's retry list (1006, 1011-1013).
CLOSE_NORMAL = 1000
CLOSE_OUTDATED = 4400
CLOSE_DENIED = 4403

POST_FIELDS = ("character", "display_name", "message")


class SceneChatConsumer(AsyncWebsocketConsumer):
    """Live posts for one scene; see the module docstring for the protocol."""

    # Connection ------------------------------------------------------------

    async def connect(self):
        self.scene_id = int(self.scope["url_route"]["kwargs"]["scene_id"])
        self.room_group_name = scene_chat.group_name(self.scene_id)
        self.user = self.scope["user"]
        self.joined = False
        query = parse_qs(self.scope.get("query_string", b"").decode())

        # A refused handshake reaches the browser as 1006, which clients retry;
        # accepting and closing with a code of our own ends the retries.
        if query.get("v") != [PROTOCOL]:
            # A tab from before the switch: its script falls back to HTTP posting.
            await self.accept()
            await self.close(code=CLOSE_OUTDATED)
            return
        # Public scenes admit anonymous readers; every other audience is
        # checked before joining the broadcast group. Missing and hidden
        # scenes are refused alike.
        if not await self.can_view():
            await self.accept()
            await self.close(code=CLOSE_DENIED)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.joined = True
        await self.accept()
        logger.info("User %s connected to scene %s", self.user, self.scene_id)

    async def disconnect(self, close_code):
        if not self.joined:  # refused with 4400 or 4403
            return
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info("User %s disconnected from scene %s", self.user, self.scene_id)

    async def deliver(self, html):
        """Send a reply; ``None`` means the viewer can no longer read the scene."""
        if html is None:
            await self.close(code=CLOSE_DENIED)
        elif html:
            await self.send(text_data=html)

    # Client messages -------------------------------------------------------

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = self.decode(text_data)
            action = data.get("action")
            if action == "post":
                reply = await self.post_reply(data)
            elif action == "sync":
                reply = await self.sync_reply(data.get("after"))
            else:
                reply = self.notice(["Unknown action."])
        except ValueError as exc:
            reply = self.notice([str(exc)])
        except Exception:
            logger.exception("Error processing scene %s socket message", self.scene_id)
            reply = self.notice(["Could not process message."])
        await self.deliver(reply)

    def decode(self, text_data):
        if text_data is None:  # a binary frame
            raise ValueError("Invalid message format.")
        limit = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
        if limit is not None and len(text_data) > limit:
            raise ValueError("Message too large.")
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid message format.") from exc
        if not isinstance(data, dict):
            raise ValueError("Invalid message format.")
        return data

    @database_sync_to_async
    def post_reply(self, data):
        scene = self.visible_scene()
        if scene is None:
            return None
        fields = {name: data[name] for name in POST_FIELDS if isinstance(data.get(name), str)}
        errors, result = self.submit(scene, fields)
        if errors:
            return self.notice(errors)
        message_fields = render_to_string(
            "game/scene/_post_message_fields.html", {"oob": True, "autofocus": True}
        )
        # A post shows up through its broadcast; a storyteller message has none.
        info = [result.message] if result.object is None else []
        return message_fields + self.notice(info, level="info")

    @database_sync_to_async
    def sync_reply(self, after):
        # JSON numbers only: a string cursor is a client bug, not a request.
        after = scene_chat.post_cursor(after) if not isinstance(after, str) else None
        if after is None:
            raise ValueError("Invalid message format.")
        scene = self.visible_scene()
        if scene is None:
            return None
        posts, more = scene_posts_after(scene, after)
        if more:
            return self.notice(
                ["You missed more posts than can be shown here."],
                level="info",
                reload_url=scene.get_absolute_url(),
            )
        return self.render_posts(scene, posts)

    # Group events ----------------------------------------------------------

    async def scene_post(self, event):
        """A post was committed."""
        await self.deliver(await self.post_html(event["post_id"]))

    async def scene_characters(self, event):
        """A character joined the scene."""
        await self.deliver(await self.characters_html(event["character_id"]))

    async def scene_closed(self, event):
        """The scene was closed: no more posting, and no reason to stay connected."""
        html = await self.closed_html()
        if html is None:
            await self.close(code=CLOSE_DENIED)
            return
        await self.send(text_data=html)
        await self.close(code=CLOSE_NORMAL)

    @database_sync_to_async
    def post_html(self, post_id):
        scene = self.visible_scene()
        if scene is None:
            return None
        post = scene_post(scene, post_id)
        return self.render_posts(scene, [post]) if post is not None else ""

    @database_sync_to_async
    def characters_html(self, character_id):
        scene = self.visible_scene()
        if scene is None:
            return None
        character = CharacterModel.objects.filter(pk=character_id).first()
        if character is None:
            return ""
        parts = [
            self.notice([f"{character.name} joined the scene."], level="info"),
            render_to_string("game/scene/_cast.html", {"oob": True, "cast": scene_cast(scene)}),
        ]
        # Signed-in viewers of an open scene have the forms these regions live in.
        if self.user.is_authenticated and not scene.finished:
            if character.owner_id == self.user.pk:
                parts.append(
                    render_to_string(
                        "game/scene/_post_character_field.html",
                        {"oob": True, "post_characters": self.post_characters(scene)},
                    )
                )
            parts.append(
                render_to_string(
                    "game/scene/_add_character_field.html",
                    {"oob": True, "add_characters": self.add_characters(scene)},
                )
            )
        return "".join(parts)

    @database_sync_to_async
    def closed_html(self):
        if self.visible_scene() is None:
            return None
        return render_to_string("game/scene/ws/_closed.html") + self.notice(
            ["This scene has been closed."], level="info"
        )

    # Shared ----------------------------------------------------------------

    @property
    def viewer_id(self):
        return self.user.pk if self.user.is_authenticated else None

    def visible_scene(self):
        """The scene if this viewer may still read it (checked on every event)."""
        scene = (
            Scene.objects.select_related("chronicle", "location").filter(pk=self.scene_id).first()
        )
        if scene is None or not can_view_scene(self.user, scene):
            return None
        return scene

    @database_sync_to_async
    def can_view(self):
        return self.visible_scene() is not None

    def submit(self, scene, fields):
        """Authorize, validate and post like ``ScenePostView``: ``(errors, result)``."""
        if scene.finished:
            return ["This scene is closed."], None
        if not scene_chat.can_post(self.user, scene):
            return ["You can only post as your own characters in this scene."], None
        form = PostForm(data=fields, user=self.user, scene=scene)
        if not form.is_valid():
            return self.form_errors(form), None
        try:
            with transaction.atomic():
                return [], scene_chat.create_post(scene, form)
        except ActionFailed as exc:
            return [str(exc)], None

    @staticmethod
    def form_errors(form):
        errors = []
        for name, messages in form.errors.items():
            if name == "__all__":
                errors += messages
            else:
                label = form.fields[name].label or name.replace("_", " ").capitalize()
                errors += [f"{label}: {message}" for message in messages]
        return errors

    def post_characters(self, scene):
        return list(PostForm(user=self.user, scene=scene).character_queryset)

    def add_characters(self, scene):
        return list(AddCharForm(user=self.user, scene=scene).fields["character_to_add"].queryset)

    def render_posts(self, scene, posts):
        """New posts for this viewer, who has now seen them. Their read marker moves
        unless unread posts before these are still unloaded on their page."""
        if not posts:
            return ""
        if self.viewer_id is not None:
            UserSceneReadStatus.objects.mark_read(
                scene, self.viewer_id, posts[-1], shown_from=posts[0]
            )
        return render_to_string(
            "game/scene/ws/_posts.html", {"posts": posts, "viewer_id": self.viewer_id}
        )

    @staticmethod
    def notice(messages, level="error", reload_url=None):
        return render_to_string(
            "game/scene/ws/_notice.html",
            {"messages": messages, "level": level, "reload_url": reload_url},
        )

    # Kept because tests pin one straighten_quotes implementation (Step 4).
    straighten_quotes = staticmethod(straighten_quotes)
