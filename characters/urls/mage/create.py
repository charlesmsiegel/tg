from characters import views
from django.urls import path

app_name = "mage:create"
urls = [
    path(
        "effect/",
        views.mage.EffectCreateView.as_view(),
        name="effect",
    ),
    path(
        "resonance/",
        views.mage.ResonanceCreateView.as_view(),
        name="resonance",
    ),
    path(
        "instruments/",
        views.mage.InstrumentCreateView.as_view(),
        name="instrument",
    ),
    path(
        "paradigms/",
        views.mage.ParadigmCreateView.as_view(),
        name="paradigm",
    ),
    path(
        "practices/",
        views.mage.PracticeCreateView.as_view(),
        name="practice",
    ),
    path(
        "specialized_practices/",
        views.mage.SpecializedPracticeCreateView.as_view(),
        name="specialized_practice",
    ),
    path(
        "corrupted_practices/",
        views.mage.CorruptedPracticeCreateView.as_view(),
        name="corrupted_practice",
    ),
    path(
        "tenet/",
        views.mage.TenetCreateView.as_view(),
        name="tenet",
    ),
    path(
        "sorcerer_fellowship/",
        views.mage.SorcererFellowshipCreateView.as_view(),
        name="sorcerer_fellowship",
    ),
    path(
        "mage_faction/",
        views.mage.MageFactionCreateView.as_view(),
        name="mage_faction",
    ),
    path(
        "rotes/",
        views.mage.RoteCreateView.as_view(),
        name="rote",
    ),
    path(
        "mtahuman/",
        views.mage.MtAHumanBasicsView.as_view(),
        name="mta_human",
    ),
    path(
        "companion/",
        views.mage.CompanionBasicsView.as_view(),
        name="companion",
    ),
    path(
        "sorcerer/",
        views.mage.SorcererBasicsView.as_view(),
        name="sorcerer",
    ),
    path(
        "mage/",
        views.mage.MageBasicsView.as_view(),
        name="mage",
    ),
    path(
        "mage/full/",
        views.mage.MageCreateView.as_view(),
        name="mage_full",
    ),
    path(
        "companion/full/",
        views.mage.CompanionCreateView.as_view(),
        name="companion_full",
    ),
    path(
        "cabal/",
        views.mage.CabalCreateView.as_view(),
        name="cabal",
    ),
]
