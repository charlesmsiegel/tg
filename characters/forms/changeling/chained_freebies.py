"""
Chained Select Changeling Freebie Forms

These forms use ChainedSelectMixin to provide cascading dropdowns
without manual AJAX. Choices are computed at form initialization
and embedded in the page JavaScript.
"""

from characters.forms.core.chained_freebies import ChainedHumanFreebiesForm
from characters.models.core.statistic import Statistic
from django import forms


class ChainedChangelingFreebiesForm(ChainedHumanFreebiesForm):
    """
    Changeling freebie spending form with chained selects.

    Adds Art, Realm, and Glamour categories.
    """

    def _get_additional_categories(self):
        """Add changeling-specific categories."""
        categories = []

        if self.instance:
            # Art - cost 5 freebies
            if self.instance.freebies >= 5:
                categories.append(("Art", "Art"))

            # Realm - cost 3 freebies
            if self.instance.freebies >= 3:
                categories.append(("Realm", "Realm"))

            # Glamour - cost 3 freebies
            if self.instance.freebies >= 3:
                categories.append(("Glamour", "Glamour"))

        return categories

    def _get_additional_example_choices(self):
        """Add changeling-specific example choices for each category."""
        choices = {}

        if self.instance:
            # Arts - all arts below 5 dots
            arts = [
                "autumn",
                "chicanery",
                "chronos",
                "contract",
                "dragons_ire",
                "legerdemain",
                "metamorphosis",
                "naming",
                "oneiromancy",
                "primal",
                "pyretics",
                "skycraft",
                "soothsay",
                "sovereign",
                "spring",
                "summer",
                "wayfare",
                "winter",
            ]
            art_options = []
            for art_name in arts:
                if getattr(self.instance, art_name, 0) < 5:
                    stat = Statistic.objects.filter(property_name=art_name).first()
                    if stat:
                        art_options.append((str(stat.pk), str(stat)))
            choices["Art"] = art_options

            # Realms - all realms below 5 dots
            realms = ["actor", "fae", "nature_realm", "prop", "scene", "time"]
            realm_options = []
            for realm_name in realms:
                if getattr(self.instance, realm_name, 0) < 5:
                    stat = Statistic.objects.filter(property_name=realm_name).first()
                    if stat:
                        realm_options.append((str(stat.pk), str(stat)))
            choices["Realm"] = realm_options

            # Glamour - no example selection needed
            choices["Glamour"] = []

        return choices
