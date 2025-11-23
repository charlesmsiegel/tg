from django.urls import path
from items import views

app_name = "demon:create"
urls = [
    path(
        "relic/",
        views.demon.RelicCreateView.as_view(),
        name="relic",
    ),
]
