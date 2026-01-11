from django.urls import path

from locations import views

app_name = "demon:create"
urls = [
    path(
        "bastion/",
        views.demon.BastionCreateView.as_view(),
        name="bastion",
    ),
    path(
        "reliquary/",
        views.demon.ReliquaryCreateView.as_view(),
        name="reliquary",
    ),
]
