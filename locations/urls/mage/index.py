from django.urls import path

from locations import views

app_name = "mage:list"
urls = [
    path("node/", views.mage.NodeListView.as_view(), name="node"),
    path("sector/", views.mage.SectorListView.as_view(), name="sector"),
    path("chantry/", views.mage.ChantryListView.as_view(), name="chantry"),
    path("library/", views.mage.LibraryListView.as_view(), name="library"),
    path("horizon_realm/", views.mage.RealmListView.as_view(), name="horizon_realm"),
    path(
        "paradox_realm/",
        views.mage.ParadoxRealmListView.as_view(),
        name="paradox_realm",
    ),
    path("sanctum/", views.mage.SanctumListView.as_view(), name="sanctum"),
    path("demesne/", views.mage.DemesneListView.as_view(), name="demesne"),
    path(
        "reality_zone/",
        views.mage.RealityZoneListView.as_view(),
        name="reality_zone",
    ),
]
