from locations.registry import registry

TrodDetailView = registry.view("locations.Trod", "detail")
TrodListView = registry.view("locations.Trod", "list")
TrodCreateView = registry.view("locations.Trod", "create")
TrodUpdateView = registry.view("locations.Trod", "update")
