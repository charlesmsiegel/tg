from django.urls import path
from items import views

app_name = "changeling:list"
urls = [
    path(
        "treasures/",
        views.changeling.TreasureListView.as_view(),
        name="treasure",
    ),
]
