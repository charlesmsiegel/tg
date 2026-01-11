from django.urls import path

from characters.views.changeling.cantrip import CantripListView
from characters.views.changeling.chimera import ChimeraListView
from characters.views.changeling.house import HouseListView
from characters.views.changeling.house_faction import HouseFactionListView
from characters.views.changeling.kith import KithListView
from characters.views.changeling.legacy import LegacyListView
from characters.views.changeling.motley import MotleyListView

urls = [
    path(
        "cantrip/",
        CantripListView.as_view(),
        name="cantrip",
    ),
    path(
        "chimera/",
        ChimeraListView.as_view(),
        name="chimera",
    ),
    path(
        "kith/",
        KithListView.as_view(),
        name="kith",
    ),
    path(
        "house/",
        HouseListView.as_view(),
        name="house",
    ),
    path(
        "house_faction/",
        HouseFactionListView.as_view(),
        name="house_faction",
    ),
    path(
        "legacy/",
        LegacyListView.as_view(),
        name="legacy",
    ),
    path(
        "motley/",
        MotleyListView.as_view(),
        name="motley",
    ),
]
