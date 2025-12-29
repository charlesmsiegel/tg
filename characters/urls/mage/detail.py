from characters import views
from characters.views.mage import (
    MtAHumanCharacterCreationView,
    MtAHumanTemplateSelectView,
)
from django.urls import path

app_name = "mage:detail"
urls = [
    # MtAHuman character creation paths
    path(
        "mtahuman/<int:pk>/template/",
        MtAHumanTemplateSelectView.as_view(),
        name="mtahuman_template",
    ),
    path(
        "mtahuman/<int:pk>/creation/",
        MtAHumanCharacterCreationView.as_view(),
        name="mtahuman_creation",
    ),
    path(
        "effect/<pk>/",
        views.mage.EffectDetailView.as_view(),
        name="effect",
    ),
    path(
        "resonances/<pk>/",
        views.mage.ResonanceDetailView.as_view(),
        name="resonance",
    ),
    path(
        "instruments/<pk>/",
        views.mage.InstrumentDetailView.as_view(),
        name="instrument",
    ),
    path(
        "paradigms/<pk>/",
        views.mage.ParadigmDetailView.as_view(),
        name="paradigm",
    ),
    path(
        "practices/<pk>/",
        views.mage.GenericPracticeDetailView.as_view(),
        name="practice",
    ),
    path(
        "tenet/<pk>/",
        views.mage.TenetDetailView.as_view(),
        name="tenet",
    ),
    path(
        "mage_factions/<pk>/",
        views.mage.MageFactionDetailView.as_view(),
        name="mage_faction",
    ),
    path(
        "sorcerer_fellowships/<pk>/",
        views.mage.SorcererFellowshipDetailView.as_view(),
        name="sorcerer_fellowship",
    ),
    path("rotes/<pk>/", views.mage.RoteDetailView.as_view(), name="rote"),
    path("paths/<pk>/", views.mage.PathDetailView.as_view(), name="path"),
    path("rituals/<pk>/", views.mage.RitualDetailView.as_view(), name="ritual"),
    path("advantages/<pk>/", views.mage.AdvantageDetailView.as_view(), name="advantage"),
    path("sphere/<pk>/", views.mage.SphereDetailView.as_view(), name="sphere"),
]
