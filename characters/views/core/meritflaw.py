from typing import Any

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.core import MeritFlaw
from characters.views.core.known_by import KnownByMixin
from core.cache import cache_page_per_visitor
from core.mixins import MessageMixin


@method_decorator(cache_page_per_visitor(60 * 15), name="dispatch")  # Cache for 15 minutes
class MeritFlawDetailView(KnownByMixin, DetailView):
    model = MeritFlaw
    template_name = "characters/core/meritflaw/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        mf_ratings = list(self.object.ratings.values_list("value", flat=True))
        mf_ratings.sort()
        context["ratings"] = ", ".join([str(x) for x in mf_ratings])
        return context


class MeritFlawCreateView(MessageMixin, CreateView):
    model = MeritFlaw
    fields = ["name", "description", "ratings", "allowed_types"]
    template_name = "characters/core/meritflaw/form.html"
    success_message = "Merit/Flaw '{name}' created successfully!"
    error_message = "Failed to create Merit/Flaw. Please correct the errors below."


class MeritFlawUpdateView(MessageMixin, UpdateView):
    model = MeritFlaw
    fields = ["name", "description", "ratings", "allowed_types"]
    template_name = "characters/core/meritflaw/form.html"
    success_message = "Merit/Flaw '{name}' updated successfully!"
    error_message = "Failed to update Merit/Flaw. Please correct the errors below."


@method_decorator(cache_page_per_visitor(60 * 15), name="dispatch")  # Cache for 15 minutes
class MeritFlawListView(ListView):
    model = MeritFlaw
    ordering = ["name"]
    template_name = "characters/core/meritflaw/list.html"

    def get_queryset(self):
        # The LINE column reads each entry's allowed character types.
        return super().get_queryset().prefetch_related("allowed_types")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        gamelines = [code for code, _ in settings.GAMELINE_CHOICES if code != "wod"]
        for mf in context["object_list"]:
            # Gamelines the entry is limited to; none means every line may take it.
            mf.line_codes = sorted(
                {t.gameline for t in mf.allowed_types.all() if t.gameline in gamelines}
            )
        context["gamelines"] = gamelines
        return context
