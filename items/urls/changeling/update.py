from django.urls import path
from items import views

urls = [
    path(
        "treasure/<pk>/",
        views.changeling.TreasureUpdateView.as_view(),
        name="treasure",
    ),
    path(
        "dross/<pk>/",
        views.changeling.DrossUpdateView.as_view(),
        name="dross",
    ),
]
