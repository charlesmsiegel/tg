from django.urls import path

from locations import views
from locations.registry import registry

urls = registry.urls("core", "detail") + [
    path("<int:pk>/", views.core.GenericLocationDetailView.as_view(), name="location")
]
