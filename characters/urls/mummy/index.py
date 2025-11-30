from characters import views
from django.urls import path

urls = [
    path("mummy/", views.mummy.MummyListView.as_view(), name="mummy"),
    path("dynasty/", views.mummy.DynastyListView.as_view(), name="dynasty"),
    path("title/", views.mummy.MummyTitleListView.as_view(), name="title"),
]
