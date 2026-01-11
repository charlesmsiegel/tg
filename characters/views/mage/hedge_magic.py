from django.views.generic import CreateView, DetailView, ListView, UpdateView

from characters.models.mage.sorcerer import LinearMagicPath, LinearMagicRitual
from core.mixins import MessageMixin


class PathDetailView(DetailView):
    model = LinearMagicPath
    template_name = "characters/mage/linear_magic_path/detail.html"


class PathCreateView(MessageMixin, CreateView):
    model = LinearMagicPath
    fields = ["name", "description", "numina_type"]
    template_name = "characters/mage/linear_magic_path/form.html"
    success_message = "Linear Magic Path created successfully."
    error_message = "There was an error creating the Linear Magic Path."


class PathUpdateView(MessageMixin, UpdateView):
    model = LinearMagicPath
    fields = ["name", "description", "numina_type"]
    template_name = "characters/mage/linear_magic_path/form.html"
    success_message = "Linear Magic Path updated successfully."
    error_message = "There was an error updating the Linear Magic Path."


class PathListView(ListView):
    model = LinearMagicPath
    ordering = ["name"]
    template_name = "characters/mage/linear_magic_path/list.html"


class RitualDetailView(DetailView):
    model = LinearMagicRitual
    template_name = "characters/mage/linear_magic_ritual/detail.html"


class RitualCreateView(MessageMixin, CreateView):
    model = LinearMagicRitual
    fields = ["name", "description", "path", "level"]
    template_name = "characters/mage/linear_magic_ritual/form.html"
    success_message = "Linear Magic Ritual created successfully."
    error_message = "There was an error creating the Linear Magic Ritual."


class RitualUpdateView(MessageMixin, UpdateView):
    model = LinearMagicRitual
    fields = ["name", "description", "path", "level"]
    template_name = "characters/mage/linear_magic_ritual/form.html"
    success_message = "Linear Magic Ritual updated successfully."
    error_message = "There was an error updating the Linear Magic Ritual."


class RitualListView(ListView):
    model = LinearMagicRitual
    ordering = ["path", "level", "name"]
    template_name = "characters/mage/linear_magic_ritual/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paths"] = LinearMagicPath.objects.all().order_by("name")
        return context
