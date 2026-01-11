from django.urls import path

from characters import views

urls = [
    path(
        "arcanos/",
        views.wraith.ArcanosCreateView.as_view(),
        name="arcanos",
    ),
    path(
        "circle/",
        views.wraith.CircleCreateView.as_view(),
        name="circle",
    ),
    path(
        "faction/",
        views.wraith.WraithFactionCreateView.as_view(),
        name="faction",
    ),
    path(
        "guild/",
        views.wraith.GuildCreateView.as_view(),
        name="guild",
    ),
    path(
        "shadow_archetype/",
        views.wraith.ShadowArchetypeCreateView.as_view(),
        name="shadow_archetype",
    ),
    path(
        "thorn/",
        views.wraith.ThornCreateView.as_view(),
        name="thorn",
    ),
    path(
        "wtohuman/",
        views.wraith.WtOHumanBasicsView.as_view(),
        name="wto_human",
    ),
    path(
        "wraith/",
        views.wraith.WraithBasicsView.as_view(),
        name="wraith",
    ),
]
