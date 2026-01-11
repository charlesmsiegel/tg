from django.urls import path

from locations import views

urls = [
    path(
        "load_chantry_examples/",
        views.mage.chantry.LoadExamplesView.as_view(),
        name="load_chantry_examples",
    ),
]
