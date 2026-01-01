from characters.forms.mummy.dynasty import DynastyForm
from characters.models.mummy.dynasty import Dynasty
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class DynastyDetailView(DetailView):
    model = Dynasty
    template_name = "characters/mummy/dynasty/detail.html"


class DynastyCreateView(MessageMixin, CreateView):
    model = Dynasty
    form_class = DynastyForm
    template_name = "characters/mummy/dynasty/form.html"
    success_message = "Dynasty '{name}' created successfully!"
    error_message = "Failed to create dynasty. Please correct the errors below."

    def get_success_url(self):
        return self.object.get_absolute_url()


class DynastyUpdateView(MessageMixin, UpdateView):
    model = Dynasty
    form_class = DynastyForm
    template_name = "characters/mummy/dynasty/form.html"
    success_message = "Dynasty '{name}' updated successfully!"
    error_message = "Failed to update dynasty. Please correct the errors below."


class DynastyListView(ListView):
    model = Dynasty
    ordering = ["name"]
    template_name = "characters/mummy/dynasty/list.html"
