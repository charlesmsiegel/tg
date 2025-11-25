from characters.views.hunter import (
    CreedListView,
    EdgeListView,
    HtRHumanListView,
    HunterListView,
    HunterOrganizationListView,
)
from django.urls import path

urls = [
    path("hunter/", HunterListView.as_view(), name="hunter"),
    path("htrhuman/", HtRHumanListView.as_view(), name="htrhuman"),
    path("creed/", CreedListView.as_view(), name="creed"),
    path("edge/", EdgeListView.as_view(), name="edge"),
    path("organization/", HunterOrganizationListView.as_view(), name="organization"),
]
