from django.urls import path
from locations import views

app_name = "locations:detail"
urls = [
    path("city/<pk>/", views.core.CityDetailView.as_view(), name="city"),
    path(
        "physical-place/<pk>/",
        views.core.PhysicalPlaceDetailView.as_view(),
        name="physical_place",
    ),
    path("<pk>/", views.core.GenericLocationDetailView.as_view(), name="location"),
]
