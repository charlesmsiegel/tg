from django.urls import path

from items import views

urls = [
    path(
        "relics/",
        views.demon.RelicListView.as_view(),
        name="relic",
    ),
]
