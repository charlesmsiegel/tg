from django.urls import path
from items import views

app_name = "hunter:list"
urls = [
    path(
        "gear/",
        views.hunter.HunterGearListView.as_view(),
        name="gear",
    ),
    path(
        "relics/",
        views.hunter.HunterRelicListView.as_view(),
        name="relic",
    ),
]
