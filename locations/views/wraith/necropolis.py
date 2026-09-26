from locations.registry import registry

NecropolisDetailView = registry.view("locations.Necropolis", "detail")
NecropolisListView = registry.view("locations.Necropolis", "list")
NecropolisCreateView = registry.view("locations.Necropolis", "create")
NecropolisUpdateView = registry.view("locations.Necropolis", "update")
