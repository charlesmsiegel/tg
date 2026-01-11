from django.urls import path

from characters import views

app_name = "mummy:update"
urls = [
    path(
        "mtrhuman/<pk>/",
        views.mummy.MtRHumanUpdateView.as_view(),
        name="mtrhuman",
    ),
    path(
        "mummy/<pk>/",
        views.mummy.MummyUpdateView.as_view(),
        name="mummy",
    ),
    path(
        "dynasty/<pk>/",
        views.mummy.DynastyUpdateView.as_view(),
        name="dynasty",
    ),
    path(
        "title/<pk>/",
        views.mummy.MummyTitleUpdateView.as_view(),
        name="title",
    ),
]
