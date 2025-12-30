from django.urls import path
from locations import views

urlpatterns = [
    path("node/", views.mage.NodeListView.as_view(), name="node-list"),
    path("sector/", views.mage.SectorListView.as_view(), name="sector-list"),
    path("chantry/", views.mage.ChantryListView.as_view(), name="chantry-list"),
    path("library/", views.mage.LibraryListView.as_view(), name="library-list"),
    path("horizon_realm/", views.mage.RealmListView.as_view(), name="horizon-realm-list"),
    path(
        "paradox_realm/",
        views.mage.ParadoxRealmListView.as_view(),
        name="paradox-realm-list",
    ),
    path("sanctum/", views.mage.SanctumListView.as_view(), name="sanctum-list"),
    path("demesne/", views.mage.DemesneListView.as_view(), name="demesne-list"),
    path(
        "reality_zone/",
        views.mage.RealityZoneListView.as_view(),
        name="reality-zone-list",
    ),
]
