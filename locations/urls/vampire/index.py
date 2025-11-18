from django.urls import path
from locations import views

app_name = "vampire:list"
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
]
