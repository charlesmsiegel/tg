from characters.models.demon.earthbound import Earthbound
from characters.models.demon.house import DemonHouse
from django import forms


class EarthboundCreationForm(forms.ModelForm):
    class Meta:
        model = Earthbound
        fields = [
            "name",
            "nature",
            "demeanor",
            "concept",
            "house",
            "reliquary_type",
            "reliquary_description",
            "chronicle",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Set up querysets
        self.fields["house"].queryset = DemonHouse.objects.all()

        # Placeholders
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["reliquary_description"].widget = forms.Textarea(attrs={"rows": 4})
        self.fields["reliquary_description"].widget.attrs.update(
            {
                "placeholder": "Describe the reliquary's appearance and nature (object, location, etc.)"
            }
        )

        # Set optional fields
        self.fields["image"].required = False
        self.fields["house"].required = False
        self.fields["reliquary_description"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
