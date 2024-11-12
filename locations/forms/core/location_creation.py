from django import forms
from game.models import ObjectType


class LocationCreationForm(forms.Form):
    loc_type = forms.ChoiceField(choices=[])
    name = forms.CharField(
        max_length=100,
        label="Name",
        required=False,
    )
    rank = forms.IntegerField(
        initial=1,
        max_value=5,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            if user.profile.is_st():
                self.fields["loc_type"].choices = [
                    (x.name, x.name.replace("_", " ").title())
                    for x in ObjectType.objects.filter(type="loc")
                ]
            else:
                self.fields["loc_type"].choices = [
                    (x.name, x.name.replace("_", " ").title())
                    for x in ObjectType.objects.filter(type="loc")
                    if x.name in []
                ]
