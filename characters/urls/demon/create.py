from characters.views.demon import (
    DemonBasicsView,
    DemonFactionCreateView,
    DemonHouseCreateView,
    DtFHumanBasicsView,
    EarthboundCreateView,
    LoreCreateView,
    PactCreateView,
    ThrallBasicsView,
    VisageCreateView,
)
from django.urls import path

urls = [
    path("demon/", DemonBasicsView.as_view(), name="demon"),
    path("dtfhuman/", DtFHumanBasicsView.as_view(), name="dtfhuman"),
    path("thrall/", ThrallBasicsView.as_view(), name="thrall"),
    path("earthbound/", EarthboundCreateView.as_view(), name="earthbound"),
    path("faction/", DemonFactionCreateView.as_view(), name="faction"),
    path("house/", DemonHouseCreateView.as_view(), name="house"),
    path("visage/", VisageCreateView.as_view(), name="visage"),
    path("lore/", LoreCreateView.as_view(), name="lore"),
    path("pact/", PactCreateView.as_view(), name="pact"),
]
