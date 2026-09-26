from items.registry import registry

MediumDetailView = registry.view("items.Medium", "detail")
MediumListView = registry.view("items.Medium", "list")
MediumCreateView = registry.view("items.Medium", "create")
MediumUpdateView = registry.view("items.Medium", "update")
