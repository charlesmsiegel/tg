from characters.views.core.archetype import ArchetypeListView
from characters.views.core.derangement import DerangementListView
from characters.views.core.meritflaw import MeritFlawListView
from characters.views.core.specialty import SpecialtyListView
from django.urls import path

app_name = "characters:list"
urls = [
    path(
        "archetypes/",
        ArchetypeListView.as_view(),
        name="archetype",
    ),
    path(
        "meritflaws/",
        MeritFlawListView.as_view(),
        name="meritflaw",
    ),
    path(
        "specialties/",
        SpecialtyListView.as_view(),
        name="specialty",
    ),
    path(
        "derangement/",
        DerangementListView.as_view(),
        name="derangement",
    ),
]
