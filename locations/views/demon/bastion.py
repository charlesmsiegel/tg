from locations.registry import registry

BastionDetailView = registry.view("locations.Bastion", "detail")
BastionListView = registry.view("locations.Bastion", "list")
BastionCreateView = registry.view("locations.Bastion", "create")
BastionUpdateView = registry.view("locations.Bastion", "update")
