from characters.models.core import Derangement
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


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


class DerangementListView(ListView):
    model = Derangement
    ordering = ["name"]
    template_name = "characters/core/derangement/list.html"
