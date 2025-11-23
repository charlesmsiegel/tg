from django.urls import path
from items import views

app_name = "wraith:list"
urls = [
    path(
        "relics/",
        views.wraith.WraithRelicListView.as_view(),
        name="relic",
    ),
    path(
        "artifacts/",
        views.wraith.WraithArtifactListView.as_view(),
        name="artifact",
    ),
]
