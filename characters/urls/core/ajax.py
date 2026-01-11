from django.urls import path

from characters.views.core.human import LoadExamplesView, LoadValuesView

app_name = "characters:ajax"
urls = [
    path("load_examples/", LoadExamplesView.as_view(), name="load_examples"),
    path("load_values/", LoadValuesView.as_view(), name="load_values"),
]
