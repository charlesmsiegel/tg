from django.urls import path

from locations import views

app_name = "locations:update"
urls = [
    path(
        "caern/<pk>/",
        views.werewolf.CaernUpdateView.as_view(),
        name="caern",
    ),
]
