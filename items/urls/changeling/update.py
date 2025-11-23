from django.urls import path
from items import views

app_name = "changeling:update"
urls = [
    path(
        "treasure/<pk>/",
        views.changeling.TreasureUpdateView.as_view(),
        name="treasure",
    ),
]
