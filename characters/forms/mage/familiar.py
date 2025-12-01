from characters.models.core.archetype import Archetype
from characters.models.mage.companion import Companion
from django import forms


class FamiliarForm(forms.ModelForm):
    class Meta:
        model = Companion
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nature"].queryset = Archetype.objects.all().order_by("name")
        self.fields["demeanor"].queryset = Archetype.objects.all().order_by("name")
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["image"].required = False

    def save(self, commit=True):
        c = super().save(commit=commit)
        c.npc = True
        c.companion_type = "familiar"
        c.save()
        return c
