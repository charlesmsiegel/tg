from characters.models.changeling.house import House
from characters.models.changeling.house_faction import HouseFaction
from django import forms


class HouseFactionForm(forms.ModelForm):
    houses = forms.ModelMultipleChoiceField(
        queryset=House.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select which houses this faction belongs to",
    )

    class Meta:
        model = HouseFaction
        fields = ["name", "description", "houses"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # If editing an existing faction, set the initial houses
            self.fields["houses"].initial = House.objects.filter(factions=self.instance)

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            # Update the House objects to reference this faction
            # First, remove this faction from all houses
            for house in House.objects.filter(factions=instance):
                house.factions.remove(instance)

            # Then add it to the selected houses
            for house in self.cleaned_data["houses"]:
                house.factions.add(instance)

        return instance
