from characters.models.demon.dtf_human import DtFHuman
from django import forms


class DtFHumanCreationForm(forms.ModelForm):
    class Meta:
        model = DtFHuman
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["image"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
