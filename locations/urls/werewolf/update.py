from django.urls import path

from locations import views

urls = [
    path(
        "caern/<pk>/",
        views.werewolf.CaernUpdateView.as_view(),
        name="caern",
    ),
]
