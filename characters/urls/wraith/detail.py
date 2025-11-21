from characters import views
from django.urls import path

urls = [
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
