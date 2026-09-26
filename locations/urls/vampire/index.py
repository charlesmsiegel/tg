from django.urls import path

from locations import views

urls = [
    path(
        "havens/",
        views.vampire.HavenListView.as_view(),
        name="haven",
    ),
    path(
        "domains/",
        views.vampire.DomainListView.as_view(),
        name="domain",
    ),
    path(
        "elysiums/",
        views.vampire.ElysiumListView.as_view(),
        name="elysium",
    ),
    path(
        "racks/",
        views.vampire.RackListView.as_view(),
        name="rack",
    ),
    path(
        "tremere_chantry/",
        views.vampire.TremereChantryListView.as_view(),
        name="tremere_chantry",
    ),
    path(
        "barrens/",
        views.vampire.BarrensListView.as_view(),
        name="barrens",
    ),
]
