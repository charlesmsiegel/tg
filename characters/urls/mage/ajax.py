from django.urls import path

from characters import views

app_name = "mage:ajax"
# Note: Most freebies AJAX views removed - now using ChainedSelect.
# Keep XP and other AJAX views for now (to be removed in later phases).
urls = [
    path(
        "load_mf_ratings/",
        views.mage.mage.LoadMFRatingsView.as_view(),
        name="load_mf_ratings",
    ),
    path(
        "load_xp_examples/",
        views.mage.mage.LoadXPExamplesView.as_view(),
        name="load_xp_examples",
    ),
    # Companion and Sorcerer freebies - complex forms, keep for now
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
        views.mage.companion.LoadCompanionValuesView.as_view(),
        name="load_advantage_values",
    ),
    path(
        "get_abilities/",
        views.mage.mage.GetAbilitiesView.as_view(),
        name="get_abilities",
    ),
    path(
        "get_practice_abilities/",
        views.mage.sorcerer.GetPracticeAbilitiesView.as_view(),
        name="get_practice_abilities",
    ),
    path(
        "load_attributes/",
        views.mage.sorcerer.LoadAttributesView.as_view(),
        name="load_attributes",
    ),
    path(
        "load_affinities/",
        views.mage.sorcerer.LoadAffinitiesView.as_view(),
        name="load_affinities",
    ),
]
