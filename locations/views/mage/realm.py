from locations.registry import registry

RealmDetailView = registry.view("locations.HorizonRealm", "detail")
RealmListView = registry.view("locations.HorizonRealm", "list")
RealmCreateView = registry.view("locations.HorizonRealm", "create")
RealmUpdateView = registry.view("locations.HorizonRealm", "update")
