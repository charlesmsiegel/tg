from django import forms

from characters.models.werewolf.bastet import Bastet
from characters.models.werewolf.corax import Corax
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.gurahl import Gurahl
from characters.models.werewolf.mokole import Mokole
from characters.models.werewolf.nuwisha import Nuwisha
from characters.models.werewolf.ratkin import Ratkin

FERA_CLASSES = {
    "ratkin": Ratkin,
    "mokole": Mokole,
    "bastet": Bastet,
    "corax": Corax,
    "nuwisha": Nuwisha,
    "gurahl": Gurahl,
}


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
        self.fields["concept"].widget.attrs.update({"placeholder": "Enter concept here"})
        self.fields["breed"].widget.attrs.update({"placeholder": "Will be set by Fera type"})
        self.fields["breed"].required = False
        self.fields["image"].required = False

    def save(self, commit=True):
        # Get the fera_type to determine which model to instantiate
        fera_type = self.cleaned_data.pop("fera_type")

        # Get the appropriate class
        fera_class = FERA_CLASSES[fera_type]

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


STARTING_GIFT_COUNT = 3


class FeraStartingGiftsForm(forms.ModelForm):
    """Exactly three rank-1 Gifts the Fera's breed and faction permit."""

    class Meta:
        model = Fera
        fields = ["gifts"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gifts"].queryset = self.instance.starting_gift_choices().order_by("name")
        self.fields["gifts"].help_text = self.instance.starting_gifts_help_text

    def clean_gifts(self):
        gifts = self.cleaned_data.get("gifts")
        if gifts.count() != STARTING_GIFT_COUNT:
            raise forms.ValidationError(
                f"You must select exactly {STARTING_GIFT_COUNT} starting Gifts."
            )
        available = self.instance.starting_gift_choices()
        for gift in gifts:
            if gift not in available:
                raise forms.ValidationError(f"{gift.name} is not available to your character.")
        return gifts


class FeraFirstChangeForm(forms.ModelForm):
    """The First Change: described, and at an age between 0 and the current age."""

    class Meta:
        model = Fera
        fields = ["first_change", "age_of_first_change"]

    def clean_first_change(self):
        first_change = self.cleaned_data.get("first_change")
        if not first_change or first_change.strip() == "":
            raise forms.ValidationError("You must describe your First Change.")
        return first_change

    def clean_age_of_first_change(self):
        age = self.cleaned_data.get("age_of_first_change")
        if age is None or age <= 0:
            raise forms.ValidationError("Age of First Change must be greater than 0.")
        if self.instance.age is not None and age >= self.instance.age:
            raise forms.ValidationError("Age of First Change must be less than current age.")
        return age
