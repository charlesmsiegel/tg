from django.urls import path
from items import views

app_name = "changeling:create"
urls = [
    path(
        "treasure/",
        views.changeling.TreasureCreateView.as_view(),
        name="treasure",
    ),
]
