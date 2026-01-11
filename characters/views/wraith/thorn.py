from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.wraith.thorn import Thorn
from core.mixins import MessageMixin


class ThornDetailView(DetailView):
    model = Thorn
    template_name = "characters/wraith/thorn/detail.html"


class ThornCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Thorn
    fields = [
        "name",
        "description",
        "thorn_type",
        "point_cost",
        "activation_cost",
        "activation_trigger",
        "mechanical_description",
        "resistance_system",
        "resistance_difficulty",
        "duration",
        "frequency_limitation",
        "limitations",
    ]
    template_name = "characters/wraith/thorn/form.html"
    success_message = "Thorn created successfully."
    error_message = "There was an error creating the Thorn."


class ThornUpdateView(MessageMixin, UpdateView):
    model = Thorn
    fields = [
        "name",
        "description",
        "thorn_type",
        "point_cost",
        "activation_cost",
        "activation_trigger",
        "mechanical_description",
        "resistance_system",
        "resistance_difficulty",
        "duration",
        "frequency_limitation",
        "limitations",
    ]
    template_name = "characters/wraith/thorn/form.html"
    success_message = "Thorn updated successfully."
    error_message = "There was an error updating the Thorn."


class ThornListView(ListView):
    model = Thorn
    ordering = ["name"]
    template_name = "characters/wraith/thorn/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique point costs for filtering
        context["point_costs"] = sorted(set(Thorn.objects.values_list("point_cost", flat=True)))
        return context
