from typing import Any

from characters.models.vampire.clan import VampireClan
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class VampireClanDetailView(DetailView):
    model = VampireClan
    template_name = "characters/vampire/clan/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["disciplines"] = ", ".join(
            [x.name for x in self.object.disciplines.all()]
        )
        if self.object.parent_clan:
            context["parent_clan"] = self.object.parent_clan
        context["bloodlines"] = VampireClan.objects.filter(parent_clan=self.object)
        return context


class VampireClanCreateView(MessageMixin, CreateView):
    model = VampireClan
    fields = [
        "name",
        "description",
        "nickname",
        "disciplines",
        "weakness",
        "is_bloodline",
        "parent_clan",
    ]
    template_name = "characters/vampire/clan/form.html"
    success_message = "Vampire Clan created successfully."
    error_message = "There was an error creating the Vampire Clan."


class VampireClanUpdateView(MessageMixin, UpdateView):
    model = VampireClan
    fields = [
        "name",
        "description",
        "nickname",
        "disciplines",
        "weakness",
        "is_bloodline",
        "parent_clan",
    ]
    template_name = "characters/vampire/clan/form.html"
    success_message = "Vampire Clan updated successfully."
    error_message = "There was an error updating the Vampire Clan."


class VampireClanListView(ListView):
    model = VampireClan
    ordering = ["name"]
    template_name = "characters/vampire/clan/list.html"
