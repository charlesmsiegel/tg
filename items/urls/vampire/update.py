from django.urls import path
from items import views

app_name = "vampire:update"
urls = [
    path(
        "artifact/<pk>/",
        views.vampire.VampireArtifactUpdateView.as_view(),
        name="artifact",
    ),
    path(
        "bloodstone/<pk>/",
        views.vampire.BloodstoneUpdateView.as_view(),
        name="bloodstone",
    ),
]
