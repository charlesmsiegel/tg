from django.urls import path
from items import views

app_name = "vampire:list"
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
