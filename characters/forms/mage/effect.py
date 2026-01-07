from characters.models.mage.effect import Effect
from django import forms
from django.forms import modelformset_factory
from widgets import CreateOrSelectField, CreateOrSelectMixin


class EffectForm(forms.ModelForm):
    class Meta:
        model = Effect
        fields = [
            "name",
            "description",
            "correspondence",
            "time",
            "spirit",
            "matter",
            "life",
            "forces",
            "entropy",
            "mind",
            "prime",
        ]


EffectFormSet = modelformset_factory(Effect, form=EffectForm, extra=1, can_delete=False)


class EffectCreateOrSelectForm(CreateOrSelectMixin, forms.ModelForm):
    """Form for selecting an existing Effect or creating a new one."""

    create_or_select_config = {
        "toggle_field": "select_or_create",
        "select_field": "select",
        "error_message": "You must either select an existing effect or choose to create a new one.",
    }

    select_or_create = CreateOrSelectField(label="Create new Effect?")
    select = forms.ModelChoiceField(queryset=Effect.objects.all(), required=False)

    class Meta:
        model = Effect
        fields = [
            "select_or_create",
            "select",
            "name",
            "description",
            "correspondence",
            "time",
            "spirit",
            "matter",
            "life",
            "forces",
            "entropy",
            "mind",
            "prime",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False

    def cost(self):
        cleaned_data = super().clean()
        if cleaned_data.get("select"):
            return cleaned_data.get("select").cost()
        return (
            cleaned_data.get("correspondence", 0)
            + cleaned_data.get("time", 0)
            + cleaned_data.get("spirit", 0)
            + cleaned_data.get("matter", 0)
            + cleaned_data.get("life", 0)
            + cleaned_data.get("forces", 0)
            + cleaned_data.get("entropy", 0)
            + cleaned_data.get("mind", 0)
            + cleaned_data.get("prime", 0)
        )


EffectCreateOrSelectFormSet = modelformset_factory(
    Effect, form=EffectCreateOrSelectForm, extra=1, can_delete=False
)
