from characters.views.demon import (
    DemonFactionListView,
    DemonHouseListView,
    # DemonListView,
    # DtFHumanListView,
    LoreListView,
    PactListView,
    # ThrallListView,
    VisageListView,
)
from django.urls import path

urls = [
    # path("demon/", DemonListView.as_view(), name="demon"),
    # path("dtfhuman/", DtFHumanListView.as_view(), name="dtfhuman"),
    # path("thrall/", ThrallListView.as_view(), name="thrall"),
    path("faction/", DemonFactionListView.as_view(), name="faction"),
    path("house/", DemonHouseListView.as_view(), name="house"),
    path("visage/", VisageListView.as_view(), name="visage"),
    path("lore/", LoreListView.as_view(), name="lore"),
    path("pact/", PactListView.as_view(), name="pact"),
]
