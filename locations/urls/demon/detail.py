from django.urls import path

from locations import views

urls = [
    path(
        "bastion/<pk>/",
        views.demon.BastionDetailView.as_view(),
        name="bastion",
    ),
    path(
        "reliquary/<pk>/",
        views.demon.ReliquaryDetailView.as_view(),
        name="reliquary",
    ),
]
