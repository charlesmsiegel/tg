from django.urls import path

from characters import views

app_name = "mummy:detail"
urls = [
    path(
        "mtrhuman/<pk>/",
        views.mummy.MtRHumanDetailView.as_view(),
        name="mtrhuman",
    ),
    path(
        "mummy/<pk>/",
        views.mummy.MummyDetailView.as_view(),
        name="mummy",
    ),
    path(
        "dynasty/<pk>/",
        views.mummy.DynastyDetailView.as_view(),
        name="dynasty",
    ),
    path(
        "title/<pk>/",
        views.mummy.MummyTitleDetailView.as_view(),
        name="title",
    ),
]
