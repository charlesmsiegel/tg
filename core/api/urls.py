"""Native TG API v1; mutations have dedicated POST endpoints per route standards."""

from django.urls import path

from core.api import auth, human_read, journal_write, scene_journal, views

app_name = "api_v1"
urlpatterns = [
    path(
        "character-profiles/human-v1/",
        human_read.HumanProfileManifestView.as_view(),
        name="human_profile_manifest",
    ),
    path(
        "catalogs/human-v1/<slug:kind>/",
        human_read.HumanCatalogView.as_view(),
        name="human_catalog",
    ),
    path(
        "characters/<int:pk>/human-profile/",
        human_read.HumanProfileView.as_view(),
        name="human_profile",
    ),
    path(
        "journals/<int:pk>/entries/append/",
        journal_write.JournalAppendView.as_view(),
        name="journal_append",
    ),
    path(
        "journals/<int:pk>/entries/<int:entry_pk>/",
        journal_write.JournalEntryDetailView.as_view(),
        name="journal_entry",
    ),
    path(
        "journals/<int:pk>/entries/<int:entry_pk>/response/",
        journal_write.JournalFirstResponseView.as_view(),
        name="journal_first_response",
    ),
    path("auth/csrf/", auth.CSRFView.as_view(), name="auth_csrf"),
    path("auth/login/", auth.LoginView.as_view(), name="auth_login"),
    path("auth/logout/", auth.SessionLogoutView.as_view(), name="auth_logout"),
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
