from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.mixins import MessageMixin
from core.models import Language


class LanguageDetailView(DetailView):
    model = Language
    template_name = "core/language/detail.html"


class LanguageCreateView(MessageMixin, CreateView):
    model = Language
    fields = ["name", "frequency"]
    template_name = "core/language/form.html"
    success_message = "Language created successfully."
    error_message = "Error creating language."


class LanguageUpdateView(MessageMixin, UpdateView):
    model = Language
    fields = ["name", "frequency"]
    template_name = "core/language/form.html"
    success_message = "Language updated successfully."
    error_message = "Error updating language."


class LanguageListView(ListView):
    model = Language
    ordering = ["name"]
    template_name = "core/language/list.html"
