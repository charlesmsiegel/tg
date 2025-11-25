from characters.views.hunter import (
    CreedUpdateView,
    EdgeUpdateView,
    HtRHumanUpdateView,
    HunterUpdateView,
    HunterOrganizationUpdateView,
)
from django.urls import path

urls = [
    path("hunter/<int:pk>/", HunterUpdateView.as_view(), name="hunter"),
    path("htrhuman/<int:pk>/", HtRHumanUpdateView.as_view(), name="htrhuman"),
    path("creed/<int:pk>/", CreedUpdateView.as_view(), name="creed"),
    path("edge/<int:pk>/", EdgeUpdateView.as_view(), name="edge"),
    path("organization/<int:pk>/", HunterOrganizationUpdateView.as_view(), name="organization"),
]
