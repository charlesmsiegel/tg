from django.urls import path
from items import views

urls = [
    path(
        "treasure/<pk>/",
        views.changeling.TreasureDetailView.as_view(),
        name="treasure",
    ),
    path(
        "dross/<pk>/",
        views.changeling.DrossDetailView.as_view(),
        name="dross",
    ),
]
