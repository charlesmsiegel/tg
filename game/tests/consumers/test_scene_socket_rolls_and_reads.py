"""Live posts over the scene socket carry the roll strip and move read markers (C4)."""

from unittest import mock

from game.models import Post, UserSceneReadStatus
from game.tests.consumers.test_scene_chat_socket import SocketTestBase


class LiveRollStripTests(SocketTestBase):
    def test_a_live_roll_renders_the_strip_for_every_viewer(self):
        async def scenario():
            owner = await self.open("owner")
            st = await self.open("st")
            with mock.patch("core.utils.random.randint", side_effect=[9, 1, 4]):
                await self.send(
                    owner, action="post", character="", display_name="", message="Duck /roll 3"
                )
                owner_frames = await self.drain(owner)
            return owner_frames, await self.drain(st)

        owner_frames, st_frames = self.run_async(scenario)
        [post] = self.posts()
        self.assertEqual(post.roll["rolls"][0]["dice"], [9, 1, 4])
        for viewer, frames in (("owner", owner_frames), ("st", st_frames)):
            with self.subTest(viewer=viewer):
                text = self.text(frames)
                self.assertIn(self.expected_post_html(post, viewer), text)
                self.assertIn('data-roll="roll"', text)
                self.assertIn('<span class="tl-roll__result">Failure</span>', text)
                self.assertIn('<span class="tl-die is-hit" aria-hidden="true">9</span>', text)
                self.assertIn('<span class="tl-die is-one" aria-hidden="true">1</span>', text)
                self.assertNotIn("tl-unread", text)

    def test_synced_old_roll_renders_as_text(self):
        old = Post.objects.create(
            scene=self.scene,
            character=self.st_character,
            display_name="Narrator",
            message="roll of 2 dice at difficulty 6: 7, 8: <b>2</b>",
        )

        async def scenario():
            owner = await self.open("owner")
            await self.send(owner, action="sync", after=0)
            return self.text(await self.drain(owner))

        text = self.run_async(scenario)
        self.assertIn(f'id="post-{old.pk}"', text)
        self.assertIn("7, 8: <b>2</b>", text)
        self.assertNotIn("tl-roll", text)


class LiveReadMarkerTests(SocketTestBase):
    def status(self, who):
        return UserSceneReadStatus.objects.get(scene=self.scene, user=self.users[who])

    def test_a_post_seen_live_is_read(self):
        self.scene.add_post(self.character, "", "Warm up")  # both players get a row
        # Both pages were opened, which read the scene through the warm-up post.
        UserSceneReadStatus.objects.mark_read(self.scene, self.users["st"].pk)

        async def scenario():
            owner = await self.open("owner")
            st = await self.open("st")
            await self.send(owner, action="post", character="", display_name="", message="Hi")
            await self.drain(owner)
            await self.drain(st)

        self.run_async(scenario)
        latest = Post.objects.filter(scene=self.scene).latest("pk")
        for who in ("owner", "st"):
            with self.subTest(who=who):
                self.assertTrue(self.status(who).read)
                self.assertEqual(self.status(who).last_read_post, latest)

    def test_sync_reads_through_the_caught_up_posts(self):
        first = self.scene.add_post(self.st_character, "", "One")
        second = self.scene.add_post(self.st_character, "", "Two")
        # The owner's page showed (and so read) through ``first``.
        UserSceneReadStatus.objects.filter(scene=self.scene, user=self.users["owner"]).update(
            last_read_post=first
        )
        self.assertFalse(self.status("owner").read)

        async def scenario():
            owner = await self.open("owner")
            await self.send(owner, action="sync", after=first.pk)
            await self.drain(owner)

        self.run_async(scenario)
        self.assertTrue(self.status("owner").read)
        self.assertEqual(self.status("owner").last_read_post, second)

    def test_a_live_post_does_not_skip_an_unloaded_backlog(self):
        """Opened with more unread posts than the window, the page keeps the marker
        behind them (read_latest); a post arriving live must not jump past them."""
        read = self.scene.add_post(self.character, "", "Read")
        unseen = self.scene.add_post(self.st_character, "", "Behind the window")

        async def scenario():
            owner = await self.open("owner")
            st = await self.open("st")
            await self.send(st, action="post", character="", display_name="", message="Live")
            await self.drain(st)
            await self.drain(owner)

        self.run_async(scenario)
        status = self.status("owner")
        self.assertFalse(status.read)
        self.assertEqual(status.last_read_post, read)
        self.assertLess(status.last_read_post_id, unseen.pk)

    def test_readers_without_a_row_are_not_tracked(self):
        async def scenario():
            staff = await self.open("staff")
            owner = await self.open("owner")
            await self.send(owner, action="post", character="", display_name="", message="Hi")
            await self.drain(owner)
            await self.drain(staff)

        self.run_async(scenario)
        self.assertFalse(
            UserSceneReadStatus.objects.filter(scene=self.scene, user=self.users["staff"]).exists()
        )
