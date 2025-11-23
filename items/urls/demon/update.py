from django.urls import path
from items import views

app_name = "demon:update"
urls = [
    path(
        "relic/<pk>/",
        views.demon.RelicUpdateView.as_view(),
        name="relic",
    ),
]
