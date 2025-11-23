from characters.models.changeling.legacy import Legacy
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class LegacyDetailView(DetailView):
    model = Legacy
    template_name = "characters/changeling/legacy/detail.html"


class LegacyCreateView(MessageMixin, CreateView):
    model = Legacy
    fields = ["name", "description", "court"]
    template_name = "characters/changeling/legacy/form.html"
    success_message = "Legacy created successfully."
    error_message = "There was an error creating the Legacy."


class LegacyUpdateView(MessageMixin, UpdateView):
    model = Legacy
    fields = ["name", "description", "court"]
    template_name = "characters/changeling/legacy/form.html"
    success_message = "Legacy updated successfully."
    error_message = "There was an error updating the Legacy."


class LegacyListView(ListView):
    model = Legacy
    ordering = ["name"]
    template_name = "characters/changeling/legacy/list.html"
