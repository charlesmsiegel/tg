from locations.registry import registry

SectorDetailView = registry.view("locations.Sector", "detail")
SectorListView = registry.view("locations.Sector", "list")
SectorCreateView = registry.view("locations.Sector", "create")
SectorUpdateView = registry.view("locations.Sector", "update")
