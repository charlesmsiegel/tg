from locations.registry import registry

CaernDetailView = registry.view("locations.Caern", "detail")
CaernListView = registry.view("locations.Caern", "list")
CaernCreateView = registry.view("locations.Caern", "create")
CaernUpdateView = registry.view("locations.Caern", "update")
