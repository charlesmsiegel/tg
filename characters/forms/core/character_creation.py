from django import forms
from game.models import ObjectType


class CharacterCreationForm(forms.Form):
    char_type = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            if user.profile.is_st():
                self.fields["char_type"].choices = [
                    (x.name, x.name.replace("_", " ").title())
                    for x in ObjectType.objects.filter(type="char")
                    if x.name
                    in [
                        "mage",
                        "cabal",
                        "group",
                        "pack",
                        "motley",
                        "sorcerer",
                        "mta_human",
                        "wto_human",
                        "ctd_human",
                        "wta_human",
                        "vtm_human",
                        "changeling",
                        "kinfolk",
                        "fomor",
                        "companion",
                        "werewolf",
                    ]
                ]
            else:
                self.fields["char_type"].choices = [
                    (x.name, x.name.replace("_", " ").title())
                    for x in ObjectType.objects.filter(type="char")
                    if x.name in ["mage", "cabal", "sorcerer"]
                ]
