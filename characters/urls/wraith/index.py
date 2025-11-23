from characters import views
from django.urls import path

urls = [
    path("thorns/", views.wraith.ThornListView.as_view(), name="thorn"),
]
