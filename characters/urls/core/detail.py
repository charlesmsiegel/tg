from django.urls import path

from characters.views.core import GenericCharacterDetailView, GenericGroupDetailView
from characters.views.core.actions import (
    CharacterDeceaseView,
    CharacterRetireView,
    CharacterSpecialtiesView,
    XPRequestApproveView,
    XPRequestRejectView,
)
from characters.views.core.archetype import ArchetypeDetailView
from characters.views.core.chargen_back import ChargenBackView
from characters.views.core.derangement import DerangementDetailView
from characters.views.core.meritflaw import MeritFlawDetailView
from characters.views.core.specialty import SpecialtyDetailView

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
    path("<int:pk>/chargen/back/", ChargenBackView.as_view(), name="chargen_back"),
    # Sheet actions: one POST endpoint each (Step 5).
    path(
        "<int:pk>/xp-requests/<int:request_pk>/approve/",
        XPRequestApproveView.as_view(),
        name="xp_request_approve",
    ),
    path(
        "<int:pk>/xp-requests/<int:request_pk>/reject/",
        XPRequestRejectView.as_view(),
        name="xp_request_reject",
    ),
    path("<int:pk>/retire/", CharacterRetireView.as_view(), name="retire"),
    path("<int:pk>/decease/", CharacterDeceaseView.as_view(), name="decease"),
    path("<int:pk>/specialties/", CharacterSpecialtiesView.as_view(), name="add_specialties"),
    path("<pk>/", GenericCharacterDetailView.as_view(), name="character"),
]
