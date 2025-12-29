from django.urls import path
from locations import views

app_name = "changeling:list"
urls = [
    path(
        "freehold/",
        views.changeling.FreeholdListView.as_view(),
        name="freehold",
    ),
    path(
        "holding/",
        views.changeling.HoldingListView.as_view(),
        name="holding",
    ),
    path(
        "trod/",
        views.changeling.TrodListView.as_view(),
        name="trod",
    ),
    path(
        "dream_realm/",
        views.changeling.DreamRealmListView.as_view(),
        name="dream_realm",
    ),
]
