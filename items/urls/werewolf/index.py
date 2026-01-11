from django.urls import path

from items import views

urls = [
    path("fetish/", views.werewolf.FetishListView.as_view(), name="fetish"),
    path("talen/", views.werewolf.TalenListView.as_view(), name="talen"),
]
