from django.urls import path
from items import views

urls = [
    path(
        "treasure/",
        views.changeling.TreasureCreateView.as_view(),
        name="treasure",
    ),
    path(
        "dross/",
        views.changeling.DrossCreateView.as_view(),
        name="dross",
    ),
]
