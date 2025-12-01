from characters.models.werewolf.charm import SpiritCharm
from core.mixins import MessageMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView


class SpiritCharmDetailView(DetailView):
    model = SpiritCharm
    template_name = "characters/werewolf/charm/detail.html"


class SpiritCharmCreateView(MessageMixin, CreateView):
    model = SpiritCharm
    fields = ["name", "description"]
    template_name = "characters/werewolf/charm/form.html"
    success_message = "Spirit Charm created successfully."
    error_message = "There was an error creating the Spirit Charm."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form


class SpiritCharmUpdateView(MessageMixin, UpdateView):
    model = SpiritCharm
    fields = ["name", "description"]
    template_name = "characters/werewolf/charm/form.html"
    success_message = "Spirit Charm updated successfully."
    error_message = "There was an error updating the Spirit Charm."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form


class SpiritCharmListView(ListView):
    model = SpiritCharm
    ordering = ["name"]
    template_name = "characters/werewolf/charm/list.html"
