"""DotRatingInput: one clickable-dots control, driven by Alpine or by plain JavaScript."""

from django import forms
from django.contrib.staticfiles import finders
from django.test import SimpleTestCase

from widgets.widgets.dots import DotRatingInput


class RatingForm(forms.Form):
    strength = forms.IntegerField(
        widget=DotRatingInput(minimum=1, maximum=5, label="Strength", alpine=False)
    )


class DotRatingInputTests(SimpleTestCase):
    def test_plain_driver_renders_hidden_dots_over_the_number_input(self):
        html = DotRatingInput(minimum=1, maximum=3, label="Wits", alpine=False).render(
            "wits", 2, attrs={"id": "id_wits"}
        )
        self.assertInHTML(
            '<span class="tg-dots-control" data-dot-rating data-min="1" data-max="3">'
            '<input type="number" name="wits" value="2" id="id_wits" class="tg-dots-number">'
            '<span class="tg-dot-buttons" role="group" aria-label="Wits" hidden>'
            '<button type="button" class="tg-dot is-filled" data-value="1" '
            'aria-label="Wits 1" aria-pressed="false"></button>'
            '<button type="button" class="tg-dot is-filled" data-value="2" '
            'aria-label="Wits 2" aria-pressed="true"></button>'
            '<button type="button" class="tg-dot" data-value="3" '
            'aria-label="Wits 3" aria-pressed="false"></button>'
            "</span></span>",
            html,
        )
        self.assertNotIn("x-", html)

    def test_plain_driver_ships_its_script_as_media(self):
        media = str(RatingForm().media)
        self.assertIn("widgets/dot_rating.js", media)
        self.assertIsNotNone(finders.find("widgets/dot_rating.js"))
        self.assertEqual(str(DotRatingInput().media), "")

    def test_empty_or_unparsable_values_fill_no_dots(self):
        for value in (None, "", "x"):
            with self.subTest(value=value):
                html = DotRatingInput(alpine=False).render("rating", value)
                self.assertNotIn("is-filled", html)

    def test_alpine_driver_is_unchanged(self):
        html = DotRatingInput(minimum=0, maximum=3, label="Alertness").render(
            "alertness", 1, attrs={"id": "id_alertness"}
        )
        self.assertIn('x-data="tgDots" data-min="0" data-max="3"', html)
        self.assertIn('x-ref="input"', html)
        self.assertIn('x-on:click="pick(3)"', html)
        self.assertNotIn("data-dot-rating", html)
