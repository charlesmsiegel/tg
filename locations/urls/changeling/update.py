from django.urls import path

from locations import views
from locations.registry import registry

urls = registry.urls("changeling", "update") + [
    path(
        "freehold/<int:pk>/",
        views.changeling.FreeholdCreationView.as_view(),
        name="freehold",
    )
]
