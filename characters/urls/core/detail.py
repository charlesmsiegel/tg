from django.urls import path

from characters.views.core import GenericCharacterDetailView, GenericGroupDetailView
from characters.views.core.archetype import ArchetypeDetailView
from characters.views.core.derangement import DerangementDetailView
from characters.views.core.meritflaw import MeritFlawDetailView
from characters.views.core.specialty import SpecialtyDetailView

app_name = "characters:detail"
urls = [
    path("groups/<pk>/", GenericGroupDetailView.as_view(), name="group"),
    path(
        "archetypes/<pk>/",
        ArchetypeDetailView.as_view(),
        name="archetype",
    ),
    path(
        "meritflaws/<pk>/",
        MeritFlawDetailView.as_view(),
        name="meritflaw",
    ),
    path(
        "specialties/<pk>/",
        SpecialtyDetailView.as_view(),
        name="specialty",
    ),
    path(
        "derangement/<pk>/",
        DerangementDetailView.as_view(),
        name="derangement",
    ),
    path("<pk>/", GenericCharacterDetailView.as_view(), name="character"),
]
