from django import forms

from characters.models.changeling.changeling import Changeling
from characters.models.changeling.legacy import Legacy


class ChangelingCreationForm(forms.ModelForm):
    class Meta:
        model = Changeling
        fields = [
            "name",
            "concept",
            "chronicle",
            "image",
            "court",
            "seelie_legacy",
            "unseelie_legacy",
            "house",
            "seeming",
            "kith",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["seelie_legacy"].queryset = Legacy.objects.filter(court="seelie")
        self.fields["unseelie_legacy"].queryset = Legacy.objects.filter(court="unseelie")

        self.fields["image"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:  # If we have a user
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
