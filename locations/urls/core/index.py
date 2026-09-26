from django.urls import path

from locations import views

urls = [
    path("city/", views.core.CityListView.as_view(), name="city"),
]
