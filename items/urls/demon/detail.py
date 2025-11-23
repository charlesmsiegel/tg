from django.urls import path
from items import views

app_name = "demon:detail"
urls = [
    path(
        "relic/<pk>/",
        views.demon.RelicDetailView.as_view(),
        name="relic",
    ),
]
