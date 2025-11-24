from characters.models.vampire.revenant import Revenant, RevenantFamily
from django import forms


class RevenantCreationForm(forms.ModelForm):
    class Meta:
        model = Revenant
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "family",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Set up querysets
        self.fields["family"].queryset = RevenantFamily.objects.all()

        # Placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["image"].required = False
        self.fields["family"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
