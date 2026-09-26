from locations.registry import registry

BywayDetailView = registry.view("locations.Byway", "detail")
BywayListView = registry.view("locations.Byway", "list")
BywayCreateView = registry.view("locations.Byway", "create")
BywayUpdateView = registry.view("locations.Byway", "update")
