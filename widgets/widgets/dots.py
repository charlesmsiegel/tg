"""Clickable dot rating for a number field (Alpine ``tgDots`` component).

The ``<input type="number">`` stays the real form control, so the form posts
the same value with or without JavaScript. The dot range comes from the
server (the step's allocation rules); the browser only renders it.
"""

from django import forms


class DotRatingInput(forms.NumberInput):
    template_name = "widgets/dot_rating.html"

    def __init__(self, *, minimum=0, maximum=5, label="", attrs=None):
        self.minimum = minimum
        self.maximum = maximum
        self.label = label
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        widget_attrs = context["widget"]["attrs"]
        widget_attrs["x-ref"] = "input"
        widget_attrs["x-on:input"] = "sync"
        widget_attrs["class"] = f"{widget_attrs.get('class', '')} tg-dots-number".strip()
        context["widget"].update(
            minimum=self.minimum,
            maximum=self.maximum,
            label=self.label or name.replace("_", " ").title(),
            values=range(1, self.maximum + 1),
        )
        return context
