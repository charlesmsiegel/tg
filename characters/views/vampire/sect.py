from characters.models.vampire.sect import VampireSect
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class VampireSectDetailView(DetailView):
    model = VampireSect
    template_name = "characters/vampire/sect/detail.html"


class VampireSectCreateView(MessageMixin, CreateView):
    model = VampireSect
    fields = [
        "name",
        "description",
        "philosophy",
    ]
    template_name = "characters/vampire/sect/form.html"
    success_message = "Vampire Sect created successfully."
    error_message = "There was an error creating the Vampire Sect."


class VampireSectUpdateView(MessageMixin, UpdateView):
    model = VampireSect
    fields = [
        "name",
        "description",
        "philosophy",
    ]
    template_name = "characters/vampire/sect/form.html"
    success_message = "Vampire Sect updated successfully."
    error_message = "There was an error updating the Vampire Sect."


class VampireSectListView(ListView):
    model = VampireSect
    ordering = ["name"]
    template_name = "characters/vampire/sect/list.html"
