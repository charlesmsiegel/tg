"""Scene chat without sockets (Step 11): partial, selectors, posting service, broadcasts."""

import asyncio

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse

from characters.models.core.human import Human
from core.actions import ActionFailed
from core.permissions import PermissionManager
from core.tests.action_audience import ActionAudienceMixin
from game import scene_chat
from game.forms import PostForm
from game.models import Post, Scene
from game.selectors import (
    scene_post,
    scene_post_window,
    scene_posts_after,
    scene_storyteller_ids,
)


class GroupListener:
    """Joins a scene's group on the in-memory channel layer and reads its events."""

    def __init__(self, scene):
        self.layer = get_channel_layer()
        async_to_sync(self.layer.flush)()
        self.channel = async_to_sync(self.layer.new_channel)()
        async_to_sync(self.layer.group_add)(scene_chat.group_name(scene.pk), self.channel)

    def events(self):
        async def drain():
            received = []
            while True:
                try:
                    received.append(await asyncio.wait_for(self.layer.receive(self.channel), 0.05))
                except asyncio.TimeoutError:
                    return received

        return async_to_sync(drain)()


class SceneChatBase(ActionAudienceMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.character = Human.objects.create(
            name="Scene Hero", owner=self.users["owner"], chronicle=self.chronicle, status="App"
        )
        self.st_character = Human.objects.create(
            name="Narrator", owner=self.users["st"], chronicle=self.chronicle, status="App"
        )
        self.scene = Scene.objects.create(name="Opening", chronicle=self.chronicle)
        self.scene.characters.add(self.character, self.st_character)

    def post(self, character, message, display=""):
        return Post.objects.create(
            scene=self.scene, character=character, display_name=display or character.name,
            message=message,
        )


class StorytellerIdsTests(SceneChatBase):
    def test_agrees_with_can_manage_scope_for_every_role(self):
        head = get_user_model().objects.create_user("action_head")
        root = get_user_model().objects.create_user("action_root", is_superuser=True)
        self.chronicle.head_st = head
        self.chronicle.save()
        users = [user for user in self.users.values() if user is not None] + [head, root]
        found = scene_storyteller_ids(self.scene, [user.pk for user in users])
        for user in users:
            with self.subTest(user=user.username):
                expected = PermissionManager.can_manage_scope(
                    user, self.scene.chronicle, self.scene.gameline
                )
                self.assertEqual(user.pk in found, expected)

    def test_one_query_and_no_query_without_users(self):
        with self.assertNumQueries(0):
            self.assertEqual(scene_storyteller_ids(self.scene, [None]), set())
        with self.assertNumQueries(1):
            scene_storyteller_ids(self.scene, [self.users["st"].pk, self.users["owner"].pk])

    def test_scene_without_chronicle_only_knows_staff(self):
        scene = Scene.objects.create(name="Loose")
        ids = [self.users["staff"].pk, self.users["st"].pk]
        self.assertEqual(scene_storyteller_ids(scene, ids), {self.users["staff"].pk})


class PostWindowTests(SceneChatBase):
    def test_latest_window_oldest_first_with_earlier_flag(self):
        posts = [self.post(self.character, f"Post {n}") for n in range(5)]
        window, has_earlier = scene_post_window(self.scene, limit=3)
        self.assertEqual([p.pk for p in window], [p.pk for p in posts[2:]])
        self.assertTrue(has_earlier)
        window, has_earlier = scene_post_window(self.scene, before=posts[2].pk, limit=3)
        self.assertEqual([p.pk for p in window], [p.pk for p in posts[:2]])
        self.assertFalse(has_earlier)

    def test_after_and_overflow(self):
        posts = [self.post(self.character, f"Post {n}") for n in range(5)]
        after, more = scene_posts_after(self.scene, posts[1].pk, limit=2)
        self.assertEqual([p.pk for p in after], [posts[2].pk, posts[3].pk])
        self.assertTrue(more)
        after, more = scene_posts_after(self.scene, posts[3].pk, limit=2)
        self.assertEqual([p.pk for p in after], [posts[4].pk])
        self.assertFalse(more)

    def test_author_roles_are_scoped_to_this_scene(self):
        other_st = Human.objects.create(
            name="Visitor", owner=self.users["other_chronicle_st"], chronicle=self.chronicle
        )
        self.scene.characters.add(other_st)
        by_st = self.post(self.st_character, "Rain falls.")
        by_other_st = self.post(other_st, "Hi.")
        by_owner = self.post(self.character, "Hello.")
        window, _ = scene_post_window(self.scene)
        roles = {post.pk: post.author_is_st for post in window}
        self.assertEqual(roles, {by_st.pk: True, by_other_st.pk: False, by_owner.pk: False})

    def test_window_costs_two_queries_whatever_its_size(self):
        for n in range(30):
            self.post(self.character if n % 2 else self.st_character, f"Post {n}")
        with self.assertNumQueries(2):
            scene_post_window(self.scene)

    def test_single_post_belongs_to_the_scene(self):
        other_scene = Scene.objects.create(name="Elsewhere", chronicle=self.chronicle)
        stray = Post.objects.create(scene=other_scene, character=self.character, message="x")
        self.assertIsNone(scene_post(self.scene, stray.pk))
        mine = self.post(self.character, "Here")
        self.assertEqual(scene_post(self.scene, mine.pk), mine)


class PostPartialTests(SceneChatBase):
    def render(self, post, viewer=None):
        post = scene_post(self.scene, post.pk)
        return render_to_string(
            "game/scene/_post.html", {"post": post, "viewer_id": getattr(viewer, "pk", None)}
        )

    def test_markup(self):
        post = self.post(self.character, 'She said "run" <script>alert(1)</script><b>now</b>')
        html = self.render(post, self.users["player"])
        self.assertIn(f'id="post-{post.pk}"', html)
        self.assertIn(f'data-post-id="{post.pk}"', html)
        # The page showed href="" for every post: the joined character is the
        # base model, which has no get_absolute_url (regression).
        self.assertIn(f'href="{self.character.get_absolute_url()}"', html)
        self.assertIn('<span class="quote">"run"</span>', html)
        self.assertIn("<b>now</b>", html)
        self.assertNotIn("<script", html)
        self.assertNotIn('class="highlight"', html)
        self.assertNotIn('class="st"', html)

    def test_display_name_is_escaped(self):
        html = self.render(self.post(self.character, "Hi", display="<i>Bob</i>"))
        self.assertIn("&lt;i&gt;Bob&lt;/i&gt;", html)

    def test_highlight_only_for_the_viewers_own_posts(self):
        post = self.post(self.character, "Mine")
        self.assertIn('class="highlight"', self.render(post, self.users["owner"]))
        self.assertNotIn('class="highlight"', self.render(post, self.users["player"]))
        self.assertNotIn('class="highlight"', self.render(post))

    def test_storyteller_style_wins_for_everyone(self):
        post = self.post(self.st_character, "Rain falls.")
        for viewer in (self.users["st"], self.users["owner"], None):
            html = self.render(post, viewer)
            self.assertIn('class="st"', html)
            self.assertNotIn('class="highlight"', html)

    def test_ownerless_post_has_no_link(self):
        post = Post.objects.create(scene=self.scene, character=None, display_name="Voice")
        html = self.render(post)
        self.assertIn("Voice", html)
        self.assertNotIn("href", html)

    def test_page_renders_posts_with_the_partial(self):
        post = self.post(self.character, "Mine")
        self.client.force_login(self.users["owner"])
        response = self.client.get(self.scene.get_absolute_url())
        self.assertTemplateUsed(response, "game/scene/_post.html")
        self.assertContains(response, self.render(post, self.users["owner"]), html=True)


class PageWindowTests(SceneChatBase):
    def test_long_scene_shows_the_latest_window_and_pages_back(self):
        posts = [self.post(self.character, f"Post number {n}") for n in range(105)]
        self.client.force_login(self.users["owner"])
        response = self.client.get(self.scene.get_absolute_url())
        self.assertNotContains(response, f'id="post-{posts[4].pk}"')
        self.assertContains(response, f'id="post-{posts[5].pk}"')
        self.assertContains(response, f'href="?before={posts[5].pk}"')
        response = self.client.get(self.scene.get_absolute_url(), {"before": posts[5].pk})
        self.assertContains(response, f'id="post-{posts[0].pk}"')
        self.assertNotContains(response, f'id="post-{posts[5].pk}"')
        self.assertNotContains(response, "?before=")
        self.assertContains(response, "Back to the latest posts")

    def test_junk_cursor_is_ignored(self):
        self.post(self.character, "Only")
        self.client.force_login(self.users["owner"])
        for junk in ("x", "-3", "0", ""):
            with self.subTest(junk=junk):
                response = self.client.get(self.scene.get_absolute_url(), {"before": junk})
                self.assertContains(response, "Only")


class CreatePostTests(SceneChatBase):
    def form(self, message, user="owner", **data):
        form = PostForm(
            data={"message": message, "display_name": "", **data},
            user=self.users[user],
            scene=self.scene,
        )
        self.assertTrue(form.is_valid(), form.errors)
        return form

    def test_posts_as_the_only_character_with_straight_quotes(self):
        with self.captureOnCommitCallbacks(execute=True):
            result = scene_chat.create_post(self.scene, self.form("“Hi”, it’s me"))
        self.assertTrue(result.success)
        self.assertEqual(result.object.message, "\"Hi\", it's me")
        self.assertEqual(result.object.character, self.character)
        self.assertEqual(result.object.display_name, "Scene Hero")

    def test_storyteller_message_is_a_success_without_a_post(self):
        result = scene_chat.create_post(self.scene, self.form("@storyteller I need help"))
        self.assertIsNone(result.object)
        self.assertEqual(result.message, "Message sent to the storyteller.")
        self.assertFalse(Post.objects.filter(scene=self.scene).exists())

    def test_malformed_command_is_refused_regression(self):
        with self.assertRaisesMessage(ActionFailed, "Command does not match"):
            scene_chat.create_post(self.scene, self.form("Leap /extended nonsense"))
        self.assertFalse(Post.objects.filter(scene=self.scene).exists())

    def test_broadcast_only_after_commit(self):
        listener = GroupListener(self.scene)
        with self.captureOnCommitCallbacks() as callbacks:
            result = scene_chat.create_post(self.scene, self.form("Hello"))
        self.assertEqual(listener.events(), [])
        for callback in callbacks:
            callback()
        self.assertEqual(
            listener.events(), [{"type": "scene.post", "post_id": result.object.pk}]
        )

    def test_can_post(self):
        self.assertTrue(scene_chat.can_post(self.users["owner"], self.scene))
        self.assertFalse(scene_chat.can_post(self.users["player"], self.scene))
        self.assertFalse(scene_chat.can_post(self.users["staff"], self.scene))
        anonymous = type("Anon", (), {"is_authenticated": False})()
        self.assertFalse(scene_chat.can_post(anonymous, self.scene))
        self.scene.finished = True
        self.assertFalse(scene_chat.can_post(self.users["owner"], self.scene))


class HttpActionBroadcastTests(SceneChatBase):
    """Step 5's endpoints announce their changes to open sockets (finding 1)."""

    def setUp(self):
        super().setUp()
        self.listener = GroupListener(self.scene)

    def messages(self, response):
        return [str(m) for m in get_messages(response.wsgi_request)]

    def test_http_post_is_broadcast_regression(self):
        self.client.force_login(self.users["owner"])
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("game:scene_post", kwargs={"pk": self.scene.pk}), {"message": "Hello"}
            )
        post = Post.objects.get(scene=self.scene)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.listener.events(), [{"type": "scene.post", "post_id": post.pk}])

    def test_http_storyteller_message_is_reported_as_such(self):
        self.client.force_login(self.users["owner"])
        response = self.client.post(
            reverse("game:scene_post", kwargs={"pk": self.scene.pk}),
            {"message": "@storyteller help"},
        )
        self.assertIn("Message sent to the storyteller.", self.messages(response))

    def test_http_bad_command_is_an_error_regression(self):
        self.client.force_login(self.users["owner"])
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("game:scene_post", kwargs={"pk": self.scene.pk}),
                {"message": "Leap /extended nonsense"},
            )
        self.assertIn("Command does not match the expected format.", self.messages(response))
        self.assertFalse(Post.objects.filter(scene=self.scene).exists())
        self.assertEqual(self.listener.events(), [])

    def test_added_character_is_broadcast(self):
        newcomer = Human.objects.create(
            name="Newcomer", owner=self.users["owner"], chronicle=self.chronicle
        )
        self.client.force_login(self.users["owner"])
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(
                reverse("game:scene_add_character", kwargs={"pk": self.scene.pk}),
                {"character_to_add": newcomer.pk},
            )
        self.assertEqual(
            self.listener.events(), [{"type": "scene.characters", "character_id": newcomer.pk}]
        )

    def test_close_is_broadcast(self):
        self.client.force_login(self.users["st"])
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("game:scene_close", kwargs={"pk": self.scene.pk}))
        self.assertEqual(self.listener.events(), [{"type": "scene.closed"}])

    def test_refused_actions_broadcast_nothing(self):
        self.client.force_login(self.users["player"])
        with self.captureOnCommitCallbacks(execute=True):
            self.client.post(reverse("game:scene_close", kwargs={"pk": self.scene.pk}))
            self.client.post(
                reverse("game:scene_post", kwargs={"pk": self.scene.pk}), {"message": "Hi"}
            )
        self.assertEqual(self.listener.events(), [])
