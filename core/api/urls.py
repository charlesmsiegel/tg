"""Native TG API v1; mutations have dedicated POST endpoints per route standards."""

from django.urls import path

from core.api import scene_journal, views

app_name = "api_v1"
urlpatterns = [
    path("scenes/", scene_journal.SceneListView.as_view(), name="scenes"),
    path("scenes/<int:pk>/", scene_journal.SceneDetailView.as_view(), name="scene"),
    path("scenes/<int:pk>/posts/", scene_journal.ScenePostsView.as_view(), name="scene_posts"),
    path("journals/", scene_journal.JournalListView.as_view(), name="journals"),
    path("journals/<int:pk>/", scene_journal.JournalDetailView.as_view(), name="journal"),
    path(
        "journals/<int:pk>/entries/",
        scene_journal.JournalEntriesView.as_view(),
        name="journal_entries",
    ),
    path(
        "characters/<int:pk>/journal/",
        scene_journal.CharacterJournalView.as_view(),
        name="character_journal",
    ),
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
