from characters import views
from django.urls import path

# Create your URLs here
app_name = "mage:update"
urls = [
    path(
        "effect/<pk>/",
        views.mage.EffectUpdateView.as_view(),
        name="effect",
    ),
    path(
        "resonances/<pk>/",
        views.mage.ResonanceUpdateView.as_view(),
        name="resonance",
    ),
    path(
        "paradigms/<pk>/",
        views.mage.ParadigmUpdateView.as_view(),
        name="paradigm",
    ),
    path(
        "instruments/<pk>/",
        views.mage.InstrumentUpdateView.as_view(),
        name="instrument",
    ),
    path(
        "practices/<pk>/",
        views.mage.PracticeUpdateView.as_view(),
        name="practice",
    ),
    path(
        "specialized_practices/<pk>/",
        views.mage.SpecializedPracticeUpdateView.as_view(),
        name="specialized_practice",
    ),
    path(
        "corrupted_practices/<pk>/",
        views.mage.CorruptedPracticeUpdateView.as_view(),
        name="corrupted_practice",
    ),
    path(
        "tenet/<pk>/",
        views.mage.TenetUpdateView.as_view(),
        name="tenet",
    ),
    path(
        "mage_factions/<pk>/",
        views.mage.MageFactionUpdateView.as_view(),
        name="mage_faction",
    ),
    path(
        "rotes/<pk>/",
        views.mage.RoteUpdateView.as_view(),
        name="rote",
    ),
    path(
        "mtahuman/<pk>/",
        views.mage.MtAHumanUpdateView.as_view(),
        name="mtahuman",
    ),
    path(
        "mage/<pk>/",
        views.mage.MageUpdateView.as_view(),
        name="mage",
    ),
]
