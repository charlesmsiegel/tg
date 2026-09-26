from locations.registry import registry

HoldingDetailView = registry.view("locations.Holding", "detail")
HoldingListView = registry.view("locations.Holding", "list")
HoldingCreateView = registry.view("locations.Holding", "create")
HoldingUpdateView = registry.view("locations.Holding", "update")
