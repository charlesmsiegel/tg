from characters import views
from django.urls import path

app_name = "changeling:ajax"
urls = [
    path(
        "load_ctdhuman_examples/",
        views.changeling.ctdhuman.CtDHumanFreebieFormPopulationView.as_view(),
        name="load_ctdhuman_examples",
    ),
    path(
        "load_changeling_examples/",
        views.changeling.changeling.ChangelingFreebieFormPopulationView.as_view(),
        name="load_changeling_examples",
    ),
]
