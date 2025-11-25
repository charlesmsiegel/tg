from django.urls import path
from items import views

app_name = "hunter:create"
urls = [
    path(
        "gear/",
        views.hunter.HunterGearCreateView.as_view(),
        name="gear",
    ),
    path(
        "relic/",
        views.hunter.HunterRelicCreateView.as_view(),
        name="relic",
    ),
]
