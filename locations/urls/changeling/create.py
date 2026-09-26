from django.urls import path

from locations import views
from locations.registry import registry

urls = registry.urls("changeling", "create") + [
    path(
        "freehold/",
        views.changeling.FreeholdBasicsView.as_view(),
        name="freehold",
    )
]
