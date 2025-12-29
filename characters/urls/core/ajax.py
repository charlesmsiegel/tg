from characters.views.core.human import LoadExamplesView, LoadValuesView
from django.urls import path

app_name = "core:create"
urls = [
    path("load_examples/", LoadExamplesView.as_view(), name="load_examples"),
    path("load_values/", LoadValuesView.as_view(), name="load_values"),
]
