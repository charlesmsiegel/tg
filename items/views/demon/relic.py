from items.registry import registry

RelicDetailView = registry.view("items.Relic", "detail")
RelicListView = registry.view("items.Relic", "list")
RelicCreateView = registry.view("items.Relic", "create")
RelicUpdateView = registry.view("items.Relic", "update")
