from django.urls import path

from characters.views.hunter import (
    CreedDetailView,
    EdgeDetailView,
    HtRHumanDetailView,
    HunterDetailView,
    HunterOrganizationDetailView,
)

urls = [
    path("hunter/<int:pk>/", HunterDetailView.as_view(), name="hunter"),
    path("htrhuman/<int:pk>/", HtRHumanDetailView.as_view(), name="htrhuman"),
    path("creed/<int:pk>/", CreedDetailView.as_view(), name="creed"),
    path("edge/<int:pk>/", EdgeDetailView.as_view(), name="edge"),
    path("organization/<int:pk>/", HunterOrganizationDetailView.as_view(), name="organization"),
]
