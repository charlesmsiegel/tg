from locations.registry import registry

TombDetailView = registry.view("locations.Tomb", "detail")
TombListView = registry.view("locations.Tomb", "list")
TombCreateView = registry.view("locations.Tomb", "create")
TombUpdateView = registry.view("locations.Tomb", "update")
CultTempleDetailView = registry.view("locations.CultTemple", "detail")
CultTempleListView = registry.view("locations.CultTemple", "list")
CultTempleCreateView = registry.view("locations.CultTemple", "create")
CultTempleUpdateView = registry.view("locations.CultTemple", "update")
UndergroundSanctuaryDetailView = registry.view("locations.UndergroundSanctuary", "detail")
UndergroundSanctuaryListView = registry.view("locations.UndergroundSanctuary", "list")
UndergroundSanctuaryCreateView = registry.view("locations.UndergroundSanctuary", "create")
UndergroundSanctuaryUpdateView = registry.view("locations.UndergroundSanctuary", "update")
