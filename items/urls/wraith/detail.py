from django.urls import path

from items import views

app_name = "wraith:detail"
urls = [
    path(
        "relic/<pk>/",
        views.wraith.WraithRelicDetailView.as_view(),
        name="relic",
    ),
    path(
        "artifact/<pk>/",
        views.wraith.WraithArtifactDetailView.as_view(),
        name="artifact",
    ),
]
