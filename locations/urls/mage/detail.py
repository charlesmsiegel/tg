from django.urls import path
from locations import views

app_name = "locations:detail"
urls = [
    path("node/<pk>/", views.mage.NodeDetailView.as_view(), name="node"),
    path("sector/<pk>/", views.mage.SectorDetailView.as_view(), name="sector"),
    path("chantry/<pk>/", views.mage.ChantryDetailView.as_view(), name="chantry"),
    path("library/<pk>/", views.mage.LibraryDetailView.as_view(), name="library"),
    path(
        "horizon_realm/<pk>/",
        views.mage.RealmDetailView.as_view(),
        name="horizon_realm",
    ),
    path("sanctum/<pk>/", views.mage.SanctumDetailView.as_view(), name="sanctum"),
    path(
        "reality_zone/<pk>/",
        views.mage.RealityZoneDetailView.as_view(),
        name="reality_zone",
    ),
]
