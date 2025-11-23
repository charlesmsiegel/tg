from django.urls import path
from locations import views

app_name = "changeling"
urls = [
    path(
        "freehold/<int:pk>/",
        views.changeling.FreeholdDetailView.as_view(),
        name="freehold",
    ),
]
