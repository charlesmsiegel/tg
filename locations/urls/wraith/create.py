from django.urls import path
from locations import views

app_name = "wraith:create"
urls = [
    path(
        "haunt/",
        views.wraith.HauntCreateView.as_view(),
        name="haunt",
    ),
    path(
        "necropolis/",
        views.wraith.NecropolisCreateView.as_view(),
        name="necropolis",
    ),
]
