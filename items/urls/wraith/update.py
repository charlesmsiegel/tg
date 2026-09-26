from django.urls import path

from items import views

urls = [
    path(
        "relic/<pk>/",
        views.wraith.WraithRelicUpdateView.as_view(),
        name="relic",
    ),
    path(
        "artifact/<pk>/",
        views.wraith.WraithArtifactUpdateView.as_view(),
        name="artifact",
    ),
]
