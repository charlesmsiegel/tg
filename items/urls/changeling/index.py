from django.urls import path
from items import views

urls = [
    path(
        "treasures/",
        views.changeling.TreasureListView.as_view(),
        name="treasure",
    ),
    path(
        "dross/",
        views.changeling.DrossListView.as_view(),
        name="dross",
    ),
]
