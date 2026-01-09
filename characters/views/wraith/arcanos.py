from characters.models.wraith.arcanos import Arcanos
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class ArcanosDetailView(DetailView):
    model = Arcanos
    template_name = "characters/wraith/arcanos/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related levels if this is a parent arcanos
        if self.object.parent_arcanos is None:
            context["levels"] = Arcanos.objects.filter(parent_arcanos=self.object).order_by("level")
        return context


class ArcanosCreateView(MessageMixin, CreateView):
    model = Arcanos
    fields = [
        "name",
        "description",
        "arcanos_type",
        "level",
        "pathos_cost",
        "angst_cost",
        "difficulty",
        "parent_arcanos",
    ]
    template_name = "characters/wraith/arcanos/form.html"
    success_message = "Arcanos created successfully."
    error_message = "There was an error creating the Arcanos."


class ArcanosUpdateView(MessageMixin, UpdateView):
    model = Arcanos
    fields = [
        "name",
        "description",
        "arcanos_type",
        "level",
        "pathos_cost",
        "angst_cost",
        "difficulty",
        "parent_arcanos",
    ]
    template_name = "characters/wraith/arcanos/form.html"
    success_message = "Arcanos updated successfully."
    error_message = "There was an error updating the Arcanos."


class ArcanosListView(ListView):
    model = Arcanos
    ordering = ["arcanos_type", "name", "level"]
    template_name = "characters/wraith/arcanos/list.html"

    def get_queryset(self):
        # Only show parent arcanoi in the list
        return super().get_queryset().filter(parent_arcanos__isnull=True)
