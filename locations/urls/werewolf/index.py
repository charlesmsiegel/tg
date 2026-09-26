from django.urls import path

from locations import views

urls = [
    path("caern/", views.werewolf.CaernListView.as_view(), name="caern"),
]
