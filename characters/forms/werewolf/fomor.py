from characters.models.werewolf.fomor import Fomor
from django import forms


class FomorCreationForm(forms.ModelForm):
    class Meta:
        model = Fomor
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

        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["image"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:  # If we have a user
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
