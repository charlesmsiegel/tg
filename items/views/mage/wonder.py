from typing import Any

from django.views.generic import CreateView, DetailView

from core.mixins import prepare_created_object
from items.models.mage import WonderResonanceRating
from items.registry import registry


class _WonderDetailView(DetailView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = (
            WonderResonanceRating.objects.filter(wonder=self.object)
            .select_related("resonance")
            .order_by("resonance__name")
        )
        return context


WonderDetailView = registry.view("items.Wonder", "detail")


class _WonderCreateView(CreateView):
    """WonderForm selects its concrete model only after validation."""

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        prepare_created_object(form, self.request)
        return super().form_valid(form)


WonderCreateView = registry.view("items.Wonder", "create")


WonderListView = registry.view("items.Wonder", "list")
WonderUpdateView = registry.view("items.Wonder", "update")
