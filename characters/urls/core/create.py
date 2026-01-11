from django.urls import path

from characters.views.core.archetype import ArchetypeCreateView
from characters.views.core.character import CharacterCreateView
from characters.views.core.derangement import DerangementCreateView
from characters.views.core.group import GroupCreateView
from characters.views.core.human import HumanBasicsView, HumanCreateView
from characters.views.core.meritflaw import MeritFlawCreateView
from characters.views.core.npc import NPCProfileCreateView
from characters.views.core.specialty import SpecialtyCreateView

app_name = "characters:create"
urls = [
    path(
        "character/",
        CharacterCreateView.as_view(),
        name="character",
    ),
    path(
        "group/",
        GroupCreateView.as_view(),
        name="group",
    ),
    path(
        "human/",
        HumanBasicsView.as_view(),
        name="human",
    ),
    path(
        "human/full/",
        HumanCreateView.as_view(),
        name="human_full",
    ),
    path(
        "npc/",
        NPCProfileCreateView.as_view(),
        name="npc",
    ),
    path(
        "npc/<int:pk>/",
        NPCProfileCreateView.as_view(),
        name="npc_for_character",
    ),
    path(
        "archetypes/",
        ArchetypeCreateView.as_view(),
        name="archetype",
    ),
    path(
        "meritflaws/",
        MeritFlawCreateView.as_view(),
        name="meritflaw",
    ),
    path(
        "specialties/",
        SpecialtyCreateView.as_view(),
        name="specialty",
    ),
    path(
        "derangement/",
        DerangementCreateView.as_view(),
        name="derangement",
    ),
]
