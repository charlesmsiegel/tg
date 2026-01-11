from typing import Any

from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.mage.faction import MageFaction


class MageFactionDetailView(DetailView):
    model = MageFaction
    template_name = "characters/mage/faction/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["languages"] = ", ".join([str(x) for x in self.object.languages.all()])
        context["affinities"] = ", ".join([x.name for x in self.object.affinities.all()])
        context["paradigms"] = ", ".join(
            [f'<a href="{x.get_absolute_url()}">{x}</a>' for x in self.object.paradigms.all()]
        )
        context["practices"] = ", ".join(
            [f'<a href="{x.get_absolute_url()}">{x}</a>' for x in self.object.practices.all()]
        )
        context["media"] = ", ".join(
            [f'<a href="{x.get_absolute_url()}">{x}</a>' for x in self.object.media.all()]
        )
        context["materials"] = ", ".join(
            [f'<a href="{x.get_absolute_url()}">{x}</a>' for x in self.object.materials.all()]
        )
        context["year"] = abs(self.object.founded)
        context["subfactions"] = ", ".join(
            [
                f'<a href="{x.get_absolute_url()}">{x}</a>'
                for x in MageFaction.objects.filter(parent=self.object)
            ]
        )
        return context


class MageFactionCreateView(CreateView):
    model = MageFaction
    fields = [
        "name",
        "description",
        "languages",
        "affinities",
        "paradigms",
        "practices",
        "media",
        "materials",
        "founded",
        "ended",
        "parent",
    ]
    template_name = "characters/mage/faction/form.html"


class MageFactionUpdateView(UpdateView):
    model = MageFaction
    fields = [
        "name",
        "description",
        "languages",
        "affinities",
        "paradigms",
        "practices",
        "media",
        "materials",
        "founded",
        "ended",
        "parent",
    ]
    template_name = "characters/mage/faction/form.html"


class MageFactionListView(ListView):
    model = MageFaction
    ordering = ["name"]
    template_name = "characters/mage/faction/list.html"
