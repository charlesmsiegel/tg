"""Scene read markers and the C4 "new" divider (Spread)."""

import re
from unittest import mock

from django.contrib.auth import get_user_model
from django.db import connection
from django.template.loader import render_to_string
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from accounts.models import Profile
from characters.models.core.human import Human
from game.models import Post, UserSceneReadStatus
from game.selectors import SCENE_POST_WINDOW, scene_post, scene_read_marker, unread_divider
from game.tests.test_scene_chat import SceneChatBase

DIVIDER = re.compile(r'<div class="tl-unread" id="unread-divider"[^>]*>New · (\d+)</div>')


class ReadMarkerBase(SceneChatBase):
    def status(self, who="owner"):
        return UserSceneReadStatus.objects.get(scene=self.scene, user=self.users[who])

    def set_status(self, who="owner", read=False, marker=None):
        UserSceneReadStatus.objects.update_or_create(
            scene=self.scene,
            user=self.users[who],
            defaults={"read": read, "last_read_post": marker},
        )

    def view(self, who="owner", **params):
        self.client.force_login(self.users[who])
        return self.client.get(self.scene.get_absolute_url(), params)

    def divider(self, response):
        """``(count, id of the post right after the divider)`` or ``None``."""
        html = response.content.decode()
        match = DIVIDER.search(html)
        if match is None:
            return None
        following = re.search(r'data-post-id="(\d+)"', html[match.end() :])
        return int(match.group(1)), int(following.group(1))


class RecordPostTests(ReadMarkerBase):
    def test_author_reads_through_their_post_and_others_have_it_unread(self):
        first = self.scene.add_post(self.character, "", "Hello")
        self.assertEqual(self.status("owner").last_read_post, first)
        self.assertTrue(self.status("owner").read)
        self.assertFalse(self.status("st").read)
        self.assertIsNone(self.status("st").last_read_post)

        reply = self.scene.add_post(self.st_character, "", "Welcome")
        self.assertEqual(self.status("st").last_read_post, reply)
        self.assertTrue(self.status("st").read)
        owner = self.status("owner")
        self.assertFalse(owner.read)
        self.assertEqual(owner.last_read_post, first)  # unchanged

    def test_rows_a_concurrent_first_post_created_get_this_posts_state(self):
        # Both first posts saw no rows; the other one's insert won the race (Codex).
        first = self.post(self.character, "First")
        insert = UserSceneReadStatus.objects.bulk_create

        def racing(rows, **kwargs):
            insert(
                [
                    UserSceneReadStatus(
                        user=self.users["owner"], scene=self.scene, read=True, last_read_post=first
                    ),
                    UserSceneReadStatus(user=self.users["st"], scene=self.scene, read=False),
                ],
                ignore_conflicts=True,
            )
            return insert(rows, **kwargs)

        with mock.patch.object(UserSceneReadStatus.objects, "bulk_create", racing):
            reply = self.scene.add_post(self.st_character, "", "Reply")
        self.assertFalse(self.status("owner").read)
        self.assertEqual((self.status("st").read, self.status("st").last_read_post), (True, reply))

    def test_rows_are_not_duplicated(self):
        for n in range(3):
            self.scene.add_post(self.character, "", f"Post {n}")
        self.assertEqual(UserSceneReadStatus.objects.filter(scene=self.scene).count(), 2)

    def test_posting_costs_the_same_whatever_the_cast(self):
        self.scene.add_post(self.character, "", "Warm up")
        with CaptureQueriesContext(connection) as small:
            self.scene.add_post(self.character, "", "One")
        for n in range(4):
            user = get_user_model().objects.create_user(f"extra{n}")
            self.scene.characters.add(
                Human.objects.create(name=f"Extra {n}", owner=user, chronicle=self.chronicle)
            )
        self.scene.add_post(self.character, "", "Warm up again")
        with CaptureQueriesContext(connection) as large:
            self.scene.add_post(self.character, "", "Two")
        self.assertEqual(len(large.captured_queries), len(small.captured_queries))


class MarkReadTests(ReadMarkerBase):
    def test_marker_never_moves_back(self):
        old, new = self.post(self.character, "Old"), self.post(self.character, "New")
        self.set_status(read=False, marker=new)
        UserSceneReadStatus.objects.mark_read(self.scene, self.users["owner"].pk, old)
        self.assertEqual(self.status().last_read_post, new)
        self.assertTrue(self.status().read)

    def test_defaults_to_the_latest_post(self):
        self.post(self.character, "One")
        latest = self.post(self.character, "Two")
        self.set_status(read=False)
        UserSceneReadStatus.objects.mark_read(self.scene, self.users["owner"].pk)
        self.assertEqual(self.status().last_read_post, latest)

    def test_a_newer_post_keeps_the_scene_unread(self):
        # The page showed ``shown``; ``newer`` landed before mark_read ran (Codex).
        shown = self.post(self.character, "Shown")
        newer = self.post(self.st_character, "Newer")
        self.set_status(read=False)
        UserSceneReadStatus.objects.mark_read(self.scene, self.users["owner"].pk, shown)
        status = self.status()
        self.assertEqual(status.last_read_post, shown)
        self.assertFalse(status.read)
        UserSceneReadStatus.objects.mark_read(self.scene, self.users["owner"].pk, newer)
        self.assertTrue(self.status().read)

    def test_shown_posts_do_not_skip_an_unread_backlog(self):
        read = self.post(self.character, "Read")
        self.post(self.st_character, "Not loaded")
        live = self.post(self.st_character, "Live")
        self.set_status(read=False, marker=read)
        owner = self.users["owner"].pk
        UserSceneReadStatus.objects.mark_read(self.scene, owner, live, shown_from=live)
        self.assertEqual(self.status().last_read_post, read)
        self.assertFalse(self.status().read)
        # Caught up to just before the shown posts: the marker moves.
        self.set_status(read=False, marker=Post.objects.get(message="Not loaded"))
        UserSceneReadStatus.objects.mark_read(self.scene, owner, live, shown_from=live)
        self.assertEqual(self.status().last_read_post, live)
        self.assertTrue(self.status().read)

    def test_an_empty_window_leaves_a_first_post_unread(self):
        # The page showed no posts; the first post landed before mark_read ran (Codex).
        self.set_status(read=False)
        self.post(self.st_character, "First")
        UserSceneReadStatus.objects.mark_read(self.scene, self.users["owner"].pk, None)
        self.assertFalse(self.status().read)
        self.assertIsNone(self.status().last_read_post)
        Post.objects.all().delete()
        UserSceneReadStatus.objects.mark_read(self.scene, self.users["owner"].pk, None)
        self.assertTrue(self.status().read)

    def test_a_reader_already_through_the_post_is_not_rewritten(self):
        shown = self.post(self.character, "Shown")
        self.set_status(read=True, marker=shown)
        owner = self.users["owner"].pk
        self.assertEqual(UserSceneReadStatus.objects.mark_read(self.scene, owner, shown), 0)
        newer = self.post(self.st_character, "Newer")
        self.set_status(read=False, marker=shown)
        self.assertEqual(UserSceneReadStatus.objects.mark_read(self.scene, owner, newer), 1)
        self.assertEqual((self.status().read, self.status().last_read_post), (True, newer))

    def test_only_updates_existing_rows(self):
        self.post(self.character, "One")
        self.assertEqual(
            UserSceneReadStatus.objects.mark_read(self.scene, self.users["player"].pk), 0
        )
        self.assertFalse(UserSceneReadStatus.objects.filter(user=self.users["player"]).exists())


class DividerSelectorTests(ReadMarkerBase):
    def test_marker_places_the_divider(self):
        posts = [self.post(self.character, f"Post {n}") for n in range(4)]
        found = unread_divider(self.scene, posts, read=False, marker=posts[1].pk, has_earlier=False)
        self.assertEqual(found, {"post_id": posts[2].pk, "count": 2})
        self.assertIsNone(
            unread_divider(self.scene, posts, read=True, marker=posts[3].pk, has_earlier=False)
        )

    def test_rows_without_a_marker(self):
        posts = [self.post(self.character, f"Post {n}") for n in range(2)]
        # Read before markers existed: nothing to show.
        self.assertIsNone(
            unread_divider(self.scene, posts, read=True, marker=None, has_earlier=False)
        )
        # Unread and never read: everything is new.
        self.assertEqual(
            unread_divider(self.scene, posts, read=False, marker=None, has_earlier=False),
            {"post_id": posts[0].pk, "count": 2},
        )

    def test_count_includes_new_posts_before_the_window(self):
        posts = [self.post(self.character, f"Post {n}") for n in range(6)]
        window = posts[3:]
        with self.assertNumQueries(1):
            found = unread_divider(
                self.scene, window, read=False, marker=posts[0].pk, has_earlier=True
            )
        self.assertEqual(found, {"post_id": posts[3].pk, "count": 5})
        with self.assertNumQueries(0):
            unread_divider(self.scene, window, read=False, marker=posts[4].pk, has_earlier=True)

    def test_read_marker_is_one_query(self):
        post = self.post(self.character, "Hi")
        self.set_status(read=False, marker=post)
        with self.assertNumQueries(1):
            self.assertEqual(
                scene_read_marker(self.scene, self.users["owner"]), (True, False, post.pk)
            )
        self.assertEqual(scene_read_marker(self.scene, self.users["player"]), (False, True, None))


class ScenePageDividerTests(ReadMarkerBase):
    def test_divider_above_the_first_unread_post_then_gone(self):
        posts = [self.post(self.st_character, f"Post {n}") for n in range(5)]
        self.set_status(read=False, marker=posts[1])
        response = self.view()
        self.assertEqual(self.divider(response), (3, posts[2].pk))
        self.assertContains(response, 'aria-label="3 new posts"')
        status = self.status()
        self.assertEqual(status.last_read_post, posts[4])
        self.assertTrue(status.read)
        self.assertIsNone(self.divider(self.view()))

    def test_all_read_shows_no_divider(self):
        posts = [self.post(self.st_character, f"Post {n}") for n in range(2)]
        self.set_status(read=True, marker=posts[1])
        self.assertIsNone(self.divider(self.view()))

    def test_new_posts_after_a_visit(self):
        self.post(self.st_character, "Before")
        self.view()  # a player's first visit starts tracking
        self.assertEqual(self.status().last_read_post.message, "Before")
        later = self.scene.add_post(self.st_character, "", "After")
        self.assertEqual(self.divider(self.view()), (1, later.pk))

    def test_own_post_moves_the_marker(self):
        theirs = self.scene.add_post(self.st_character, "", "Theirs")
        mine = self.scene.add_post(self.character, "", "Mine")
        self.assertEqual(self.status().last_read_post, mine)
        self.assertLess(theirs.pk, mine.pk)
        self.assertIsNone(self.divider(self.view()))

    def test_readers_outside_the_cast_are_not_tracked(self):
        self.post(self.st_character, "Hello")
        response = self.view("staff")
        self.assertIsNone(self.divider(response))
        self.assertFalse(UserSceneReadStatus.objects.filter(user=self.users["staff"]).exists())

    def test_history_pages_neither_show_nor_move_the_marker(self):
        posts = [self.post(self.st_character, f"Post {n}") for n in range(3)]
        self.set_status(read=False, marker=posts[0])
        response = self.view(before=posts[2].pk)
        self.assertIsNone(self.divider(response))
        self.assertEqual(self.status().last_read_post, posts[0])
        self.assertFalse(self.status().read)
        fragment = self.client.get(
            self.scene.get_absolute_url(), {"before": posts[2].pk}, headers={"HX-Request": "true"}
        )
        self.assertNotContains(fragment, "tl-unread")
        self.assertEqual(self.status().last_read_post, posts[0])

    def test_whole_window_unread_counts_every_new_post(self):
        posts = [self.post(self.st_character, f"Post {n}") for n in range(SCENE_POST_WINDOW + 3)]
        self.set_status(read=False, marker=posts[0])
        self.assertEqual(self.divider(self.view()), (SCENE_POST_WINDOW + 2, posts[3].pk))

    def test_unread_past_the_window_is_not_skipped(self):
        # More unread posts than the page loads: the marker stays until the reader
        # loads back to the first unread post from the live page.
        posts = [self.post(self.st_character, f"Post {n}") for n in range(SCENE_POST_WINDOW + 3)]
        self.set_status(read=False, marker=posts[0])
        self.view()
        self.assertEqual(self.status().last_read_post, posts[0])
        self.assertFalse(self.status().read)

        earlier = {"before": posts[3].pk, "reading": "1"}
        self.client.get(self.scene.get_absolute_url(), earlier, headers={"HX-Request": "true"})
        status = self.status()
        self.assertTrue(status.read)
        self.assertEqual(status.last_read_post, posts[-1])

    def test_live_page_earlier_link_carries_the_reading_flag(self):
        posts = [self.post(self.st_character, f"Post {n}") for n in range(SCENE_POST_WINDOW + 1)]
        self.assertContains(self.view(), f"?before={posts[1].pk}&amp;reading=1")
        self.assertNotContains(self.view(before=posts[-1].pk), "reading=1")

    def test_live_socket_fragment_has_no_divider(self):
        post = self.post(self.st_character, "Live")
        html = render_to_string(
            "game/scene/ws/_posts.html",
            {"posts": [scene_post(self.scene, post.pk)], "viewer_id": self.users["owner"].pk},
        )
        self.assertNotIn("tl-unread", html)

    def test_query_count_does_not_grow_with_posts(self):
        def count():
            self.set_status(read=False, marker=Post.objects.filter(scene=self.scene).first())
            self.client.force_login(self.users["owner"])
            with CaptureQueriesContext(connection) as context:
                response = self.client.get(self.scene.get_absolute_url())
            self.assertIsNotNone(self.divider(response))
            return len(context.captured_queries)

        for n in range(3):
            self.post(self.st_character, f"Post {n}")
        few = count()
        for n in range(30):
            self.post(self.character if n % 2 else self.st_character, f"More {n}")
        self.assertEqual(count(), few)


class ReadStatusCompatibilityTests(ReadMarkerBase):
    def unread_scenes(self, who="owner"):
        return list(Profile.objects.get(user=self.users[who]).unread_scenes())

    def test_viewing_the_scene_clears_it_from_unread_scenes(self):
        self.scene.add_post(self.st_character, "", "Knock knock")
        self.assertEqual(self.unread_scenes(), [self.scene])
        self.view()
        self.assertEqual(self.unread_scenes(), [])

    def test_mark_read_sets_the_marker(self):
        self.scene.add_post(self.st_character, "", "One")
        latest = self.scene.add_post(self.st_character, "", "Two")
        self.client.force_login(self.users["owner"])
        self.client.post(reverse("accounts:mark_scene_read", kwargs={"scene_pk": self.scene.pk}))
        status = self.status()
        self.assertTrue(status.read)
        self.assertEqual(status.last_read_post, latest)
        self.assertEqual(self.unread_scenes(), [])
        self.assertIsNone(self.divider(self.view()))

    def test_deleted_marker_post_falls_back_to_the_read_flag(self):
        posts = [self.post(self.st_character, f"Post {n}") for n in range(2)]
        self.set_status(read=True, marker=posts[0])
        posts[0].delete()
        self.assertIsNone(self.status().last_read_post)
        self.assertIsNone(self.divider(self.view()))
