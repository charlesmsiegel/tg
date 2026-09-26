from collections import namedtuple
from typing import Any

from django.views.generic import DetailView

from items.registry import registry

EmptyRote = namedtuple("EmptyRote", ["name", "spheres"])
empty_rote = EmptyRote("", "")


class _GrimoireDetailView(DetailView):

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["abilities"] = "<br>".join([x.name for x in self.object.abilities.all()])
        context["spheres"] = "<br>".join([x.name for x in self.object.spheres.all()])
        context["practices"] = "<br>".join(
            [f'<a href="{x.get_absolute_url()}">{x}</a>' for x in self.object.practices.all()]
        )
        context["instruments"] = "<br>".join(
            [f'<a href="{x.get_absolute_url()}">{x}</a>' for x in self.object.instruments.all()]
        )
        context["year"] = abs(self.object.date_written)
        return context


GrimoireDetailView = registry.view("items.Grimoire", "detail")


GrimoireListView = registry.view("items.Grimoire", "list")
GrimoireCreateView = registry.view("items.Grimoire", "create")
GrimoireUpdateView = registry.view("items.Grimoire", "update")
