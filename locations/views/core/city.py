from locations.registry import registry

CityDetailView = registry.view("locations.City", "detail")
CityListView = registry.view("locations.City", "list")
CityCreateView = registry.view("locations.City", "create")
CityUpdateView = registry.view("locations.City", "update")
