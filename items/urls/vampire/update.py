from django.urls import path

from items import views

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
