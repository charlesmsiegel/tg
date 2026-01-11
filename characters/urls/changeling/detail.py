from django.urls import path

from characters import views as characters
from characters.views.changeling.autumn_person import AutumnPersonDetailView
from characters.views.changeling.cantrip import CantripDetailView
from characters.views.changeling.changeling import ChangelingDetailView
from characters.views.changeling.chimera import ChimeraDetailView
from characters.views.changeling.house import HouseDetailView
from characters.views.changeling.house_faction import HouseFactionDetailView
from characters.views.changeling.inanimae import InanimaeDetailView
from characters.views.changeling.kith import KithDetailView
from characters.views.changeling.legacy import LegacyDetailView
from characters.views.changeling.motley import MotleyDetailView
from characters.views.changeling.nunnehi import NunnehiDetailView

urls = [
    path(
        "autumn_person/<pk>/",
        AutumnPersonDetailView.as_view(),
        name="autumn_person",
    ),
    path(
        "inanimae/<pk>/",
        InanimaeDetailView.as_view(),
        name="inanimae",
    ),
    path(
        "nunnehi/<pk>/",
        NunnehiDetailView.as_view(),
        name="nunnehi",
    ),
    path(
        "kith/<pk>/",
        KithDetailView.as_view(),
        name="kith",
    ),
    path(
        "house/<pk>/",
        HouseDetailView.as_view(),
        name="house",
    ),
    path(
        "house_faction/<pk>/",
        HouseFactionDetailView.as_view(),
        name="house_faction",
    ),
    path(
        "legacy/<pk>/",
        LegacyDetailView.as_view(),
        name="legacy",
    ),
    path(
        "ctdhuman/<int:pk>/template/",
        characters.changeling.CtDHumanTemplateSelectView.as_view(),
        name="ctdhuman_template",
    ),
    path(
        "ctdhuman/<int:pk>/creation/",
        characters.changeling.CtDHumanCharacterCreationView.as_view(),
        name="ctdhuman_creation",
    ),
    path(
        "changeling/<pk>/",
        ChangelingDetailView.as_view(),
        name="changeling",
    ),
    path(
        "motley/<pk>/",
        MotleyDetailView.as_view(),
        name="motley",
    ),
    path(
        "cantrip/<pk>/",
        CantripDetailView.as_view(),
        name="cantrip",
    ),
    path(
        "chimera/<pk>/",
        ChimeraDetailView.as_view(),
        name="chimera",
    ),
]
