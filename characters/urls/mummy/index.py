from django.urls import path

from characters import views

urls = [
    path("mtrhuman/", views.mummy.MtRHumanListView.as_view(), name="mtrhuman"),
    path("mummy/", views.mummy.MummyListView.as_view(), name="mummy"),
    path("dynasty/", views.mummy.DynastyListView.as_view(), name="dynasty"),
    path("title/", views.mummy.MummyTitleListView.as_view(), name="title"),
]
