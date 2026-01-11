from characters import views
from django.urls import path

urls = [
    path("clan/", views.vampire.VampireClanListView.as_view(), name="clan"),
    path("coterie/", views.vampire.CoterieListView.as_view(), name="coterie"),
    path("discipline/", views.vampire.DisciplineListView.as_view(), name="discipline"),
    path("path/", views.vampire.PathListView.as_view(), name="path"),
    path("sect/", views.vampire.VampireSectListView.as_view(), name="sect"),
    path("title/", views.vampire.VampireTitleListView.as_view(), name="title"),
]
