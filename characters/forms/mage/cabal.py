from characters.models.core.human import Human
from characters.models.mage.cabal import Cabal
from django import forms


class CabalForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and user.is_authenticated:
            # Filter the leader field to only include Humans owned by `user`
            self.fields["leader"].queryset = Human.objects.filter(owner=user)

    class Meta:
        model = Cabal
        fields = [
            "name",
            "description",
            "leader",
            "chronicle",
            "public_info",
        ]
