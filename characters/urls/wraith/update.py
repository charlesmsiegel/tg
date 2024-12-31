from characters import views
from django.urls import path

urls = [
    path(
        "wtohuman/<pk>/",
        views.wraith.WtOHumanUpdateView.as_view(),
        name="wto_human",
    ),
    path(
        "wto_human/full/<pk>/",
        views.wraith.WtOHumanUpdateView.as_view(),
        name="wto_human_full",
    ),
]
