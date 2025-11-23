from django.urls import path
from items import views

app_name = "changeling:detail"
urls = [
    path(
        "treasure/<pk>/",
        views.changeling.TreasureDetailView.as_view(),
        name="treasure",
    ),
]
