"""Tests for the Spread design template tags (core/templatetags/tl.py)."""

import re

from django.template import Context, Template
from django.test import SimpleTestCase, TestCase

from core.templatetags.tl import boxes, cover_title_class, dots, gameline_code, qp_wheel, track
from game.models import Chronicle


class DotsTest(SimpleTestCase):
    def test_fills_value_of_max(self):
        html = dots(3, 5)
        self.assertEqual(html.count('class="tl-dot is-on"'), 3)
        self.assertEqual(html.count('class="tl-dot"'), 2)
        self.assertIn('aria-label="3 of 5"', html)

    def test_accent_and_large_variants(self):
        self.assertIn("tl-dots tl-dots--acc tl-dots--lg", dots(1, 5, "acc", "lg"))

    def test_none_and_junk_count_as_zero(self):
        self.assertIn('aria-label="0 of 5"', dots(None))
        self.assertIn('aria-label="0 of 5"', dots("n/a"))

    def test_boxes(self):
        html = boxes(4, 10)
        self.assertEqual(html.count('class="tl-box is-on"'), 4)
        self.assertEqual(html.count('class="tl-box"'), 6)


class TrackTest(SimpleTestCase):
    def test_permanent_and_temporary_rows(self):
        html = track("Willpower", perm=6, temp=4)
        self.assertIn("Willpower", html)
        self.assertIn('aria-label="6 of 10"', html)
        self.assertIn('class="tl-boxes" role="img" aria-label="4 of 10"', html)

    def test_either_row_can_be_omitted(self):
        self.assertNotIn("tl-boxes", track("Arete", perm=3))
        self.assertNotIn("tl-dots", track("Blood", temp=10, total=20))


class TraitTagTest(SimpleTestCase):
    def test_renders_label_specialty_and_dots(self):
        html = Template('{% load tl %}{% trait "Perception" 4 "Hidden details" %}').render(
            Context()
        )
        self.assertIn("Perception", html)
        self.assertIn('<span class="tl-trait__spec">Hidden details</span>', html)
        self.assertIn('aria-label="4 of 5"', html)


class QPWheelTest(SimpleTestCase):
    def boxes(self, html):
        return re.findall(
            r'class="tl-qp__box([^"]*)" style="left:([\d.-]+)px;top:([\d.-]+)px"', html
        )

    def test_quintessence_from_the_start_paradox_from_the_end(self):
        found = self.boxes(qp_wheel(4, 2))
        self.assertEqual(len(found), 20)
        states = [state.strip() for state, _, _ in found]
        self.assertEqual(states[:4], ["is-q"] * 4)
        self.assertEqual(states[18:], ["is-p"] * 2)
        self.assertEqual(set(states[4:18]), {""})

    def test_paradox_wins_where_the_two_overlap(self):
        # 19 Quintessence and 3 Paradox claim boxes 17-18 twice: they show as Paradox.
        states = [state.strip() for state, _, _ in self.boxes(qp_wheel(19, 3))]
        self.assertEqual(states[:17], ["is-q"] * 17)
        self.assertEqual(states[17:], ["is-p"] * 3)

    def test_first_box_sits_left_of_centre(self):
        _, left, top = self.boxes(qp_wheel(0, 0))[0]
        # 189 degrees: just above the horizontal, on the left.
        self.assertLess(float(left), 10)
        self.assertAlmostEqual(float(top), 82 + 72 * -0.1564 - 7.5, delta=0.2)

    def test_label_and_centre_numbers(self):
        html = qp_wheel(4, 2, label="Primal Energy")
        self.assertIn('aria-label="Primal Energy 4, Paradox 2, of 20"', html)
        self.assertIn('<span class="tl-qp__q">4</span>', html)
        self.assertIn('<span class="tl-qp__p">2</span>', html)


class CoverTitleClassTest(SimpleTestCase):
    def test_steps_by_longest_word(self):
        self.assertEqual(cover_title_class("Marisol Quintero", "vtm"), "")
        self.assertEqual(cover_title_class("The Cartographers", "vtm"), "tl-cover__name--m")
        self.assertEqual(cover_title_class("Correspondence", "vtm"), "tl-cover__name--m")
        self.assertEqual(cover_title_class("Sternenkartenzeichner", "vtm"), "tl-cover__name--s")

    def test_font_factor(self):
        self.assertEqual(cover_title_class("Cartographer", 1.0), "tl-cover__name--l")
        self.assertEqual(cover_title_class("Cartographer", 1.5), "tl-cover__name--s")


class GamelineCodeTest(TestCase):
    def test_strings(self):
        self.assertEqual(gameline_code("mta"), "mta")
        self.assertEqual(gameline_code("vtm_heading"), "vtm")
        self.assertEqual(gameline_code("nope"), "wod")
        self.assertEqual(gameline_code(""), "wod")
        self.assertEqual(gameline_code(None), "wod")

    def test_chronicle_uses_its_headings(self):
        self.assertEqual(gameline_code(Chronicle(name="C", headings="wta_heading")), "wta")
        self.assertEqual(gameline_code(Chronicle(name="C")), "wod")
