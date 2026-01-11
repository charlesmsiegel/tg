from django.urls import path

from locations import views

app_name = "demon:list"
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
