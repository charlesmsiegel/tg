from django.urls import path
from items import views

app_name = "wraith:create"
urls = [
    path(
        "relic/",
        views.wraith.WraithRelicCreateView.as_view(),
        name="relic",
    ),
    path(
        "artifact/",
        views.wraith.WraithArtifactCreateView.as_view(),
        name="artifact",
    ),
]
