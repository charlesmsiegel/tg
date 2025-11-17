from django.urls import path

from locations import views

urls = [
    path("haunt/", views.wraith.HauntListView.as_view(), name="haunt"),
    path("necropolis/", views.wraith.NecropolisListView.as_view(), name="necropolis"),
]
