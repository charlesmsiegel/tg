from django import forms

from game.models import ObjectType


class GroupCreationForm(forms.Form):
    group_type = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Group types that should be available
        group_types = ["cabal", "pack", "motley", "group", "coterie", "circle", "conclave"]

        if user and user.is_authenticated:
            if user.profile.is_st():
                # STs can create all group types
                choices = [
                    (x.name, x.name.replace("_", " ").title())
                    for x in ObjectType.objects.filter(type="char", name__in=group_types)
                ]
                # Sort alphabetically by label
                self.fields["group_type"].choices = sorted(choices, key=lambda x: x[1])
            else:
                # Regular users can only create cabals (mage groups)
                self.fields["group_type"].choices = [
                    (x.name, x.name.replace("_", " ").title())
                    for x in ObjectType.objects.filter(type="char", name="cabal")
                ]
