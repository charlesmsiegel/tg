from django.urls import path

from locations import views

app_name = "locations:create"
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
