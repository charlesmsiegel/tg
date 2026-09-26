from locations.registry import registry

HauntDetailView = registry.view("locations.Haunt", "detail")
HauntListView = registry.view("locations.Haunt", "list")
HauntCreateView = registry.view("locations.Haunt", "create")
HauntUpdateView = registry.view("locations.Haunt", "update")
