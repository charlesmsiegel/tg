from items.registry import registry

WeaponDetailView = registry.view("items.Weapon", "detail")
WeaponListView = registry.view("items.Weapon", "list")
WeaponCreateView = registry.view("items.Weapon", "create")
WeaponUpdateView = registry.view("items.Weapon", "update")
