from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.vampire.sect import VampireSect
from core.mixins import MessageMixin


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
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


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 15 minutes
class VampireSectListView(ListView):
    model = VampireSect
    ordering = ["name"]
    template_name = "characters/vampire/sect/list.html"
