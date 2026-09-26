from django.urls import path

from locations import views

urls = [
    path(
        "location/<pk>/",
        views.core.LocationUpdateView.as_view(),
        name="location",
    ),
    path(
        "city/<pk>/",
        views.core.CityUpdateView.as_view(),
        name="city",
    ),
]
