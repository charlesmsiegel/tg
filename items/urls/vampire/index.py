from django.urls import path

from items import views

urls = [
    path(
        "artifacts/",
        views.vampire.VampireArtifactListView.as_view(),
        name="artifact",
    ),
    path(
        "bloodstones/",
        views.vampire.BloodstoneListView.as_view(),
        name="bloodstone",
    ),
]
