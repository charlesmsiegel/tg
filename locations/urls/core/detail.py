from django.urls import path

from locations import views

urls = [
    path("city/<pk>/", views.core.CityDetailView.as_view(), name="city"),
    path("<pk>/", views.core.GenericLocationDetailView.as_view(), name="location"),
]
