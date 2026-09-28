"""Clickable dot rating for a number field.

The ``<input type="number">`` stays the real form control, so the form posts
the same value with or without JavaScript. The dot range comes from the
server (the step's allocation rules); the browser only renders it.

Two drivers render the same control: the Alpine ``tgDots`` component on
interactive (htmx) pages (``alpine=True``), and ``widgets/dot_rating.js``, plain
JavaScript declared as the widget's media, everywhere else. Without JavaScript
the dots stay hidden and the number input is the control.
"""

from django import forms


class DotRatingInput(forms.NumberInput):
    template_name = "widgets/dot_rating.html"

    def __init__(self, *, minimum=0, maximum=5, label="", alpine=True, attrs=None):
        self.minimum = minimum
        self.maximum = maximum
        self.label = label
        self.alpine = alpine
        super().__init__(attrs=attrs)

    @property
    def media(self):
        if self.alpine:
            return forms.Media()
        return forms.Media(js=["widgets/dot_rating.js"])

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget_attrs = context["widget"]["attrs"]
        if self.alpine:
            widget_attrs["x-ref"] = "input"
            widget_attrs["x-on:input"] = "sync"
        widget_attrs["class"] = f"{widget_attrs.get('class', '')} tg-dots-number".strip()
        try:
            current = int(value)
        except (TypeError, ValueError):
            current = 0
        context["widget"].update(
            minimum=self.minimum,
            maximum=self.maximum,
            label=self.label or name.replace("_", " ").title(),
            values=range(1, self.maximum + 1),
            alpine=self.alpine,
            current=current,
        )
        return context
