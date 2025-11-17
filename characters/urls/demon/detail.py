from characters.views.demon import (
    DemonDetailView,
    DemonFactionDetailView,
    DemonHouseDetailView,
    DtFHumanDetailView,
    LoreDetailView,
    PactDetailView,
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
]
