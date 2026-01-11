from django.urls import path

from items import views

urls = [
    path(
        "fetish/<pk>/",
        views.werewolf.FetishUpdateView.as_view(),
        name="fetish",
    ),
    path(
        "talen/<pk>/",
        views.werewolf.TalenUpdateView.as_view(),
        name="talen",
    ),
]
