from django.urls import path
from locations import views

app_name = "changeling:update"
urls = [
    path(
        "freehold/<int:pk>/",
        views.changeling.FreeholdUpdateView.as_view(),
        name="freehold",
    ),
]
