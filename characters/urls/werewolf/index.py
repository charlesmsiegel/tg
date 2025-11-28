from characters import views
from django.urls import path

urls = [
    path(
        "charms/",
        views.werewolf.SpiritCharmListView.as_view(),
        name="charm",
    ),
    path(
        "totems/",
        views.werewolf.TotemListView.as_view(),
        name="totem",
    ),
    path("rites/", views.werewolf.RiteListView.as_view(), name="rite"),
    path(
        "tribes/",
        views.werewolf.TribeListView.as_view(),
        name="tribe",
    ),
    path("gifts/", views.werewolf.GiftListView.as_view(), name="gift"),
    path(
        "battlescar/",
        views.werewolf.BattleScarListView.as_view(),
        name="battlescar",
    ),
    path(
        "renownincidents/",
        views.werewolf.RenownIncidentListView.as_view(),
        name="renownincident",
    ),
    path("camps/", views.werewolf.CampListView.as_view(), name="camp"),
    path(
        "fomoripower/",
        views.werewolf.FomoriPowerListView.as_view(),
        name="fomoripower",
    ),
    path("pack/", views.werewolf.PackListView.as_view(), name="pack"),
]
