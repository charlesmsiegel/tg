from django.urls import path
from locations import views

app_name = "changeling:create"
urls = [
    path(
        "freehold/",
        views.changeling.FreeholdCreateView.as_view(),
        name="freehold",
    ),
]
