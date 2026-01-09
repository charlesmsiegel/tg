from characters.models.wraith.arcanos import Arcanos
from core.mixins import MessageMixin
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView


@method_decorator(cache_page(60 * 15), name="dispatch")
class ArcanosDetailView(DetailView):
    model = Arcanos
    template_name = "characters/wraith/arcanos/detail.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(Prefetch("levels", queryset=Arcanos.objects.order_by("level")))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related levels if this is a parent arcanos (already prefetched with ordering)
        if self.object.parent_arcanos is None:
            context["levels"] = self.object.levels.all()
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


@method_decorator(cache_page(60 * 15), name="dispatch")
class ArcanosListView(ListView):
    model = Arcanos
    ordering = ["arcanos_type", "name", "level"]
    template_name = "characters/wraith/arcanos/list.html"

    def get_queryset(self):
        # Only show parent arcanoi in the list
        return super().get_queryset().filter(parent_arcanos__isnull=True)
