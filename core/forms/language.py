from django import forms

from core.models import Language
from core.widgets import AutocompleteTextInput


class HumanLanguageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        num_languages = kwargs.pop("num_languages", 1)
        human_pk = kwargs.pop("pk", None)

        super().__init__(*args, **kwargs)

        # Query once before loop to avoid repeated database queries
        language_suggestions = [
            x.name for x in Language.objects.order_by("frequency").exclude(name="English")
        ]

        # Dynamically create fields
        for i in range(num_languages):
            self.fields[f"language_{i+1}"] = forms.CharField(
                widget=AutocompleteTextInput(suggestions=language_suggestions),
                label=f"Language {i + 1}",
            )
