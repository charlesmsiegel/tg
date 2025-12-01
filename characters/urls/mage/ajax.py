from characters import views
from django.urls import path

app_name = "mage:ajax"
urls = [
    path(
        "load_faction_details/",
        views.mage.load_factions,
        name="load_factions",
    ),
    path(
        "load_subfaction_details/",
        views.mage.load_subfactions,
        name="load_subfactions",
    ),
    path(
        "load_mf_ratings/",
        views.mage.load_mf_ratings,
        name="load_mf_ratings",
    ),
    path(
        "load_xp_examples/",
        views.mage.mage.LoadXPExamplesView.as_view(),
        name="load_xp_examples",
    ),
    path(
        "load_mage_examples/",
        views.mage.mage.MageFreebieFormPopulationView.as_view(),
        name="load_mage_examples",
    ),
    path(
        "load_mtahuman_examples/",
        views.mage.mtahuman.MtAHumanFreebieFormPopulationView.as_view(),
        name="load_mtahuman_examples",
    ),
    path(
        "load_companion_examples/",
        views.mage.companion.LoadExamplesView.as_view(),
        name="load_companion_examples",
    ),
    path(
        "load_sorcerer_examples/",
        views.mage.sorcerer.LoadExamplesView.as_view(),
        name="load_sorcerer_examples",
    ),
    path(
        "load_advantage_values/",
        views.mage.companion.load_companion_values,
        name="load_advantage_values",
    ),
    path(
        "get_abilities/",
        views.mage.mage.get_abilities,
        name="get_abilities",
    ),
    path(
        "get_practice_abilities/",
        views.mage.sorcerer.get_abilities,
        name="get_practice_abilities",
    ),
    path("load_attributes/", views.mage.sorcerer.load_attributes, name="load_attributes"),
    path("load_affinities/", views.mage.sorcerer.load_affinities, name="load_affinities"),
]
