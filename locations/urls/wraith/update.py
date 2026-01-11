from django.urls import path

from locations import views

app_name = "locations:update"
urls = [
    path(
        "byway/<pk>/",
        views.wraith.BywayUpdateView.as_view(),
        name="byway",
    ),
    path(
        "citadel/<pk>/",
        views.wraith.CitadelUpdateView.as_view(),
        name="citadel",
    ),
    path(
        "freehold/<pk>/",
        views.wraith.WraithFreeholdUpdateView.as_view(),
        name="freehold",
    ),
    path(
        "haunt/<pk>/",
        views.wraith.HauntUpdateView.as_view(),
        name="haunt",
    ),
    path(
        "necropolis/<pk>/",
        views.wraith.NecropolisUpdateView.as_view(),
        name="necropolis",
    ),
    path(
        "nihil/<pk>/",
        views.wraith.NihilUpdateView.as_view(),
        name="nihil",
    ),
]
