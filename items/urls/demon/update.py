from django.urls import path
from items import views

urls = [
    path(
        "relic/<pk>/",
        views.demon.RelicUpdateView.as_view(),
        name="relic",
    ),
]
