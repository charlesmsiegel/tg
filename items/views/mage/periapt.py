from typing import Any

from django.views.generic import DetailView

from items.models.mage import WonderResonanceRating
from items.registry import registry


class _PeriaptDetailView(DetailView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = WonderResonanceRating.objects.filter(wonder=self.object).order_by(
            "resonance__name"
        )
        return context


PeriaptDetailView = registry.view("items.Periapt", "detail")


PeriaptListView = registry.view("items.Periapt", "list")
PeriaptCreateView = registry.view("items.Periapt", "create")
PeriaptUpdateView = registry.view("items.Periapt", "update")
