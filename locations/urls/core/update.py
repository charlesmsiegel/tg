from django.urls import path
from locations import views

app_name = "locations:update"
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
    path(
        "physical-place/<pk>/",
        views.core.PhysicalPlaceUpdateView.as_view(),
        name="physical_place",
    ),
]
