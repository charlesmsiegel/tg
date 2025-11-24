from django.urls import path
from locations import views

app_name = "vampire:create"
urls = [
    path(
        "haven/",
        views.vampire.HavenCreateView.as_view(),
        name="haven",
    ),
    path(
        "domain/",
        views.vampire.DomainCreateView.as_view(),
        name="domain",
    ),
    path(
        "elysium/",
        views.vampire.ElysiumCreateView.as_view(),
        name="elysium",
    ),
    path(
        "rack/",
        views.vampire.RackCreateView.as_view(),
        name="rack",
    ),
    path(
        "chantry/",
        views.vampire.TremereChantryCreateView.as_view(),
        name="chantry",
    ),
    path(
        "barrens/",
        views.vampire.BarrensCreateView.as_view(),
        name="barrens",
    ),
]
