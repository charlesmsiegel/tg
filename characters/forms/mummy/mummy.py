from characters.models.mummy.dynasty import Dynasty
from characters.models.mummy.mummy import Mummy
from django import forms


class MummyCreationForm(forms.ModelForm):
    class Meta:
        model = Mummy
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "dynasty",
            "web",
            "ancient_name",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["dynasty"].queryset = Dynasty.objects.all()
        self.fields["dynasty"].required = False

        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["ancient_name"].widget.attrs.update(
            {"placeholder": "Name from First Life in ancient Egypt"}
        )
        self.fields["image"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
