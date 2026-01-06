"""
Example: Mage the Ascension Faction Selector - Minimal Setup Version

This shows the simplest possible usage. Just define the form fields and you're done.
No AJAX endpoints, no URL configuration, no extra JavaScript setup.
"""

from chained_select import ChainedChoiceField, ChainedSelectMixin
from django import forms

# =============================================================================
# Just define your form - that's it!
# =============================================================================


class MageFactionForm(ChainedSelectMixin, forms.Form):
    """
    Complete faction selector with zero configuration.

    Usage in view:
        form = MageFactionForm()

    Usage in template:
        {{ form.as_p }}    {# That's it! JavaScript auto-injects. #}

    The cascading behavior works automatically.
    """

    affiliation = ChainedChoiceField(
        label="Affiliation",
        choices=[
            ("traditions", "Council of Nine Mystic Traditions"),
            ("technocracy", "Technocratic Union"),
        ],
        empty_label="Select affiliation...",
    )

    faction = ChainedChoiceField(
        label="Tradition / Convention",
        parent_field="affiliation",
        empty_label="Select tradition/convention...",
        choices_map={
            "traditions": [
                ("akashic", "Akashic Brotherhood"),
                ("celestial_chorus", "Celestial Chorus"),
                ("cult_of_ecstasy", "Cult of Ecstasy"),
                ("dreamspeakers", "Dreamspeakers"),
                ("euthanatos", "Euthanatos"),
                ("hermetic", "Order of Hermes"),
                ("sons_of_ether", "Sons of Ether"),
                ("verbena", "Verbena"),
                ("virtual_adepts", "Virtual Adepts"),
            ],
            "technocracy": [
                ("iteration_x", "Iteration X"),
                ("new_world_order", "New World Order"),
                ("progenitors", "Progenitors"),
                ("syndicate", "Syndicate"),
                ("void_engineers", "Void Engineers"),
            ],
        },
    )

    subfaction = ChainedChoiceField(
        label="Subfaction / Methodology",
        parent_field="faction",
        empty_label="Select subfaction...",
        required=False,
        choices_map={
            # Traditions subfactions
            "akashic": [
                ("kannagara", "Kannagara"),
                ("li_hai", "Li-Hai"),
                ("mo_ai", "Mo-Ai"),
                ("shaolin", "Shaolin"),
                ("vajrapani", "Vajrapani"),
                ("wu_lung", "Wu Lung"),
            ],
            "celestial_chorus": [
                ("alexandrian", "Alexandrian Society"),
                ("anchorite", "Anchorite"),
                ("latitudinarian", "Latitudinarian"),
                ("monist", "Monist"),
                ("nashimite", "Nashimite"),
                ("septarian", "Septarian"),
                ("song", "Song of the Ancients"),
            ],
            "cult_of_ecstasy": [
                ("aghoris", "Aghoris"),
                ("clubkids", "Club Kids"),
                ("dissonance", "Dissonance Society"),
                ("freyja", "Children of Freyja"),
                ("joybringers", "Joybringers"),
                ("maenad", "Maenad"),
                ("acharne", "K'an Lu / Acharne"),
            ],
            "dreamspeakers": [
                ("balombe", "Balombe"),
                ("baruti", "Baruti"),
                ("ghost_wheel", "Ghost Wheel Society"),
                ("kopa_loei", "Kopa Loei"),
                ("red_spears", "Red Spear Society"),
                ("spirit_smiths", "Spirit Smiths"),
                ("solitaries", "Solitaries"),
            ],
            "euthanatos": [
                ("aided", "Aided"),
                ("albireo", "Albireo"),
                ("chakravanti", "Chakravanti"),
                ("golden_chalice", "Golden Chalice"),
                ("lhaksmists", "Lhaksmists"),
                ("madzimbabwe", "Madzimbabwe"),
                ("natatapas", "Natatapas"),
                ("pomegranate", "Pomegranate Deme"),
                ("vrati", "Vrati"),
            ],
            "hermetic": [
                ("bonisagus", "House Bonisagus"),
                ("criamon", "House Criamon"),
                ("ex_miscellanea", "House Ex Miscellanea"),
                ("flambeau", "House Flambeau"),
                ("fortunae", "House Fortunae"),
                ("hong_lei", "House Hong Lei"),
                ("janissary", "House Janissary"),
                ("merinita", "House Merinita"),
                ("quaesitor", "House Quaesitor"),
                ("shaea", "House Shaea"),
                ("skopos", "House Skopos"),
                ("solificati", "House Solificati"),
                ("tharsis", "House Tharsis"),
                ("tytalus", "House Tytalus"),
                ("verditius", "House Verditius"),
                ("xaos", "House Xaos"),
            ],
            "sons_of_ether": [
                ("adventurers", "Adventurers"),
                ("cybernauts", "Cybernauts"),
                ("ethernauts", "Ethernauts"),
                ("mad_scientists", "Mad Scientists"),
                ("progressivists", "Progressivists"),
                ("utopians", "Utopians"),
            ],
            "verbena": [
                ("gardeners", "Gardeners of the Tree"),
                ("lifeweavers", "Lifeweavers"),
                ("moon_seekers", "Moon-Seekers"),
                ("twisters", "Twisters of Fate"),
                ("techno_pagans", "Techno-Pagans"),
            ],
            "virtual_adepts": [
                ("cypherpunks", "Cypherpunks"),
                ("chaoticians", "Chaoticians"),
                ("cyberpunks", "Cyberpunks"),
                ("nexplorers", "Nexplorers"),
                ("reality_coders", "Reality Coders"),
            ],
            # Technocracy methodologies
            "iteration_x": [
                ("biome", "BioMechanics"),
                ("macrotechnicians", "Macrotechnicians"),
                ("statisticians", "Statisticians"),
                ("time_motion", "Time-Motion Managers"),
            ],
            "new_world_order": [
                ("ivory_tower", "Ivory Tower"),
                ("operatives", "Operatives"),
                ("q_division", "Q Division"),
                ("watchers", "Watchers"),
            ],
            "progenitors": [
                ("facade", "FACADE Engineers"),
                ("genegineers", "Genegineers"),
                ("pharmacopoeists", "Pharmacopoeists"),
                ("preservationists", "Preservationists"),
                ("shalihotran", "Shalihotran Society"),
            ],
            "syndicate": [
                ("disbursements", "Disbursements"),
                ("enforcers", "Enforcers"),
                ("financiers", "Financiers"),
                ("media_control", "Media Control"),
                ("special_projects", "Special Projects Division"),
            ],
            "void_engineers": [
                ("border_corps", "Border Corps Division"),
                ("deep_exploration", "Deep Exploration Teams"),
                ("earth_frontier", "Earth Frontier Division"),
                ("neutralization", "Neutralization Specialist Corps"),
                ("pan_dimensional", "Pan-Dimensional Corps"),
                ("research", "Research & Execution"),
            ],
        },
    )

    # You can mix in regular fields too
    character_name = forms.CharField(
        label="Character Name",
        max_length=100,
        required=False,
    )


# =============================================================================
# Example with 4+ levels (showing extensibility)
# =============================================================================


class ExtendedFactionForm(ChainedSelectMixin, forms.Form):
    """Example showing deeper nesting works automatically."""

    game_line = ChainedChoiceField(
        choices=[
            ("mage", "Mage: The Ascension"),
            ("vampire", "Vampire: The Masquerade"),
            ("werewolf", "Werewolf: The Apocalypse"),
        ],
        empty_label="Select game...",
    )

    affiliation = ChainedChoiceField(
        parent_field="game_line",
        empty_label="Select affiliation...",
        choices_map={
            "mage": [
                ("traditions", "Traditions"),
                ("technocracy", "Technocracy"),
            ],
            "vampire": [
                ("camarilla", "Camarilla"),
                ("sabbat", "Sabbat"),
                ("anarchs", "Anarchs"),
            ],
            "werewolf": [
                ("garou_nation", "Garou Nation"),
            ],
        },
    )

    faction = ChainedChoiceField(
        parent_field="affiliation",
        empty_label="Select faction...",
        choices_map={
            "traditions": [
                ("hermetic", "Order of Hermes"),
                ("verbena", "Verbena"),
                # ... etc
            ],
            "technocracy": [
                ("iteration_x", "Iteration X"),
                # ... etc
            ],
            "camarilla": [
                ("ventrue", "Ventrue"),
                ("toreador", "Toreador"),
                ("tremere", "Tremere"),
                # ... etc
            ],
            # ... etc
        },
    )


# =============================================================================
# That's really all you need! Here's a complete view for reference:
# =============================================================================

"""
# views.py
from django.views.generic import FormView
from .forms import MageFactionForm

class CharacterCreateView(FormView):
    template_name = 'character_create.html'
    form_class = MageFactionForm
    success_url = '/characters/'
    
    def form_valid(self, form):
        data = form.cleaned_data
        # Create your character...
        return super().form_valid(form)


# urls.py - No AJAX endpoint needed!
from django.urls import path
from .views import CharacterCreateView

urlpatterns = [
    path('character/create/', CharacterCreateView.as_view()),
]


# templates/character_create.html
'''
<!DOCTYPE html>
<html>
<head>
    <title>Create Character</title>
    <!-- No special includes needed! JavaScript auto-injects. -->
</head>
<body>
    <h1>Create Character</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Create</button>
    </form>
</body>
</html>
'''
"""
