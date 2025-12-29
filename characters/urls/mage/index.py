from characters import views
from django.urls import path

app_name = "mage:detail"
urls = [
    path(
        "effect/",
        views.mage.EffectListView.as_view(),
        name="effect",
    ),
    path(
        "resonances/",
        views.mage.ResonanceListView.as_view(),
        name="resonance",
    ),
    path(
        "instruments/",
        views.mage.InstrumentListView.as_view(),
        name="instrument",
    ),
    path(
        "paradigms/",
        views.mage.ParadigmListView.as_view(),
        name="paradigm",
    ),
    path(
        "practices/",
        views.mage.PracticeListView.as_view(),
        name="practice",
    ),
    path(
        "tenet/",
        views.mage.TenetListView.as_view(),
        name="tenet",
    ),
    path(
        "mage_factions/",
        views.mage.MageFactionListView.as_view(),
        name="mage_faction",
    ),
    path(
        "sorcerer_fellowships/",
        views.mage.SorcererFellowshipListView.as_view(),
        name="sorcerer_fellowship",
    ),
    path("rotes/", views.mage.RoteListView.as_view(), name="rote"),
    path("paths/", views.mage.PathListView.as_view(), name="path"),
    path("rituals/", views.mage.RitualListView.as_view(), name="ritual"),
    path("cabal/", views.mage.CabalListView.as_view(), name="cabal"),
    path("spheres/", views.mage.SphereListView.as_view(), name="sphere"),
]
