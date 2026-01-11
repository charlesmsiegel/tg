from django.urls import path

from characters import views

app_name = "mummy:create"
urls = [
    path(
        "mtrhuman/",
        views.mummy.MtRHumanCreateView.as_view(),
        name="mtrhuman",
    ),
    path(
        "mummy/",
        views.mummy.MummyCreateView.as_view(),
        name="mummy",
    ),
    path(
        "dynasty/",
        views.mummy.DynastyCreateView.as_view(),
        name="dynasty",
    ),
    path(
        "title/",
        views.mummy.MummyTitleCreateView.as_view(),
        name="title",
    ),
]
