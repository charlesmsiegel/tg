from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.vampire import Vampire
from django import forms


class GhoulCreationForm(forms.ModelForm):
    class Meta:
        model = Ghoul
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "domitor",
            "is_independent",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Set up querysets
        self.fields["domitor"].queryset = Vampire.objects.none()

        # Placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["image"].required = False
        self.fields["domitor"].required = False

        if self.is_bound:
            self.fields["domitor"].queryset = Vampire.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
