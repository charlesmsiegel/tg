from django.urls import path

from characters.views.demon import (
    ApocalypticFormTraitListView,
    ConclaveListView,
    DemonFactionListView,
    DemonHouseListView,
    DemonListView,
    DtFHumanListView,
    EarthboundListView,
    LoreListView,
    PactListView,
    RitualListView,
    ThrallListView,
    VisageListView,
)

urls = [
    path("apocalyptic_trait/", ApocalypticFormTraitListView.as_view(), name="apocalyptic_trait"),
    path("conclave/", ConclaveListView.as_view(), name="conclave"),
    path("demon/", DemonListView.as_view(), name="demon"),
    path("dtfhuman/", DtFHumanListView.as_view(), name="dtfhuman"),
    path("thrall/", ThrallListView.as_view(), name="thrall"),
    path("earthbound/", EarthboundListView.as_view(), name="earthbound"),
    path("faction/", DemonFactionListView.as_view(), name="faction"),
    path("house/", DemonHouseListView.as_view(), name="house"),
    path("visage/", VisageListView.as_view(), name="visage"),
    path("lore/", LoreListView.as_view(), name="lore"),
    path("pact/", PactListView.as_view(), name="pact"),
    path("ritual/", RitualListView.as_view(), name="ritual"),
]
