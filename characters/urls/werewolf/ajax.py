from characters import views
from django.urls import path

app_name = "werewolf:ajax"
urls = [
    path(
        "load_wtahuman_examples/",
        views.werewolf.wtahuman.WtAHumanFreebieFormPopulationView.as_view(),
        name="load_wtahuman_examples",
    ),
    path(
        "load_kinfolk_examples/",
        views.werewolf.kinfolk.KinfolkFreebieFormPopulationView.as_view(),
        name="load_kinfolk_examples",
    ),
    path(
        "load_fomor_examples/",
        views.werewolf.fomor.FomorFreebieFormPopulationView.as_view(),
        name="load_fomor_examples",
    ),
]
