from django.urls import path

from characters import views

urls = [
    # Arcanos detail view
    path(
        "arcanos/<pk>/",
        views.wraith.ArcanosDetailView.as_view(),
        name="arcanos",
    ),
    # Circle detail view
    path(
        "circle/<pk>/",
        views.wraith.CircleDetailView.as_view(),
        name="circle",
    ),
    # Faction detail view
    path(
        "faction/<pk>/",
        views.wraith.WraithFactionDetailView.as_view(),
        name="faction",
    ),
    # Guild detail view
    path(
        "guild/<pk>/",
        views.wraith.GuildDetailView.as_view(),
        name="guild",
    ),
    # Shadow Archetype detail view
    path(
        "shadow_archetype/<pk>/",
        views.wraith.ShadowArchetypeDetailView.as_view(),
        name="shadow_archetype",
    ),
    # Wraith detail view
    path(
        "wraith/<pk>/",
        views.wraith.WraithDetailView.as_view(),
        name="wraith",
    ),
    # Thorn detail view
    path(
        "thorn/<pk>/",
        views.wraith.ThornDetailView.as_view(),
        name="thorn",
    ),
    # Staged character creation routes
    path(
        "wraith/<int:pk>/chargen/",
        views.wraith.WraithCharacterCreationView.as_view(),
        name="wraith_chargen",
    ),
    path(
        "wtohuman/<int:pk>/chargen/",
        views.wraith.WtOHumanCharacterCreationView.as_view(),
        name="wto_human_chargen",
    ),
    path(
        "wtohuman/<int:pk>/template/",
        views.wraith.WtOHumanTemplateSelectView.as_view(),
        name="wtohuman_template",
    ),
    path(
        "wtohuman/<int:pk>/creation/",
        views.wraith.WtOHumanCharacterCreationView.as_view(),
        name="wtohuman_creation",
    ),
]
