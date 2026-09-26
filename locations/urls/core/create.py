from django.urls import path

from locations import views

urls = [
    path(
        "location/",
        views.core.LocationCreateView.as_view(),
        name="location",
    ),
    path(
        "city/",
        views.core.CityCreateView.as_view(),
        name="city",
    ),
]
