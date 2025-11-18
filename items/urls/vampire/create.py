from django.urls import path
from items import views

app_name = "vampire:create"
urls = [
    path(
        "artifact/",
        views.vampire.VampireArtifactCreateView.as_view(),
        name="artifact",
    ),
    path(
        "bloodstone/",
        views.vampire.BloodstoneCreateView.as_view(),
        name="bloodstone",
    ),
]
