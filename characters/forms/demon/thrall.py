from characters.models.demon.thrall import Thrall
from characters.models.demon.demon import Demon
from django import forms


class ThrallCreationForm(forms.ModelForm):
    class Meta:
        model = Thrall
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "master",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Set up querysets
        self.fields["master"].queryset = Demon.objects.none()

        # Placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["image"].required = False
        self.fields["master"].required = False

        if self.is_bound:
            self.fields["master"].queryset = Demon.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
