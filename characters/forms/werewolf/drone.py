from characters.models.werewolf.drone import Drone
from django import forms


class DroneCreationForm(forms.ModelForm):
    class Meta:
        model = Drone
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "chronicle",
            "image",
            "npc",
            "bane_name",
            "bane_type",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["bane_name"].widget.attrs.update({"placeholder": "Name of possessing Bane"})
        self.fields["bane_type"].widget.attrs.update(
            {"placeholder": "Type of Bane (e.g., Scrags, Psychomachiae)"}
        )
        self.fields["image"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:  # If we have a user
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
