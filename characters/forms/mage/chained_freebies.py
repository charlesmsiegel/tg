"""
Chained Select Mage Freebie Forms

These forms use ChainedSelectMixin to provide cascading dropdowns
without manual AJAX. Choices are computed at form initialization
and embedded in the page JavaScript.
"""

from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.models.mage.focus import Practice, Tenet
from characters.models.mage.resonance import Resonance
from characters.models.mage.sphere import Sphere
from core.widgets import AutocompleteTextInput
from django import forms


class ChainedMageFreebiesForm(ChainedHumanFreebiesForm):
    """
    Mage freebie spending form with chained selects.

    Adds Sphere, Arete, Quintessence, Rotes, Resonance, Tenet, Practice categories.
    """

    resonance = forms.CharField(required=False, widget=AutocompleteTextInput(suggestions=[]))

    def __init__(self, *args, suggestions=None, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            if suggestions is None:
                suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
            self.fields["resonance"].widget.suggestions = suggestions

    def _get_additional_categories(self):
        """Add mage-specific categories with affordability filtering."""
        categories = []

        # Arete - check availability
        if self.instance:
            can_add_arete = True
            if self.instance.freebies < 4:
                can_add_arete = False
            elif self.instance.total_freebies() == 45 and self.instance.arete >= 4:
                can_add_arete = False
            elif self.instance.total_freebies() != 45 and self.instance.arete >= 3:
                can_add_arete = False
            elif self.instance.other_tenets.count() + 3 == self.instance.arete:
                can_add_arete = False

            if can_add_arete:
                categories.append(("Arete", "Arete"))

            # Sphere - check affordability
            if self.instance.freebies >= 7:
                categories.append(("Sphere", "Sphere"))

            # Resonance - check affordability
            if self.instance.freebies >= 3:
                categories.append(("Resonance", "Resonance"))

            # Quintessence and Rotes - always available
            categories.append(("Quintessence", "Quintessence"))
            categories.append(("Rotes", "Rotes"))

            # Tenet and Practice
            categories.append(("Tenet", "Tenet"))
            categories.append(("Practice", "Practice"))

        return categories

    def _get_additional_example_choices(self):
        """Add mage-specific example choices for each category."""
        choices = {}

        if self.instance:
            # Spheres - filter to those below max
            spheres = [
                s
                for s in Sphere.objects.order_by("name")
                if getattr(self.instance, s.property_name, 0) < 5
            ]
            choices["Sphere"] = [(str(s.pk), str(s)) for s in spheres]

            # Arete - show level options
            arete_options = []
            current_arete = self.instance.arete
            max_arete = 4 if self.instance.total_freebies() == 45 else 3
            if current_arete < max_arete:
                arete_options.append((str(current_arete + 1), f"Arete {current_arete + 1}"))
            choices["Arete"] = arete_options

            # Tenets
            tenets = Tenet.objects.order_by("name")
            choices["Tenet"] = [(str(t.pk), str(t)) for t in tenets]

            # Practices
            practices = (
                Practice.objects.exclude(polymorphic_ctype__model="specializedpractice")
                .exclude(polymorphic_ctype__model="corruptedpractice")
                .order_by("name")
            )
            choices["Practice"] = [(str(p.pk), str(p)) for p in practices]

            # Categories with no example selection
            choices["Quintessence"] = []
            choices["Rotes"] = []
            choices["Resonance"] = []

        return choices

    def clean(self):
        cleaned_data = super().clean()
        category = self.data.get("category")

        if category == "Resonance" and self.data.get("resonance", "") == "":
            raise forms.ValidationError("Must Choose Resonance")

        return cleaned_data
