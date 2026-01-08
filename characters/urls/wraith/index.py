from characters import views
from django.urls import path

urls = [
    path("arcanoi/", views.wraith.ArcanosListView.as_view(), name="arcanos"),
    path("circles/", views.wraith.CircleListView.as_view(), name="circle"),
    path("factions/", views.wraith.WraithFactionListView.as_view(), name="faction"),
    path("guilds/", views.wraith.GuildListView.as_view(), name="guild"),
    path("shadow_archetypes/", views.wraith.ShadowArchetypeListView.as_view(), name="shadow_archetype"),
    path("thorns/", views.wraith.ThornListView.as_view(), name="thorn"),
]
