from django.urls import path

from characters.views.core.archetype import ArchetypeUpdateView
from characters.views.core.character import CharacterUpdateView
from characters.views.core.derangement import DerangementUpdateView
from characters.views.core.group import GroupUpdateView
from characters.views.core.human import HumanCharacterCreationView, HumanUpdateView
from characters.views.core.meritflaw import MeritFlawUpdateView
from characters.views.core.specialty import SpecialtyUpdateView

app_name = "characters:update"
urls = [
    path(
        "character/<pk>/",
        CharacterUpdateView.as_view(),
        name="character",
    ),
    path(
        "group/<pk>/",
        GroupUpdateView.as_view(),
        name="group",
    ),
    path(
        "human/full/<pk>/",
        HumanUpdateView.as_view(),
        name="human_full",
    ),
    path(
        "human/<pk>/",
        HumanCharacterCreationView.as_view(),
        name="human",
    ),
    path(
        "archetypes/<pk>/",
        ArchetypeUpdateView.as_view(),
        name="archetype",
    ),
    path(
        "meritflaws/<pk>/",
        MeritFlawUpdateView.as_view(),
        name="meritflaw",
    ),
    path(
        "specialties/<pk>/",
        SpecialtyUpdateView.as_view(),
        name="specialty",
    ),
    path(
        "derangement/<pk>/",
        DerangementUpdateView.as_view(),
        name="derangement",
    ),
]
