"""Structured dice rolls on scene posts and the C4 roll strip (Spread)."""

from unittest import mock

from django.template.loader import render_to_string
from django.urls import reverse

from characters.models.core.human import Human
from game.models import Post, process_message
from game.rolls import roll_strip
from game.selectors import scene_post
from game.tests.test_scene_chat import SceneChatBase


def dice_sequence(*values):
    """Patch the d10 so the next rolls come up ``values`` in order."""
    return mock.patch("core.utils.random.randint", side_effect=list(values))


class RollParsingTests(SceneChatBase):
    def setUp(self):
        super().setUp()
        self.character.dexterity = 3
        self.character.firearms = 2
        self.character.save()

    def process(self, message, *values):
        with dice_sequence(*values):
            return process_message(self.character, message)

    def test_plain_message_has_no_roll(self):
        self.assertEqual(self.process("Just talking."), ("Just talking.", None))

    def test_roll(self):
        message, roll = self.process("I shoot /roll 5 difficulty 7", 8, 7, 3, 1, 10)
        # The text keeps the roll written out, exactly as before.
        self.assertEqual(
            message, "I shoot: roll of 5 dice at difficulty 7: 8, 7, 3, 1, 10: <b>2</b>"
        )
        self.assertEqual(
            roll,
            {
                "version": 1,
                "kind": "roll",
                "text": "I shoot",
                "spent": "",
                "pool": 5,
                "pool_label": "",
                "difficulty": 7,
                "specialty": False,
                "willpower": False,
                "rolls": [
                    {"dice": [8, 7, 3, 1, 10], "difficulty": 7, "successes": 2, "botch": False}
                ],
                "roll_count": 1,
                "successes": 2,
                "botch": False,
            },
        )

    def test_botch(self):
        message, roll = self.process("/roll 3", 1, 3, 2)
        self.assertTrue(message.endswith("1, 3, 2: <b>-1</b>"))
        self.assertTrue(roll["botch"])
        self.assertEqual(roll["successes"], 0)
        self.assertEqual(roll["rolls"][0]["successes"], -1)
        self.assertEqual(roll["text"], "")

    def test_specialty_counts_tens_twice(self):
        _message, roll = self.process("/roll 3 difficulty 6 true", 10, 10, 2)
        self.assertTrue(roll["specialty"])
        self.assertEqual(roll["successes"], 4)

    def test_willpower_adds_a_success_and_cancels_a_botch(self):
        self.character.temporary_willpower = 3
        self.character.save()
        message, roll = self.process("Grit #WP /roll 3", 1, 2, 3)
        self.assertIn("#WP: roll of 3 dice", message)
        self.assertTrue(roll["willpower"])
        self.assertEqual(roll["spent"], "#WP")
        self.assertEqual(roll["text"], "Grit #WP")
        self.assertEqual(roll["successes"], 0)
        self.assertFalse(roll["botch"])

    def test_stat(self):
        message, roll = self.process("Aim /stat Dexterity + Firearms + 1", 6, 6, 6, 6, 6, 6)
        self.assertIn("roll of Dexterity (3) + Firearms (2) + 1 = 6 dice", message)
        self.assertEqual(roll["kind"], "stat")
        self.assertEqual(roll["pool"], 6)
        self.assertEqual(roll["pool_label"], "Dexterity (3) + Firearms (2) + 1")
        self.assertEqual(roll["successes"], 6)

    def test_rolls_raise_difficulty_after_a_failure(self):
        message, roll = self.process("/rolls 3 rolls @ 2", 2, 3, 7, 8, 9, 2)
        self.assertIn("difficulty increased to 7", message)
        self.assertEqual(roll["kind"], "rolls")
        self.assertEqual(roll["requested_rolls"], 3)
        self.assertEqual(roll["roll_count"], 3)
        self.assertEqual([r["difficulty"] for r in roll["rolls"]], [6, 7, 7])
        self.assertEqual([r["successes"] for r in roll["rolls"]], [0, 2, 1])

    def test_rolls_stop_at_a_botch(self):
        _message, roll = self.process("/rolls 3 rolls @ 2", 1, 2)
        self.assertEqual(roll["roll_count"], 1)
        self.assertTrue(roll["botch"])

    def test_extended_reaches_its_target(self):
        message, roll = self.process("Research /extended 2 target 3", 6, 7, 8, 2)
        self.assertIn("SUCCESS! Target of 3 reached in 2 rolls.", message)
        self.assertEqual(roll["kind"], "extended")
        self.assertEqual(roll["target"], 3)
        self.assertEqual(roll["roll_count"], 2)
        self.assertEqual(roll["successes"], 3)
        self.assertEqual(roll["max_rolls"], 100)
        self.assertTrue(roll["complete"])

    def test_extended_botch(self):
        message, roll = self.process("/extended 2 target 5", 7, 3, 1, 1)
        self.assertIn("BOTCH!", message)
        self.assertTrue(roll["botch"])
        self.assertFalse(roll["complete"])
        self.assertEqual(roll["successes"], 1)

    def test_malformed_command_raises(self):
        with self.assertRaises(ValueError):
            process_message(self.character, "Leap /extended nonsense")

    def test_refused_command_spends_nothing(self):
        self.character.temporary_willpower = 3
        self.character.save()
        self.assertIsNone(self.scene.add_post(self.character, "", "#WP Leap /extended nonsense"))
        self.character.refresh_from_db()
        self.assertEqual(self.character.temporary_willpower, 3)

    def test_add_post_stores_the_roll(self):
        with dice_sequence(9, 9):
            post = self.scene.add_post(self.character, "", "/roll 2")
        post.refresh_from_db()
        self.assertEqual(post.roll["successes"], 2)
        self.assertIn("roll of 2 dice", post.message)
        plain = self.scene.add_post(self.character, "", "Hello")
        plain.refresh_from_db()
        self.assertIsNone(plain.roll)

    def test_http_post_stores_the_roll(self):
        self.client.force_login(self.users["owner"])
        with dice_sequence(4, 4, 4):
            self.client.post(
                reverse("game:scene_post", kwargs={"pk": self.scene.pk}),
                {"message": "Sneak /roll 3"},
            )
        post = Post.objects.get(scene=self.scene)
        self.assertEqual(post.roll["kind"], "roll")
        self.assertEqual(post.roll["rolls"][0]["dice"], [4, 4, 4])


class RollStripTests(SceneChatBase):
    def record(self, message, *values):
        with dice_sequence(*values):
            return process_message(self.character, message)[1]

    def test_single_roll(self):
        strip = roll_strip(self.record("/roll 5 difficulty 7", 8, 7, 3, 1, 10))
        self.assertEqual(strip["label"], "Roll · Diff 7")
        self.assertEqual(strip["pool"], "5 dice")
        self.assertEqual(strip["result"], "2 successes")
        self.assertFalse(strip["multi"])
        faces = strip["rows"][0]["dice"]
        self.assertEqual([face["hit"] for face in faces], [True, True, False, False, True])
        self.assertEqual([face["one"] for face in faces], [False, False, False, True, False])

    def test_results(self):
        self.assertEqual(roll_strip(self.record("/roll 1", 7))["result"], "1 success")
        self.assertEqual(roll_strip(self.record("/roll 1", 3))["result"], "Failure")
        strip = roll_strip(self.record("/roll 1", 1))
        self.assertEqual(strip["result"], "Botch")
        self.assertTrue(strip["botch"])
        self.assertEqual(roll_strip(self.record("/roll 1 difficulty 6 true", 1))["pool"], "1 die")

    def test_flags_in_the_label(self):
        self.character.temporary_willpower = 2
        self.character.save()
        strip = roll_strip(self.record("#WP /roll 2 difficulty 8 true", 9, 2))
        self.assertEqual(strip["label"], "Roll · Diff 8 · Specialty · Willpower")
        self.assertEqual(strip["spent"], "#WP")

    def test_multi_roll_kinds(self):
        strip = roll_strip(self.record("/rolls 2 rolls @ 2", 2, 3, 7, 8))
        self.assertEqual(strip["label"], "2 rolls · Diff 6")
        self.assertTrue(strip["multi"])
        self.assertEqual([row["raised"] for row in strip["rows"]], [False, True])
        self.assertEqual(strip["result"], "")
        strip = roll_strip(self.record("/extended 2 target 3", 6, 7, 8, 2))
        self.assertEqual(strip["label"], "Extended roll · Diff 6 · Target 3")
        self.assertEqual([row["total"] for row in strip["rows"]], [2, 3])
        self.assertEqual(strip["result"], "Success · 2 rolls")
        strip = roll_strip(self.record("/extended 1 target 5", 1))
        self.assertEqual(strip["result"], "Botch")

    def test_missing_or_damaged_data_falls_back_to_text(self):
        good = self.record("/roll 2", 5, 6)
        for data in (
            None,
            "roll",
            {},
            {**good, "kind": "poker"},
            {**good, "rolls": []},
            {**good, "rolls": [{"dice": [11], "successes": 0, "botch": False}]},
            {**good, "difficulty": "hard"},
            {**good, "rolls": "6, 6"},
        ):
            with self.subTest(data=data):
                self.assertIsNone(roll_strip(data))


class RollStripMarkupTests(SceneChatBase):
    def rolled_post(self, message, *values, character=None):
        with dice_sequence(*values):
            return self.scene.add_post(character or self.character, "", message)

    def render(self, post, viewer=None):
        return render_to_string(
            "game/scene/_post.html",
            {"post": scene_post(self.scene, post.pk), "viewer_id": getattr(viewer, "pk", None)},
        )

    def test_strip_replaces_the_written_out_roll(self):
        post = self.rolled_post('She says "now" /roll 5 difficulty 7', 8, 7, 3, 1, 10)
        html = self.render(post)
        self.assertIn('class="tl-roll" data-roll="roll"', html)
        self.assertIn("Roll · Diff 7", html)
        self.assertIn('<span class="tl-roll__pool">5 dice</span>', html)
        self.assertEqual(html.count('class="tl-die'), 5)
        self.assertEqual(html.count('class="tl-die is-hit"'), 3)
        self.assertEqual(html.count('class="tl-die is-one"'), 1)
        self.assertIn('<span class="tl-sr">Dice: 8, 7, 3, 1, 10</span>', html)
        self.assertIn('<span class="tl-roll__result">2 successes</span>', html)
        # The prose keeps the post's text styling; the old roll line is not repeated.
        self.assertIn('She says <span class="quote">"now"</span>', html)
        self.assertNotIn("roll of 5 dice", html)
        self.assertIn(f'data-post-id="{post.pk}"', html)

    def test_botch_is_marked(self):
        html = self.render(self.rolled_post("/roll 2", 1, 2))
        self.assertIn('<span class="tl-roll__result is-botch">Botch</span>', html)
        self.assertNotIn("tl-turn__text", html)  # no prose, no empty text line

    def test_extended_rows(self):
        html = self.render(self.rolled_post("Dig /extended 2 target 3", 6, 7, 8, 2))
        self.assertIn('data-roll="extended"', html)
        self.assertEqual(html.count('<li class="tl-roll__row">'), 2)
        self.assertIn("1 success · total 3", html)
        self.assertIn("Success · 2 rolls", html)

    def test_rolls_rows_show_a_raised_difficulty(self):
        html = self.render(self.rolled_post("/rolls 2 rolls @ 2", 2, 3, 7, 8))
        self.assertIn("2 · diff 7", html)
        self.assertNotIn('class="tl-roll__result', html)

    def test_prose_and_labels_are_sanitized(self):
        post = self.rolled_post("<script>x()</script><b>Go</b> /roll 1", 7)
        post.roll["pool_label"] = "<i>pool</i>"
        post.save()
        html = self.render(post)
        self.assertNotIn("<script", html)
        self.assertIn("<b>Go</b>", html)
        self.assertIn("&lt;i&gt;pool&lt;/i&gt;", html)

    def test_older_posts_render_their_text(self):
        post = self.post(self.character, "Old: roll of 2 dice at difficulty 6: 7, 8: <b>2</b>")
        html = self.render(post)
        self.assertNotIn("tl-roll", html)
        self.assertIn("roll of 2 dice at difficulty 6: 7, 8: <b>2</b>", html)

    def test_page_shows_the_strip(self):
        post = self.rolled_post("/roll 2", 9, 9)
        self.client.force_login(self.users["st"])
        response = self.client.get(self.scene.get_absolute_url())
        self.assertContains(response, 'data-roll="roll"')
        self.assertContains(response, self.render(post, self.users["st"]), html=True)

    def test_storyteller_roll_keeps_the_turn_styling(self):
        html = self.render(self.rolled_post("/roll 1", 8, character=self.st_character))
        self.assertIn("tl-turn--st", html)
        self.assertIn("tl-roll", html)


class RollStripHumanTests(SceneChatBase):
    """Every kind renders through the page without errors."""

    def test_each_kind(self):
        hero = Human.objects.create(
            name="Tester", owner=self.users["owner"], chronicle=self.chronicle, strength=2
        )
        self.scene.characters.add(hero)
        commands = ["/roll 3", "/stat Strength + 1", "/rolls 2 rolls @ 2", "/extended 2 target 2"]
        for command in commands:
            self.scene.add_post(hero, "", command)
        self.client.force_login(self.users["owner"])
        response = self.client.get(self.scene.get_absolute_url())
        for kind in ("roll", "stat", "rolls", "extended"):
            self.assertContains(response, f'data-roll="{kind}"')
