from characters.models.wraith.guild import Guild
from characters.models.wraith.wraith import Wraith
from django import forms


class WraithCreationForm(forms.ModelForm):
    class Meta:
        model = Wraith
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "chronicle",
            "image",
            "guild",
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
        self.fields["guild"].required = True
        self.fields["guild"].queryset = Guild.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
