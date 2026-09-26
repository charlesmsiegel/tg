from django.urls import path

from locations import views

urls = [
    path(
        "caern/",
        views.werewolf.CaernCreateView.as_view(),
        name="caern",
    ),
]
