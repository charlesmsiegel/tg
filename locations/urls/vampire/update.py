from django.urls import path
from locations import views

app_name = "vampire:update"
urls = [
    path(
        "haven/<pk>/",
        views.vampire.HavenUpdateView.as_view(),
        name="haven",
    ),
    path(
        "domain/<pk>/",
        views.vampire.DomainUpdateView.as_view(),
        name="domain",
    ),
    path(
        "elysium/<pk>/",
        views.vampire.ElysiumUpdateView.as_view(),
        name="elysium",
    ),
    path(
        "rack/<pk>/",
        views.vampire.RackUpdateView.as_view(),
        name="rack",
    ),
]
