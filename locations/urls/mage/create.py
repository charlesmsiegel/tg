from django.urls import path
from locations import views

app_name = "mage:create"
urls = [
    path(
        "node/",
        views.mage.NodeCreateView.as_view(),
        name="node",
    ),
    path(
        "sector/",
        views.mage.SectorCreateView.as_view(),
        name="sector",
    ),
    path(
        "realm/",
        views.mage.RealmCreateView.as_view(),
        name="horizon_realm",
    ),
    path(
        "paradox_realm/",
        views.mage.ParadoxRealmCreateView.as_view(),
        name="paradox_realm",
    ),
    path(
        "sanctum/",
        views.mage.SanctumCreateView.as_view(),
        name="sanctum",
    ),
    path(
        "demesne/",
        views.mage.DemesneCreateView.as_view(),
        name="demesne",
    ),
    path(
        "library/",
        views.mage.LibraryCreateView.as_view(),
        name="library",
    ),
    path(
        "chantry/",
        views.mage.ChantryBasicsView.as_view(),
        name="chantry",
    ),
    path(
        "reality_zone/",
        views.mage.RealityZoneCreateView.as_view(),
        name="reality_zone",
    ),
]
