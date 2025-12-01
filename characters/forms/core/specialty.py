from characters.models.core.specialty import Specialty
from characters.models.core.statistic import Statistic
from core.widgets import AutocompleteTextInput
from django import forms


class SpecialtiesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        specialties_needed = kwargs.pop("specialties_needed")
        character = kwargs.pop("object")
        super().__init__(*args, **kwargs)
        for field in specialties_needed:
            s = (
                Statistic.objects.filter(property_name=field)
                .exclude(polymorphic_ctype__model="background")
                .first()
            )
            self.fields[field] = forms.CharField(
                widget=AutocompleteTextInput(
                    suggestions=[x.name for x in Specialty.objects.filter(stat=s.property_name)]
                ),
            )
            self.fields[field].label = s.name
