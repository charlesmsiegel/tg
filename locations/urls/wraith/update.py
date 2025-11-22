from django.urls import path
from locations import views

app_name = "locations:update"
urls = [
    path(
        "haunt/<pk>/",
        views.wraith.HauntUpdateView.as_view(),
        name="haunt",
    ),
    path(
        "necropolis/<pk>/",
        views.wraith.NecropolisUpdateView.as_view(),
        name="necropolis",
    ),
]
