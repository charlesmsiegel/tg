from django.urls import path

from locations import views

app_name = "locations:detail"
urls = [
    path("byway/<pk>/", views.wraith.BywayDetailView.as_view(), name="byway"),
    path("citadel/<pk>/", views.wraith.CitadelDetailView.as_view(), name="citadel"),
    path("freehold/<pk>/", views.wraith.WraithFreeholdDetailView.as_view(), name="freehold"),
    path("haunt/<pk>/", views.wraith.HauntDetailView.as_view(), name="haunt"),
    path(
        "necropolis/<pk>/",
        views.wraith.NecropolisDetailView.as_view(),
        name="necropolis",
    ),
    path("nihil/<pk>/", views.wraith.NihilDetailView.as_view(), name="nihil"),
]
