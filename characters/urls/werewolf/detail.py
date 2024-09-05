from characters import views
from django.urls import path

urls = [
    path(
        "charms/<pk>/",
        views.werewolf.SpiritCharmDetailView.as_view(),
        name="charm",
    ),
    path(
        "spirits/<pk>/",
        views.werewolf.SpiritDetailView.as_view(),
        name="spirit",
    ),
    path(
        "totems/<pk>/",
        views.werewolf.TotemDetailView.as_view(),
        name="totem",
    ),
    path("rites/<pk>/", views.werewolf.RiteDetailView.as_view(), name="rite"),
    path(
        "tribes/<pk>/",
        views.werewolf.TribeDetailView.as_view(),
        name="tribe",
    ),
    path("gifts/<pk>/", views.werewolf.GiftDetailView.as_view(), name="gift"),
    path(
        "battlescar/<pk>/",
        views.werewolf.BattleScarDetailView.as_view(),
        name="battlescar",
    ),
    path(
        "renownincidents/<pk>/",
        views.werewolf.RenownIncidentDetailView.as_view(),
        name="renownincident",
    ),
    path("camps/<pk>/", views.werewolf.CampDetailView.as_view(), name="camp"),
    path(
        "fomoripower/<pk>/",
        views.werewolf.FomoriPowerDetailView.as_view(),
        name="fomoripower",
    ),
]
