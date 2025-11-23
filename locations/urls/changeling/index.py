from django.urls import path
from locations import views

app_name = "changeling:list"
urls = [
    path(
        "freehold/",
        views.changeling.FreeholdListView.as_view(),
        name="freehold",
    ),
]
