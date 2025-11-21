from core.models import Language
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class LanguageDetailView(DetailView):
    model = Language
    template_name = "core/language/detail.html"


class LanguageCreateView(MessageMixin, CreateView):
    model = Language
    fields = "__all__"
    template_name = "core/language/form.html"
    success_message = "Language created successfully."
    error_message = "Error creating language."


class LanguageUpdateView(MessageMixin, UpdateView):
    model = Language
    fields = "__all__"
    template_name = "core/language/form.html"
    success_message = "Language updated successfully."
    error_message = "Error updating language."


class LanguageListView(ListView):
    model = Language
    ordering = ["name"]
    template_name = "core/language/list.html"
