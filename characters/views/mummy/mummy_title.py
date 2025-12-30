from characters.forms.mummy.mummy_title import MummyTitleForm
from characters.models.mummy.mummy_title import MummyTitle
from core.mixins import MessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class MummyTitleDetailView(LoginRequiredMixin, DetailView):
    model = MummyTitle
    template_name = "characters/mummy/title/detail.html"


class MummyTitleCreateView(MessageMixin, CreateView):
    model = MummyTitle
    form_class = MummyTitleForm
    template_name = "characters/mummy/title/form.html"
    success_message = "Title '{name}' created successfully!"
    error_message = "Failed to create title. Please correct the errors below."

    def get_success_url(self):
        return self.object.get_absolute_url()


class MummyTitleUpdateView(MessageMixin, UpdateView):
    model = MummyTitle
    form_class = MummyTitleForm
    template_name = "characters/mummy/title/form.html"
    success_message = "Title '{name}' updated successfully!"
    error_message = "Failed to update title. Please correct the errors below."


class MummyTitleListView(ListView):
    model = MummyTitle
    ordering = ["rank_level", "name"]
    template_name = "characters/mummy/title/list.html"
