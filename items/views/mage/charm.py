from typing import Any

from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from items.models.mage import Charm, WonderResonanceRating


class CharmDetailView(DetailView):
    model = Charm
    template_name = "items/mage/charm/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = WonderResonanceRating.objects.filter(
            wonder=self.object
        ).order_by("resonance__name")
        return context


class CharmListView(ListView):
    model = Charm
    ordering = ["name"]
    template_name = "items/mage/charm/list.html"


class CharmCreateView(MessageMixin, CreateView):
    model = Charm
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "power",
        "arete",
    ]
    template_name = "items/mage/charm/form.html"
    success_message = "Charm '{name}' created successfully!"
    error_message = "Failed to create Charm. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class CharmUpdateView(MessageMixin, UpdateView):
    model = Charm
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "power",
        "arete",
    ]
    template_name = "items/mage/charm/form.html"
    success_message = "Charm '{name}' updated successfully!"
    error_message = "Failed to update Charm. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
