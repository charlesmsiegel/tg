from characters import views
from django.urls import path

app_name = "vampire:detail"
urls = [
    path(
        "vampire/<pk>/",
        views.vampire.VampireDetailView.as_view(),
        name="vampire",
    ),
    path(
        "ghoul/<pk>/",
        views.vampire.GhoulDetailView.as_view(),
        name="ghoul",
    ),
    path(
        "clan/<pk>/",
        views.vampire.VampireClanDetailView.as_view(),
        name="clan",
    ),
    path(
        "sect/<pk>/",
        views.vampire.VampireSectDetailView.as_view(),
        name="sect",
    ),
    path(
        "path/<pk>/",
        views.vampire.PathDetailView.as_view(),
        name="path",
    ),
    path(
        "title/<pk>/",
        views.vampire.VampireTitleDetailView.as_view(),
        name="title",
    ),
    path(
        "discipline/<pk>/",
        views.vampire.DisciplineDetailView.as_view(),
        name="discipline",
    ),
]
