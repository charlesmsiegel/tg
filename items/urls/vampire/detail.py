from django.urls import path

from items import views

urls = [
    path(
        "artifact/<pk>/",
        views.vampire.VampireArtifactDetailView.as_view(),
        name="artifact",
    ),
    path(
        "bloodstone/<pk>/",
        views.vampire.BloodstoneDetailView.as_view(),
        name="bloodstone",
    ),
]
