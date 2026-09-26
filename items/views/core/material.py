from items.registry import registry

MaterialDetailView = registry.view("items.Material", "detail")
MaterialListView = registry.view("items.Material", "list")
MaterialCreateView = registry.view("items.Material", "create")
MaterialUpdateView = registry.view("items.Material", "update")
