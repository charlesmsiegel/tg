from django.urls import path

from locations import views

app_name = "demon:update"
urls = [
    path(
        "bastion/<pk>/",
        views.demon.BastionUpdateView.as_view(),
        name="bastion",
    ),
    path(
        "reliquary/<pk>/",
        views.demon.ReliquaryUpdateView.as_view(),
        name="reliquary",
    ),
]
