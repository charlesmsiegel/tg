from characters.models.vampire.coterie import Coterie
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class CoterieDetailView(DetailView):
    model = Coterie
    template_name = "characters/vampire/coterie/detail.html"


class CoterieCreateView(MessageMixin, CreateView):
    model = Coterie
    fields = ["name", "description", "leader", "chronicle", "public_info"]
    template_name = "characters/vampire/coterie/form.html"
    success_message = "Coterie '{name}' created successfully!"
    error_message = "Failed to create Coterie. Please correct the errors below."


class CoterieUpdateView(MessageMixin, UpdateView):
    model = Coterie
    fields = ["name", "description", "leader", "members", "chronicle", "public_info"]
    template_name = "characters/vampire/coterie/form.html"
    success_message = "Coterie '{name}' updated successfully!"
    error_message = "Failed to update Coterie. Please correct the errors below."


class CoterieListView(ListView):
    model = Coterie
    ordering = ["name"]
    template_name = "characters/vampire/coterie/list.html"
