# Treasure Views
# Dross Views
from items.registry import registry

TreasureDetailView = registry.view("items.Treasure", "detail")
TreasureListView = registry.view("items.Treasure", "list")
TreasureCreateView = registry.view("items.Treasure", "create")
TreasureUpdateView = registry.view("items.Treasure", "update")
DrossDetailView = registry.view("items.Dross", "detail")
DrossListView = registry.view("items.Dross", "list")
DrossCreateView = registry.view("items.Dross", "create")
DrossUpdateView = registry.view("items.Dross", "update")
