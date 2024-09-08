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
    path("rotes/", views.mage.RoteListView.as_view(), name="rote"),
]
