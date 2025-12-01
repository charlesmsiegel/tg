from characters.views.demon import (
    ConclaveUpdateView,
    DemonFactionUpdateView,
    DemonHouseUpdateView,
    DemonUpdateView,
    DtFHumanUpdateView,
    EarthboundUpdateView,
    LoreUpdateView,
    PactUpdateView,
    RitualUpdateView,
    ThrallUpdateView,
    VisageUpdateView,
)
from django.urls import path

urls = [
    path("demon/<int:pk>/", DemonUpdateView.as_view(), name="demon"),
    path("dtfhuman/<int:pk>/", DtFHumanUpdateView.as_view(), name="dtfhuman"),
    path("thrall/<int:pk>/", ThrallUpdateView.as_view(), name="thrall"),
    path("earthbound/<int:pk>/", EarthboundUpdateView.as_view(), name="earthbound"),
    path("conclave/<int:pk>/", ConclaveUpdateView.as_view(), name="conclave"),
    path("faction/<int:pk>/", DemonFactionUpdateView.as_view(), name="faction"),
    path("house/<int:pk>/", DemonHouseUpdateView.as_view(), name="house"),
    path("visage/<int:pk>/", VisageUpdateView.as_view(), name="visage"),
    path("lore/<int:pk>/", LoreUpdateView.as_view(), name="lore"),
    path("pact/<int:pk>/", PactUpdateView.as_view(), name="pact"),
    path("ritual/<int:pk>/", RitualUpdateView.as_view(), name="ritual"),
]
