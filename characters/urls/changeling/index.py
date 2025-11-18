from characters.views.changeling.house import HouseListView
from characters.views.changeling.house_faction import HouseFactionListView
from characters.views.changeling.kith import KithListView
from characters.views.changeling.legacy import LegacyListView
from django.urls import path

urls = [
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
]
