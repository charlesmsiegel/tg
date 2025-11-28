from characters import views as characters
from characters.views.changeling.autumn_person import AutumnPersonDetailView
from characters.views.changeling.house import HouseDetailView
from characters.views.changeling.house_faction import HouseFactionDetailView
from characters.views.changeling.inanimae import InanimaeDetailView
from characters.views.changeling.kith import KithDetailView
from characters.views.changeling.legacy import LegacyDetailView
from characters.views.changeling.nunnehi import NunnehiDetailView
from django.urls import path

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
]
