from characters.views.demon import (
    DemonCharacterCreationView,
    DemonDetailView,
    DemonFactionDetailView,
    DemonHouseDetailView,
    DtFHumanCharacterCreationView,
    DtFHumanDetailView,
    DtFHumanTemplateSelectView,
    LoreDetailView,
    PactDetailView,
    ThrallCharacterCreationView,
    ThrallDetailView,
    VisageDetailView,
)
from django.urls import path

urls = [
    path("demon/<int:pk>/", DemonDetailView.as_view(), name="demon"),
    path("dtfhuman/<int:pk>/", DtFHumanDetailView.as_view(), name="dtfhuman"),
    path("thrall/<int:pk>/", ThrallDetailView.as_view(), name="thrall"),
    path("faction/<int:pk>/", DemonFactionDetailView.as_view(), name="faction"),
    path("house/<int:pk>/", DemonHouseDetailView.as_view(), name="house"),
    path("visage/<int:pk>/", VisageDetailView.as_view(), name="visage"),
    path("lore/<int:pk>/", LoreDetailView.as_view(), name="lore"),
    path("pact/<int:pk>/", PactDetailView.as_view(), name="pact"),
    # Staged character creation routes
    path(
        "demon/<int:pk>/chargen/",
        DemonCharacterCreationView.as_view(),
        name="demon_chargen",
    ),
    path(
        "dtfhuman/<int:pk>/chargen/",
        DtFHumanCharacterCreationView.as_view(),
        name="dtfhuman_chargen",
    ),
    path(
        "thrall/<int:pk>/chargen/",
        ThrallCharacterCreationView.as_view(),
        name="thrall_chargen",
    ),
    path(
        "dtfhuman/<int:pk>/template/",
        DtFHumanTemplateSelectView.as_view(),
        name="dtfhuman_template",
    ),
    path(
        "dtfhuman/<int:pk>/creation/",
        DtFHumanCharacterCreationView.as_view(),
        name="dtfhuman_creation",
    ),
]
