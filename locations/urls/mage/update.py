from django.urls import path
from locations import views

app_name = "locations:update"
urls = [
    path(
        "node/<pk>/",
        views.mage.NodeUpdateView.as_view(),
        name="node",
    ),
    path(
        "sector/<pk>/",
        views.mage.SectorUpdateView.as_view(),
        name="sector",
    ),
    path(
        "library/<pk>/",
        views.mage.LibraryUpdateView.as_view(),
        name="library",
    ),
    path(
        "realm/<pk>/",
        views.mage.RealmUpdateView.as_view(),
        name="horizon_realm",
    ),
    path(
        "paradox_realm/<pk>/",
        views.mage.ParadoxRealmUpdateView.as_view(),
        name="paradox_realm",
    ),
    path(
        "sanctum/<pk>/",
        views.mage.SanctumUpdateView.as_view(),
        name="sanctum",
    ),
    path(
        "chantry/<pk>/",
        views.mage.ChantryUpdateView.as_view(),
        name="chantry",
    ),
    path(
        "reality_zone/<pk>/",
        views.mage.RealityZoneUpdateView.as_view(),
        name="reality_zone",
    ),
]
