from collections import namedtuple
from typing import Any

from django.views.generic import CreateView, DetailView, UpdateView
from items.models.mage.grimoire import Grimoire

EmptyRote = namedtuple("EmptyRote", ["name", "spheres"])
empty_rote = EmptyRote("", "")


class GrimoireDetailView(DetailView):
    model = Grimoire
    template_name = "items/mage/grimoire/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["abilities"] = "<br>".join(
            [x.name for x in self.object.abilities.all()]
        )
        context["spheres"] = "<br>".join([x.name for x in self.object.spheres.all()])
        context["practices"] = "<br>".join(
            [
                f'<a href="{x.get_absolute_url()}">{x}</a>'
                for x in self.object.practices.all()
            ]
        )
        context["instruments"] = "<br>".join(
            [
                f'<a href="{x.get_absolute_url()}">{x}</a>'
                for x in self.object.instruments.all()
            ]
        )
        context["year"] = abs(self.object.date_written)
        return context


class GrimoireCreateView(CreateView):
    model = Grimoire
    fields = [
        "name",
        "rank",
        "background_cost",
        "description",
        "abilities",
        "spheres",
        "date_written",
        "faction",
        "practices",
        "instruments",
        "is_primer",
        "language",
        "length",
        "cover_material",
        "inner_material",
        "medium",
        "rotes",
    ]
    template_name = "items/mage/grimoire/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form


class GrimoireUpdateView(UpdateView):
    model = Grimoire
    fields = [
        "name",
        "rank",
        "description",
        "abilities",
        "spheres",
        "date_written",
        "faction",
        "practices",
        "instruments",
        "is_primer",
        "language",
        "length",
        "cover_material",
        "inner_material",
        "medium",
        "rotes",
    ]
    template_name = "items/mage/grimoire/form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description here"}
        )
        return form
