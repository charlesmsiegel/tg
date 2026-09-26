from locations.registry import registry

SafehouseDetailView = registry.view("locations.Safehouse", "detail")
SafehouseListView = registry.view("locations.Safehouse", "list")
SafehouseCreateView = registry.view("locations.Safehouse", "create")
SafehouseUpdateView = registry.view("locations.Safehouse", "update")
