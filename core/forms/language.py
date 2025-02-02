from core.models import Language
from core.widgets import AutocompleteTextInput
from django import forms


class HumanLanguageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        num_languages = kwargs.pop("num_languages", 1)
        human_pk = kwargs.pop("pk", None)

        super().__init__(*args, **kwargs)

        # Dynamically create fields
        for i in range(num_languages):
            self.fields[f"language_{i+1}"] = forms.CharField(
                widget=AutocompleteTextInput(
                    suggestions=[
                        x.name
                        for x in Language.objects.order_by("frequency").exclude(
                            name="English"
                        )
                    ]
                ),
                label=f"Language {i + 1}",
            )
