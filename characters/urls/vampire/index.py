from characters import views
from django.urls import path

urls = [
    path("coterie/", views.vampire.CoterieListView.as_view(), name="coterie"),
]
