from characters import views
from django.urls import path

urls = [
    path(
        "wtohuman/",
        views.wraith.WtOHumanBasicsView.as_view(),
        name="wto_human",
    ),
]
