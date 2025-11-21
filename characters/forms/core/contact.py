from characters.models.changeling.ctdhuman import CtDHuman
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from characters.models.vampire.vtmhuman import VtMHuman
from characters.models.werewolf.spirit_character import SpiritCharacter
from characters.models.werewolf.wtahuman import WtAHuman
from characters.models.wraith.wtohuman import WtOHuman
from django import forms


class ContactForm(forms.Form):
    CONTACT_TYPE_CHOICES = [
        ("vtmhuman", "Human (Vampire)"),
        ("wtahuman", "Human (Werewolf)"),
        ("mtahuman", "Human (Mage)"),
        ("ctdhuman", "Human (Changeling)"),
        ("wtohuman", "Human (Wraith)"),
        ("mage", "Mage"),
        ("sorcerer", "Sorcerer"),
        ("spirit", "Spirit"),
    ]
    CONTACT_CLASSES = {
        "vtmhuman": VtMHuman,
        "wtahuman": WtAHuman,
        "mtahuman": MtAHuman,
        "ctdhuman": CtDHuman,
        "wtohuman": WtOHuman,
        "mage": Mage,
        "sorcerer": Sorcerer,
        "spirit": SpiritCharacter,
    }

    contact_type = forms.ChoiceField(choices=CONTACT_TYPE_CHOICES, label="Contact Type")
    name = forms.CharField(
        max_length=100,
        label="Name",
        widget=forms.TextInput(attrs={"placeholder": "Name"}),
    )
    rank = forms.IntegerField(min_value=0, max_value=5, initial=1, label="Contact Rating")
    concept = forms.CharField(
        max_length=100,
        label="Concept",
        widget=forms.TextInput(attrs={"placeholder": "Concept"}),
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Describe your contact's area of expertise and connections", "rows": 4}),
        label="Note"
    )

    def __init__(self, *args, **kwargs):
        self.obj = kwargs.pop("obj", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        note = (
            self.cleaned_data["note"]
            + "<br>Rank "
            + str(self.cleaned_data["rank"])
            + " Contact"
        )
        if self.obj is not None:
            note += " for " + self.obj.name
        obj = self.CONTACT_CLASSES[self.cleaned_data["contact_type"]].objects.create(
            name=self.cleaned_data["name"],
            concept=self.cleaned_data["concept"],
            notes=note,
            status="Un",
            npc=True,
        )
        return obj
