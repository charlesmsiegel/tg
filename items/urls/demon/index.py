from django.urls import path

from items import views

app_name = "demon:list"
urls = [
    path(
        "relics/",
        views.demon.RelicListView.as_view(),
        name="relic",
    ),
]
