from characters.views.demon import (
    DemonCreateView,
    DemonFactionCreateView,
    DemonHouseCreateView,
    DtFHumanCreateView,
    LoreCreateView,
    PactCreateView,
    ThrallCreateView,
    VisageCreateView,
)
from django.urls import path

urls = [
    path("demon/", DemonCreateView.as_view(), name="demon"),
    path("dtfhuman/", DtFHumanCreateView.as_view(), name="dtfhuman"),
    path("thrall/", ThrallCreateView.as_view(), name="thrall"),
    path("faction/", DemonFactionCreateView.as_view(), name="faction"),
    path("house/", DemonHouseCreateView.as_view(), name="house"),
    path("visage/", VisageCreateView.as_view(), name="visage"),
    path("lore/", LoreCreateView.as_view(), name="lore"),
    path("pact/", PactCreateView.as_view(), name="pact"),
]
