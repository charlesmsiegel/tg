from django.urls import path

from locations import views

urls = [
    path("byway/", views.wraith.BywayListView.as_view(), name="byway"),
    path("citadel/", views.wraith.CitadelListView.as_view(), name="citadel"),
    path("freehold/", views.wraith.WraithFreeholdListView.as_view(), name="freehold"),
    path("haunt/", views.wraith.HauntListView.as_view(), name="haunt"),
    path("necropolis/", views.wraith.NecropolisListView.as_view(), name="necropolis"),
    path("nihil/", views.wraith.NihilListView.as_view(), name="nihil"),
]
