from django.urls import path

from locations import views
from locations.registry import registry

urls = registry.urls("mage", "create") + [
    path(
        "chantry/",
        views.mage.ChantryBasicsView.as_view(),
        name="chantry",
    ),
]
