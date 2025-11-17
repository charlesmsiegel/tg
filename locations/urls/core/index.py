from django.urls import path
from locations import views

app_name = "locations:detail"
urls = [
    path("city/", views.core.CityListView.as_view(), name="city"),
]
