from django.urls import path

from locations import views

urls = [
    path(
        "bastion/",
        views.demon.BastionListView.as_view(),
        name="bastion",
    ),
    path(
        "reliquary/",
        views.demon.ReliquaryListView.as_view(),
        name="reliquary",
    ),
]
