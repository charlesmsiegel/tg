from characters import views
from django.urls import path

app_name = "vampire:update"
urls = [
    path(
        "vtmhuman/<pk>/",
        views.vampire.VtMHumanUpdateView.as_view(),
        name="vtm_human",
    ),
    path(
        "vtm_human/full/<pk>/",
        views.vampire.VtMHumanUpdateView.as_view(),
        name="vtm_human_full",
    ),
    path(
        "vampire/<pk>/",
        views.vampire.VampireUpdateView.as_view(),
        name="vampire",
    ),
    path(
        "ghoul/<pk>/",
        views.vampire.GhoulUpdateView.as_view(),
        name="ghoul",
    ),
    path(
        "clan/<pk>/",
        views.vampire.VampireClanUpdateView.as_view(),
        name="clan",
    ),
    path(
        "sect/<pk>/",
        views.vampire.VampireSectUpdateView.as_view(),
        name="sect",
    ),
    path(
        "path/<pk>/",
        views.vampire.PathUpdateView.as_view(),
        name="path",
    ),
    path(
        "title/<pk>/",
        views.vampire.VampireTitleUpdateView.as_view(),
        name="title",
    ),
    path(
        "discipline/<pk>/",
        views.vampire.DisciplineUpdateView.as_view(),
        name="discipline",
    ),
]
