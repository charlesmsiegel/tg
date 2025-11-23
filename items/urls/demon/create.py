from django.urls import path
from items import views

urls = [
    path(
        "relic/",
        views.demon.RelicCreateView.as_view(),
        name="relic",
    ),
]
