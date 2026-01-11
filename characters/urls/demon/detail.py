from django.urls import path

from characters.views.demon import (
    ApocalypticFormTraitDetailView,
    ConclaveDetailView,
    DemonCharacterCreationView,
    DemonDetailView,
    DemonFactionDetailView,
    DemonHouseDetailView,
    DtFHumanCharacterCreationView,
    DtFHumanDetailView,
    DtFHumanTemplateSelectView,
    EarthboundDetailView,
    LoreDetailView,
    PactDetailView,
    RitualDetailView,
    ThrallCharacterCreationView,
    ThrallDetailView,
    VisageDetailView,
)

urls = [
    path(
        "apocalyptic_trait/<int:pk>/",
        ApocalypticFormTraitDetailView.as_view(),
        name="apocalyptic_trait",
    ),
    path("conclave/<int:pk>/", ConclaveDetailView.as_view(), name="conclave"),
    path("demon/<int:pk>/", DemonDetailView.as_view(), name="demon"),
    path("dtfhuman/<int:pk>/", DtFHumanDetailView.as_view(), name="dtfhuman"),
    path("thrall/<int:pk>/", ThrallDetailView.as_view(), name="thrall"),
    path("earthbound/<int:pk>/", EarthboundDetailView.as_view(), name="earthbound"),
    path("faction/<int:pk>/", DemonFactionDetailView.as_view(), name="faction"),
    path("house/<int:pk>/", DemonHouseDetailView.as_view(), name="house"),
    path("visage/<int:pk>/", VisageDetailView.as_view(), name="visage"),
    path("lore/<int:pk>/", LoreDetailView.as_view(), name="lore"),
    path("pact/<int:pk>/", PactDetailView.as_view(), name="pact"),
    path("ritual/<int:pk>/", RitualDetailView.as_view(), name="ritual"),
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
