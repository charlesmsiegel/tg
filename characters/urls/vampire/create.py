from characters import views
from django.urls import path

app_name = "vampire:create"
urls = [
    path(
        "vtmhuman/",
        views.vampire.VtMHumanBasicsView.as_view(),
        name="vtm_human",
    ),
    path(
        "vampire/",
        views.vampire.VampireBasicsView.as_view(),
        name="vampire",
    ),
    path(
        "ghoul/",
        views.vampire.GhoulBasicsView.as_view(),
        name="ghoul",
    ),
    path(
        "revenant/",
        views.vampire.RevenantCreateView.as_view(),
        name="revenant",
    ),
    path(
        "clan/",
        views.vampire.VampireClanCreateView.as_view(),
        name="clan",
    ),
    path(
        "sect/",
        views.vampire.VampireSectCreateView.as_view(),
        name="sect",
    ),
    path(
        "path/",
        views.vampire.PathCreateView.as_view(),
        name="path",
    ),
    path(
        "title/",
        views.vampire.VampireTitleCreateView.as_view(),
        name="title",
    ),
    path(
        "discipline/",
        views.vampire.DisciplineCreateView.as_view(),
        name="discipline",
    ),
]
