from locations.registry import registry

ReliquaryDetailView = registry.view("locations.Reliquary", "detail")
ReliquaryListView = registry.view("locations.Reliquary", "list")
ReliquaryCreateView = registry.view("locations.Reliquary", "create")
ReliquaryUpdateView = registry.view("locations.Reliquary", "update")
