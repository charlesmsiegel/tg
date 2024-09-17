from typing import Any

from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView
from items.models.mage import WonderResonanceRating
from items.models.mage.talisman import Talisman


class TalismanDetailView(DetailView):
    model = Talisman
    template_name = "items/mage/talisman/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["resonance"] = WonderResonanceRating.objects.filter(
            wonder=self.object
        ).order_by("resonance__name")
        return context


class TalismanCreateView(CreateView):
    model = Talisman
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "powers",
        "arete",
    ]
    template_name = "items/mage/talisman/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class TalismanUpdateView(UpdateView):
    model = Talisman
    fields = [
        "name",
        "rank",
        "background_cost",
        "quintessence_max",
        "description",
        "powers",
        "arete",
    ]
    template_name = "items/mage/talisman/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
