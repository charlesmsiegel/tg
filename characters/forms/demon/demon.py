from characters.models.demon.demon import Demon
from characters.models.demon.faction import DemonFaction
from characters.models.demon.house import DemonHouse
from characters.models.demon.visage import Visage
from django import forms


class DemonCreationForm(forms.ModelForm):
    class Meta:
        model = Demon
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "house",
            "faction",
            "visage",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Set up querysets
        self.fields["house"].queryset = DemonHouse.objects.all()
        self.fields["faction"].queryset = DemonFaction.objects.all()
        self.fields["visage"].queryset = Visage.objects.all()

        # Placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["image"].required = False
        self.fields["house"].required = False
        self.fields["faction"].required = False
        self.fields["visage"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
