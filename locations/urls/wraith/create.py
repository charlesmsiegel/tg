from django.urls import path

from locations import views

app_name = "wraith:create"
urls = [
    path(
        "byway/",
        views.wraith.BywayCreateView.as_view(),
        name="byway",
    ),
    path(
        "citadel/",
        views.wraith.CitadelCreateView.as_view(),
        name="citadel",
    ),
    path(
        "freehold/",
        views.wraith.WraithFreeholdCreateView.as_view(),
        name="freehold",
    ),
    path(
        "haunt/",
        views.wraith.HauntCreateView.as_view(),
        name="haunt",
    ),
    path(
        "necropolis/",
        views.wraith.NecropolisCreateView.as_view(),
        name="necropolis",
    ),
    path(
        "nihil/",
        views.wraith.NihilCreateView.as_view(),
        name="nihil",
    ),
]
