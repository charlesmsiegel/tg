from characters.models.werewolf.bastet import Bastet
from characters.models.werewolf.corax import Corax
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gurahl import Gurahl
from characters.models.werewolf.mokole import Mokole
from characters.models.werewolf.nuwisha import Nuwisha
from characters.models.werewolf.ratkin import Ratkin
from django import forms


class FeraCreationForm(forms.ModelForm):
    """Base form for creating Fera characters."""

    FERA_TYPES = [
        ("ratkin", "Ratkin (Wererats)"),
        ("mokole", "Mokole (Weresaurians)"),
        ("bastet", "Bastet (Werecats)"),
        ("corax", "Corax (Wereravens)"),
        ("nuwisha", "Nuwisha (Werecoyotes)"),
        ("gurahl", "Gurahl (Werebears)"),
    ]

    fera_type = forms.ChoiceField(
        choices=FERA_TYPES,
        label="Fera Type",
        help_text="Select which type of shapeshifter you want to create.",
    )

    class Meta:
        model = Fera
        fields = [
            "name",
            "concept",
            "chronicle",
            "breed",
            "image",
            "npc",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["concept"].widget.attrs.update(
            {"placeholder": "Enter concept here"}
        )
        self.fields["breed"].widget.attrs.update(
            {"placeholder": "Will be set by Fera type"}
        )
        self.fields["breed"].required = False
        self.fields["image"].required = False

    def save(self, commit=True):
        # Get the fera_type to determine which model to instantiate
        fera_type = self.cleaned_data.pop("fera_type")

        # Map fera types to their model classes
        fera_class_map = {
            "ratkin": Ratkin,
            "mokole": Mokole,
            "bastet": Bastet,
            "corax": Corax,
            "nuwisha": Nuwisha,
            "gurahl": Gurahl,
        }

        # Get the appropriate class
        fera_class = fera_class_map[fera_type]

        # Create instance of the specific fera type
        instance = fera_class()

        # Set basic fields
        instance.name = self.cleaned_data["name"]
        instance.concept = self.cleaned_data["concept"]
        instance.chronicle = self.cleaned_data.get("chronicle")
        instance.image = self.cleaned_data.get("image")
        instance.npc = self.cleaned_data.get("npc", False)

        if self.user:
            instance.owner = self.user

        if commit:
            instance.save()

        return instance
