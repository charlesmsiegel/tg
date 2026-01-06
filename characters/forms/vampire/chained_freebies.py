"""
Vampire-specific Chained Select Freebie Forms
"""

from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.models.vampire.discipline import Discipline


class ChainedGhoulFreebiesForm(ChainedHumanFreebiesForm):
    """Ghoul freebie form with Discipline category."""

    def _get_additional_categories(self):
        return [("Discipline", "Discipline")]

    def _get_additional_example_choices(self):
        """Add Discipline options."""
        disciplines = Discipline.objects.order_by("name")
        return {
            "Discipline": [(str(d.pk), str(d)) for d in disciplines],
        }


class ChainedVampireFreebiesForm(ChainedHumanFreebiesForm):
    """Vampire freebie form with Discipline, Virtue, Humanity, Path Rating categories."""

    def _get_additional_categories(self):
        return [
            ("Discipline", "Discipline"),
            ("Virtue", "Virtue"),
            ("Humanity", "Humanity"),
            ("Path Rating", "Path Rating"),
        ]

    def _get_additional_example_choices(self):
        """Add Vampire-specific options."""
        disciplines = Discipline.objects.order_by("name")

        # Virtues are integer fields on the character, not separate model instances
        # Build virtue options based on which virtues the character uses
        virtue_options = []
        if self.instance:
            # Standard virtues
            if not getattr(self.instance, "has_conviction", False):
                virtue_options.append(("conscience", "Conscience"))
            else:
                virtue_options.append(("conviction", "Conviction"))
            if not getattr(self.instance, "has_instinct", False):
                virtue_options.append(("self_control", "Self-Control"))
            else:
                virtue_options.append(("instinct", "Instinct"))
            virtue_options.append(("courage", "Courage"))

        return {
            "Discipline": [(str(d.pk), str(d)) for d in disciplines],
            "Virtue": virtue_options,
            "Humanity": [],  # No example selection needed
            "Path Rating": [],  # No example selection needed
        }
