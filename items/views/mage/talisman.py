from typing import Any

from django.views.generic import DetailView

from items.models.mage import WonderResonanceRating
from items.registry import registry


class _TalismanDetailView(DetailView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = WonderResonanceRating.objects.filter(wonder=self.object).order_by(
            "resonance__name"
        )
        return context


TalismanDetailView = registry.view("items.Talisman", "detail")


TalismanListView = registry.view("items.Talisman", "list")
TalismanCreateView = registry.view("items.Talisman", "create")
TalismanUpdateView = registry.view("items.Talisman", "update")
