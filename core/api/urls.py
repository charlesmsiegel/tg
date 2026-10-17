"""Native TG API v1; mutations have dedicated POST endpoints per route standards."""

from django.urls import path

from core.api import views

app_name = "api_v1"
urlpatterns = [
    path("session/", views.SessionView.as_view(), name="session"),
    path("chronicles/", views.ChronicleListView.as_view(), name="chronicles"),
    path("chronicles/create/", views.ChronicleCreateView.as_view(), name="chronicle_create"),
    path("chronicles/<int:pk>/", views.ChronicleDetailView.as_view(), name="chronicle"),
    path(
        "chronicles/<int:pk>/allowed-objects/",
        views.AllowedObjectsView.as_view(),
        name="allowed_objects",
    ),
    path(
        "chronicles/<int:pk>/characters/",
        views.ChronicleCharactersView.as_view(),
        name="characters",
    ),
    path("characters/<int:pk>/", views.CharacterDetailView.as_view(), name="character"),
    path(
        "characters/<int:pk>/update/", views.CharacterUpdateView.as_view(), name="character_update"
    ),
]
