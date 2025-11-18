from django import forms


class FetterForm(forms.Form):
    """Form for adding a Fetter during character creation."""

    FETTER_TYPE_CHOICES = [
        ("object", "Object"),
        ("location", "Location"),
        ("person", "Person"),
    ]

    fetter_type = forms.ChoiceField(
        choices=FETTER_TYPE_CHOICES,
        help_text="Type of fetter",
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Describe this anchor to the mortal world",
                "rows": 3,
            }
        ),
        help_text="What this fetter is",
    )
    rating = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        help_text="Strength of this fetter (1-10)",
    )
