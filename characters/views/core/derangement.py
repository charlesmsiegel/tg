from characters.models.core import Derangement
from core.mixins import MessageMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class DerangementDetailView(DetailView):
    model = Derangement
    template_name = "characters/core/derangement/detail.html"


class DerangementCreateView(MessageMixin, CreateView):
    model = Derangement
    fields = ["name", "description"]
    template_name = "characters/core/derangement/form.html"
    success_message = "Derangement '{name}' created successfully!"
    error_message = "Failed to create Derangement. Please correct the errors below."


class DerangementUpdateView(MessageMixin, UpdateView):
    model = Derangement
    fields = ["name", "description"]
    template_name = "characters/core/derangement/form.html"
    success_message = "Derangement '{name}' updated successfully!"
    error_message = "Failed to update Derangement. Please correct the errors below."


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class DerangementListView(ListView):
    model = Derangement
    ordering = ["name"]
    template_name = "characters/core/derangement/list.html"
