from django import forms


class PassionForm(forms.Form):
    """Form for adding a Passion during character creation."""

    emotion = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "e.g., Love, Hate, Fear, Hope"}),
        help_text="The emotion driving this passion",
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Describe what or who this passion is about",
                "rows": 3,
            }
        ),
        help_text="What this passion is connected to",
    )
    rating = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        help_text="Strength of this passion (1-10)",
    )
    is_dark_passion = forms.BooleanField(
        required=False,
        label="Dark Passion",
        help_text="Check if this is a Dark Passion (driven by Shadow)",
    )
