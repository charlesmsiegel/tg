# WraithRelic Views
# WraithArtifact Views
from items.registry import registry

WraithRelicDetailView = registry.view("items.WraithRelic", "detail")
WraithRelicListView = registry.view("items.WraithRelic", "list")
WraithRelicCreateView = registry.view("items.WraithRelic", "create")
WraithRelicUpdateView = registry.view("items.WraithRelic", "update")
WraithArtifactDetailView = registry.view("items.WraithArtifact", "detail")
WraithArtifactListView = registry.view("items.WraithArtifact", "list")
WraithArtifactCreateView = registry.view("items.WraithArtifact", "create")
WraithArtifactUpdateView = registry.view("items.WraithArtifact", "update")
