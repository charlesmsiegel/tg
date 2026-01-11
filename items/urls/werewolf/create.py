from django.urls import path

from items import views

urls = [
    path(
        "fetish/",
        views.werewolf.FetishCreateView.as_view(),
        name="fetish",
    ),
    path(
        "talen/",
        views.werewolf.TalenCreateView.as_view(),
        name="talen",
    ),
]
