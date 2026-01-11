from django.urls import path

from characters.views.changeling.autumn_person import AutumnPersonUpdateView
from characters.views.changeling.cantrip import CantripUpdateView
from characters.views.changeling.changeling import ChangelingUpdateView
from characters.views.changeling.chimera import ChimeraUpdateView
from characters.views.changeling.ctdhuman import CtDHumanUpdateView
from characters.views.changeling.house import HouseUpdateView
from characters.views.changeling.house_faction import HouseFactionUpdateView
from characters.views.changeling.inanimae import InanimaeUpdateView
from characters.views.changeling.kith import KithUpdateView
from characters.views.changeling.legacy import LegacyUpdateView
from characters.views.changeling.motley import MotleyUpdateView
from characters.views.changeling.nunnehi import NunnehiUpdateView

urls = [
    path(
        "changeling/<pk>/",
        ChangelingUpdateView.as_view(),
        name="changeling",
    ),
    path(
        "changeling/full/<pk>/",
        ChangelingUpdateView.as_view(),
        name="changeling_full",
    ),
    path(
        "motley/<pk>/",
        MotleyUpdateView.as_view(),
        name="motley",
    ),
    path(
        "kith/<pk>/",
        KithUpdateView.as_view(),
        name="kith",
    ),
    path(
        "house/<pk>/",
        HouseUpdateView.as_view(),
        name="house",
    ),
    path(
        "house_faction/<pk>/",
        HouseFactionUpdateView.as_view(),
        name="house_faction",
    ),
    path(
        "legacy/<pk>/",
        LegacyUpdateView.as_view(),
        name="legacy",
    ),
    path(
        "ctdhuman/<pk>/",
        CtDHumanUpdateView.as_view(),
        name="ctd_human",
    ),
    path(
        "ctdhuman/full/<pk>/",
        CtDHumanUpdateView.as_view(),
        name="ctd_human_full",
    ),
    path(
        "inanimae/<pk>/",
        InanimaeUpdateView.as_view(),
        name="inanimae",
    ),
    path(
        "nunnehi/<pk>/",
        NunnehiUpdateView.as_view(),
        name="nunnehi",
    ),
    path(
        "autumn_person/<pk>/",
        AutumnPersonUpdateView.as_view(),
        name="autumn_person",
    ),
    path(
        "cantrip/<pk>/",
        CantripUpdateView.as_view(),
        name="cantrip",
    ),
    path(
        "chimera/<pk>/",
        ChimeraUpdateView.as_view(),
        name="chimera",
    ),
]
