from django.urls import path

from characters.views.hunter import (
    CreedCreateView,
    EdgeCreateView,
    HtRHumanCreateView,
    HunterCreateView,
    HunterOrganizationCreateView,
)

urls = [
    path("hunter/", HunterCreateView.as_view(), name="hunter"),
    path("htrhuman/", HtRHumanCreateView.as_view(), name="htrhuman"),
    path("creed/", CreedCreateView.as_view(), name="creed"),
    path("edge/", EdgeCreateView.as_view(), name="edge"),
    path("organization/", HunterOrganizationCreateView.as_view(), name="organization"),
]
