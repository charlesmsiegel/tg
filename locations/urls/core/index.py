from django.urls import path
from locations import views

app_name = "locations:detail"
urls = [
    path("city/", views.core.CityListView.as_view(), name="city"),
    path("physical-place/", views.core.PhysicalPlaceListView.as_view(), name="physical_place"),
]
