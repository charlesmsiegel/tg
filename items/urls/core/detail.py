from django.urls import path

from items import views
from items.registry import registry

urls = registry.urls("core", "detail") + [
    path("<int:pk>/", views.core.GenericItemDetailView.as_view(), name="item")
]
