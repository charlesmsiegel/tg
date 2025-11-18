from characters.views.changeling.house import HouseDetailView
from characters.views.changeling.house_faction import HouseFactionDetailView
from characters.views.changeling.kith import KithDetailView
from characters.views.changeling.legacy import LegacyDetailView
from django.urls import path

urls = [
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
]
