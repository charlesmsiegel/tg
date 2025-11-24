from django.urls import path
from locations import views

app_name = "vampire:detail"
urls = [
    path(
        "haven/<pk>/",
        views.vampire.HavenDetailView.as_view(),
        name="haven",
    ),
    path(
        "domain/<pk>/",
        views.vampire.DomainDetailView.as_view(),
        name="domain",
    ),
    path(
        "elysium/<pk>/",
        views.vampire.ElysiumDetailView.as_view(),
        name="elysium",
    ),
    path(
        "rack/<pk>/",
        views.vampire.RackDetailView.as_view(),
        name="rack",
    ),
    path(
        "chantry/<pk>/",
        views.vampire.TremereChantryDetailView.as_view(),
        name="chantry",
    ),
    path(
        "barrens/<pk>/",
        views.vampire.BarrensDetailView.as_view(),
        name="barrens",
    ),
]
