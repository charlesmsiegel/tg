from items.registry import registry

TalenDetailView = registry.view("items.Talen", "detail")
TalenListView = registry.view("items.Talen", "list")
TalenCreateView = registry.view("items.Talen", "create")
TalenUpdateView = registry.view("items.Talen", "update")
