from characters.views.changeling.changeling import ChangelingUpdateView
from characters.views.changeling.ctdhuman import CtDHumanUpdateView
from characters.views.changeling.house import HouseUpdateView
from characters.views.changeling.house_faction import HouseFactionUpdateView
from characters.views.changeling.kith import KithUpdateView
from characters.views.changeling.legacy import LegacyUpdateView
from characters.views.changeling.motley import MotleyUpdateView
from django.urls import path

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
]
