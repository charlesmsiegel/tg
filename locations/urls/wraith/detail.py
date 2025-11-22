from django.urls import path
from locations import views

app_name = "locations:detail"
urls = [
    path("haunt/<pk>/", views.wraith.HauntDetailView.as_view(), name="haunt"),
    path(
        "necropolis/<pk>/",
        views.wraith.NecropolisDetailView.as_view(),
        name="necropolis",
    ),
]
